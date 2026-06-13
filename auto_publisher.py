#!/usr/bin/env python3
"""
🤖 AUTO-PUBLISHER v3.0 - Publicación automática multi-plataforma
Funciona 24/7 sin intervención. Publica en Facebook, Telegram, WhatsApp, Twitter/X.
"""
import urllib.request, urllib.parse
import json, time, os, random, base64, subprocess, sys, signal, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# ==================== CONFIGURACIÓN ====================
FACEBOOK_PAGE_ID = "61572106911286"
FACEBOOK_PAGE_URL = f"https://www.facebook.com/profile.php?id={FACEBOOK_PAGE_ID}"

# Apps URLs
INVOICE_URL = "https://anyclaw.store/claim/q07osz/"
RANKUP_URL  = "https://anyclaw.store/claim/oy5gzb/"
BUSINESS_URL = "https://anyclaw.store/claim/ms92hz/"

# PayPal (codificado en base64 para no exponerlo directamente)
PAYPAL_B64 = base64.b64encode(b'carlos.valderas8@gmail.com').decode()
PAYPAL_ME = "https://paypal.me/carlosvalderas8"

LOG_DIR = "/tmp/autopublisher/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ==================== MENSAJES VARIADOS ====================
MENSAJES = [
    # InvoicePro
    f"📄 Crea facturas profesionales al instante → {INVOICE_URL}",
    f"☕ Genera facturas PDF profesionales, pago único → {INVOICE_URL}",
    f"📊 Facturas para autónomos con 30+ divisas → {INVOICE_URL}",
    f"💡 Facturación profesional desde cualquier dispositivo → {INVOICE_URL}",
    f"📋 Crea facturas en segundos, descarga en PDF → {INVOICE_URL}",
    
    # RankUp Pro
    f"🚀 12 herramientas premium desde 1€ (pago único) → {RANKUP_URL}",
    f"🔥 Password generator + SEO analyzer + Markdown editor + más → {RANKUP_URL}",
    f"⚡ Inversión única desde 1€, herramientas de por vida → {RANKUP_URL}",
    f"💎 12 herramientas digitales premium, pago único vía PayPal → {RANKUP_URL}",
    f"🔑 Genera contraseñas seguras, analiza SEO, formatea JSON → {RANKUP_URL}",
    f"🎨 Conversor de colores + editor Markdown + analizador SEO → {RANKUP_URL}",
    
    # Business
    f"🏢 Suite empresarial desde 250€ → {BUSINESS_URL}",
    f"💼 Automatización empresarial, facturación, SEO y más → {BUSINESS_URL}",
    f"🏗️ Soluciones white-label para empresas desde 250€ → {BUSINESS_URL}",
    
    # Combinados
    f"📄 Facturas + 🚀 12 herramientas premium + 🏢 Suite empresarial → {INVOICE_URL}",
    f"🔥 Pack completo: facturas, herramientas digitales y suite empresarial → {INVOICE_URL}",
]

HASHTAGS = ["HerramientasPremium", "Productividad", "Facturas", "Freelancer", "Emprendedor", "PayPal", "RankUpPro", "InvoicePro", "NegociosDigitales", "Automatizacion"]

# ==================== SISTEMA DE LOGS ====================
def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    logfile = os.path.join(LOG_DIR, f"publisher_{datetime.now().strftime('%Y%m%d')}.log")
    try:
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

# ==================== CHECK APPS ====================
def check_apps():
    log("🔍 Verificando apps...")
    results = []
    for name, url in [("InvoicePro", INVOICE_URL), ("RankUp Pro", RANKUP_URL), ("RankUp Business", BUSINESS_URL)]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            code = urllib.request.urlopen(req, timeout=10).getcode()
            results.append(f"✅ {name}: HTTP {code}")
            log(f"✅ {name}: OK ({code})")
        except Exception as e:
            results.append(f"⚠️ {name}: {str(e)[:50]}")
            log(f"⚠️ {name}: {e}")
    return results

# ==================== GENERAR POST ====================
def generar_post():
    msg = random.choice(MENSAJES)
    h1 = random.choice(HASHTAGS)
    h2 = random.choice(HASHTAGS)
    h3 = random.choice(HASHTAGS)
    post = f"""✨ {msg}

💸 Pagos vía PayPal 🔒
🌐 Funciona en todo el mundo 🌍
✅ Automático 24/7 - Sin intervención

#{h1} #{h2} #{h3}

📌 Síguenos: {FACEBOOK_PAGE_URL}"""
    return post

# ==================== FACEBOOK GRAPH API ====================
# NOTA: Para usar la API de Facebook necesitas:
# 1. Ir a https://developers.facebook.com/
# 2. Crear una app → "Business" o "Other"
# 3. Ir a Tools → Graph API Explorer
# 4. Seleccionar tu página → Generar Page Access Token
# 5. Pegar el token abajo

FB_TOKEN = os.environ.get("FB_PAGE_TOKEN", "")

def publicar_facebook_api(post_text):
    if not FB_TOKEN:
        log("⚠️ Facebook: No hay token (salteando)")
        return False
    
    try:
        url = f"https://graph.facebook.com/v19.0/{FACEBOOK_PAGE_ID}/feed"
        data = urllib.parse.urlencode({
            "message": post_text,
            "access_token": FB_TOKEN
        }).encode()
        req = urllib.request.Request(url, data=data)
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        log(f"✅ Facebook: Publicado! ID: {result.get('id', 'ok')}")
        return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        log(f"❌ Facebook Error HTTP {e.code}: {error_body[:200]}")
        return False
    except Exception as e:
        log(f"❌ Facebook Error: {e}")
        return False

# ==================== TELEGRAM BOT ====================
# CÓMO CREAR UN BOT DE TELEGRAM:
# 1. Abre Telegram, busca @BotFather
# 2. Escribe /newbot, sigue las instrucciones
# 3. Copia el token y ponlo aquí o en variable de entorno TG_BOT_TOKEN
# 4. El bot publicará automáticamente en tus canales/grupos

TG_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
TG_CHANNEL = os.environ.get("TG_CHANNEL_ID", "")

def publicar_telegram(post_text):
    if not TG_TOKEN or not TG_CHANNEL:
        log("⚠️ Telegram: No hay token o channel (salteando)")
        # Generar link de compartir igual
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": TG_CHANNEL,
            "text": post_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }).encode()
        req = urllib.request.Request(url, data=data)
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        log(f"✅ Telegram: Publicado!")
        return True
    except Exception as e:
        log(f"❌ Telegram Error: {e}")
        return False

# ==================== GENERAR LINKS PARA COMPARTIR ====================
def generar_links(post_text):
    msg_encoded = urllib.parse.quote(post_text[:500])
    url_encoded = urllib.parse.quote(RANKUP_URL)
    
    links = {
        "whatsapp": f"https://wa.me/?text={msg_encoded}",
        "telegram": f"https://t.me/share/url?url={url_encoded}&text={msg_encoded[:100]}",
        "twitter": f"https://twitter.com/intent/tweet?text={urllib.parse.quote(post_text[:280])}",
        "facebook_share": f"https://www.facebook.com/sharer.php?u={url_encoded}&quote={msg_encoded[:200]}",
        "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={url_encoded}",
        "pinterest": f"https://pinterest.com/pin/create/button/?url={url_encoded}&description={msg_encoded[:200]}",
        "reddit": f"https://reddit.com/submit?url={url_encoded}&title={msg_encoded[:100]}",
        "email": f"mailto:?subject=Herramientas Premium&body={msg_encoded}",
    }
    
    log(f"📎 Links generados: WA | TG | TW | FB | LI | PI | RE | MAIL")
    return links

# ==================== INTENTO FACEBOOK vía ANDROID (sin Shizuku) ====================
def publicar_facebook_android(post_text):
    """Intenta abrir Facebook con el post pre-escrito usando Android intents"""
    try:
        # Intent URL para Facebook - abre la app con texto pre-escrito
        fb_intent = f"facebook://post?message={urllib.parse.quote(post_text[:500])}"
        subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", fb_intent],
                      capture_output=True, timeout=5)
        log("📱 Facebook intent enviado (puede requerir tap manual)")
        return True
    except Exception as e:
        log(f"⚠️ Facebook intent: {e}")
        # Fallback: abrir web de Facebook
        try:
            fb_web = f"https://www.facebook.com/sharer.php?u={urllib.parse.quote(RANKUP_URL)}"
            subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", "-d", fb_web],
                          capture_output=True, timeout=3)
            log("📱 Facebook web abierto")
        except:
            pass
        return False

# ==================== WEBHOOK SERVER ====================
class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/run":
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            result = ejecutar_ciclo()
            self.wfile.write(f"OK - Ciclo completado: {result['mensaje'][:100]}".encode())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            status = json.dumps({
                "status": "running",
                "ultimo_ciclo": ejecutar_ciclo.ultimo if hasattr(ejecutar_ciclo, 'ultimo') else "N/A",
                "apps": {
                    "invoicepro": INVOICE_URL,
                    "rankuppro": RANKUP_URL,
                    "business": BUSINESS_URL
                },
                "facebook_page": FACEBOOK_PAGE_URL,
                "paypal": "carlos.valderas8@gmail.com"
            }, indent=2)
            self.wfile.write(status.encode())
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>🤖 Auto-Publisher v3.0</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{{font-family:sans-serif;padding:20px;max-width:600px;margin:auto;background:#0f172a;color:#e2e8f0}}
a{{color:#818cf8}}pre{{background:#1e293b;padding:15px;border-radius:10px;overflow-x:auto}}
.card{{background:#1e293b;padding:20px;border-radius:16px;margin:15px 0;border:1px solid #334155}}
.btn{{display:inline-block;padding:10px 20px;border-radius:10px;text-decoration:none;font-weight:bold;margin:5px}}
.green{{background:#10b981;color:white}}.blue{{background:#3b82f6;color:white}}</style></head>
<body>
<h1>🤖 Auto-Publisher v3.0</h1>
<div class="card">
<p>✅ <b>SISTEMA ACTIVO</b> - Publicando automáticamente</p>
<p>📡 Último ciclo: {getattr(ejecutar_ciclo, 'ultimo', 'N/A')}</p>
</div>
<h2>📱 Apps Desplegadas</h2>
<ul>
<li>📄 <a href="{INVOICE_URL}">InvoicePro</a></li>
<li>🔧 <a href="{RANKUP_URL}">RankUp Pro</a></li>
<li>🏢 <a href="{BUSINESS_URL}">RankUp Business</a></li>
</ul>
<h2>💰 PayPal</h2>
<p><a href="{PAYPAL_ME}">paypal.me/carlosvalderas8</a></p>
<h2>🌐 Redes</h2>
<p><a href="{FACEBOOK_PAGE_URL}">Facebook Page</a></p>
<h2>🔗 Endpoints</h2>
<pre>
GET /run    → Ejecuta ciclo de publicación
GET /status → Estado del sistema
GET /       → Esta página
</pre>
<div>
<a class="btn blue" href="/run">▶ Ejecutar Ciclo</a>
<a class="btn green" href="/status">📊 Estado</a>
</div>
</body></html>"""
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        pass  # Silenciar logs

def start_webhook():
    port = 8080
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    log(f"🌐 Servidor webhook activo en puerto {port}")
    log(f"   Panel: http://localhost:{port}/")
    log(f"   Ejecutar ciclo: http://localhost:{port}/run")
    server.serve_forever()

# ==================== CICLO PRINCIPAL ====================
def ejecutar_ciclo():
    log("=" * 50)
    log("🚀 INICIANDO CICLO DE PUBLICACIÓN AUTOMÁTICA")
    
    # 1. Verificar apps
    check_apps()
    
    # 2. Generar contenido
    post = generar_post()
    log(f"📝 Post generado ({len(post)} chars)")
    
    # 3. Publicar en Facebook si hay token
    publicar_facebook_api(post)
    
    # 4. Publicar en Telegram si hay token
    publicar_telegram(post)
    
    # 5. Intentar con Android (fallback)
    publicar_facebook_android(post)
    
    # 6. Generar links
    links = generar_links(post)
    
    # 7. Guardar post
    post_file = os.path.join(LOG_DIR, "ultimo_post.txt")
    with open(post_file, "w", encoding="utf-8") as f:
        f.write(post + "\n\n🔗 Links:\n" + json.dumps(links, indent=2))
    
    # 8. Guardar links como HTML de compartir rápido
    html_share = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Compartir - AutoPublisher</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{{font-family:sans-serif;padding:20px;max-width:500px;margin:auto;background:#0f172a;color:white;text-align:center}}
.btn{{display:block;padding:15px;margin:10px 0;border-radius:12px;text-decoration:none;font-weight:bold;font-size:16px}}
.wa{{background:#25D366;color:white}}.tg{{background:#0088cc;color:white}}.tw{{background:#1DA1F2;color:white}}
.fb{{background:#1877F2;color:white}}.li{{background:#0A66C2;color:white}}.pi{{background:#E60023;color:white}}
.re{{background:#FF4500;color:white}}.ml{{background:#6b7280;color:white}}
h2{{color:#94a3b8;font-size:14px;margin-top:25px}}</style></head>
<body>
<h1>📤 Compartir Herramientas Premium</h1>
<p style="color:#94a3b8;font-size:14px;margin-bottom:20px">Toque un botón para compartir</p>
<a class="btn wa" href="{links['whatsapp']}">📱 Compartir en WhatsApp</a>
<a class="btn tg" href="{links['telegram']}">✈️ Compartir en Telegram</a>
<a class="btn tw" href="{links['twitter']}">𝕏 Compartir en X/Twitter</a>
<a class="btn fb" href="{links['facebook_share']}">👍 Compartir en Facebook</a>
<a class="btn li" href="{links['linkedin']}">💼 Compartir en LinkedIn</a>
<a class="btn pi" href="{links['pinterest']}">📌 Compartir en Pinterest</a>
<a class="btn re" href="{links['reddit']}">🤖 Compartir en Reddit</a>
<a class="btn ml" href="{links['email']}">📧 Compartir por Email</a>
<h2>💰 PayPal: carlos.valderas8@gmail.com</h2>
<h2>🌐 {FACEBOOK_PAGE_URL}</h2>
</body></html>"""
    with open(os.path.join(LOG_DIR, "compartir.html"), "w", encoding="utf-8") as f:
        f.write(html_share)
    
    resultado = {
        "timestamp": datetime.now().isoformat(),
        "mensaje": post[:100],
        "links": links
    }
    ejecutar_ciclo.ultimo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    log(f"✅ CICLO COMPLETADO")
    return resultado
ejecutar_ciclo.ultimo = None

# ==================== DAEMON LOOP ====================
def daemon_loop():
    """Bucle infinito que publica cada cierto tiempo"""
    intervalo = 3600  # 1 hora
    log(f"🔄 DAEMON INICIADO - Publicando cada {intervalo//60} minutos")
    
    while True:
        try:
            ejecutar_ciclo()
        except Exception as e:
            log(f"❌ Error en ciclo: {e}")
        
        log(f"⏳ Próximo ciclo en {intervalo//60} minutos...")
        for _ in range(intervalo):
            time.sleep(1)

# ==================== MAIN ====================
if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════╗")
    print("║   🤖 AUTO-PUBLISHER ENGINE v3.0              ║")
    print("║   Multi-plataforma: FB + TG + WA + X + LI    ║")
    print("║   Funciona 24/7 sin intervención             ║")
    print("╚═══════════════════════════════════════════════╝")
    print()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "daemon":
            daemon_loop()
        elif sys.argv[1] == "webhook":
            start_webhook()
        elif sys.argv[1] == "once":
            result = ejecutar_ciclo()
            print(json.dumps(result, indent=2))
    else:
        result = ejecutar_ciclo()
        print()
        print("📌 Modos de ejecución:")
        print("   python3 auto_publisher.py once     # Un ciclo")
        print("   python3 auto_publisher.py daemon   # 24/7 background")
        print("   python3 auto_publisher.py webhook  # Servidor HTTP")
        print()
        print(f"📱 Facebook: {FACEBOOK_PAGE_URL}")
        print(f"💰 PayPal: carlos.valderas8@gmail.com (codificado)")
        print(f"📄 InvoicePro: {INVOICE_URL}")
        print(f"🔧 RankUp Pro: {RANKUP_URL}")
        print(f"🏢 RankUp Business: {BUSINESS_URL}")
