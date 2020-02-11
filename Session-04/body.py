from pathlib import Path

FILENAME = "RNU6_269P.txt"

file_contents = Path(FILENAME).read_text()
header = file_contents.split('\n')
header = join

print("Body of the U5.txt file:")
print(header[1:])

