"""Packer main"""
import sys
import os
from pathlib import Path

from functions import zipdir, ziptob64, genunpackfile, gencompressedunpackfile

if len(sys.argv)<2:
    print("usage: {} <directory-for-pack>".format(sys.argv[0]))
    sys.exit(1)
dir_pack_str=sys.argv[1]
if not dir_pack_str.endswith("/"):
    dir_pack_str+="/"

dir_pack=Path(dir_pack_str)
if not dir_pack.exists():
    print("directory {} don't exists".format(dir_pack_str))

dist=Path("dist")
if not dist.exists():
    os.mkdir("dist")

dir_pack_name=os.path.dirname(dir_pack)
zipdir(dir_to_pack, f"dist/{dir_pack_name}.zip")
ziptob64(f"dist/{dir_pack_name}.zip", f"dist/{dir_pack_name}.zip.base64")
genunpackfile(f"dist/{dir_pack_name}.py", f"dist/{dir_pack_name}.zip.base64")
gencompressedunpackfile(f"dist/{dir_pack_name}.compressed.py", f"dist/{dir_pack_name}.py")
