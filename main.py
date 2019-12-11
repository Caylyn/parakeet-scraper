import re
import requests
import sys

def main(*kwargs):
  parsing_url = kwargs[0][0]
  start = int(kwargs[0][1])
  count = int(kwargs[0][2])
  block_size = 10_000
  for num in range(start, start+count):
    print("starting new book")
    with requests.get("http://www.gutenberg.org/cache/epub/%d/pg%d.txt" % (num, num), stream=True) as r:
      content = r.iter_content(block_size)
      buffer = ""
      for i in content.__next__().decode('utf-8'):
        buffer += i
      buffer = re.split(r'Project Gutenberg(?:(?:\'s)|(?: EBook of)) ', buffer, maxsplit=1)[1]
      title, buffer = re.split(r'\n', buffer, maxsplit=1)
      print(title)
      while len(buffer) > 0:
        print("sending chunk")
        chunk, buffer = buffer[:block_size], buffer[block_size:]
        requests.post(parsing_url, json={"title": title, "text": chunk})

if __name__ == "__main__":
  main(sys.argv[1:])
