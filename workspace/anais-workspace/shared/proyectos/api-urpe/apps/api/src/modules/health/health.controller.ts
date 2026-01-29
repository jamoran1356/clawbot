import { Controller, Get } from '@nestjs/common';
import { HealthService } from './health.service';

@Controller('health')
export class HealthController {
  constructor(private healthService: HealthService) {}

  @Get()
  async check() {
    return this.healthService.checkHealth();
  }

  /**
   * Endpoint simplificado para uptime robots (solo status simple)
   */
  @Get('simple')
  async simple() {
    const health = await this.healthService.checkHealth();
    return {
      status: health.status === 'healthy' ? 'ok' : health.status,
      uptime: health.uptime,
      timestamp: health.timestamp,
    };
  }
}
