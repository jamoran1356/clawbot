import { IsString, IsNotEmpty, IsOptional, IsEnum, IsBoolean, IsInt, IsUrl, IsJSON } from 'class-validator';

export class CreateApiEndpointDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsOptional()
  slug?: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsEnum(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
  @IsOptional()
  method?: string;

  @IsUrl()
  @IsNotEmpty()
  targetUrl: string;

  @IsOptional()
  requestTransform?: any;

  @IsOptional()
  responseTransform?: any;

  @IsOptional()
  headers?: any;

  @IsBoolean()
  @IsOptional()
  requireApiKey?: boolean;

  @IsOptional()
  allowedOrigins?: any;

  @IsInt()
  @IsOptional()
  rateLimit?: number;

  @IsString()
  @IsOptional()
  connectionId?: string;
}

export class UpdateApiEndpointDto {
  @IsString()
  @IsOptional()
  name?: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsEnum(['ACTIVE', 'INACTIVE', 'SUSPENDED'])
  @IsOptional()
  status?: 'ACTIVE' | 'INACTIVE' | 'SUSPENDED';

  @IsUrl()
  @IsOptional()
  targetUrl?: string;

  @IsOptional()
  requestTransform?: any;

  @IsOptional()
  responseTransform?: any;

  @IsOptional()
  headers?: any;

  @IsInt()
  @IsOptional()
  rateLimit?: number;
}
