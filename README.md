
# OrangYT Downloader

OrangYT is a lightweight graphical YouTube downloader built with customtkinter and the powerful yt-dlp library.  
It lets you quickly grab video **or** audio from any YouTube link in a few clicks—all wrapped in a minimal dark-themed interface.

<div align="center">
  <img width="588" height="439" alt="OrangYT screenshot" src="https://github.com/user-attachments/assets/eb794fea-a77f-44e0-96d4-598970049868" />
</div>

---

## 😎 OS Support

| OS | Support |
|------|-------------|
| Windows | Yea |
| Linux | Hell yea |
| MacOS | IDK try yourself or port

---


## ✨ Features

* **Simple GUI** – no command line knowledge required.
* **Multiple output formats**  
  • Video: `mp4`, `mkv`  
  • Audio: `mp3`, `flac`, `ogg`, `wav`, `m4a`
* **Automatic cleaning** – intermediate files are removed after post-processing.
* **Progress feedback** – live percentage and file-size information while downloading.
* **Smart URL handling** – supports shortened `youtu.be` links and adds missing protocols automatically.
* **Removes Ads!!!** – Removes unwanted ads from video when downloaded.


---

## 📚 How to use?
1. **Download from here: [Link](https://github.com/adasjusk/OrangYT/releases)**

2. **Launch EXE or Python file**

---

## 🚀 How to get working source?
1. **Download Source Code or Clone the repository**
   ```bash
   git clone https://github.com/adasjusk/OrangYT.git
   cd OrangYT
   ```
2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage

Run the application directly with Python:

```bash
python orangyt.py
```

1. Paste the YouTube video URL in the text field.
2. Select **Video** or **Audio**.
3. Choose the desired output format from the dropdown.
4. Click **Download** and watch the progress bar.

The file is saved in the same folder as the script (or your working directory) using the original video title.

---

## 🚑 Troubleshooting

* **`ffmpeg not found`** – Ensure FFmpeg is installed and accessible in your `PATH`.
* **`ERROR: Unsupported URL`** – Double-check the link; it should be a valid YouTube watch URL.
* **No GUI appears** – Make sure you are running the script with a Python version ≥ 3.8 with Tk support.

---

## 🛡️ License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

* [yt-dlp](https://github.com/yt-dlp/yt-dlp) – an actively maintained `youtube-dl` fork.
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) – a modern skin for Tkinter.
---

Made with 🧡  by *adasjusk*
