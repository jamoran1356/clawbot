import { registerAs } from '@nestjs/config';

export default registerAs('email', () => ({
  smtp: {
    host: process.env.SMTP_HOST || 'localhost',
    port: parseInt(process.env.SMTP_PORT || '587', 10),
    secure: process.env.SMTP_SECURE === 'true', // true for 465, false for other ports
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD,
    },
  },
  from: {
    email: process.env.SMTP_FROM_EMAIL || 'noreply@example.com',
    name: process.env.SMTP_FROM_NAME || 'API Platform',
  },
  batchSize: parseInt(process.env.EMAIL_BATCH_SIZE || '100', 10),
  delayBetweenBatches: parseInt(process.env.EMAIL_DELAY_BETWEEN_BATCHES || '1000', 10),
}));
