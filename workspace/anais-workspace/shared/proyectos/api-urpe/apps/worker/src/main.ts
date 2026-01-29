import { NestFactory } from '@nestjs/core';
import { WorkerModule } from './worker.module';

async function bootstrap() {
  const app = await NestFactory.createApplicationContext(WorkerModule);
  
  console.log('Worker started and listening for jobs...');
  
  process.on('SIGTERM', async () => {
    await app.close();
  });
}

bootstrap();
