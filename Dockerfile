# English: Use an official Python runtime as a parent image.
# Français: Utilise une image Python officielle comme image parente.
FROM python:3.11-slim

# English: Set the working directory in the container.
# Français: Définit le répertoire de travail dans le conteneur.
WORKDIR /app

# English: Copy the dependencies file and install them.
# Français: Copie le fichier de dépendances et les installe.
# Note: You will need to create a requirements.txt file.
# Note: Vous devrez créer un fichier requirements.txt.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# English: Copy the rest of the application's code.
# Français: Copie le reste du code de l'application.
COPY . .

# English: Command to run the application.
# Français: Commande pour exécuter l'application.
CMD ["python", "main.py"]