import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

console.log('🚀 Starting NewsFlow application...');

platformBrowserDynamic().bootstrapModule(AppModule)
  .then(() => {
    console.log('✅ Application bootstrap successful');
  })
  .catch(err => {
    console.error('❌ Application bootstrap failed:', err);
  });

