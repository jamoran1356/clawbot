import { Module } from '@nestjs/common';
import { ApiEndpointsController } from './api-endpoints.controller';
import { ApiEndpointsService } from './api-endpoints.service';

@Module({
  controllers: [ApiEndpointsController],
  providers: [ApiEndpointsService],
  exports: [ApiEndpointsService],
})
export class ApiEndpointsModule {}
