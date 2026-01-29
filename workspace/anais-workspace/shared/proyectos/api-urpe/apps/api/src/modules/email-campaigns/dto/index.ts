import { IsString, IsNotEmpty, IsEmail, IsOptional, IsArray, IsDateString, IsNumber } from 'class-validator';

export class CreateEmailCampaignDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsNotEmpty()
  subject: string;

  @IsString()
  @IsNotEmpty()
  body: string;

  @IsEmail()
  @IsNotEmpty()
  fromEmail: string;

  @IsString()
  @IsOptional()
  fromName?: string;

  @IsArray()
  @IsNotEmpty()
  recipients: string[]; // Array de emails

  @IsDateString()
  @IsOptional()
  scheduledAt?: string;
}

export class UpdateEmailCampaignDto {
  @IsString()
  @IsOptional()
  name?: string;

  @IsString()
  @IsOptional()
  subject?: string;

  @IsString()
  @IsOptional()
  body?: string;

  @IsArray()
  @IsOptional()
  recipients?: string[];

  @IsDateString()
  @IsOptional()
  scheduledAt?: string;
}

export class SendCampaignDto {
  @IsNumber()
  @IsOptional()
  batchSize?: number; // Tamaño de lote personalizado

  @IsNumber()
  @IsOptional()
  delayBetweenBatches?: number; // Delay en ms entre lotes
}

export class UploadRecipientsDto {
  @IsArray()
  @IsNotEmpty()
  emails: string[];
}
