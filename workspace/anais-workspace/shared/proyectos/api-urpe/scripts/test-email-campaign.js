#!/usr/bin/env node

/**
 * Script de prueba para el sistema de envío masivo de emails
 * 
 * Uso:
 *   node scripts/test-email-campaign.js
 * 
 * Requisitos:
 * - API corriendo en localhost:3000
 * - Worker corriendo
 * - Redis corriendo
 * - Usuario creado en la BD
 */

const API_URL = 'http://localhost:3000';
const TEST_EMAIL = 'admin@example.com';
const TEST_PASSWORD = 'password123';

async function main() {
  console.log('🚀 Iniciando test de sistema de email campaigns\n');

  try {
    // 1. Login
    console.log('1️⃣ Autenticando...');
    const loginResponse = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: TEST_EMAIL,
        password: TEST_PASSWORD,
      }),
    });

    if (!loginResponse.ok) {
      throw new Error(`Login failed: ${loginResponse.status}`);
    }

    const { access_token } = await loginResponse.json();
    console.log('✅ Autenticado correctamente\n');

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${access_token}`,
    };

    // 2. Crear campaña
    console.log('2️⃣ Creando campaña de prueba...');
    const createResponse = await fetch(`${API_URL}/email-campaigns`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        name: `Test Campaign ${new Date().toISOString()}`,
        subject: 'Email de Prueba - Sistema de Envío Masivo',
        body: `
          <html>
            <body>
              <h1>¡Hola!</h1>
              <p>Este es un email de prueba del sistema de envío masivo.</p>
              <p>Enviado el: ${new Date().toLocaleString()}</p>
            </body>
          </html>
        `,
        fromEmail: 'test@empresa.com',
        fromName: 'Sistema de Pruebas',
        recipients: [
          'test1@example.com',
          'test2@example.com',
          'test3@example.com',
        ],
      }),
    });

    if (!createResponse.ok) {
      throw new Error(`Create campaign failed: ${createResponse.status}`);
    }

    const campaign = await createResponse.json();
    console.log('✅ Campaña creada:', campaign.id);
    console.log(`   Nombre: ${campaign.name}`);
    console.log(`   Estado: ${campaign.status}\n`);

    // 3. Añadir más destinatarios
    console.log('3️⃣ Añadiendo destinatarios adicionales...');
    const addRecipientsResponse = await fetch(`${API_URL}/email-campaigns/${campaign.id}/recipients`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        emails: ['test4@example.com', 'test5@example.com'],
      }),
    });

    if (!addRecipientsResponse.ok) {
      throw new Error(`Add recipients failed: ${addRecipientsResponse.status}`);
    }

    console.log('✅ Destinatarios añadidos\n');

    // 4. Enviar campaña
    console.log('4️⃣ Enviando campaña...');
    const sendResponse = await fetch(`${API_URL}/email-campaigns/${campaign.id}/send`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        batchSize: 2,
        delayBetweenBatches: 500,
      }),
    });

    if (!sendResponse.ok) {
      throw new Error(`Send campaign failed: ${sendResponse.status}`);
    }

    const sendResult = await sendResponse.json();
    console.log('✅ Campaña encolada para envío');
    console.log(`   Job ID: ${sendResult.jobId}`);
    console.log(`   Destinatarios: ${sendResult.recipientCount}\n`);

    // 5. Monitorear progreso
    console.log('5️⃣ Monitoreando progreso...\n');
    
    let completed = false;
    let attempts = 0;
    const maxAttempts = 30;

    while (!completed && attempts < maxAttempts) {
      await sleep(2000);
      attempts++;

      const statusResponse = await fetch(`${API_URL}/email-campaigns/${campaign.id}/status`, {
        method: 'GET',
        headers,
      });

      if (!statusResponse.ok) {
        throw new Error(`Get status failed: ${statusResponse.status}`);
      }

      const status = await statusResponse.json();
      const progress = status.job?.progress || 0;
      
      console.log(`   Estado: ${status.campaign.status} | Enviados: ${status.campaign.sentCount}/${status.campaign.totalRecipients} | Progreso: ${progress.toFixed(1)}%`);

      if (status.campaign.status === 'SENT' || status.campaign.status === 'FAILED') {
        completed = true;
        console.log('\n✅ Campaña finalizada');
        console.log(`   Estado final: ${status.campaign.status}`);
        console.log(`   Enviados: ${status.campaign.sentCount}`);
        console.log(`   Fallidos: ${status.campaign.failedCount}`);
      }
    }

    if (!completed) {
      console.log('\n⚠️  Tiempo de espera agotado. Verifica el worker.');
    }

    // 6. Listar campañas
    console.log('\n6️⃣ Listando todas las campañas...');
    const listResponse = await fetch(`${API_URL}/email-campaigns`, {
      method: 'GET',
      headers,
    });

    if (!listResponse.ok) {
      throw new Error(`List campaigns failed: ${listResponse.status}`);
    }

    const campaigns = await listResponse.json();
    console.log(`✅ Total de campañas: ${campaigns.length}\n`);

    console.log('🎉 Test completado exitosamente!\n');

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

main();
