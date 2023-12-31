import app.pagefuncs as pagefuncs
from app.params import Params
from app.sets import Settings

try:
    import usocket as socket
except:
    import socket
import time
import machine

server_socket = None


def save_sets(client, request):
    ampersand_split = request.decode("utf-8").split("\r\n\r\n")[1] \
        .replace("%21", "!").replace("%3F", "?").replace("%2C", ",") \
        .replace("%2E", ".").replace("%3A", ":").replace("%3B", ";") \
        .replace("%5F", "_").replace("%28", "(").replace("%29", ")") \
        .split("&")
    int_list = ['ap_channel']
    response_dict = {}
    for element in ampersand_split:
        equal_split = element.split("=")
        if equal_split[0] in int_list:
            response_dict[equal_split[0]] = int(equal_split[1])
        else:
            response_dict[equal_split[0]] = equal_split[1]

    key = response_dict.pop('dict', None)
    if key is not None:
        sets = Settings.load_settings()
        if key == '1w':
            for k in sets.onewire_dict:
                if k in response_dict:
                    sets.onewire_dict[k] = response_dict[k]
        elif key == 'wifi':
            if len(sets.wifi_dict) == len(response_dict):
                sets.wifi_dict = response_dict
        elif key == 'loads':
            if len(sets.loads_dict) == len(response_dict):
                sets.loads_dict = response_dict
        else:
            pagefuncs.send_response(client, "Peezda", status_code=400)
    else:
        pagefuncs.send_response(client, "Peezda", status_code=400)

    if sets.save_settings():
        pagefuncs.send_response(client,
                                '<p>' + str(sets.wifi_dict) +
                                '</p><p>' + str(sets.onewire_dict) +
                                '</p><p>' + str(sets.loads_dict),
                                status_code=200)
    else:
        pagefuncs.send_response(client, "Peezda", status_code=400)


def stop_web():
    global server_socket
    if server_socket:
        server_socket.close()
        server_socket = None


def start_web(ip, port=80):
    global server_socket
    addr = socket.getaddrinfo(ip, port)[0][-1]

    stop_web()
    try:
        server_socket = socket.socket()
        server_socket.bind(addr)
        server_socket.listen(1)
    except:
        time.sleep(3)
        machine.reset()

    print('Listening on:', addr)

    while True:
        client, addr = server_socket.accept()
        print('Client connected from', addr)
        try:
            client.settimeout(3.0)
            request = b''
            try:
                while "\r\n\r\n" not in request:
                    request += client.recv(2048)
            except OSError as e:
                print('Invalid request', e)

            print("Request is: {}".format(request))
            if "HTTP" not in request:  # skip invalid requests
                continue

            if str(request).find('/settings') == 6 or \
                    str(request).find('/settings') == 7:
                pagefuncs.handle_settings(
                    client,
                    request,
                    Settings.load_settings(),
                )

            elif str(request).find('/1wcalibr') == 6:
                pagefuncs.handle_1w_calibration(
                    client,
                    Settings.load_settings(),
                    Params.onw_read(),
                )

            elif str(request).find('/monitor') == 6:
                Params.digi_sensors()
                Params.anal_sensors()
                pagefuncs.handle_monitor(client, Params.__dict__)

            elif str(request).find('/restart') == 6:
                pagefuncs.send_response(client,
                                        'Hujawei will restart.',
                                        status_code=200
                                        )
                time.sleep(5)
                machine.reset()

            elif str(request).find('/save') == 7:
                save_sets(client, request)

            elif str(request).find('/clear') == 6:
                pagefuncs.handle_clear(client)

            elif str(request).find('/delsetsfile') == 6:
                import os
                os.remove(Settings.file_name)
                pagefuncs.handle_index(client)
                time.sleep(5)
                machine.reset()

            else:
                pagefuncs.handle_index(client)

        finally:
            client.close()
