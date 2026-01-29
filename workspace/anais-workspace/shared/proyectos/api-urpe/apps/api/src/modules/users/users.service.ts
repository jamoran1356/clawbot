import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../../infra/prisma';
import { CreateUserDto, UpdateUserDto } from './dto';
import { hash } from '@node-rs/argon2';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async create(dto: CreateUserDto) {
    const hashedPassword = await hash(dto.password, {
      memoryCost: 19456,
      timeCost: 2,
      outputLen: 32,
      parallelism: 1,
    });

    return this.prisma.user.create({
      data: {
        ...dto,
        password: hashedPassword,
      },
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        isActive: true,
        createdAt: true,
      },
    });
  }

  async findAll(role?: string) {
    const where = role ? { role: role as any } : {};

    return this.prisma.user.findMany({
      where,
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        isActive: true,
        createdAt: true,
        _count: {
          select: {
            apis: true,
            apiKeys: true,
          },
        },
      },
      orderBy: { createdAt: 'desc' },
    });
  }

  async findOne(id: string) {
    const user = await this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        isActive: true,
        createdAt: true,
        updatedAt: true,
      },
    });

    if (!user) {
      throw new NotFoundException('User not found');
    }

    return user;
  }

  async update(id: string, dto: UpdateUserDto) {
    const data: any = { ...dto };

    if (dto.password) {
      data.password = await hash(dto.password, {
        memoryCost: 19456,
        timeCost: 2,
        outputLen: 32,
        parallelism: 1,
      });
    }

    return this.prisma.user.update({
      where: { id },
      data,
      select: {
        id: true,
        email: true,
        name: true,
        role: true,
        isActive: true,
        updatedAt: true,
      },
    });
  }

  async remove(id: string) {
    await this.prisma.user.delete({ where: { id } });
    return { message: 'User deleted successfully' };
  }

  async getUserStats(id: string) {
    const [user, apisCount, requestsCount, emailsCount] = await Promise.all([
      this.findOne(id),
      this.prisma.apiEndpoint.count({ where: { userId: id } }),
      this.prisma.request.count({
        where: { endpoint: { userId: id } },
      }),
      this.prisma.emailCampaign.count({ where: { userId: id } }),
    ]);

    const last30Days = new Date();
    last30Days.setDate(last30Days.getDate() - 30);

    const recentRequests = await this.prisma.request.count({
      where: {
        endpoint: { userId: id },
        createdAt: { gte: last30Days },
      },
    });

    return {
      user,
      stats: {
        totalApis: apisCount,
        totalRequests: requestsCount,
        recentRequests,
        totalEmails: emailsCount,
      },
    };
  }
}
