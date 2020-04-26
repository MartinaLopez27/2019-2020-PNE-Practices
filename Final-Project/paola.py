import http.client
import http.server
import socketserver
import json
from pathlib import Path

import termcolor

PORT = 8080  # -- Define the Server's port
socketserver.TCPServer.allow_reuse_address = True  # -- This is for preventing the error: "Port already in use"

BASES = ['A', 'C', 'G', 'T']


def get_json(ENDPOINT):  # -- Access information contained in json files on the Ensembl API
    conn = http.client.HTTPSConnection("rest.ensembl.org")
    parameters = '?content-type=application/json'

    if 'overlap' in ENDPOINT:
        parameters = parameters + ';feature=gene'

    conn.request('GET', ENDPOINT + parameters)
    r1 = conn.getresponse()
    data1 = r1.read().decode("utf-8")
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
        error_code = 200
        termcolor.cprint(self.requestline, 'green')  # -- Print the request line

        if self.path == "/":
            contents = Path("index.html").read_text()

        # -- BASIC LEVEL
        elif "/listSpecies" in self.path:
            contents = Path("index.html").read_text()
            if 'limit' in self.path:
                try:  # -- Type error
                    value = self.get_arguments(self.path)
                    limit = value['limit']
                    species = get_json('/info/species')['species']
                except TypeError:
                    error_code = 400
                    species = get_json('/info/species')['species']
                    limit = len(species)

                try:  # -- Value error
                    int(limit)
                except ValueError:
                    error_code = 404
                    limit = len(species)

            else:
                species = get_json('/info/species')['species']
                limit = len(species)

                count = 0
                list = []

                for element in species:
                    specie = element['name']
                    list.append(specie)
                    count = count + 1

                    if int(count) == int(limit):
                        break

                dicc = {}
                dicc['Species'] = list

                contents = """
                                <html>
                      <body style="background-color: green;">
                        <h1>List of all species</h1>
                                <ul>"""

                count = 0
                for element in species:
                    contents = contents + f'''<!DOCTYPE html> 
                                                <ul class="a">
                                                <li>{element['name']}</li>
                                                </ul>
                                                '''
                    count = count + 1
                    if int(count) == int(limit):
                        break

                contents = contents + """
                                            </ul>
                                            </body>
                                            </html>
                                            """


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