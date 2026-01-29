import { Module } from '@nestjs/common';
import { BullModule } from '@nestjs/bullmq';
import { EmailCampaignsController } from './email-campaigns.controller';
import { EmailCampaignsService } from './email-campaigns.service';

@Module({
  imports: [
    BullModule.registerQueue({
      name: 'email-campaigns',
    }),
  ],
  controllers: [EmailCampaignsController],
  providers: [EmailCampaignsService],
})
export class EmailCampaignsModule {}

