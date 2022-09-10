import os
import zipfile
from base64 import b64encode

TEMPLATE="""#!/usr/bin/python3
data='{}'
from io import BytesIO
import zipfile, os, shutil, tempfile
from base64 import b64decode
import json
tempdir=tempfile.mkdtemp()
with zipfile.ZipFile(BytesIO(b64decode(data.encode())), "r") as zipf:
    zipf.extractall(tempdir)
data=json.load(open(tempdir+"/manifest.json"))
if os.name not in data["run"]:
    print("This is unsupported on your platform")
os.chdir(tempdir)
os.system(data["run"][os.name])
shutil.rmtree(tempdir)"""

TEMPLATE_COMPRESSED="""import base64;exit(exec(base64.b64decode({}).decode()))"""

def zipdir(directory, filename):
    with zipfile.ZipFile(f"{filename}", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root,file), 
                           os.path.relpath(os.path.join(file), 
                                           os.path.join(directory, '..')))
    return filename

def ziptob64(fromfile, tofile):
    with open(fromfile, "rb") as ff:
        with open(tofile, "wb") as tf:
            tf.write(b64encode(ff.read()))

def genunpackfile(unpackfile, zipb64):
    b64data=""
    with open(zipb64, "r") as f:
        b64data=f.read()
    data=TEMPLATE.format(b64data)
    with open(unpackfile, "w+") as f:
        f.write(data)

def gencompressedunpackfile(compressedunpackfile, unpackfile):
    with open(unpackfile, "r") as f:
        with open(compressedunpackfile, "w") as cf:
            cf.write(TEMPLATE_COMPRESSED.format(b64encode(f.read().encode())))