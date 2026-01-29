import { Injectable, BadRequestException, UnauthorizedException, HttpException } from '@nestjs/common';
import { Request, Response } from 'express';
import { PrismaService } from '../../infra/prisma';
import { ApiEndpointsService } from '../api-endpoints/api-endpoints.service';
import { ApiKeyCryptoService } from '../../shared/services';
import axios from 'axios';

@Injectable()
export class ProxyService {
  constructor(
    private prisma: PrismaService,
    private apiEndpointsService: ApiEndpointsService,
    private apiKeyCrypto: ApiKeyCryptoService,
  ) {}

  async handleRequest(slug: string, req: Request, res: Response, apiKey?: string) {
    const startTime = Date.now();
    
    try {
      // 1. Buscar el endpoint
      const endpoint = await this.apiEndpointsService.findBySlug(slug);
      
      // 1.5 Validar SSRF
      if (endpoint && endpoint.targetUrl) {
        this.validateTargetUrl(endpoint.targetUrl);
      }
      
      if (!endpoint) {
        throw new BadRequestException('Endpoint not found');
      }

      // 2. Validar API Key si es requerida
      let validApiKey = null;
      if (endpoint.requireApiKey) {
        if (!apiKey) {
          throw new UnauthorizedException('API Key required');
        }

        // Buscar API Keys activas para este endpoint
        const candidateKeys = await this.prisma.apiKey.findMany({
          where: {
            isActive: true,
            OR: [
              { endpointId: endpoint.id },
              { endpointId: null }, // Keys globales
            ],
          },
          select: {
            id: true,
            key: true, // Hash almacenado
            endpointId: true,
          },
        });

        // Verificar contra hashes
        for (const candidate of candidateKeys) {
          const isValid = await this.apiKeyCrypto.verifyKey(
            apiKey,
            candidate.key,
          );
          if (isValid) {
            validApiKey = candidate;
            break;
          }
        }

        if (!validApiKey) {
          throw new UnauthorizedException('Invalid API Key');
        }

        // Actualizar último uso
        await this.prisma.apiKey.update({
          where: { id: validApiKey.id },
          data: { lastUsedAt: new Date() },
        });
      }

      // 3. Verificar rate limit
      await this.checkRateLimit(endpoint.id, endpoint.rateLimit);

      // 4. Transformar request si es necesario
      let requestBody = req.body;
      if (endpoint.requestTransform) {
        requestBody = this.transformData(req.body, endpoint.requestTransform);
      }

      // 5. Preparar headers
      const headers: any = {
        'Content-Type': 'application/json',
        'User-Agent': 'URPE-API-Gateway/1.0',
        ...(endpoint.headers ? endpoint.headers as Record<string, any> : {}),
      };

      // Si es Supabase, agregar auth
      if (endpoint.connection?.type === 'SUPABASE') {
        const config = endpoint.connection.config as any;
        headers['apikey'] = config.apiKey;
        headers['Authorization'] = `Bearer ${config.apiKey}`;
      }

      // 6. Hacer la petición al servicio destino
      const response = await axios({
        method: req.method.toLowerCase(),
        url: endpoint.targetUrl,
        data: requestBody,
        params: req.query,
        headers,
        timeout: 30000,
      });

      // 7. Transformar response si es necesario
      let responseData = response.data;
      if (endpoint.responseTransform) {
        responseData = this.transformData(response.data, endpoint.responseTransform);
      }

      const responseTime = Date.now() - startTime;

      // 8. Registrar la petición
      await this.logRequest({
        endpointId: endpoint.id,
        apiKeyId: validApiKey?.id,
        method: req.method,
        path: req.path,
        headers: req.headers,
        body: req.body,
        query: req.query,
        statusCode: response.status,
        responseTime,
        responseBody: responseData,
        ipAddress: req.ip,
        userAgent: req.get('user-agent'),
      });

      // 9. Enviar respuesta
      return res.status(response.status).json(responseData);

    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      // Registrar error
      await this.logRequest({
        endpointId: slug,
        method: req.method,
        path: req.path,
        headers: req.headers,
        body: req.body,
        query: req.query,
        statusCode: error.response?.status || 500,
        responseTime,
        responseBody: { error: error.message },
        ipAddress: req.ip,
        userAgent: req.get('user-agent'),
      });

      if (error instanceof HttpException) {
        return res.status(error.getStatus()).json({
          error: error.message,
          statusCode: error.getStatus(),
        });
      }

      return res.status(error.response?.status || 500).json({
        error: error.message || 'Internal server error',
        statusCode: error.response?.status || 500,
      });
    }
  }

  private async checkRateLimit(endpointId: string, limit: number) {
    const oneMinuteAgo = new Date(Date.now() - 60000);
    
    const count = await this.prisma.request.count({
      where: {
        endpointId,
        createdAt: { gte: oneMinuteAgo },
      },
    });

    if (count >= limit) {
      throw new HttpException('Rate limit exceeded', 429);
    }
  }

  private transformData(data: any, transform: any): any {
    // Implementar lógica de transformación
    // Puede ser con JSONata, JMESPath, o lógica custom
    try {
      if (typeof transform === 'function') {
        return transform(data);
      }
      
      if (typeof transform === 'object') {
        // Mapeo simple de campos
        const result: any = {};
        for (const [key, value] of Object.entries(transform)) {
          if (typeof value === 'string' && value.startsWith('$.')) {
            // Simple JSON path
            const path = value.substring(2).split('.');
            result[key] = path.reduce((obj, p) => obj?.[p], data);
          } else {
            result[key] = value;
          }
        }
        return result;
      }

      return data;
    } catch (error) {
      console.error('Transform error:', error);
      return data;
    }
  }

  private async logRequest(data: any) {
    try {
      await this.prisma.request.create({
        data: {
          endpointId: data.endpointId,
          apiKeyId: data.apiKeyId,
          method: data.method,
          path: data.path,
          headers: data.headers || {},
          body: data.body || {},
          query: data.query || {},
          statusCode: data.statusCode,
          responseTime: data.responseTime,
          responseBody: data.responseBody || {},
          ipAddress: data.ipAddress,
          userAgent: data.userAgent,
        },
      });
    } catch (error) {
      console.error('Failed to log request:', error);
    }
  }

  /**
   * Validación SSRF: Rechaza URLs peligrosas
   * - localhost, 127.0.0.1, 0.0.0.0
   * - IPs privadas (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
   * - Metadata endpoints (169.254.169.254)
   */
  private validateTargetUrl(url: string): boolean {
    try {
      const parsed = new URL(url);
      const hostname = parsed.hostname || '';

      // Blocklist de dominios/IPs peligrosas
      const blocklist = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '169.254.169.254', // AWS metadata
        '::1', // IPv6 localhost
        '[::1]',
      ];

      if (blocklist.includes(hostname)) {
        throw new UnauthorizedException(
          `Target URL not allowed: ${hostname} is blocked`,
        );
      }

      // Validar que no sea IP privada
      if (this.isPrivateIp(hostname)) {
        throw new UnauthorizedException(
          `Target URL not allowed: ${hostname} is a private IP address`,
        );
      }

      return true;
    } catch (error) {
      if (error instanceof UnauthorizedException) {
        throw error;
      }
      throw new BadRequestException(`Invalid target URL: ${error.message}`);
    }
  }

  /**
   * Detecta rangos de IPs privadas (IPv4 e IPv6)
   */
  private isPrivateIp(ip: string): boolean {
    // Rangos privados IPv4
    const ipv4Patterns = [
      /^10\./,                           // 10.0.0.0/8
      /^172\.(1[6-9]|2[0-9]|3[01])\./,  // 172.16.0.0/12
      /^192\.168\./,                      // 192.168.0.0/16
      /^169\.254\./,                      // Link-local (169.254.0.0/16)
    ];

    // Rangos privados IPv6
    const ipv6Patterns = [
      /^fc[0-9a-f]{2}:/i,                 // ULA (fc00::/7)
      /^fe80:/i,                          // Link-local (fe80::/10)
      /^::1$/i,                           // Loopback
      /^\[.*\]$/,                         // Wrapped IPv6
    ];

    return (
      ipv4Patterns.some((pattern) => pattern.test(ip)) ||
      ipv6Patterns.some((pattern) => pattern.test(ip))
    );
  }
}
