# Utilise une image de base Python 3.12
FROM python:3.12-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers nécessaires dans l'image
COPY ./* ./

# Donne les permissions d'exécution au script init.sh
RUN chmod +x ./init.sh

# Installe pip et les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Déclare la commande par défaut pour le conteneur
CMD ["./init.sh"]