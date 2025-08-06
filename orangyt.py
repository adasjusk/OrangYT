import customtkinter as ctk
import tkinter as tk
import sys
import os, threading, yt_dlp
from urllib.request import build_opener, install_opener

opener = build_opener()
opener.addheaders = [
    (
        "User-Agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    )
]
install_opener(opener)

# ---------------------------------------------------------------------------
#  Helper to load window icon (works for normal run & PyInstaller bundle)
# ---------------------------------------------------------------------------

def load_icon(filename: str) -> tk.PhotoImage:
    """Return a Tk PhotoImage for the given filename.
    The path is resolved correctly when bundled with PyInstaller."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return tk.PhotoImage(file=os.path.join(base_path, filename))
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class OrangYT(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OrangYT Downloader")
        self.geometry("600x450")
        self.orange_colour = "#ff6b00"
        self.configure(fg_color=("gray90", "gray16"))
        # Set application icon
        self.icon = load_icon("orange.png")  # keep reference to avoid GC
        self.iconphoto(False, self.icon)
        self.url_label = ctk.CTkLabel(self, text="Enter YouTube URL:", text_color=self.orange_colour)
        self.url_label.pack(pady=10)
        self.url_entry = ctk.CTkEntry(self, width=400, border_color=self.orange_colour, fg_color=("gray95", "gray20"))
        self.url_entry.pack(pady=5)
        self.format_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.format_frame.pack(pady=20)
        self.format_var = ctk.StringVar(value="video")
        self.video_radio = ctk.CTkRadioButton(
            self.format_frame,
            text="Video",
            variable=self.format_var,
            value="video",
            command=self._update_format_options,
            fg_color=self.orange_colour,
            border_color=self.orange_colour,
        )
        self.video_radio.pack(side="left", padx=10)
        self.audio_radio = ctk.CTkRadioButton(
            self.format_frame,
            text="Audio",
            variable=self.format_var,
            value="audio",
            command=self._update_format_options,
            fg_color=self.orange_colour,
            border_color=self.orange_colour,
        )
        self.audio_radio.pack(side="left", padx=10)
        self.format_options_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.format_options_frame.pack(pady=10)
        self.format_option_var = ctk.StringVar()
        self.format_menu = ctk.CTkOptionMenu(
            self.format_options_frame,
            variable=self.format_option_var,
            fg_color=self.orange_colour,
            button_color=self.orange_colour,
            button_hover_color=self.orange_colour,
            dropdown_hover_color=self.orange_colour,
        )
        self.format_menu.pack(pady=10)
        self.download_button = ctk.CTkButton(
            self,
            text="Download",
            command=self._start_download_thread,
            fg_color=self.orange_colour,
            hover_color=self.orange_colour,
            height=40,
        )
        self.download_button.pack(pady=20)
        self.progress_label = ctk.CTkLabel(self, text="", text_color=self.orange_colour)
        self.progress_label.pack(pady=10)
        # Available video formats (removed webm to avoid unwanted container)
        self.video_formats = ["mp4", "mkv"]
        self.audio_formats = ["mp3", "flac", "ogg", "wav", "m4a"]
        self._update_format_options()
    def _update_format_options(self):
        formats = self.video_formats if self.format_var.get() == "video" else self.audio_formats
        # Update dropdown values correctly using configure (required by customtkinter)
        self.format_menu.configure(values=formats)
        # Keep current selection if still valid, otherwise set to first option
        if self.format_option_var.get() not in formats:
            self.format_option_var.set(formats[0])

    def _start_download_thread(self):
        self.download_button.configure(state="disabled")
        self.progress_label.configure(text="Starting download…")
        threading.Thread(target=self._download, daemon=True).start()
    # -------------------------------------------------------------------
    #  core download logic using yt-dlp
    # -------------------------------------------------------------------
    def _download(self):
        try:
            url = self.url_entry.get().strip()
            if not url:
                raise ValueError("Please enter a YouTube URL")
            if "youtu.be" in url and not url.startswith("https://www.youtube.com/watch?v="):
                video_id = url.split("/")[-1]
                url = f"https://www.youtube.com/watch?v={video_id}"
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            format_type = self.format_var.get() 
            selected_format = self.format_option_var.get()
            def hook(d):
                status = d.get("status")
                if status == "downloading":
                    downloaded = d.get("downloaded_bytes", 0)
                    total = d.get("total_bytes") or d.get("total_bytes_estimate")
                    if total:
                        pct_float = downloaded / total * 100
                        mb_downloaded = downloaded / 1024 / 1024
                        mb_total = total / 1024 / 1024
                        self.progress_label.configure(
                            text=f"Downloading: {pct_float:.1f}% (" \
                                 f"{mb_downloaded:.1f}/{mb_total:.1f} MB)"
                        )
                    else:
                        # Fallback to percent string if total unknown
                        pct = d.get("_percent_str", "0% ").strip().rstrip("%")
                        try:
                            pct_float = float(pct)
                            self.progress_label.configure(text=f"Downloading: {pct_float:.1f}%")
                        except ValueError:
                            pass
                elif status == "finished":
                    self.progress_label.configure(text="Post-processing…")
            ydl_opts = {
                "quiet": True,
                "progress_hooks": [hook],
                # Correct template placeholders to include actual title and extension
                "outtmpl": "%(title)s.%(ext)s",
                # Remove intermediary files created during post-processing
                "keepvideo": False,
            }
            if format_type == "video":
                # Select streams that match chosen container when possible
                if selected_format == "mp4":
                    # Prefer MP4 video+audio streams to avoid later conversion
                    ydl_opts["format"] = (
                        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                    )
                else:
                    # Grab best quality, we'll convert afterwards
                    ydl_opts["format"] = "bestvideo+bestaudio/best"

                # Always run video converter so final container matches choice
                ydl_opts["merge_output_format"] = selected_format  # ensure final container
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": selected_format,
                    }
                ]
            else:
                ydl_opts["format"] = "bestaudio/best"
                # Map GUI selection to correct ffmpeg codec name if necessary
                codec_map = {
                    "ogg": "vorbis",  # OGG container uses the Vorbis codec
                }
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": codec_map.get(selected_format, selected_format),
                        "preferredquality": "192",
                    }
                ]
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                output_path = ydl.prepare_filename(info)

            # --- cleanup of any leftover temporary files (e.g., webm, m4a) ---
            base_title = os.path.splitext(output_path)[0]
            for ext in ("webm", "m4a", "mp4", "mkv"):
                tmp_path = f"{base_title}.{ext}"
                # keep the final chosen file, delete others if present
                if ext != selected_format and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except OSError:
                        pass

            self.progress_label.configure(
                text=f"Download complete!\nSaved as: {os.path.basename(base_title + '.' + selected_format)}"
            )
        except Exception as exc:
            self.progress_label.configure(text=f"Error: {exc}")
        finally:
            self.download_button.configure(state="normal")
if __name__ == "__main__":
    app = OrangYT()
    app.mainloop()
