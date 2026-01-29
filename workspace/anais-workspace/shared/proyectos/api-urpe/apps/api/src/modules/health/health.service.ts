import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../../infra/prisma';
import { ConfigService } from '@nestjs/config';
import Redis from 'ioredis';

interface HealthCheckResult {
  status: 'healthy' | 'degraded' | 'unhealthy';
  checks: {
    database: {
      status: 'up' | 'down';
      message?: string;
      latency?: number;
    };
    redis: {
      status: 'up' | 'down';
      message?: string;
      latency?: number;
    };
    memory: {
      status: 'ok' | 'warning' | 'critical';
      heapUsedPercent: number;
      heapUsedMB: number;
      heapTotalMB: number;
      message?: string;
    };
  };
  uptime: number;
  timestamp: string;
}

@Injectable()
export class HealthService {
  private readonly logger = new Logger(HealthService.name);
  private readonly startTime = Date.now();
  private redis: Redis;

  constructor(
    private prisma: PrismaService,
    private configService: ConfigService,
  ) {
    this.redis = new Redis({
      host: this.configService.get('REDIS_HOST', 'localhost'),
      port: this.configService.get('REDIS_PORT', 6379),
      password: this.configService.get('REDIS_PASSWORD'),
      lazyConnect: true,
    });
  }

  async checkHealth(): Promise<HealthCheckResult> {
    const checks = await Promise.all([
      this.checkDatabase(),
      this.checkRedis(),
      this.checkMemory(),
    ]);

    const [database, redisCheck, memory] = checks;

    // Determinar status general
    let status: 'healthy' | 'degraded' | 'unhealthy' = 'healthy';

    if (database.status === 'down' || redisCheck.status === 'down') {
      status = 'unhealthy';
    } else if (memory.status === 'critical') {
      status = 'degraded';
    }

    const uptime = Math.floor((Date.now() - this.startTime) / 1000); // en segundos

    return {
      status,
      checks: {
        database,
        redis: redisCheck,
        memory,
      },
      uptime,
      timestamp: new Date().toISOString(),
    };
  }

  private async checkDatabase(): Promise<HealthCheckResult['checks']['database']> {
    try {
      const start = Date.now();
      await this.prisma.$queryRaw`SELECT 1`;
      const latency = Date.now() - start;

      return {
        status: 'up',
        latency,
      };
    } catch (error) {
      this.logger.error('Database health check failed', error);
      return {
        status: 'down',
        message: 'Failed to connect to database',
      };
    }
  }

  private async checkRedis(): Promise<HealthCheckResult['checks']['redis']> {
    try {
      const start = Date.now();
      await this.redis.ping();
      const latency = Date.now() - start;

      return {
        status: 'up',
        latency,
      };
    } catch (error) {
      this.logger.warn('Redis health check failed', error.message);
      return {
        status: 'down',
        message: 'Failed to connect to Redis',
      };
    }
  }

  private checkMemory(): HealthCheckResult['checks']['memory'] {
    const memUsage = process.memoryUsage();
    const heapUsedMB = Math.round(memUsage.heapUsed / 1024 / 1024);
    const heapTotalMB = Math.round(memUsage.heapTotal / 1024 / 1024);
    const heapUsedPercent = Math.round((memUsage.heapUsed / memUsage.heapTotal) * 100);

    let status: 'ok' | 'warning' | 'critical' = 'ok';
    let message: string | undefined;

    if (heapUsedPercent > 90) {
      status = 'critical';
      message = `Heap usage critical: ${heapUsedPercent}%`;
    } else if (heapUsedPercent > 75) {
      status = 'warning';
      message = `Heap usage high: ${heapUsedPercent}%`;
    }

    return {
      status,
      heapUsedPercent,
      heapUsedMB,
      heapTotalMB,
      message,
    };
  }
}
