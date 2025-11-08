import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHealth() {
    return {
      status: 'ok',
      time: new Date().toISOString(),
      service: 'sales-optimizer-api',
      version: '1.0.0',
    };
  }
}
