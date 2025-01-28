# Exam CTF

Ce projet contient des scripts et des fichiers pour résoudre des challenges CTF.

## Contenu

- **CTF_Scripting.py** : Script principal qui gere la connexion, et envoie les réponses au serveur CTF.
- **download_nltk.py** : Script pour télécharger des ressources NLTK (dico anglais).
- **Dockerfile** : Configuration pour exécuter le projet dans un conteneur Docker.
- **init.sh** : Script d'initialisation.
- **.env** : Fichier d'environnement pour les variables sensibles.

## Utilisation
1. Installez le repo git:
  ```bash
  git clone https://github.com/Vullwen/CTF_Awnsers
  cd CTF_Awnsers
  ```
2. Assurez-vous d'avoir Docker installé.
3. Changer le port de connexion en fonction de celui donné par le CTF dans le `.env`
4. Lancez le conteneur avec la commande :
   ```bash
   docker build -t exam_ctf .
   docker run --rm -it exam_ctf
   ```
5. Dans le cas ou une erreur se produit, relancez le conteneur avec la commande :
   ```bash
   docker run --rm -it exam_ctf
   ```

## Auteur

- **Vullwen** - **Célian Pinquier**
