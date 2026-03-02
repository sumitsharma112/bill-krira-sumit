#!/bin/bash
cd /var/www/bill-krira/backend
source venv/bin/activate
# Kill existing screen if any
screen -S billing -X quit || true
# Start new screen
screen -d -m -S billing python app.py
echo Backend started in detached screen billing.

