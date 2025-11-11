# discord-bot-prayer-time

## 1 - Description

Ce projet est un bot Discord minimaliste qui fournit les horaires de prière (Fajr, Dhuhr, Asr, Maghrib, Isha) pour une ville et une date données. Il récupère les données depuis une API externe, prétraite les horaires et les expose via des commandes Discord.

## 2 - Fonctionnalités

- Automatiser la diffusion des horaires de prière dans un serveur Discord (chat vocal).
- Fournir des horaires exacts et la possibilité d'ajuster (par ex. -20 minutes) pour les alarmes.
- Profil par utilisateur pour de la personnalisation (ville, décalage, plus à l'avenir)

## 3 - Initialize

Prérequis : Python 3.8+ et accès internet.

1. Cloner le dépôt :

	git clone <url-du-depot>
	cd discord-bot-prayer-time

2. Installer les dépendances. Si un fichier `requirements.txt` n'existe pas, installez les paquets courants :

	pip install discord.py python-dotenv requests

3. Configurer vos variables d'environnement :

	Créer un fichier `.env` à la racine du projet et y ajouter au minimum :

	DISCORD_TOKEN=Votre_Token_Discord

	(Ajoutez d'autres variables si votre configuration ou l'API externe le requiert.)

4. Lancer le bot :

	python main.py

## 4 - License et créateurs

Licence : MIT License (voir le fichier `LICENSE` pour le texte complet).

Créateurs / Mainteneurs principaux :

- Clément REVERBEL
- Zyad REYNIER

Contributions : bienvenue ! Ouvrez une issue ou une pull request pour proposer des améliorations.

---

Merci d'utiliser `discord-bot-prayer-time` — n'hésitez pas à signaler des bugs ou proposer des fonctionnalités.

