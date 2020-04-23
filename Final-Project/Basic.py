import http.server
import socketserver
import termcolor
from pathlib import Path
from Seq1 import Seq

# Define the Server's port
PORT = 8080


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Analize the request line
        req_line = self.requestline.split(' ')

        # Get the path. It always start with the / symbol
        path = req_line[1]

        # Read the arguments
        arguments = path.split('?')

        # Get the verb. It is the first argument
        verb = arguments[0]

        # -- Content type header
        # -- Both, the error and the main page are in HTML
        contents = Path('Error.html').read_text()
        error_code = 404

        if verb == "/":
            # Open the form1.html file
            # Read the index from the file
            contents = Path('basic index.html').read_text()
            error_code = 200

        elif verb == "/listSpecies":
            conn = http.client.HTTPConnection('rest.ensembl.org')
            conn.request("GET", "/info/species?content-type=application/json")
            r1 = conn.getresponse()

            # -- Print the status
            print()
            print("Response received: ", end='')
            print(r1.status, r1.reason)

            # -- Generate the html code
            contents = """
                              <html>
                              <body style ="background-color: salmon;">
                              <ul> """

            cont = 0
            for specie in species:
                contents = contents + "<li>" + specie['display_name'] + "</li>"
                cont = cont + 1
                print(cont, limit)
                if (cont == limit):
                    break

            contents = contents + """<ul>
                                              <body>
                                              <html>
                                              """

            error_code = 200

        # Generating the response message
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
