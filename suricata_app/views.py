# suricata_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import platform
import subprocess

# suricata log eve.json
def view_events(request):
    #with open("/var/log/suricata/eve.json", "r") as events_file:
    #    events_content = events_file.read()
    #events_content = events_content[-8048:]  # Ottieni gli ultimi 2048 byte
    #command = ['/usr/bin/tail',' -n500', '/var/log/suricata/eve.json', '|', 'jq']
    command = "/usr/bin/tail -n2000 /var/log/suricata/eve.json | /usr/bin/jq"
    processo = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errore = processo.communicate()
    #events_content = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
    events_content = output.decode('utf-8')
    # events_data = json.loads(events_content)
    return render(request, "suricata_app/events.html", {"events_data": events_content})

# suricata log stats.log
def view_stats(request):
    with open("/var/log/suricata/stats.log", "r") as stats_file:
        stats_content = stats_file.read()
    stats_content = stats_content[-24000:]  # Ottieni gli ultimi 2048 byte
    return render(request, "suricata_app/stats.html", {"stats_content": stats_content})

# suricata log fast.log
def view_fast(request):
    with open("/var/log/suricata/fast.log", "r") as fast_file:
        fast_content = fast_file.read()
    # fast_content = fast_content[-2048:]  # Ottieni gli ultimi 2048 byte
    return render(request, "suricata_app/fast.html", {"fast_content": fast_content})

# main web page
def index(request):
    # Ottieni il nome dell'host
    host_name = os.uname().nodename
    # Ottieni il nome del sistema operativo e il tipo
    os_name = platform.system()
    os_type = platform.release()
    # Ottieni l'uptime del sistema
    uptime = subprocess.check_output("uptime", shell=True).decode("utf-8")
    # Includi i dati nel contesto
    context = {
        "host_name": host_name,
        "os_name": os_name,
        "os_type": os_type,
        "uptime": uptime,
    }
    return render(request, "index.html", context)


# reinvent webmin!?
@csrf_exempt
def service_control(request):
    if request.method == 'POST':
        selected_service = request.POST.get('selected_service')
        action = request.POST.get('action')

        if action == 'start':
            command = ['/usr/bin/sudo', '/bin/systemctl', 'start', selected_service]
        elif action == 'stop':
            command = ['/usr/bin/sudo', '/bin/systemctl', 'stop', selected_service]
        elif action == 'status':
            command = ['/usr/bin/sudo', '/bin/systemctl', 'status', selected_service]
        elif action == 'restart':
            command = ['/usr/bin/sudo', '/bin/systemctl', 'restart', selected_service]
        elif action == 'ps':
            command = ['/usr/bin/sudo', '/usr/bin/ps', 'aux']
        else:
            return HttpResponse("Azione non valida")

        try:
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output

        return render(request, 'suricata_app/service_control.html', {'result': result})

    # Altrimenti, se il metodo della richiesta è GET, carica la pagina con il menu a tendina
    # e il form per selezionare l'azione da eseguire.
    return render(request, 'suricata_app/service_control.html')


