#!/bin/bash
# 🚀 Auto-Start Publisher - Se ejecuta solo al arrancar
# No requiere intervención humana

DIR="/tmp/autopublisher"
cd "$DIR"

# Crear carpetas necesarias
mkdir -p "$DIR/logs"

# Matar instancias anteriores si existen
pkill -f "auto_publisher.py daemon" 2>/dev/null
pkill -f "auto_publisher.py webhook" 2>/dev/null

# Iniciar en background (NO TERMINAL)
nohup python3 auto_publisher.py daemon > /dev/null 2>&1 &

# Iniciar webhook server (para monitoreo)
nohup python3 auto_publisher.py webhook > /dev/null 2>&1 &

# Guardar PIDs
PID_DAEMON=$!
echo "$PID_DAEMON" > "$DIR/daemon.pid"
echo "✅ Sistema iniciado - PID daemon: $(cat $DIR/daemon.pid)"
echo "📡 Webhook: http://localhost:8080/"
echo "📊 Estado: http://localhost:8080/status"
