#!/bin/bash
cd /home/flavio/suricata_monitor/suricata_monitor
/home/flavio/suricata_monitor/venv/bin/gunicorn suricata_monitor.wsgi:application
