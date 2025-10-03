import customtkinter as ctk
from tkinter import filedialog
from yt_dlp import YoutubeDL
import threading
import os
import sys
import re

# Variable globale pour stopper le téléchargement
download_thread = None
stop_download_flag = threading.Event()

# ---------- Fonction téléchargement ----------
def download_video():

    url = url_entry.get().strip()
    format_choice = format_var.get()
    # Validation de l'URL
    url_regex = re.compile(r'^(https?://)?(www\.)?([\w\-]+\.)+[\w\-]+(/[ \w\-./?%&=]*)?$', re.IGNORECASE)
    if not url:
        status_label.configure(text="❌ Veuillez entrer une URL.", text_color="red")
        return
    if not url.startswith("http://") and not url.startswith("https://"):
        status_label.configure(text="❌ Lien invalide (doit commencer par http(s)://)", text_color="red")
        return
    if not url_regex.match(url):
        status_label.configure(text="❌ Lien non valide.", text_color="red")
        return


    # Affiche le titre et le spinner côte à côte
    video_title_label.configure(text="")
    spinner_frame.pack()
    spinner_label.start()

    # Réinitialise la barre et le label stats
    progress_bar.set(0)
    stats_label.configure(text="")
    status_label.configure(text="Téléchargement en cours...", text_color="blue")
    # Désactive le bouton de téléchargement
    download_btn.configure(state="disabled")


    def run():
        stop_download_flag.clear()
        # Récupère le titre de la vidéo avant téléchargement
        try:
            with YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                extractor = info.get('extractor_key', 'Unknown Site')
                title = info.get('title', 'Titre inconnu')
                #print("info on video", title, extractor)
                app.after(0, lambda: video_title_label.configure(text=f"🎬 {title} - ( {extractor} ) "))
        except Exception:
            app.after(0, lambda: video_title_label.configure(text="Titre non trouvé"))

        def progress_hook(d):
            if stop_download_flag.is_set():
                raise Exception("Téléchargement arrêté par l'utilisateur.")
            if d.get('status') == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                percent = (downloaded / total_bytes) if total_bytes else 0
                speed = d.get('speed')
                eta = d.get('eta')
                
                speed_str = f"{(speed/1024):.1f}" if speed is not None else "?"
                eta_str = f"{eta:.2f}" if eta is not None else "?"
                app.after(0, lambda: progress_bar.set(percent))
                stats = f"{percent*100:.1f}%  |  {speed_str} Ko/s  |  ETA: {eta_str}s"
                app.after(0, lambda: stats_label.configure(text=stats))
            elif d.get('status') == 'finished':
                app.after(0, lambda: progress_bar.set(1))
                app.after(0, lambda: stats_label.configure(text="Fusion ou finalisation..."))
                app.after(0, lambda: download_btn.configure(state="normal"))
                app.after(0, lambda: spinner_label.stop())
                app.after(0, lambda: spinner_frame.pack_forget())


        try:
            # Détection du chemin ffmpeg embarqué compatible PyInstaller (onefile ou onedir)
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)

            ffmpeg_path = os.path.join(base_path, "ffmpeg", "bin", "ffmpeg.exe")
            # Pour PyInstaller onefile, build avec :
            # pyinstaller --onefile --add-data "ffmpeg/bin/ffmpeg.exe;ffmpeg/bin" main.py

            # Options yt-dlp avec timeout, retries et hook de progression
            ydl_opts = {
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'ffmpeg_location': ffmpeg_path,
                'retries': 10,
                'socket_timeout': 30,
                'progress_hooks': [progress_hook],
            }

            if format_choice == "mp3":
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({'format': 'bestvideo+bestaudio/best'})

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            app.after(0, lambda: status_label.configure(text="✅ Téléchargement terminé !", text_color="green"))
            app.after(0, lambda: stats_label.configure(text=""))
            app.after(0, lambda: download_btn.configure(state="normal"))
            app.after(0, lambda: spinner_label.stop())
            app.after(0, lambda: spinner_frame.pack_forget())

        except Exception as e:
            app.after(0, lambda err=e: status_label.configure(text=f"Erreur : {err}", text_color="red"))
            app.after(0, lambda: download_btn.configure(state="normal"))
            app.after(0, lambda: spinner_label.stop())
            app.after(0, lambda: spinner_frame.pack_forget())

    global download_thread
    download_thread = threading.Thread(target=run)
    download_thread.start()

# Fonction pour stopper le téléchargement
def stop_download():
    stop_download_flag.set()
    status_label.configure(text="⏹️ Téléchargement arrêté.", text_color="orange")
    download_btn.configure(state="normal")
    spinner_label.stop()
    spinner_frame.pack_forget()

# Fonction pour quitter l'application
def quit_app():
    app.destroy()

# ---------- Fonction choix dossier ----------
def choose_folder():
    global download_folder
    folder = filedialog.askdirectory()
    if folder:
        download_folder = folder
        folder_label.configure(text=f"Dossier : {download_folder}")

# ---------- UI ----------
ctk.set_appearance_mode("light")  # "light" ou "dark"
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Audio/Video Downloader")
app.geometry("800x500")
app.resizable(False, False)

# Variables
format_var = ctk.StringVar(value="mp4")
download_folder = os.path.expanduser("~/Downloads")
download_button_state="normal"


# Champ URL
url_entry = ctk.CTkEntry(app, placeholder_text="Coller le lien ici...", width=400)
url_entry.pack(pady=20)


# Frame pour le titre et le spinner côte à côte
spinner_frame = ctk.CTkFrame(app, fg_color="transparent")
spinner_frame.pack_forget()
video_title_label = ctk.CTkLabel(spinner_frame, text="", text_color="blue")
video_title_label.pack(side="left", padx=5)
spinner_label = ctk.CTkProgressBar(spinner_frame, width=30, height=20, mode="indeterminate")
spinner_label.set(0.5)
spinner_label.pack(side="left", padx=5)

# Choix format
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

mp3_btn = ctk.CTkRadioButton(frame, text="MP3", variable=format_var, value="mp3")
mp3_btn.pack(side="left", padx=10)

mp4_btn = ctk.CTkRadioButton(frame, text="MP4", variable=format_var, value="mp4")
mp4_btn.pack(side="left", padx=10)


# Boutons action
action_frame = ctk.CTkFrame(app, fg_color="transparent")
action_frame.pack(pady=10)
download_btn = ctk.CTkButton(action_frame, text="Télécharger", command=download_video, state=download_button_state)
download_btn.pack(side="left", padx=10)
stop_btn = ctk.CTkButton(action_frame, text="Arrêter", command=stop_download)
stop_btn.pack(side="left", padx=10)
quit_btn = ctk.CTkButton(action_frame, text="Quitter", command=quit_app)
quit_btn.pack(side="left", padx=10)


# Barre de progression
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(pady=10)

# Label stats
stats_label = ctk.CTkLabel(app, text="", text_color="grey")
stats_label.pack()

# Dossier de sortie
folder_btn = ctk.CTkButton(app, text="Changer dossier de sortie", command=choose_folder)
folder_btn.pack(pady=5)

folder_label = ctk.CTkLabel(app, text=f"Dossier : {download_folder}")
folder_label.pack()

# Label status
status_label = ctk.CTkLabel(app, text="", text_color="grey")
status_label.pack(pady=10)

app.mainloop()
