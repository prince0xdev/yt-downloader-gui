import customtkinter as ctk
from tkinter import filedialog
from yt_dlp import YoutubeDL
import threading
import os
import sys

# ---------- Fonction téléchargement ----------
def download_video():
    url = url_entry.get()
    format_choice = format_var.get()
    if not url:
        status_label.configure(text="❌ Veuillez entrer une URL.", text_color="red")
        return


    # Réinitialise la barre et le label stats
    progress_bar.set(0)
    stats_label.configure(text="")
    status_label.configure(text="Téléchargement en cours...", text_color="blue")

    def run():
        def progress_hook(d):
            if d.get('status') == 'downloading':
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                percent = (downloaded / total_bytes) if total_bytes else 0
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                # MAJ UI dans le thread principal
                app.after(0, lambda: progress_bar.set(percent))
                stats = f"{percent*100:.1f}%  |  {speed/1024:.1f} Ko/s  |  ETA: {eta}s"
                app.after(0, lambda: stats_label.configure(text=stats))
            elif d.get('status') == 'finished':
                app.after(0, lambda: progress_bar.set(1))
                app.after(0, lambda: stats_label.configure(text="Fusion ou finalisation..."))

        try:
            # Détection du chemin ffmpeg embarqué
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)

            ffmpeg_path = os.path.join(base_path, "ffmpeg", "bin", "ffmpeg.exe")

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

        except Exception as e:
            app.after(0, lambda: status_label.configure(text=f"Erreur : {e}", text_color="red"))

    threading.Thread(target=run).start()

# ---------- Fonction choix dossier ----------
def choose_folder():
    global download_folder
    folder = filedialog.askdirectory()
    if folder:
        download_folder = folder
        folder_label.configure(text=f"Dossier : {download_folder}")

# ---------- UI ----------
ctk.set_appearance_mode("light")  # "light" ou "dark"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Audio/Video Downloader")
app.geometry("600x400")
app.resizable(False, False)

# Variables
format_var = ctk.StringVar(value="mp4")
download_folder = os.path.expanduser("~/Downloads")

# Champ URL
url_entry = ctk.CTkEntry(app, placeholder_text="Coller le lien ici...", width=400)
url_entry.pack(pady=20)

# Choix format
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

mp3_btn = ctk.CTkRadioButton(frame, text="MP3", variable=format_var, value="mp3")
mp3_btn.pack(side="left", padx=10)

mp4_btn = ctk.CTkRadioButton(frame, text="MP4", variable=format_var, value="mp4")
mp4_btn.pack(side="left", padx=10)

# Bouton télécharger
download_btn = ctk.CTkButton(app, text="Télécharger", command=download_video)
download_btn.pack(pady=20)


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
