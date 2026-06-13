# 🤖 Auto-Publisher v3.0

Sistema de publicación automática multi-plataforma 24/7. Funciona sin intervención humana.

## Plataformas compatibles
- 📱 WhatsApp (link directo)
- ✈️ Telegram (link directo + Bot API)
- 𝕏 Twitter/X
- 👍 Facebook (Graph API + Share link)
- 💼 LinkedIn
- 📌 Pinterest
- 🤖 Reddit
- 📧 Email

## Apps promocionadas
- **InvoicePro** - Generador de facturas profesionales
- **RankUp Pro** - 12 herramientas premium por niveles (1€-100€)
- **RankUp Business** - Suite empresarial (250€-10.000€+)

## Pago
- **PayPal**: carlos.valderas8@gmail.com
- **Pago único**: Desde 1€ hasta 10.000€+

## Cómo se mantiene vivo
- 🔄 Daemon en background con auto-recuperación
- ⏰ Cron cada 5 minutos verifica que esté vivo
- 🌐 Servidor webhook para monitoreo externo
- 🛡️ Sistema launcher resiliente

## Endpoints
- `http://localhost:8080/` - Panel de control
- `http://localhost:8080/status` - Estado JSON
- `http://localhost:8080/run` - Ejecutar ciclo manual
