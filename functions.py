"""Packer functions"""
import os
import zipfile
from base64 import b64encode

TEMPLATE="""#!/usr/bin/python3
\"\"\"Packer executable\"\"\"
import zipfile
import os
import shutil
import tempfile
import sys
import json
from io import BytesIO
from base64 import b64decode
B64DATA=b"{}"
tempdir=tempfile.mkdtemp()
curr_dir=os.getcwd()
data=b64decode(B64DATA)
datastream=BytesIO(data)
with zipfile.ZipFile(datastream, "r") as zipfilestream:
    zipfilestream.extractall(tempdir)
MANIFEST={}
with open(tempdir+"/manifest.json","r",encoding="UTF-8") as manifestFile:
    MANIFEST=json.load(manifestFile)
if os.name not in data["run"]:
    print("This is unsupported on your platform")
    sys.exit(1)
os.chdir(tempdir)
os.system(data["run"][os.name]+" "+" ".join(sys.argv[1:]))
os.chdir(curr_dir)
shutil.rmtree(tempdir)
"""

TEMPLATE_COMPRESSED="""exec(__import__('base64').b64decode({}).decode())"""

def zipdir(directory, filename):
    """Zip directory"""
    with zipfile.ZipFile(f"{filename}", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root,file),
                    os.path.relpath(os.path.join(file),
                        os.path.join(directory, '..')))
    return filename

def ziptob64(fromfile, tofile):
    """convert zip to base64"""
    with open(fromfile, "rb") as from_file:
        with open(tofile, "wb") as to_file:
            to_file.write(b64encode(from_file.read()))

def genunpackfile(unpackfile, zipb64):
    """generate unpack.py"""
    b64data=""
    with open(zipb64, "r", encoding="UTF-8") as zipb64stream:
        b64data=zipb64stream.read()
    data=TEMPLATE.format(b64data,{})
    with open(unpackfile, "w+", encoding="UTF-8") as unpack_file:
        unpack_file.write(data)

def gencompressedunpackfile(compressedunpackfile, unpackfile):
    """compress unpack.py"""
    with open(unpackfile, "r", encoding="UTF-8") as unpack_file:
        with open(compressedunpackfile, "w", encoding="UTF-8") as compressed_unpack_file:
            compressed_unpack_file.write(
                TEMPLATE_COMPRESSED.format(b64encode(unpack_file.read().encode())))
