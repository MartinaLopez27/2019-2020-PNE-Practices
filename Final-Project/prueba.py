import http.server
import socketserver
from pathlib import Path

import requests
import termcolor

PORT = 8080  # -- Define the Server's port
socketserver.TCPServer.allow_reuse_address = True  # -- This is for preventing the error: "Port already in use"


def get_json(server, endpoint, parameters):
    if 'specie' in parameters.keys():
        specie = parameters['specie']
        try:
            chromo = parameters['chromo']
        except KeyError:
            chromo = ""
        url_link = server + endpoint + specie + "/" + chromo
        r = requests.get(url_link, headers={"Content-Type": "application/json"})
        if not r.ok:
            error = r.json()['error']
            return {'There are not species with that name': error}

        try:
            length = r.json()['length']
            return {'length': length}
        except KeyError:
            data_karyotype = r.json()['karyotype']
            return data_karyotype

    else:
        r = requests.get(server + endpoint, headers={"Content-Type": "application/json"})

        if not r.ok:
            error = r.json()['error']
            return {'error': error}

        data_species = r.json()['species']
        return data_species


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
        server = "http://rest.ensembl.org"
        termcolor.cprint(self.requestline, 'green')  # -- Print the request line
        parameters = self.get_arguments(self.path)

        if self.path == "/":
            contents = Path("index.html").read_text()
            error_code = 200

        # -- BASIC LEVEL
        elif "listSpecies" in self.path:
            endpoint = "/info/species"
            info_list = get_json(server, endpoint, parameters)

            if 'limit' in parameters:  # -- In case the limit number is not included in the length of the info_list.
                try:
                    limit = int(parameters['limit'])  # -- Convert the limit into integer value as it was a string.
                except:
                    limit = 0
            else:
                limit = 0

            if 0 < limit <= 267:
                contents = f''' <body style="background-color: lightblue;">       
                                 <p>The total number of species in the ensembl is: {len(info_list)}</p>
                                 <p>The limit you have selected is: {limit}</p>
                                 <p>The name of the species are: </p>'''


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
                        
                contents = contents + '''<a href="/">Main page</a>
                                                  </body>
                                                  </html>'''
                error_code = 200

        elif "karyotype" in self.path:
            endpoint = "/info/assembly/"
            info_list = get_json(server, endpoint, parameters)

            contents = ''' <body style="background-color: lightblue;">    
                            <p>The names of the chromosomes are:</p>  '''

            for element in info_list:
                contents = contents + '<li>' + element + '</li>'

            contents = contents + '''<a href="/">Main page</a>
                                  </body>
                                  </html>'''
            error_code = 200

        elif "chromosomeLength" in self.path:
            endpoint = "/info/assembly/"
            info_list = get_json(server, endpoint, parameters)

            if 'length' in info_list.keys():
                contents = f"""<body style="background-color: lightblue;">
                            <p>The length of the chromosome {parameters['chromo']} 
                            of the specie {parameters['specie']}
                            is: {info_list['length']} </p>"""
            else:
                contents = Path('Error.html').read_text()
                error_code = 404

            error_code = 200

        else:
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
