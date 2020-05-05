import http.client

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

conn = http.client.HTTPConnection(SERVER, PORT)

# 7 TRY FOR JSON
conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)