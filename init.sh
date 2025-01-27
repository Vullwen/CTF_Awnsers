#!/bin/bash

# Installe les dépendances
python3 -m pip install -r ./requirements.txt

# Lance le fichier python (download le dictionnaire anglais)
python3 ./download_nltk.py

# Lance le fichier principal
python3 ./CTF_Scripting.py