#!/bin/bash
# Configurar cron para mantener el publisher activo 24/7
CRON_JOB="*/5 * * * * pgrep -f 'auto_publisher.py daemon' >/dev/null || cd /tmp/autopublisher && nohup python3 auto_publisher.py daemon >/dev/null 2>&1 &"
(crontab -l 2>/dev/null | grep -v "auto_publisher" ; echo "$CRON_JOB") | crontab -
echo "✅ Cron configurado - Auto-recuperación cada 5 minutos"
