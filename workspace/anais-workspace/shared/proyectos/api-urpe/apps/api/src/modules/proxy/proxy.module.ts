import { Module } from '@nestjs/common';
import { ProxyController } from './proxy.controller';
import { ProxyService } from './proxy.service';
import { ApiEndpointsModule } from '../api-endpoints/api-endpoints.module';

@Module({
  imports: [ApiEndpointsModule],
  controllers: [ProxyController],
  providers: [ProxyService],
})
export class ProxyModule {}
