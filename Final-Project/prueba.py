import http.server
import http.client
import socketserver
import json
from pathlib import Path

import requests
import termcolor

PORT = 8080  # -- Define the Server's port
socketserver.TCPServer.allow_reuse_address = True  # -- This is for preventing the error: "Port already in use"


def get_json(server, endpoint, parameters):  # -- Access information contained in json files on the Ensembl API

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

    def get_arguments(self):  # -- Split the path to get the arguments, returns a dicctionary
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
        parameters = self.get_arguments()
        error_code = 200

        if self.path == "/":
            contents = Path("index.html").read_text()

        # -- BASIC LEVEL
        elif "listSpecies" in self.path:
            endpoint = "/info/species"
            info_list = get_json(server, endpoint, parameters)

            try:
                limit = int(parameters['limit'])
                if 0 < limit <= 267:
                    contents = f''' <!DOCTYPE html>
                                    <html lang = "en">            
                                    <head>
                                        <meta charset="UTF-8">
                                        <title>LIST OF SPECIES IN THE BROWSER</title>
                                    </head>
                                    <body style="background-color: paleturquoise;">
                                    <body>
                                     The total number of species in the ensembl is: {len(info_list)}<br>
                                     The limit you have selected is: {limit}<br>
                                     The name of the species are: <br>'''

                    count = 0
                    for element in info_list:
                        contents = contents + f''' <ul class="a">
                                                <li>{element["display_name"]}</li>
                                                </ul> '''

                        count = count + 1
                        if count == limit:
                            break

                    contents = contents + '''<a href="/">Main page</a>
                                            </body>
                                            </html>'''
            except ValueError:
                contents = Path('Error.html').read_text()
                error_code = 404

        elif "karyotype" in self.path:
            endpoint = "/info/assembly/"
            info_list = get_json(server, endpoint, parameters)

            contents = '''  <!DOCTYPE html>
                            <html lang = "en">             
                            <head>
                                <meta charset="UTF-8">
                                <title>KARYOTYPE INFORMATION OF A SPECIE</title>
                            </head>
                            <body style="background-color: paleturquoise;">
                            <body>   
                              The names of the chromosomes are:'''

            for element in info_list:
                contents = contents + '<li>' + element + '</li>'

            contents = contents + '''<a href="/">Main page</a>
                                        </body>
                                        </html>'''

        elif "chromosomeLength" in self.path:
            endpoint = "/info/assembly/"
            info_list = get_json(server, endpoint, parameters)

            if 'length' in info_list.keys():
                contents = f''' <!DOCTYPE html>
                                <html lang = "en">            
                                <head>
                                    <meta charset="UTF-8">
                                    <title>CHROMOSOME LENGTH OF A SPECIE</title>
                                </head>
                                <body style="background-color: paleturquoise;">
                                <body>
                                    The length of the chromosome {parameters['chromo']} of the specie {parameters['specie']} is: {info_list['length']}<br>'''

                contents = contents + '''<a href="/">Main page</a>
                                        </body>
                                        </html>'''
            else:
                contents = Path('Error.html').read_text()
                error_code = 404

        elif "/geneSeq" in self.path:
            try:
                gene_id = parameters["gene"]

                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene_id + "?content-type=application/json")
                r1 = conn.getresponse()
                data1 = r1.read().decode('utf-8')
                response = json.loads(data1)

                id_name = response['data'][0]['id']
                conn.request('GET', '/sequence/id/' + id_name + '?content-type=application/json')
                r1 = conn.getresponse()
                data1 = r1.read().decode('utf-8')
                response = json.loads(data1)

                DNA_sequence = response['seq']

                # Dict = {}  #para el json
                # Dict['DNAsequence'] = response['seq']

                contents = f""" <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>SEQUENCE OF A HUMAN GENE</title>
                                </head>
                                <body style ="background-color: palegoldenrod;">
                                <body>
                                    The sequence of the human gene {gene_id} is:<br>
                                """

                contents = contents + "<li>" + DNA_sequence + "<li>"

                contents = contents + '''<a href="/">Main page</a>
                                        </body>
                                        </html>'''
            except KeyError:
                contents = Path('Error.html').read_text()
                error_code = 404

        elif "geneInfo" in self.path:
            try:
                gene_id = parameters["gene"]

                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene_id + "?content-type=application/json")
                r1 = conn.getresponse()
                data1 = r1.read().decode('utf-8')
                response = json.loads(data1)

                id_name = response['data'][0]['id']
                conn.request('GET', '/overlap/id/' + id_name + '?feature=gene;content-type=application/json')
                r1 = conn.getresponse()
                data1 = r1.read().decode('utf-8')
                response = json.loads(data1)

                start = response[0]['start']
                end = response[0]['end']
                id = response[0]['id']
                lenght = end - start
                chromosome = response[0]['assembly_name']

                contents = f""" <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>INFORMATION OF A HUMAN GENE</title>
                                </head>
                                <body style ="background-color: palegoldenrod;">
                                <body>
                                    The information available about the gene {gene_id} is:<br>
                                    """

                contents = contents + "<h4>The Id of the gene is:</h4>" "<li>" + id + "</li>"
                contents = contents + "<h4>The gene start on position:</h4>" "<li>" + str(start) + "</li>"
                contents = contents + "<h4>The gene ends on position:</h4>" "<li>" + str(end) + "</li>"
                contents = contents + "<h4>The length of the gene is:</h4>" "<li>" + str(lenght) + "</li>"
                contents = contents + "<h4>The gene is on chromosome:</h4>""<li>" + chromosome + "</li><br>"

                contents = contents + '''<a href="/">Main page</a>
                                                    </body>
                                                    </html>'''
            except KeyError:
                contents = Path('Error.html').read_text()
                error_code = 404









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
