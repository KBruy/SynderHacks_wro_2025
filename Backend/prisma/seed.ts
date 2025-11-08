import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Create test user
  const user = await prisma.user.upsert({
    where: { email: 'test@example.com' },
    update: {},
    create: {
      email: 'test@example.com',
      passwordHash: '$2b$10$abcdefghijklmnopqrstuvwxyz', // placeholder
      name: 'Test User',
    },
  });

  console.log('✅ Created user:', user.email);

  // Create test products
  const products = await Promise.all([
    prisma.product.upsert({
      where: { sku: 'PROD-001' },
      update: {},
      create: {
        sku: 'PROD-001',
        name: 'Wireless Bluetooth Headphones',
        description: 'High-quality wireless headphones with noise cancellation',
        price: 89.99,
        stock: 150,
        rotation: 'MEDIUM',
        views: 1250,
        ctr: 3.2,
        cr: 1.8,
        ageDays: 45,
      },
    }),
    prisma.product.upsert({
      where: { sku: 'PROD-002' },
      update: {},
      create: {
        sku: 'PROD-002',
        name: 'Smart Watch Pro',
        description: 'Feature-rich smartwatch with fitness tracking',
        price: 199.99,
        stock: 75,
        rotation: 'HIGH',
        views: 2100,
        ctr: 4.5,
        cr: 2.3,
        ageDays: 15,
      },
    }),
    prisma.product.upsert({
      where: { sku: 'PROD-003' },
      update: {},
      create: {
        sku: 'PROD-003',
        name: 'USB-C Cable 2m',
        description: 'Durable USB-C charging cable',
        price: 12.99,
        stock: 500,
        rotation: 'LOW',
        views: 450,
        ctr: 1.2,
        cr: 0.8,
        ageDays: 120,
      },
    }),
  ]);

  console.log(`✅ Created ${products.length} products`);

  // Create test channel
  const channel = await prisma.channel.upsert({
    where: { id: 'test-shopify-channel' },
    update: {},
    create: {
      id: 'test-shopify-channel',
      type: 'SHOPIFY',
      name: 'Test Shopify Store',
      status: 'CONNECTED',
    },
  });

  console.log('✅ Created channel:', channel.name);

  // Create test recommendations
  const recommendations = await Promise.all([
    prisma.recommendation.create({
      data: {
        productId: products[0].id,
        type: 'PRICE_CHANGE',
        title: 'Reduce price to match competition',
        summary: 'Market analysis shows competitors pricing similar products at $79.99',
        impact: 0.75,
        effort: 0.2,
        confidence: 0.85,
        status: 'PENDING',
        proposal: {
          currentPrice: 89.99,
          suggestedPrice: 79.99,
          reason: 'Competitive pricing analysis',
          expectedImpact: {
            ctrDelta: 0.04,
            crDelta: 0.02,
          },
        },
        reasoning:
          'Based on market analysis, reducing price to $79.99 aligns with competitor pricing and should increase CTR by 4% and CR by 2%.',
      },
    }),
    prisma.recommendation.create({
      data: {
        productId: products[2].id,
        type: 'PROMOTION',
        title: 'Create bundle offer',
        summary: 'Bundle with other accessories for bulk discount',
        impact: 0.65,
        effort: 0.4,
        confidence: 0.72,
        status: 'PENDING',
        proposal: {
          bundleProducts: ['PROD-003', 'PROD-001'],
          discount: 0.15,
          bundlePrice: 87.54,
        },
        reasoning: 'Creating bundles can help move slow-rotating inventory while increasing AOV.',
      },
    }),
  ]);

  console.log(`✅ Created ${recommendations.length} recommendations`);

  console.log('');
  console.log('✅ Seeding completed successfully!');
  console.log('');
  console.log('📊 Database summary:');
  console.log(`   - Users: 1`);
  console.log(`   - Products: ${products.length}`);
  console.log(`   - Channels: 1`);
  console.log(`   - Recommendations: ${recommendations.length}`);
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
