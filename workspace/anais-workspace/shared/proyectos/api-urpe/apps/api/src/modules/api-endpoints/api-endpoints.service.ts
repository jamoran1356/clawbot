import { Injectable, NotFoundException, ForbiddenException } from '@nestjs/common';
import { PrismaService } from '../../infra/prisma';
import { CreateApiEndpointDto, UpdateApiEndpointDto } from './dto';
import { ApiKeyCryptoService } from '../../shared/services';
import { customAlphabet } from 'nanoid';

const nanoid = customAlphabet('0123456789abcdefghijklmnopqrstuvwxyz', 12);

@Injectable()
export class ApiEndpointsService {
  constructor(
    private prisma: PrismaService,
    private apiKeyCrypto: ApiKeyCryptoService,
  ) {}

  async create(dto: CreateApiEndpointDto, userId: string) {
    const slug = dto.slug || `${dto.name.toLowerCase().replace(/\s+/g, '-')}-${nanoid(6)}`;

    const endpoint = await this.prisma.apiEndpoint.create({
      data: {
        ...dto,
        slug,
        userId,
      },
      include: {
        connection: true,
      },
    });

    // Auto-generar API Key para el endpoint (con hash)
    const plainKey = this.apiKeyCrypto.generateKey();
    const hashedKey = await this.apiKeyCrypto.hashKey(plainKey);

    const apiKey = await this.prisma.apiKey.create({
      data: {
        key: hashedKey,
        name: `${dto.name} - Default Key`,
        userId,
        endpointId: endpoint.id,
      },
    });

    return {
      ...endpoint,
      apiKey: plainKey, // Mostrar solo una vez
      url: `https://api.urpeailab.com/api/v1/proxy/${endpoint.slug}`,
      warning: 'Save your API Key securely. You will not be able to see it again.',
    };
  }

  async findAll(userId: string, role: string, status?: string) {
    const where: any = role === 'ADMIN' ? {} : { userId };
    
    if (status) {
      where.status = status;
    }

    const endpoints = await this.prisma.apiEndpoint.findMany({
      where,
      include: {
        connection: true,
        _count: {
          select: { requests: true },
        },
      },
      orderBy: { createdAt: 'desc' },
    });

    return endpoints.map((ep) => ({
      ...ep,
      url: `https://api.urpeailab.com/api/v1/proxy/${ep.slug}`,
      totalRequests: ep._count.requests,
    }));
  }

  async findOne(id: string, userId: string, role: string) {
    const endpoint = await this.prisma.apiEndpoint.findUnique({
      where: { id },
      include: {
        connection: true,
        apiKeys: {
          where: { isActive: true },
          select: {
            id: true,
            key: true,
            name: true,
            createdAt: true,
            lastUsedAt: true,
          },
        },
      },
    });

    if (!endpoint) {
      throw new NotFoundException('API Endpoint not found');
    }

    if (role !== 'ADMIN' && endpoint.userId !== userId) {
      throw new ForbiddenException('Access denied');
    }

    return {
      ...endpoint,
      url: `https://api.urpeailab.com/api/v1/proxy/${endpoint.slug}`,
    };
  }

  async update(id: string, dto: UpdateApiEndpointDto, userId: string, role: string) {
    const endpoint = await this.findOne(id, userId, role);

    return this.prisma.apiEndpoint.update({
      where: { id },
      data: dto,
      include: { connection: true },
    });
  }

  async remove(id: string, userId: string, role: string) {
    await this.findOne(id, userId, role);

    await this.prisma.apiEndpoint.delete({ where: { id } });

    return { message: 'API Endpoint deleted successfully' };
  }

  async getStats(id: string, userId: string, role: string) {
    await this.findOne(id, userId, role);

    const now = new Date();
    const last24h = new Date(now.getTime() - 24 * 60 * 60 * 1000);
    const last7d = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    const [total, last24hCount, last7dCount, avgResponseTime] = await Promise.all([
      this.prisma.request.count({ where: { endpointId: id } }),
      this.prisma.request.count({
        where: { endpointId: id, createdAt: { gte: last24h } },
      }),
      this.prisma.request.count({
        where: { endpointId: id, createdAt: { gte: last7d } },
      }),
      this.prisma.request.aggregate({
        where: { endpointId: id },
        _avg: { responseTime: true },
      }),
    ]);

    return {
      totalRequests: total,
      last24Hours: last24hCount,
      last7Days: last7dCount,
      avgResponseTime: avgResponseTime._avg.responseTime || 0,
    };
  }

  async findBySlug(slug: string) {
    return this.prisma.apiEndpoint.findUnique({
      where: { slug, status: 'ACTIVE' },
      include: { connection: true },
    });
  }
}
