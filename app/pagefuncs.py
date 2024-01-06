def send_header(client, status_code=200, content_length=None):
    client.sendall(f"HTTP/1.0 {status_code} OK\r\n")
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
        client.sendall(f"Content-Length: {content_length}\r\n")
    client.sendall("\r\n")


def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)


def give_head(client, title, refresh=None):
    client.sendall(f"""\
    <html>
        <head>
            <title>{title}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
    """)
    if refresh is not None:
        client.sendall(f"""\
        <meta http-equiv="refresh" content="{refresh}">
        """)
    try:
        with open('app/templates/black_style.css', 'r', encoding='utf-8') as file:
            client.sendall(f"""\
            <link rel="icon" href="data:,">
            <style>{file.read()}</style>
            </head>
            <body>
            <h1>{title}</h1>
            """)
    except OSError as exc:
        print('Error:', exc)


def give_back(client):
    client.sendall("""\
  </body>
</html>
    """)


def handle_index(client):
    send_header(client)
    give_head(client, 'Hujawei Index')
    try:
        with open('app/templates/index.html', 'r', encoding='utf-8') as file:
            client.sendall(file.read())
    except OSError as exc:
        print('Error:', exc)
    give_back(client)


def handle_monitor(client, pars):
    send_header(client)
    give_head(client, 'Hujawei Monitor', 20)
    try:
        with open('app/templates/monitor.html', 'r', encoding='utf-8') as file:
            client.sendall(
                file.read().format(str(pars['chip_tmp'])
                                   str(pars['ec_upper']),
                                   str(pars['ec_lower']),
                                   str(round(pars['air_ds_temp'], 1)),
                                   str(round(pars['space_ds_temp'], 1)),
                                   str(pars['brd_tmp']),                                   
                                   str(pars['brd_hmd']),
                                   str(round(pars['air_tmp'], 1)),
                                   str(round(pars['air_hmd'], 1)),
                                   str(pars['i_bat']),
                                   str(pars['v_bat']),
                                   str(pars['v_ps']),
                                   ))
    except OSError as exc:
        print('Error:', exc)
    give_back(client)


def handle_1w_calibration(client, sets, temps):
    send_header(client)
    give_head(client, '1wire Calibration', 10)
    data = f"""\
    <form action="/save" method="post">
      <input type="hidden" id="dict" name="dict" value="1w">
      <label for="air">Air: </label>
      {sets.onewire_dict['air']}<br>
      <select name="air" id="air">
    """
    for rom in temps:
        data += f'<option value="{rom}"> {rom} | {round(temps[rom], 1)}&#8451;</option>'
    data += f"""\
        <option value="None">None</option>
      </select><br><br>
      <label for="space">Space: </label>
      {sets.onewire_dict['space']}<br>
      <select name="space" id="space">
    """
    for rom in temps:
        data += f'<option value="{rom}"> {rom} | {round(temps[rom], 1)}&#8451;</option>'
    data += """\
      <option value="None">None</option>
    </select><br><br>
      <input type="submit" value="Save" class = "button">
    </form>
    """
    client.sendall(data)
    give_back(client)


def handle_anal_calibration(client, anal_dict):
    send_header(client)
    give_head(client, 'Anal Calibration', 10)
    data = f"""\
          <form action="/save" method="post">
            <input type="hidden" id="dict" name="dict" value="anal">
            <input type="submit" value="Save" class = "button">
          </form>
           """.format(anal_dict['pH_k'],
                      anal_dict['ec_k'],
                      )

    client.sendall(data)
    give_back(client)


def handle_settings(client, request, sets):
    sets_dict = None
    if str(request).find('POST') == 2:
        key, val = request.decode("utf-8").split("\r\n\r\n")[1] \
            .split("&")[0].split("=")
        if key == 'dict':
            sets_dict = val
    send_header(client)
    give_head(client, 'Hujawei Settings')
    try:
        with open('app/templates/sets_menu.html', 'r', encoding='utf-8') as file:
            client.sendall(file.read())
    except OSError as exc:
        print('Error:', exc)
    if sets_dict == 'wifi':
        try:
            client.sendall("""\
<h2>WiFi</h2>
<form action="/save" method="post">
    <input type="hidden" id="dict" name="dict" value="wifi">
    <h3>Access Point</h3>
    <label for="ap_ssid">SSID </label>
    <input type="text" id="ap_ssid" name="ap_ssid" value="{0}">
    <br>
    <label for="ap_password">Password </label>
    <input type="text" id="ap_password" name="ap_password" value="{1}">
    <br>
    <label for="ap_channel">Channel </label>
    <input type="number" id="ap_channel" name="ap_channel" min="1" max="12" value="{2}">
    <br>
    <h3>Station</h3>
    
                
                
                
                
                """.format(sets.wifi_dict['ap_ssid'],
                           sets.wifi_dict['ap_password'],
                           sets.wifi_dict['ap_channel'],
                           ))

            logins_dict = sets.wifi_dict['sta_dict']
            for ssid in logins_dict:
                password = logins_dict[ssid]

# TODO: show logins at page
                client.sendall("""\
                <p>Saved logins</p>

                
                """.format(

                ))

                client.sendall("""\
    <label for="sta_ssid">SSID </label>
        <input type="text" id="sta_ssid" name="sta_ssid" value="{0}">
        <br>
        <label for="sta_password">Password </label>
        <input type="text" id="sta_password" name="sta_password" value="{1}">
        <br>
    <input type="submit" value="Save" class="button">
    <br>
    <p>Legal password symbols: * - ! ? , . ; : _ ( ) ZalOopa 666</p>
</form>
                """.format(ssid, password))
        except OSError as exc:
            print('Error:', exc)
    elif sets_dict == 'solution':
        try:
            with open('app/templates/sets_solution.html', 'r', encoding='utf-8') as file:
                client.sendall(
                    file.read().format(sets.solution_dict['pH_min'],
                                       sets.solution_dict['pH_max'],
                                       sets.solution_dict['ec_min'],
                                       sets.solution_dict['ec_max'],
                                       sets.solution_dict['solution_temp_min'],
                                       sets.solution_dict['solution_temp_max'],
                                       ))
        except OSError as exc:
            print('Error:', exc)
    elif sets_dict == 'air':
        try:
            with open('app/templates/sets_air.html', 'r', encoding='utf-8') as file:
                client.sendall(
                    file.read().format(sets.air_dict['rh_min'],
                                       sets.air_dict['rh_max'],
                                       sets.air_dict['pressure_min'],
                                       sets.air_dict['pressure_max'],
                                       sets.air_dict['air_temp_min'],
                                       sets.air_dict['air_temp_max'],
                                       ))
        except OSError as exc:
            print('Error:', exc)
    elif sets_dict == 'power':
        try:
            with open('app/templates/sets_power.html', 'r', encoding='utf-8') as file:
                client.sendall(
                    file.read().format(sets.power_dict['v_bat_min'],
                                       sets.power_dict['v_bat_max'],
                                       sets.power_dict['v_ps_min'],
                                       sets.power_dict['v_ps_max'],
                                       sets.power_dict['brd_temp_min'],
                                       sets.power_dict['brd_temp_max'],
                                       sets.power_dict['high_voltage'],
                                       ))
        except OSError as exc:
            print('Error:', exc)
    elif sets_dict == 'light':
        try:
            with open('app/templates/sets_light.html', 'r', encoding='utf-8') as file:
                client.sendall(
                    file.read().format(sets.light_dict['full_time'],
                                       sets.light_dict['seed_days'],
                                       sets.light_dict['veg_morning_on'],  # 2
                                       sets.light_dict['veg_morning_off'],
                                       sets.light_dict['veg_main_on'],
                                       sets.light_dict['veg_main_off'],
                                       sets.light_dict['veg_evening_on'],
                                       sets.light_dict['veg_evening_off'],
                                       sets.light_dict['veg_uva_mins'],
                                       sets.light_dict['veg_days'],
                                       sets.light_dict['blm_morning_on'],  # 10
                                       sets.light_dict['blm_morning_off'],
                                       sets.light_dict['blm_main_on'],
                                       sets.light_dict['blm_main_off'],
                                       sets.light_dict['blm_evening_on'],
                                       sets.light_dict['blm_evening_off'],
                                       sets.light_dict['blm_uva_mins'],
                                       sets.light_dict['blm_days'],
                                       sets.light_dict['frt_morning_on'],  # 18
                                       sets.light_dict['frt_morning_off'],
                                       sets.light_dict['frt_main_on'],
                                       sets.light_dict['frt_main_off'],
                                       sets.light_dict['frt_evening_on'],
                                       sets.light_dict['frt_evening_off'],
                                       sets.light_dict['frt_uva_mins'],
                                       sets.light_dict['frt_days'],
                                       ))
        except OSError as exc:
            print('Error:', exc)
    elif sets_dict == 'sensors':
        try:
            with open('app/templates/sets_sensors.html', 'r', encoding='utf-8') as file:
                client.sendall(
                    file.read().format(sets.sensors_dict['solution_temp'],
                                       sets.sensors_dict['air_temp'],
                                       sets.sensors_dict['space_temp'],
                                       sets.sensors_dict['dht11'],
                                       sets.sensors_dict['bmp085'],
                                       sets.sensors_dict['co2'],
                                       sets.sensors_dict['v_bat'],
                                       ))
        except OSError as exc:
            print('Error:', exc)
    give_back(client)


def handle_clear(client):
    send_header(client)
    give_head(client, 'Set Defaults')
    client.sendall("""\
            <p>
              <a href="/delsetsfile">
                <button class="button">Delete Settings File</button>
              </a>
              <a href="/settings">
                <button class="button button2">Cancel</button>
              </a>
            </p>
        """)

    give_back(client)
