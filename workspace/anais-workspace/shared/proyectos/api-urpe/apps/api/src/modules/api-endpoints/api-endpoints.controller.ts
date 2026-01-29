import { Controller, Get, Post, Put, Delete, Body, Param, UseGuards, Query } from '@nestjs/common';
import { ApiEndpointsService } from './api-endpoints.service';
import { CreateApiEndpointDto, UpdateApiEndpointDto } from './dto';
import { JwtAuthGuard } from '../../common/guards';
import { CurrentUser } from '../../common/decorators';

@Controller('api-endpoints')
@UseGuards(JwtAuthGuard)
export class ApiEndpointsController {
  constructor(private readonly service: ApiEndpointsService) {}

  @Post()
  create(@Body() dto: CreateApiEndpointDto, @CurrentUser() user: any) {
    return this.service.create(dto, user.id);
  }

  @Get()
  findAll(@CurrentUser() user: any, @Query('status') status?: string) {
    return this.service.findAll(user.id, user.role, status);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.findOne(id, user.id, user.role);
  }

  @Put(':id')
  update(
    @Param('id') id: string,
    @Body() dto: UpdateApiEndpointDto,
    @CurrentUser() user: any,
  ) {
    return this.service.update(id, dto, user.id, user.role);
  }

  @Delete(':id')
  remove(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.remove(id, user.id, user.role);
  }

  @Get(':id/stats')
  getStats(@Param('id') id: string, @CurrentUser() user: any) {
    return this.service.getStats(id, user.id, user.role);
  }
}
