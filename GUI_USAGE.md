# MangaDex Downloader GUI Usage Guide

## Overview

MangaDex Downloader now includes a modern graphical user interface (GUI) built with [customtkinter](https://github.com/TomSchimansky/CustomTkinter). The GUI provides an intuitive way to access all CLI features without using the command line.

## Installation

### Requirements

- Python 3.10 or higher
- tkinter (usually comes with Python)
- customtkinter (installed as optional dependency)

### Install with GUI support

```bash
# Install with all optional dependencies (recommended)
pip install mangadex-downloader[optional]

# Or install just the GUI dependency
pip install mangadex-downloader customtkinter
```

### Linux-specific requirements

On Linux systems, you may need to install python3-tk:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

## Running the GUI

There are several ways to launch the GUI:

### Method 1: Python module (recommended)

```bash
python3 -m mangadex_downloader.gui
```

### Method 2: Using the launcher script

```bash
python3 run_gui.py
```

### Method 3: From Python code

```python
from mangadex_downloader.gui import MangaDexDownloaderGUI

app = MangaDexDownloaderGUI()
app.mainloop()
```

## GUI Features

### Search Tab

The Search tab allows you to search for manga on MangaDex and browse results with cover images.

**Features:**
- **Search Input**: Enter manga title or keywords to search
- **Search Results**: Browse manga with:
  - Cover images (automatically loaded)
  - Title and alternative titles
  - Authors and artists
  - Status and genres
  - Description preview
- **Download Button**: Click on any search result to load it into the Download tab

**Usage:**
1. Enter your search query (e.g., "One Piece", "Naruto")
2. Click the Search button
3. Browse through results with cover images
4. Click "Download This Manga" on any result to prepare it for download
5. Switch to Download tab to configure and start the download

### Download Tab

The main tab for downloading manga from MangaDex.

**Fields:**
- **URL Input**: Enter a MangaDex URL or browse for a file containing multiple URLs
- **Download Type**: Select from:
  - Auto (detect automatically)
  - Manga
  - Chapter
  - List
  - Cover
  - Legacy manga/chapter (for old URLs)
- **Language**: Choose download language (supports all MangaDex languages)
- **Format**: Select output format:
  - Raw images (raw, raw-volume, raw-single)
  - PDF (pdf, pdf-volume, pdf-single)
  - CBZ (cbz, cbz-volume, cbz-single)
  - CB7 (cb7, cb7-volume, cb7-single) - requires py7zr
  - EPUB (epub, epub-volume, epub-single) - requires lxml
- **Cover Quality**: Choose cover image quality (original, 512px, 256px, none)
- **Options**:
  - Replace existing files
  - Use alternative details
  - No oneshot chapters
  - Use compressed images
- **Chapter Range**: Optionally specify start and end chapters

### Authentication Tab

Login to MangaDex to access your library and authenticated features.

**Fields:**
- **Login Method**: Choose OAuth2 (recommended) or Legacy
- **Username**: Your MangaDex username
- **Password**: Your MangaDex password
- **Cache credentials**: Save login for future sessions

**Buttons:**
- **Login**: Authenticate with MangaDex
- **Logout**: Clear authentication

### Settings Tab

Configure application and network settings.

**Download Settings:**
- **Download Path**: Choose where to save downloaded manga

**Network Settings:**
- **Proxy**: Configure HTTP/SOCKS proxy
- **Timeout**: Set request timeout in seconds
- **Delay**: Add delay between requests
- **DNS over HTTPS**: Use secure DNS (Google or Cloudflare)

**Other Options:**
- **Force HTTPS**: Always use HTTPS for downloads
- **Disable chapter tracking**: Don't track downloaded chapters
- **Log Level**: Set logging verbosity (DEBUG, INFO, WARNING, ERROR)

### Logs Tab

View real-time logs of all operations.

**Features:**
- Real-time log display
- Shows download progress, errors, and warnings
- Clear button to reset logs

## Tips and Best Practices

### For Batch Downloads

1. Create a text file with one MangaDex URL per line
2. Use the Browse button to select the file
3. Configure your preferred settings
4. Click Download

### Using Authentication

For downloading from your library or accessing age-restricted content:
1. Go to the Authentication tab
2. Enter your credentials
3. Enable "Cache credentials" to save login
4. Click Login
5. Return to Download tab and proceed normally

### Network Issues

If you experience connection issues:
1. Go to Settings tab
2. Try enabling DNS over HTTPS
3. If behind a proxy, configure proxy settings
4. Increase timeout if downloads are slow

### Format Selection

- **Raw**: Best for reading on computer or custom readers
- **PDF**: Universal format, readable on any device
- **CBZ/CB7**: For comic book readers
- **EPUB**: For e-readers (requires lxml)

Volume vs Single vs Chapter:
- **Volume**: One file per volume
- **Single**: All chapters in one file
- **Default**: One file per chapter

## Troubleshooting

### GUI won't start

**Error: "No module named 'tkinter'"**
- Solution: Install python3-tk package for your OS

**Error: "No module named 'customtkinter'"**
- Solution: Install with `pip install customtkinter` or `pip install mangadex-downloader[optional]`

### Download Issues

**Error: "Download failed"**
- Check the Logs tab for detailed error messages
- Verify the URL is correct
- Check your internet connection
- Try enabling DNS over HTTPS in Settings

**Error: "Authentication required"**
- Some manga require login to download
- Go to Authentication tab and login
- Try downloading again

### Performance

**Slow downloads:**
- Increase timeout in Settings
- Check your internet connection
- Disable virus scanner temporarily (if it's scanning downloads)

**GUI freezing:**
- This is normal during downloads - the GUI shows progress in Logs tab
- Don't close the window while downloading

## CLI vs GUI

All CLI features are available in the GUI. The GUI internally calls the same CLI backend, ensuring consistency.

**CLI Advantages:**
- Scriptable and automatable
- Faster for power users
- Can run on headless servers

**GUI Advantages:**
- User-friendly interface
- Visual feedback with cover images
- Search manga with visual preview
- No need to remember commands
- Easy configuration management

You can use both interchangeably based on your preference!

## Contributing

If you find bugs or want to suggest GUI improvements:
1. Check existing issues on GitHub
2. Create a new issue with:
   - What you were trying to do
   - What happened instead
   - Screenshots (if applicable)
   - Log output from the Logs tab

## Additional Resources

- [CLI Documentation](https://mangadex-dl.mansuf.link/)
- [MangaDex API Documentation](https://api.mangadex.org/docs/)
- [GitHub Repository](https://github.com/mansuf/mangadex-downloader)
- [customtkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
