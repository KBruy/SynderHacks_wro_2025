import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Enable CORS for frontend
  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true,
  });

  // Global validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  // API prefix
  app.setGlobalPrefix('api/v1');

  const port = process.env.PORT || 3000;
  await app.listen(port);

  console.log('');
  console.log('🚀 Sales Optimizer Backend');
  console.log(`📍 Running on: http://localhost:${port}`);
  console.log(`📍 API Base: http://localhost:${port}/api/v1`);
  console.log(`📍 Health Check: http://localhost:${port}/api/v1/health`);
  console.log('');
}

bootstrap();
