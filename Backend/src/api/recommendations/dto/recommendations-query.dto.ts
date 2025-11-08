import { IsOptional, IsString, IsEnum, IsInt, Min } from 'class-validator';
import { Type } from 'class-transformer';

export class RecommendationsQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  limit?: number = 20;

  @IsOptional()
  @IsEnum(['PENDING', 'APPLIED', 'REJECTED', 'EXPIRED'])
  status?: 'PENDING' | 'APPLIED' | 'REJECTED' | 'EXPIRED';

  @IsOptional()
  @IsEnum([
    'PRICE_CHANGE',
    'PROMOTION',
    'BUNDLE',
    'TITLE_OPTIMIZATION',
    'IMAGE_UPDATE',
    'CHANNEL_DISTRIBUTION',
  ])
  type?:
    | 'PRICE_CHANGE'
    | 'PROMOTION'
    | 'BUNDLE'
    | 'TITLE_OPTIMIZATION'
    | 'IMAGE_UPDATE'
    | 'CHANNEL_DISTRIBUTION';

  @IsOptional()
  @IsString()
  sku?: string; // Product SKU filter
}
