def web_config():
	list_of_wifi = wifi_lookup()
  
	if get_current_ip() == "0.0.0.0":
		current_wifi, current_ip = "Cannot Connect to " + get_current_wifi(), ""
	else:
		current_wifi, current_ip = "Connected to " + get_current_wifi(), "IP: " + get_current_ip()

	html = """
	<html> <head> <title>CONFIG_ME - Home</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}.button2{background-color: #4286f4;}</style> </head> <body> <h1>Wifi Configuration</h1> <p><strong>"""+ current_wifi +"""</strong></p><p><strong>"""+ current_ip +"""</strong></p><form action="/"> <p> <select name="wifi_name"> <option value="" disabled selected>Please select the WIFI</option> """+ list_of_wifi +""" </select> </p><input type="submit" value="Connect" class="button"> </form> </body>
	"""
  
	return html
  
def get_current_ip():
	current_ip = station.ifconfig()[0]
	
	return current_ip
  
def get_current_wifi():
	with open("config","r") as file:
		config_ssid = file.read()
	
	return config_ssid

def wifi_lookup():
	global wifi_list
	wifi_list, list_of_wifi, nets = [], """""", station.scan()
	
	for net in nets:
		wifi_name = net[0].decode('UTF-8')
		wifi_list.append(wifi_name.replace(" ", "+") + " ")
		list_of_wifi += "<option value=\"" + wifi_name + "\">" + net[0].decode('UTF-8') + "</option>"
	
	return list_of_wifi
  
def connect_to_wifi(request):
	wifi_params = request.find("/?wifi_name=")
	
	if wifi_params == 6:#6 mean found
		
		for wifi in wifi_list:
			wifi_name = request.find(wifi)
			if wifi_name == 18:#18 mean found
				ssid = wifi.replace(" ","").replace("+", " ")
				with open("config","w+") as file:
					file.write(ssid)
				reset.value(0)
	
	else: 
		return web_config()

while True:
  	try:
	    prime_conn, prime_addr = prim_socket.accept()
	    print('Got a connection from %s' % str(prime_addr))
	    request = str(prime_conn.recv(1024))
	    response = connect_to_wifi(request)
	    prime_conn.send('HTTP/1.1 200 OK\n')
	    prime_conn.send('Content-Type: text/html\n')
	    prime_conn.send('Connection: close\n\n')
	    prime_conn.sendall(response)
	    prime_conn.close()
	except Exception as e:
		pass