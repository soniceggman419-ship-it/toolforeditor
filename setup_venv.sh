#!/bin/bash
set -e

cd "$(dirname "$(readlink -f "$0")")"

if [ -d venv ]; then
    echo "Removing existing venv..."
    rm -rf venv
fi

echo "Creating Python virtual environment..."
python3 -m venv --without-pip venv

echo "Activating venv and installing pip..."
source venv/bin/activate
curl -sS https://bootstrap.pypa.io/get-pip.py | python3 > /dev/null

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Build Cython extensions? (optional, run: python setup.py all)"
echo ""
echo "Done. Activate with: source venv/bin/activate"
echo "Run MCEdit with: python mcedit.py"
