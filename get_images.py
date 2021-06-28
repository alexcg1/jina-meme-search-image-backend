import os
import requests
import sys
import json
import random
from config import random_seed, backend_datafile, images_dir
import imghdr

try:
    __import__("pretty_errors")
except ImportError:
    pass

def check_image_ok(filename, ok_types=['jpeg', 'png']):
    filetype = imghdr.what(filename)
    if ((filetype in ok_types) and (os.path.getsize(filename) > 10_000)):
        return True
    else:
        return False

max_docs = int(sys.argv[1])

if not os.path.isfile(backend_datafile):
    os.system(
        "mkdir -p data; wget -O data/memes.json https://github.com/alexcg1/ml-datasets/blob/master/nlp/memes/memes.json?raw=true"
    )

if not os.path.isdir(images_dir):
    os.makedirs(images_dir)

with open(backend_datafile, "r") as file:
    raw_json = json.loads(file.read())

os.chdir(images_dir)
memes = []
for template in raw_json:
    for meme in template["generated_memes"]:
        meme["template"] = template["name"]
    memes.extend(template["generated_memes"])

random.seed(random_seed)
random.shuffle(memes)

for meme in memes[:max_docs]:
    filename = meme["image_url"].split("/")[-1]
    image_url = "http:" + meme["image_url"]
    print(f"Downloading {image_url}")
    r = requests.get(image_url, allow_redirects=True)
    with open(filename, "wb") as file:
        file.write(r.content)
    if not check_image_ok(filename):
        os.remove(filename)
