import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { BullModule } from '@nestjs/bullmq';
import { HealthModule } from './modules/health/health.module';
import { PrismaModule } from './infra/prisma';
import { AuthModule } from './modules/auth/auth.module';
import { UsersModule } from './modules/users/users.module';
import { ApiEndpointsModule } from './modules/api-endpoints/api-endpoints.module';
import { ProxyModule } from './modules/proxy/proxy.module';
import { EmailCampaignsModule } from './modules/email-campaigns/email-campaigns.module';
import { authConfig } from './config/auth.config';
import { databaseConfig } from './config/database.config';
import { redisConfig } from './config/redis.config';
import emailConfig from './config/email.config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
      load: [authConfig, databaseConfig, redisConfig, emailConfig],
    }),
    BullModule.forRoot({
      connection: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT || '6379', 10),
        password: process.env.REDIS_PASSWORD,
      },
    }),
    PrismaModule,
    HealthModule,
    AuthModule,
    UsersModule,
    ApiEndpointsModule,
    ProxyModule,
    EmailCampaignsModule,
  ],
})
export class AppModule {}

