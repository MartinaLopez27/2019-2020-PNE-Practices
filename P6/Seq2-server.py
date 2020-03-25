import http.server
from pathlib import Path

import termcolor

from Seq1 import Seq
import socketserver

# Server´s port
PORT = 8080

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True

FOLDER = "../Session-04/"
EXT = ".txt"

SEQ_GET = [
    "ACCTCCTCTCCAG",
    "AAAAACATTAATC",
    "CAAGGTCCCCTTC",
    "CCCTAGCCTGACT",
    "AGCGCAAACGCTA",]



# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        #User line
        user_line = self.requestline.split(" ")

        #Take the symbol / out of the path
        path = user_line[1]

        #Read the text
        u_text = path.split('?')

        #Read the first thing of the text
        header = u_text[0]

        # Open the form1.html file
        # Read the index from the file
        contents = Path('Error.html').read_text()
        error_code = 404


        if header == "/":
            # Read the index from the file open
            contents = Path('form-4.html').read_text()
            error_code = 200


        elif header =="/ping":
            contents = """
            <!DOCTYPE html>
            <html lang = "en">
            <head>
            <meta charset = "utf-8" >
                <title> PING </title >
            </head >
            <body>
            <h2> PING OK!</h2>
            <p> The SEQ2 server in running... </p>
            <a href="/">Main page</a>
            </body>
            </html>
            """
            error_code = 200


        elif header == "/get":
            u_set = u_text[1]
            sets = u_set.split("&")
            key, value = sets[0].split("=")
            n = int(value)

            seq = SEQ_GET[n]

            # Html code
            contents = f"""
                        <!DOCTYPE html>
                        <html lang = "en">
                        <head>
                        <meta charset = "utf-8" >
                          <title> GET </title >
                        </head >
                        <body>
                        <h2> Sequence number {n}</h2>
                        <p> {seq} </p>
                        <a href="/">Main page</a>
                        </body>
                        </html>
                        """
            error_code = 200


        elif header == "/gene":
            u_set = u_text[1]
            sets = u_set.split("&")
            key, gene = sets[0].split("=")

            s = Seq()
            s.read_fasta(FOLDER + gene + EXT)
            gene_str = str(s)
            # html code
            contents = f"""
                        <!DOCTYPE html>
                        <html lang = "en">
                        <head>
                        <meta charset = "utf-8" >
                          <title> GENE </title >
                        </head >
                        <body>
                        <h2> Gene: {gene}</h2>
                        <textarea readonly rows="20" cols="80"> {gene_str} </textarea>
                        <br>
                        <br>
                        <a href="/">Main page</a>
                        </body>
                        </html>
                        """
            error_code = 200


        elif header == "/operation":
            u_set = u_text[1]
            sets = u_set.split("&")
            key, seq = sets[0].split("=")
            key, op = sets[1].split("=")

            # -- Create the sequence
            s = Seq(seq)

            if op == "comp":
                resp = s.complement()
            elif op == "rev":
                resp = s.reverse()
            else:
                sl = s.len()
                ca = s.count_base('A')
                pa = "{:.1f}".format(100 * ca / sl)
                cc = s.count_base('C')
                pc = "{:.1f}".format(100 * cc / sl)
                cg = s.count_base('G')
                pg = "{:.1f}".format(100 * cg / sl)
                ct = s.count_base('T')
                pt = "{:.1f}".format(100 * ct / sl)

                resp = f"""
                <p>Total length: {sl}</p>
                <p>A: {ca} ({pa}%)</p>
                <p>C: {cc} ({pc}%)</p>
                <p>G: {cg} ({pg}%)</p>
                <p>T: {ct} ({pt}%)</p>"""

            contents = f"""
                        <!DOCTYPE html>
                        <html lang = "en">
                        <head>
                        <meta charset = "utf-8" >
                          <title> OPERATION </title >
                        </head >
                        <body>
                        <h2> Sequence </h2>
                        <p>{seq}</p>
                        <h2> Operation: </h2>
                        <p>{op}</p>
                        <h2> Result: </h2>
                        <p>{resp}</p>
                        <br>
                        <br>
                        <a href="/">Main page</a>
                        </body>
                        </html>
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
        print("Stoped by the user")
        httpd.server_close()


