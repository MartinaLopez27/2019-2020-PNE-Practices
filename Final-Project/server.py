import http.client
import http.server
import socketserver
import json
from pathlib import Path

import termcolor

PORT = 8080  # -- Define the Server's port
socketserver.TCPServer.allow_reuse_address = True  # -- This is for preventing the error: "Port already in use"


def get_json(ENDPOINT):  # -- Access information contained in json files on the Ensembl API
    conn = http.client.HTTPSConnection("rest.ensembl.org")
    parameters = '?content-type=application/json'

    if 'overlap' in ENDPOINT:
        parameters = parameters + ';feature=gene'

    conn.request('GET', ENDPOINT + parameters, None,
                 {'User-Agent': 'http-client'})  # -- Establishing connection with our database server:
    r1 = conn.getresponse()

    print()  # -- Print the status
    print("Response received: ", end='')
    print(r1.status, r1.reason)

    data1 = r1.read().decode("utf-8")  # -- Read the response's body and close the connection
    conn.close()

    return json.loads(data1)


class TestHandler(http.server.BaseHTTPRequestHandler):  # -- Our class inheritates all his methods and properties

    def get_arguments(self, path):  # -- Split the path to get the arguments, returns a dicctionary
        dicctionary = dict()
        if '?' in self.path:
            dicc = self.path.split("?")[1]
            dicc = dicc.split(" ")[0]
            piece = dicc.split("&")
            for element in piece:
                if '=' in element:
                    key = element.split("=")[0]
                    value = element.split("=")[1]
                    dicctionary[key] = value
            return dicctionary

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')  # -- Print the request line
        req_line = self.requestline.split(' ')  # -- Analize the request line

        arguments = req_line[1].split('?')  # -- Get the path and read the parameters
        verb = arguments[0]  # -- Get the first argument

        if verb == "/":
            contents = Path("index.html").read_text()
            error_code = 200

        # -- BASIC LEVEL
        elif verb in "/listSpecies":
            parameters = self.get_arguments(self.path)

            if 'limit' in parameters:  # -- In case the limit number is not included in the length of the info_list.
                try:
                    limit = int(parameters['limit'])  # -- Convert the limit into integer value as it was a string.
                except:
                    limit = 0
            else:
                limit = 0

            info_list = get_json('/info/species')['species']

            if 0 < limit <= 267:
                contents = f'''<!DOCTYPE html>
                               <html lang = "en">            
                               <head>  
                               <meta charset = "utf-8">
                                    <title> LIST OF SPECIES </title>
                                     </head>
                                     <body style="background-color: lightblue;">       
                                     <p>The total number of species in the ensembl is: {len(info_list)}</p>
                                     <p>The limit you have selected is: {limit}</p>
                                    <p>The name of the species are: </p>
                               '''

                count = 0
                for element in info_list:
                    contents = contents + f'''<!DOCTYPE html> 
                                                <ul class="a">
                                                <li>{element['display_name']}</li>
                                                </ul>
                                                '''
                    count = count + 1
                    if count == limit:
                        break
                error_code = 200

        elif verb in "/karyotype":
            parameters = self.get_arguments(self.path)

            if 'specie' in parameters and parameters['specie'] != '':  # In the case that a specie has a value assigned
                parameters = parameters["specie"]
                try:
                    info_list = get_json('/info/assembly/{}'.format(parameters))
                    chromo_list = info_list["karyotype"]

                    contents = f'''<!DOCTYPE html>
                           <html lang = "en">            
                           <head>  
                           <meta charset = "utf-8"
                                 <title>The name of chromosomes are:</title>
                                 </head>
                                 <body style="background-color: lightblue;">       
                          '''

                    for parameters in chromo_list:
                        contents = contents + f'''<!DOCTYPE html> 
                                                <ul class="a">
                                                <li>{parameters['display_name']}</li>
                                                </ul>
                                                '''

                    contents = contents + f'''<a href="/">Main page</a>
                                                  </body>
                                                  </html>'''
                    error_code = 200

                except KeyError:  # -- In the case the introduced specie is not a valid one
                    contents = Path('Error.html').read_text()
                    error_code = 404

            else:  # In the case specie is not defined
                contents = Path('Error.html').read_text()
                error_code = 404

        # -- Generating the response message
        self.send_response(error_code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
