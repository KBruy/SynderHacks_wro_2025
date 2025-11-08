import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../../common/prisma.service';
import { ProductsQueryDto } from './dto/products-query.dto';

@Injectable()
export class ProductsService {
  constructor(private prisma: PrismaService) {}

  async findAll(query: ProductsQueryDto) {
    const { page = 1, limit = 20, rotation, channel, q } = query;
    const skip = (page - 1) * limit;

    // Build where clause
    const where = {
      ...(rotation && { rotation }),
      ...(q && {
        OR: [
          { name: { contains: q, mode: 'insensitive' as const } },
          { sku: { contains: q, mode: 'insensitive' as const } },
        ],
      }),
      ...(channel && {
        channels: {
          some: {
            channel: {
              id: channel,
            },
          },
        },
      }),
    };

    const [items, total] = await Promise.all([
      this.prisma.product.findMany({
        where,
        skip,
        take: limit,
        include: {
          channels: {
            include: {
              channel: {
                select: {
                  id: true,
                  name: true,
                  type: true,
                  status: true,
                },
              },
            },
          },
          _count: {
            select: {
              recommendations: true,
            },
          },
        },
        orderBy: {
          createdAt: 'desc',
        },
      }),
      this.prisma.product.count({ where }),
    ]);

    return {
      items,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  async findOne(sku: string) {
    const product = await this.prisma.product.findUnique({
      where: { sku },
      include: {
        channels: {
          include: {
            channel: true,
          },
        },
        recommendations: {
          where: {
            status: 'PENDING',
          },
          orderBy: {
            impact: 'desc',
          },
        },
      },
    });

    if (!product) {
      throw new NotFoundException(`Product with SKU ${sku} not found`);
    }

    return product;
  }
}
