import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { PrismaService } from '../../common/prisma.service';
import { RecommendationsQueryDto } from './dto/recommendations-query.dto';
import { ApplyRecommendationDto } from './dto/apply-recommendation.dto';
import { RecommendationType } from '@prisma/client';

@Injectable()
export class RecommendationsService {
  constructor(private prisma: PrismaService) {}

  async findAll(query: RecommendationsQueryDto) {
    const { page = 1, limit = 20, status, type, sku } = query;
    const skip = (page - 1) * limit;

    // Build where clause
    const where = {
      ...(status && { status }),
      ...(type && { type: type as RecommendationType }),
      ...(sku && {
        product: {
          sku,
        },
      }),
    };

    const [items, total] = await Promise.all([
      this.prisma.recommendation.findMany({
        where,
        skip,
        take: limit,
        include: {
          product: {
            select: {
              id: true,
              sku: true,
              name: true,
              price: true,
              stock: true,
            },
          },
        },
        orderBy: [{ impact: 'desc' }, { createdAt: 'desc' }],
      }),
      this.prisma.recommendation.count({ where }),
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

  async findOne(id: string) {
    const recommendation = await this.prisma.recommendation.findUnique({
      where: { id },
      include: {
        product: true,
      },
    });

    if (!recommendation) {
      throw new NotFoundException(`Recommendation with ID ${id} not found`);
    }

    return recommendation;
  }

  async apply(id: string, dto: ApplyRecommendationDto) {
    // Find recommendation
    const recommendation = await this.prisma.recommendation.findUnique({
      where: { id },
      include: { product: true },
    });

    if (!recommendation) {
      throw new NotFoundException(`Recommendation with ID ${id} not found`);
    }

    if (recommendation.status !== 'PENDING') {
      throw new BadRequestException(
        `Recommendation is already ${recommendation.status.toLowerCase()}`,
      );
    }

    // For MVP, we'll just update the status
    // In production, this would trigger the ActionExecutor to apply changes to platforms
    const updated = await this.prisma.recommendation.update({
      where: { id },
      data: {
        status: 'APPLIED',
        appliedAt: new Date(),
      },
      include: {
        product: true,
      },
    });

    // TODO: In production, trigger action executor here
    // await this.actionExecutor.execute(updated);

    return {
      success: true,
      recommendation: updated,
      message: 'Recommendation applied successfully (MVP - actual platform sync not implemented)',
    };
  }

  async reject(id: string) {
    const recommendation = await this.prisma.recommendation.findUnique({
      where: { id },
    });

    if (!recommendation) {
      throw new NotFoundException(`Recommendation with ID ${id} not found`);
    }

    return await this.prisma.recommendation.update({
      where: { id },
      data: {
        status: 'REJECTED',
      },
    });
  }
}
