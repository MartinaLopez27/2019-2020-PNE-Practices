import http.client


PORT = 8080
SERVER = 'localhost'
METHOD = "GET"

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

endpoints = ['/listSpecies?limit=5&json=1', '/karyotype?specie=mouse&json=1', '/chromosomeLength?specie=cat&chromo=A2&json=1',
             '/geneSeq?gene=ATR&json=1', '/geneInfo?gene=TNF&json=1', '/geneCalc?gene=APOE&json=1',
             '/geneList?chromo=2&start=0&end=600000&json=1']

for element in endpoints:
    conn = http.client.HTTPConnection(SERVER, PORT)  # -- Connect with the server

    try:
        conn.request(METHOD, element)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()  # -- Read the response message from the server

    data1 = r1.read().decode("utf-8")  # -- Read the response's body

    print(f"CONTENT: {data1}")  # -- Print the received data

