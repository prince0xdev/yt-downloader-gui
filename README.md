
# 🎵 YT Downloader GUI

![version](https://img.shields.io/badge/version-0.0.1-blue)

![screenshot](/assets/demo.png)

Une application graphique moderne pour télécharger facilement des vidéos et musiques YouTube, basée sur Python, yt-dlp et CustomTkinter.

---

## 🛠️ Exporter en .exe (Windows)

1. Installe PyInstaller :
   ```bash
   pip install pyinstaller
   ```
2. Compile l'exécutable :
   ```bash
   pyinstaller yt-downloader.spec
   ```
3. Le .exe sera dans le dossier `dist/yt-downloader/`

**N'oublie pas de garder le dossier ffmpeg/bin/ffmpeg.exe dans la structure !**

---

---

## ✨ Fonctionnalités
- Interface moderne et responsive (CustomTkinter)
- Téléchargement audio (MP3) ou vidéo (MP4/WebM)
- Barre de progression en temps réel et stats (débit, ETA)
- Sélection du dossier de destination
- Support de ffmpeg embarqué
- Gestion des erreurs et logs

---

## 🚀 Installation

1. **Cloner le repo**
   ```bash
   git clone <repo-url>
   cd yt-downloader
   ```
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
   ou
   ```bash
   pip install customtkinter yt-dlp
   ```
3. **Lancer l'application**
   ```bash
   python main.py
   ```

---


## 🤝 Contribuer

Les contributions sont les bienvenues ! Merci de lire le fichier [CONTRIBUTING.md](CONTRIBUTING.md) avant toute PR.

1. Forkez le projet
2. Créez une branche (`feature/ma-fonctionnalite`)
3. Commitez vos changements
4. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE).

---

## 👤 Auteur

- [EKpinse Prince](https://github.com/princeOxdev)

---

## ⭐️ N’hésitez pas à star le repo si ce projet vous a aidé !
