import { Processor, WorkerHost } from '@nestjs/bullmq';
import { Logger } from '@nestjs/common';
import { Job } from 'bullmq';
import { PrismaClient } from '@prisma/client';
import * as nodemailer from 'nodemailer';
import { Transporter } from 'nodemailer';

interface SendEmailJobData {
  campaignId: string;
  recipients: string[];
  subject: string;
  body: string;
  fromEmail: string;
  fromName?: string;
  batchSize?: number;
  delayBetweenBatches?: number;
}

@Processor('email-campaigns')
export class EmailCampaignProcessor extends WorkerHost {
  private readonly logger = new Logger(EmailCampaignProcessor.name);
  private prisma: PrismaClient;
  private transporter: Transporter;

  constructor() {
    super();
    this.prisma = new PrismaClient();
    this.initializeTransporter();
  }

  private initializeTransporter() {
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'localhost',
      port: parseInt(process.env.SMTP_PORT || '587', 10),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASSWORD,
      },
    });
  }

  async process(job: Job<SendEmailJobData>): Promise<any> {
    const { campaignId, recipients, subject, body, fromEmail, fromName, batchSize = 100, delayBetweenBatches = 1000 } = job.data;

    this.logger.log(`Processing email campaign ${campaignId} with ${recipients.length} recipients`);

    try {
      // Actualizar estado a SENDING
      await this.prisma.emailCampaign.update({
        where: { id: campaignId },
        data: { status: 'SENDING' },
      });

      let sentCount = 0;
      let failedCount = 0;

      // Procesar en lotes
      for (let i = 0; i < recipients.length; i += batchSize) {
        const batch = recipients.slice(i, i + batchSize);
        const batchNumber = Math.floor(i / batchSize) + 1;
        const totalBatches = Math.ceil(recipients.length / batchSize);

        this.logger.log(`Processing batch ${batchNumber}/${totalBatches} (${batch.length} emails)`);

        // Enviar emails del lote
        for (const recipient of batch) {
          try {
            await this.sendEmail({
              to: recipient,
              subject,
              body,
              fromEmail,
              fromName,
            });
            sentCount++;
            
            // Actualizar progreso cada 10 emails
            if (sentCount % 10 === 0) {
              await this.updateProgress(campaignId, sentCount, failedCount);
              await job.updateProgress((sentCount / recipients.length) * 100);
            }
          } catch (error) {
            this.logger.error(`Failed to send email to ${recipient}: ${error.message}`);
            failedCount++;
          }
        }

        // Delay entre lotes para no saturar el servidor SMTP
        if (i + batchSize < recipients.length) {
          await this.sleep(delayBetweenBatches);
        }
      }

      // Actualizar campaña como completada
      await this.prisma.emailCampaign.update({
        where: { id: campaignId },
        data: {
          status: 'SENT',
          sentAt: new Date(),
          sentCount,
          failedCount,
        },
      });

      this.logger.log(`Campaign ${campaignId} completed: ${sentCount} sent, ${failedCount} failed`);

      return { sentCount, failedCount };
    } catch (error) {
      this.logger.error(`Campaign ${campaignId} failed: ${error.message}`, error.stack);

      // Marcar campaña como fallida
      await this.prisma.emailCampaign.update({
        where: { id: campaignId },
        data: { status: 'FAILED' },
      });

      throw error;
    }
  }

  private async sendEmail(options: {
    to: string;
    subject: string;
    body: string;
    fromEmail: string;
    fromName?: string;
  }): Promise<void> {
    const from = options.fromName
      ? `"${options.fromName}" <${options.fromEmail}>`
      : options.fromEmail;

    await this.transporter.sendMail({
      from,
      to: options.to,
      subject: options.subject,
      html: options.body,
    });
  }

  private async updateProgress(campaignId: string, sentCount: number, failedCount: number): Promise<void> {
    await this.prisma.emailCampaign.update({
      where: { id: campaignId },
      data: { sentCount, failedCount },
    });
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async onModuleDestroy() {
    await this.prisma.$disconnect();
  }
}
