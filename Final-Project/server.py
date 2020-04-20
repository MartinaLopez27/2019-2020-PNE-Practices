import http.server
import socketserver
import termcolor
import json
import http.client
from Seq import Seq

# Define the Server's port
PORT = 8000


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):
    def dictionary_split(self, path):
        dictionary = dict()
        if '?' in self.path:
            dicc = self.path.split("?")[1]
            dicc = dicc.split(" ")[0]
            piece = dicc.split("&")
            for pair in piece:
                if '=' in pair:
                    key = pair.split("=")[0]
                    value = pair.split("=")[1]
                    dictionary[key] = value
        return (dictionary)


    def do_GET(self):
        response_code = 200
        json_response = False

        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # -- Message to send back to the client
        if self.path == "/":
            with open("index.html", "r") as f:
                contents = f.read()
        # -- Here we read the index.html code.


        elif "listSpecies" in self.path:
            dicc = self.dictionary_split(self.path)
            if 'limit' in dicc:
                try:
                    limit = int(dicc['limit'])
                except:
                    limit = 0
            else:
                limit = 0

            conn = http.client.HTTPConnection('rest.ensembl.org')
            conn.request("GET", "/info/species?content-type=application/json")
            result = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(result.status, result.reason)

            # -- Read the response's body and close
            # -- the connection
            text_json = result.read().decode("utf-8")
            response = json.loads(text_json)
            print(response)

            species = response['species']
            if 'json' in dicc and dicc['json'] == '1':
                json_response = True
                if limit == 0:
                    limit = len(species)
                newlist = species[1:limit]
                contents = json.dumps(newlist)
            else:
                if limit == 0:
                    limit = len(species)

                print("Limit: ", limit)
                contents = """
                                       <html>
                                       <body style ="background-color: lavender;">
                                       <ul> """

                count = 0
                for specie in species:
                    contents = contents + "<li>" + specie['display_name'] + "</li>"
                    count = count + 1
                    print(count, limit)
                    if (count == limit):
                        break

                contents = contents + """<ul>
                                           <body>
                                           <html>
                                           """

            conn.close()


        elif "karyotype" in self.path:
            dicc = self.dictionary_split(self.path)
            if 'specie' in dicc and dicc['specie'] != '':
                specie = dicc['specie']
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")
                result = conn.getresponse()
                text_json = result.read().decode("utf-8")
                response = json.loads(text_json)
                print(response)
                if 'karyotype' in response:
                    list_chromosome = response['karyotype']
                    if 'json' in dicc and dicc['json'] == '1':
                        json_response = True
                        print(list_chromosome)
                        contents = json.dumps(list_chromosome)
                    else:
                        contents = """
                                      <html>
                                      <body style ="background-color: salmon;">
                                      <ul> """

                        for chromosome in list_chromosome:
                            contents = contents + "<li>" + chromosome + "</li>"

                        contents = contents + """</ul>
                                              </body>
                                              </html>
                                              """
                else:
                    response_code = 400
                    f = open('Error.html', 'r')
                    contents = f.read()
            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()


        elif "chromosomeLength" in self.path:
            dicc = self.dictionary_split(self.path)
            if 'chromosome' in dicc and 'specie' in dicc and dicc['chromosome'] != '' and dicc['specie'] != '':
                u_chromo = dicc['chromosome']
                specie = dicc['specie']
                print(u_chromo)
                print(specie)
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")
                result = conn.getresponse()
                text_json = result.read().decode("utf-8")
                response = json.loads(text_json)
                info = response['top_level_region']

                if 'json' in dicc and dicc['json'] == '1':
                    json_response = True
                    long = 0
                    for element in info:
                        if (element['name'] == u_chromo):
                            long = element['length']
                    dic = dict()
                    dic['len'] = long
                    contents = json.dumps(dic)
                else:
                    long = 0
                    for element in info:
                        if (element['name'] == u_chromo):
                            long = element['length']
                    contents = """
                                      <html>
                                      <body style ="background-color: salmon;">
                                      <ul> """

                    contents = contents + "<li>" + str(long) + "</li>"

                    contents = contents + """</ul>
                                               </body>
                                               </html>"""
            else:
                response_code = 400
                f = open('Error.html', 'r')
                contents = f.read()

            # -- Generating the response message
            self.send_response(response_code)  # -- Status line: OK!
            if (json_response == True):
                # Define the content-type header:
                self.send_header('Content-Type', 'application/json')
            else:
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
    socketserver.TCPServer.allow_reuse_address = True

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

    print("")
    print("Server Stopped")