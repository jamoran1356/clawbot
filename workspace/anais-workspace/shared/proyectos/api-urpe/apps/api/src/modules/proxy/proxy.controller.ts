import { Controller, All, Param, Req, Res, Headers } from '@nestjs/common';
import { Request, Response } from 'express';
import { ProxyService } from './proxy.service';

@Controller('proxy')
export class ProxyController {
  constructor(private readonly proxyService: ProxyService) {}

  @All(':slug/*')
  async handleWildcard(
    @Param('slug') slug: string,
    @Req() req: Request,
    @Res() res: Response,
    @Headers('x-api-key') apiKey?: string,
  ) {
    return this.proxyService.handleRequest(slug, req, res, apiKey);
  }

  @All(':slug')
  async handle(
    @Param('slug') slug: string,
    @Req() req: Request,
    @Res() res: Response,
    @Headers('x-api-key') apiKey?: string,
  ) {
    return this.proxyService.handleRequest(slug, req, res, apiKey);
  }
}
