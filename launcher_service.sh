#!/bin/bash
# 🛡️ LAUNCHER RESILIENTE - Se asegura de que el publisher SIGA VIVO
# Funciona incluso si cierras la app de Anyclaw o Termux

DIR="/tmp/autopublisher"
cd "$DIR"

# Bucle infinito de protección
while true; do
    # Verificar que el daemon esté vivo
    if ! pgrep -f "auto_publisher.py daemon" >/dev/null; then
        echo "[$(date)] Daemon caído - Reiniciando..."
        nohup python3 auto_publisher.py daemon > /dev/null 2>&1 &
        echo "[$(date)] Daemon reiniciado con PID $!"
    fi
    
    # Verificar webhook
    if ! pgrep -f "auto_publisher.py webhook" >/dev/null; then
        echo "[$(date)] Webhook caído - Reiniciando..."
        nohup python3 auto_publisher.py webhook > /dev/null 2>&1 &
    fi
    
    sleep 30
done
