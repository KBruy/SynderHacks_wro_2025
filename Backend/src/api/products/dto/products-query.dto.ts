import { IsOptional, IsString, IsEnum, IsInt, Min } from 'class-validator';
import { Type } from 'class-transformer';

export class ProductsQueryDto {
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
  @IsEnum(['LOW', 'MEDIUM', 'HIGH'])
  rotation?: 'LOW' | 'MEDIUM' | 'HIGH';

  @IsOptional()
  @IsString()
  channel?: string;

  @IsOptional()
  @IsString()
  q?: string; // search query
}
