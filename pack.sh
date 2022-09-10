if [ "x$1" == "x" ]
then
	echo "please enter app dir"
	exit 1
fi

cd $1
zip -r data.zip *
cd ..
cat $1/data.zip | base64 -w 0 > data.zip.base64

echo "data='$(cat data.zip.base64)'" > unpack.py

echo 'from io import BytesIO' >> unpack.py
echo 'import zipfile, os, shutil, tempfile' >> unpack.py
echo 'from base64 import b64decode' >> unpack.py
echo 'import json' >> unpack.py
echo 'tempdir=tempfile.mkdtemp()' >> unpack.py
echo 'with zipfile.ZipFile(BytesIO(b64decode(data.encode())), "r") as zipf:' >> unpack.py
echo '    zipf.extractall(tempdir)' >> unpack.py
echo 'data=json.load(open(f"{tempdir}/manifest.json"))' >> unpack.py
echo 'if os.name not in data["run"]:' >> unpack.py
echo '    print("This is unsupported on your platform")' >> unpack.py
echo 'os.chdir(tempdir)' >> unpack.py
echo 'os.system(data["run"][os.name])' >> unpack.py
echo 'shutil.rmtree(tempdir)' >> unpack.py

echo "import base64;exit(exec(base64.b64decode(b\"$(cat unpack.py | base64 -w 0)\").decode()))" > unpack.compressed.py