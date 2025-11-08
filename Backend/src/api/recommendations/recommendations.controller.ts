import { Controller, Get, Post, Param, Query, Body } from '@nestjs/common';
import { RecommendationsService } from './recommendations.service';
import { RecommendationsQueryDto } from './dto/recommendations-query.dto';
import { ApplyRecommendationDto } from './dto/apply-recommendation.dto';

@Controller('recommendations')
export class RecommendationsController {
  constructor(private readonly recommendationsService: RecommendationsService) {}

  @Get()
  async findAll(@Query() query: RecommendationsQueryDto) {
    return this.recommendationsService.findAll(query);
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.recommendationsService.findOne(id);
  }

  @Post(':id/apply')
  async apply(@Param('id') id: string, @Body() dto: ApplyRecommendationDto) {
    return this.recommendationsService.apply(id, dto);
  }

  @Post(':id/reject')
  async reject(@Param('id') id: string) {
    return this.recommendationsService.reject(id);
  }
}
