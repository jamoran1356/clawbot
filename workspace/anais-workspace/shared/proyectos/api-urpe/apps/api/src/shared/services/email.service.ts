import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as nodemailer from 'nodemailer';
import { Transporter } from 'nodemailer';

export interface EmailOptions {
  to: string | string[];
  subject: string;
  html?: string;
  text?: string;
  from?: string;
  fromName?: string;
}

@Injectable()
export class EmailService {
  private readonly logger = new Logger(EmailService.name);
  private transporter: Transporter;

  constructor(private configService: ConfigService) {
    this.initializeTransporter();
  }

  private initializeTransporter() {
    const smtpConfig = this.configService.get('email.smtp');
    
    this.transporter = nodemailer.createTransport({
      host: smtpConfig.host,
      port: smtpConfig.port,
      secure: smtpConfig.secure,
      auth: {
        user: smtpConfig.auth.user,
        pass: smtpConfig.auth.pass,
      },
    });

    this.logger.log(`SMTP transporter initialized: ${smtpConfig.host}:${smtpConfig.port}`);
  }

  async sendEmail(options: EmailOptions): Promise<boolean> {
    try {
      const defaultFrom = this.configService.get('email.from');
      const from = options.fromName || options.from
        ? `"${options.fromName || defaultFrom.name}" <${options.from || defaultFrom.email}>`
        : `"${defaultFrom.name}" <${defaultFrom.email}>`;

      const mailOptions = {
        from,
        to: Array.isArray(options.to) ? options.to.join(',') : options.to,
        subject: options.subject,
        html: options.html,
        text: options.text,
      };

      const info = await this.transporter.sendMail(mailOptions);
      this.logger.log(`Email sent: ${info.messageId} to ${mailOptions.to}`);
      return true;
    } catch (error) {
      this.logger.error(`Failed to send email: ${error.message}`, error.stack);
      return false;
    }
  }

  async sendBulkEmails(
    recipients: string[],
    subject: string,
    body: string,
    fromEmail?: string,
    fromName?: string,
  ): Promise<{ sent: number; failed: number }> {
    let sent = 0;
    let failed = 0;

    for (const recipient of recipients) {
      const success = await this.sendEmail({
        to: recipient,
        subject,
        html: body,
        from: fromEmail,
        fromName,
      });

      if (success) {
        sent++;
      } else {
        failed++;
      }
    }

    return { sent, failed };
  }

  async verifyConnection(): Promise<boolean> {
    try {
      await this.transporter.verify();
      this.logger.log('SMTP connection verified successfully');
      return true;
    } catch (error) {
      this.logger.error(`SMTP connection failed: ${error.message}`, error.stack);
      return false;
    }
  }
}
