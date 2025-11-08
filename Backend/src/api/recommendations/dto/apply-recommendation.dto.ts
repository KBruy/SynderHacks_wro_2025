import { IsOptional, IsString, IsDateString } from 'class-validator';

export class ApplyRecommendationDto {
  @IsOptional()
  @IsString()
  actor?: string; // User ID who applied it

  @IsOptional()
  @IsDateString()
  schedule?: string | null; // Schedule for later
}
