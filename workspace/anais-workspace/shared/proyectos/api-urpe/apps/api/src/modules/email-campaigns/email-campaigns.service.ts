import { Injectable, NotFoundException, ForbiddenException } from '@nestjs/common';
import { PrismaService } from '../../infra/prisma';
import { CreateEmailCampaignDto, UpdateEmailCampaignDto, SendCampaignDto } from './dto';
import { Queue } from 'bullmq';
import { InjectQueue } from '@nestjs/bullmq';

@Injectable()
export class EmailCampaignsService {
  constructor(
    private prisma: PrismaService,
    @InjectQueue('email-campaigns') private emailQueue: Queue,
  ) {}

  async create(dto: CreateEmailCampaignDto, userId: string) {
    return this.prisma.emailCampaign.create({
      data: {
        ...dto,
        userId,
        status: 'DRAFT',
      },
    });
  }

  async findAll(userId: string, role: string) {
    const where = role === 'ADMIN' ? {} : { userId };

    return this.prisma.emailCampaign.findMany({
      where,
      orderBy: { createdAt: 'desc' },
    });
  }

  async findOne(id: string, userId: string, role: string) {
    const campaign = await this.prisma.emailCampaign.findUnique({
      where: { id },
    });

    if (!campaign) {
      throw new NotFoundException('Email campaign not found');
    }

    if (role !== 'ADMIN' && campaign.userId !== userId) {
      throw new ForbiddenException('Access denied');
    }

    return campaign;
  }

  async update(id: string, dto: UpdateEmailCampaignDto, userId: string, role: string) {
    await this.findOne(id, userId, role);

    return this.prisma.emailCampaign.update({
      where: { id },
      data: dto,
    });
  }

  async remove(id: string, userId: string, role: string) {
    await this.findOne(id, userId, role);

    await this.prisma.emailCampaign.delete({ where: { id } });

    return { message: 'Email campaign deleted successfully' };
  }

  async sendCampaign(id: string, userId: string, role: string, options?: SendCampaignDto) {
    const campaign = await this.findOne(id, userId, role);

    if (campaign.status === 'SENT') {
      throw new ForbiddenException('Campaign already sent');
    }

    if (campaign.status === 'SENDING') {
      throw new ForbiddenException('Campaign is currently being sent');
    }

    // Validar que hay destinatarios
    const recipients = Array.isArray(campaign.recipients) ? campaign.recipients : [];
    if (recipients.length === 0) {
      throw new ForbiddenException('Campaign has no recipients');
    }

    // Agregar job a la cola de BullMQ
    const job = await this.emailQueue.add('send-campaign', {
      campaignId: id,
      recipients,
      subject: campaign.subject,
      body: campaign.body,
      fromEmail: campaign.fromEmail,
      fromName: campaign.fromName,
      batchSize: options?.batchSize,
      delayBetweenBatches: options?.delayBetweenBatches,
    }, {
      removeOnComplete: false, // Mantener jobs completados para auditoría
      removeOnFail: false,
      attempts: 3, // Reintentar hasta 3 veces si falla
      backoff: {
        type: 'exponential',
        delay: 5000, // Delay inicial de 5s
      },
    });

    // Actualizar estado inmediatamente
    await this.prisma.emailCampaign.update({
      where: { id },
      data: { status: 'QUEUED' },
    });

    return {
      message: 'Campaign queued for sending',
      campaignId: id,
      jobId: job.id,
      recipientCount: recipients.length,
    };
  }

  async getCampaignStatus(id: string, userId: string, role: string) {
    const campaign = await this.findOne(id, userId, role);

    // Buscar el job asociado en la cola
    const jobs = await this.emailQueue.getJobs(['waiting', 'active', 'completed', 'failed']);
    const job = jobs.find(j => j.data.campaignId === id);

    return {
      campaign: {
        id: campaign.id,
        name: campaign.name,
        status: campaign.status,
        sentCount: campaign.sentCount,
        failedCount: campaign.failedCount,
        totalRecipients: Array.isArray(campaign.recipients) ? campaign.recipients.length : 0,
        sentAt: campaign.sentAt,
        createdAt: campaign.createdAt,
      },
      job: job ? {
        id: job.id,
        state: await job.getState(),
        progress: job.progress,
        attemptsMade: job.attemptsMade,
        processedOn: job.processedOn,
        finishedOn: job.finishedOn,
        failedReason: job.failedReason,
      } : null,
    };
  }

  async cancelCampaign(id: string, userId: string, role: string) {
    const campaign = await this.findOne(id, userId, role);

    if (campaign.status !== 'QUEUED' && campaign.status !== 'SENDING') {
      throw new ForbiddenException('Cannot cancel campaign with status: ' + campaign.status);
    }

    // Buscar y cancelar el job
    const jobs = await this.emailQueue.getJobs(['waiting', 'active']);
    const job = jobs.find(j => j.data.campaignId === id);

    if (job) {
      await job.remove();
    }

    // Actualizar estado
    await this.prisma.emailCampaign.update({
      where: { id },
      data: { status: 'CANCELLED' },
    });

    return { message: 'Campaign cancelled successfully' };
  }

  async addRecipients(id: string, emails: string[], userId: string, role: string) {
    const campaign = await this.findOne(id, userId, role);

    if (campaign.status !== 'DRAFT') {
      throw new ForbiddenException('Can only add recipients to draft campaigns');
    }

    const currentRecipients = Array.isArray(campaign.recipients) ? campaign.recipients : [];
    const uniqueRecipients = [...new Set([...currentRecipients, ...emails])];

    return this.prisma.emailCampaign.update({
      where: { id },
      data: { recipients: uniqueRecipients },
    });
  }
}

