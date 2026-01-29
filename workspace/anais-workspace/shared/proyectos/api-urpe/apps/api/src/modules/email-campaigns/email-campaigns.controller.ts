import { Controller, Get, Post, Put, Delete, Body, Param, UseGuards } from '@nestjs/common';
import { EmailCampaignsService } from './email-campaigns.service';
import { JwtAuthGuard } from '../../common/guards';
import { CurrentUser } from '../../common/decorators';
import { CreateEmailCampaignDto, UpdateEmailCampaignDto, SendCampaignDto, UploadRecipientsDto } from './dto';

@Controller('email-campaigns')
@UseGuards(JwtAuthGuard)
export class EmailCampaignsController {
  constructor(private readonly service: EmailCampaignsService) {}

  @Post()
  create(@Body() dto: CreateEmailCampaignDto, @CurrentUser() user: any) {
    return this.service.create(dto, user.id);
  }

  @Get()
  findAll(@CurrentUser() user: any) {
    return this.service.findAll(user.id, user.role);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.findOne(id, user.id, user.role);
  }

  @Put(':id')
  update(
    @Param('id') id: string,
    @Body() dto: UpdateEmailCampaignDto,
    @CurrentUser() user: any,
  ) {
    return this.service.update(id, dto, user.id, user.role);
  }

  @Delete(':id')
  remove(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.remove(id, user.id, user.role);
  }

  @Post(':id/send')
  send(
    @Param('id') id: string,
    @Body() dto: SendCampaignDto,
    @CurrentUser() user: any,
  ) {
    return this.service.sendCampaign(id, user.id, user.role, dto);
  }

  @Get(':id/status')
  getStatus(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.getCampaignStatus(id, user.id, user.role);
  }

  @Post(':id/cancel')
  cancel(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.cancelCampaign(id, user.id, user.role);
  }

  @Post(':id/recipients')
  addRecipients(
    @Param('id') id: string,
    @Body() dto: UploadRecipientsDto,
    @CurrentUser() user: any,
  ) {
    return this.service.addRecipients(id, dto.emails, user.id, user.role);
  }
}

