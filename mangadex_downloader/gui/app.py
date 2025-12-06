# MIT License

# Copyright (c) 2022-present Rahman Yusuf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import customtkinter as ctk
import threading
import logging
import queue
from tkinter import filedialog, messagebox
from io import BytesIO

from ..language import Language
from ..format import formats
from ..cover import valid_cover_types
from ..cli.utils import setup_logging
from .. import __version__
from ..iterator import IteratorManga
from ..utils import get_cover_art_url
from ..network import Net

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Configure customtkinter appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

log = logging.getLogger(__name__)


class LogHandler(logging.Handler):
    """Custom logging handler to redirect logs to GUI"""
    
    def __init__(self, log_widget):
        super().__init__()
        self.log_widget = log_widget
        self.log_queue = queue.Queue()
        
    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)


class MangaDexDownloaderGUI(ctk.CTk):
    """Main GUI application for MangaDex Downloader"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(f"MangaDex Downloader v{__version__}")
        self.geometry("1000x700")
        
        # Initialize variables
        self.download_thread = None
        self.log_handler = None
        
        # Create UI components
        self.create_widgets()
        
        # Setup logging
        self.setup_logging()
        
        # Start log update loop
        self.update_logs()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Create main container with tabs
        self.tabview = ctk.CTkTabview(self, width=980, height=680)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Create tabs
        self.tab_search = self.tabview.add("Search")
        self.tab_download = self.tabview.add("Download")
        self.tab_auth = self.tabview.add("Authentication")
        self.tab_settings = self.tabview.add("Settings")
        self.tab_logs = self.tabview.add("Logs")
        
        # Setup each tab
        self.setup_search_tab()
        self.setup_download_tab()
        self.setup_auth_tab()
        self.setup_settings_tab()
        self.setup_logs_tab()
        
    def setup_search_tab(self):
        """Setup the search tab"""
        
        # Search Input Frame
        search_frame = ctk.CTkFrame(self.tab_search)
        search_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(search_frame, text="Search Manga:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Title search
        title_search_frame = ctk.CTkFrame(search_frame)
        title_search_frame.pack(padx=10, pady=(0, 5), fill="x")
        
        ctk.CTkLabel(title_search_frame, text="Title:", width=60).pack(side="left", padx=(0, 5), pady=5)
        self.search_entry = ctk.CTkEntry(title_search_frame, placeholder_text="Enter manga title to search")
        self.search_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        
        # Author search
        author_search_frame = ctk.CTkFrame(search_frame)
        author_search_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        ctk.CTkLabel(author_search_frame, text="Author:", width=60).pack(side="left", padx=(0, 5), pady=5)
        self.author_entry = ctk.CTkEntry(author_search_frame, placeholder_text="Enter author name (optional)")
        self.author_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        
        self.search_button = ctk.CTkButton(author_search_frame, text="Search", width=100, command=self.start_search)
        self.search_button.pack(side="left", padx=5, pady=5)
        
        # Search Results Frame
        results_frame = ctk.CTkFrame(self.tab_search)
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(results_frame, text="Search Results:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Scrollable frame for results
        self.search_results_frame = ctk.CTkScrollableFrame(results_frame, width=940, height=500)
        self.search_results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Status label
        self.search_status_label = ctk.CTkLabel(self.tab_search, text="Ready to search")
        self.search_status_label.pack(padx=10, pady=5)
        
        # Variable to store search results
        self.search_results = []
        
    def setup_download_tab(self):
        """Setup the download tab"""
        
        # URL Input Frame
        url_frame = ctk.CTkFrame(self.tab_download)
        url_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(url_frame, text="MangaDex URL or File:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        url_input_frame = ctk.CTkFrame(url_frame)
        url_input_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        self.url_entry = ctk.CTkEntry(url_input_frame, placeholder_text="Enter MangaDex URL or path to file with URLs")
        self.url_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        
        self.browse_button = ctk.CTkButton(url_input_frame, text="Browse", width=100, command=self.browse_file)
        self.browse_button.pack(side="left", padx=5, pady=5)
        
        # Type Selection
        type_frame = ctk.CTkFrame(self.tab_download)
        type_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(type_frame, text="Download Type:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.type_var = ctk.StringVar(value="auto")
        type_options = ["auto", "manga", "chapter", "list", "cover", "legacy-manga", "legacy-chapter"]
        
        type_option_frame = ctk.CTkFrame(type_frame)
        type_option_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        for i, option in enumerate(type_options):
            radio = ctk.CTkRadioButton(type_option_frame, text=option.capitalize(), variable=self.type_var, value=option)
            radio.grid(row=i//4, column=i%4, padx=10, pady=5, sticky="w")
        
        # Options Frame
        options_frame = ctk.CTkFrame(self.tab_download)
        options_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(options_frame, text="Download Options:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Left column
        left_col = ctk.CTkFrame(options_frame)
        left_col.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Language
        lang_frame = ctk.CTkFrame(left_col)
        lang_frame.pack(padx=5, pady=5, fill="x")
        ctk.CTkLabel(lang_frame, text="Language:").pack(side="left", padx=5)
        lang_list = [lang.name for lang in Language]
        self.language_var = ctk.StringVar(value="English")
        self.language_menu = ctk.CTkOptionMenu(lang_frame, variable=self.language_var, values=lang_list)
        self.language_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Format
        format_frame = ctk.CTkFrame(left_col)
        format_frame.pack(padx=5, pady=5, fill="x")
        ctk.CTkLabel(format_frame, text="Format:").pack(side="left", padx=5)
        self.format_var = ctk.StringVar(value="raw")
        self.format_menu = ctk.CTkOptionMenu(format_frame, variable=self.format_var, values=list(formats.keys()))
        self.format_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Cover Quality
        cover_frame = ctk.CTkFrame(left_col)
        cover_frame.pack(padx=5, pady=5, fill="x")
        ctk.CTkLabel(cover_frame, text="Cover:").pack(side="left", padx=5)
        self.cover_var = ctk.StringVar(value="original")
        self.cover_menu = ctk.CTkOptionMenu(cover_frame, variable=self.cover_var, values=valid_cover_types)
        self.cover_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Right column
        right_col = ctk.CTkFrame(options_frame)
        right_col.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Checkboxes
        self.replace_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(right_col, text="Replace existing files", variable=self.replace_var).pack(anchor="w", padx=5, pady=5)
        
        self.use_alt_details_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(right_col, text="Use alternative details", variable=self.use_alt_details_var).pack(anchor="w", padx=5, pady=5)
        
        self.no_oneshot_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(right_col, text="No oneshot chapters", variable=self.no_oneshot_var).pack(anchor="w", padx=5, pady=5)
        
        self.use_compressed_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(right_col, text="Use compressed images", variable=self.use_compressed_var).pack(anchor="w", padx=5, pady=5)
        
        # Chapter range
        range_frame = ctk.CTkFrame(right_col)
        range_frame.pack(padx=5, pady=5, fill="x")
        
        ctk.CTkLabel(range_frame, text="Start Chapter:").pack(side="left", padx=5)
        self.start_chapter_entry = ctk.CTkEntry(range_frame, width=80, placeholder_text="Optional")
        self.start_chapter_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(range_frame, text="End:").pack(side="left", padx=5)
        self.end_chapter_entry = ctk.CTkEntry(range_frame, width=80, placeholder_text="Optional")
        self.end_chapter_entry.pack(side="left", padx=5)
        
        # Download button
        button_frame = ctk.CTkFrame(self.tab_download)
        button_frame.pack(padx=10, pady=10, fill="x")
        
        self.download_button = ctk.CTkButton(
            button_frame, 
            text="Download", 
            font=("Arial", 14, "bold"),
            height=40,
            command=self.start_download
        )
        self.download_button.pack(padx=10, pady=10, fill="x")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.tab_download)
        self.progress_bar.pack(padx=10, pady=5, fill="x")
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(self.tab_download, text="Ready")
        self.progress_label.pack(padx=10, pady=5)
        
    def setup_auth_tab(self):
        """Setup the authentication tab"""
        
        auth_frame = ctk.CTkFrame(self.tab_auth)
        auth_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(auth_frame, text="MangaDex Authentication", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Login method
        method_frame = ctk.CTkFrame(auth_frame)
        method_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(method_frame, text="Login Method:").pack(side="left", padx=5)
        self.login_method_var = ctk.StringVar(value="oauth2")
        self.login_method_menu = ctk.CTkOptionMenu(method_frame, variable=self.login_method_var, values=["oauth2", "legacy"])
        self.login_method_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Username
        username_frame = ctk.CTkFrame(auth_frame)
        username_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(username_frame, text="Username:").pack(side="left", padx=5)
        self.username_entry = ctk.CTkEntry(username_frame, placeholder_text="Your MangaDex username")
        self.username_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Password
        password_frame = ctk.CTkFrame(auth_frame)
        password_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(password_frame, text="Password:").pack(side="left", padx=5)
        self.password_entry = ctk.CTkEntry(password_frame, show="*", placeholder_text="Your MangaDex password")
        self.password_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Cache option
        self.login_cache_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(auth_frame, text="Cache login credentials", variable=self.login_cache_var).pack(pady=10)
        
        # Login/Logout buttons
        button_frame = ctk.CTkFrame(auth_frame)
        button_frame.pack(pady=20)
        
        self.login_button = ctk.CTkButton(button_frame, text="Login", width=150, command=self.login)
        self.login_button.pack(side="left", padx=10)
        
        self.logout_button = ctk.CTkButton(button_frame, text="Logout", width=150, command=self.logout)
        self.logout_button.pack(side="left", padx=10)
        
        # Status
        self.auth_status_label = ctk.CTkLabel(auth_frame, text="Not logged in", font=("Arial", 12))
        self.auth_status_label.pack(pady=10)
        
    def setup_settings_tab(self):
        """Setup the settings tab"""
        
        settings_frame = ctk.CTkFrame(self.tab_settings)
        settings_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(settings_frame, text="Application Settings", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Download path
        path_frame = ctk.CTkFrame(settings_frame)
        path_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(path_frame, text="Download Path:").pack(side="left", padx=5)
        self.path_entry = ctk.CTkEntry(path_frame, placeholder_text="Default: current directory")
        self.path_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.path_browse_button = ctk.CTkButton(path_frame, text="Browse", width=100, command=self.browse_directory)
        self.path_browse_button.pack(side="left", padx=5)
        
        # Network settings
        network_frame = ctk.CTkFrame(settings_frame)
        network_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(network_frame, text="Network Settings", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        # Proxy
        proxy_frame = ctk.CTkFrame(network_frame)
        proxy_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(proxy_frame, text="Proxy:").pack(side="left", padx=5)
        self.proxy_entry = ctk.CTkEntry(proxy_frame, placeholder_text="http://proxy:port or socks5://proxy:port")
        self.proxy_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Timeout
        timeout_frame = ctk.CTkFrame(network_frame)
        timeout_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(timeout_frame, text="Timeout (seconds):").pack(side="left", padx=5)
        self.timeout_entry = ctk.CTkEntry(timeout_frame, width=100, placeholder_text="Default: 300")
        self.timeout_entry.pack(side="left", padx=5)
        
        # Delay
        delay_frame = ctk.CTkFrame(network_frame)
        delay_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(delay_frame, text="Delay between requests (seconds):").pack(side="left", padx=5)
        self.delay_entry = ctk.CTkEntry(delay_frame, width=100, placeholder_text="Default: 0")
        self.delay_entry.pack(side="left", padx=5)
        
        # DNS over HTTPS
        dns_frame = ctk.CTkFrame(network_frame)
        dns_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(dns_frame, text="DNS over HTTPS:").pack(side="left", padx=5)
        self.dns_var = ctk.StringVar(value="none")
        dns_options = ["none", "google", "cloudflare"]
        self.dns_menu = ctk.CTkOptionMenu(dns_frame, variable=self.dns_var, values=dns_options)
        self.dns_menu.pack(side="left", padx=5, fill="x", expand=True)
        
        # Other options
        options_frame = ctk.CTkFrame(settings_frame)
        options_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(options_frame, text="Other Options", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        
        self.force_https_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Force HTTPS", variable=self.force_https_var).pack(anchor="w", padx=10, pady=5)
        
        self.no_track_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Disable chapter tracking", variable=self.no_track_var).pack(anchor="w", padx=10, pady=5)
        
        # Log level
        log_frame = ctk.CTkFrame(settings_frame)
        log_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(log_frame, text="Log Level:").pack(side="left", padx=5)
        self.log_level_var = ctk.StringVar(value="INFO")
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        self.log_level_menu = ctk.CTkOptionMenu(log_frame, variable=self.log_level_var, values=log_levels)
        self.log_level_menu.pack(side="left", padx=5, fill="x", expand=True)
        
    def setup_logs_tab(self):
        """Setup the logs tab"""
        
        logs_frame = ctk.CTkFrame(self.tab_logs)
        logs_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Logs text widget
        self.logs_text = ctk.CTkTextbox(logs_frame, wrap="word", state="disabled")
        self.logs_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Clear button
        clear_button = ctk.CTkButton(logs_frame, text="Clear Logs", command=self.clear_logs)
        clear_button.pack(pady=5)
        
    def setup_logging(self):
        """Setup logging to GUI"""
        
        # Setup logging
        log = setup_logging("mangadex_downloader", False)
        
        # Add custom handler for GUI
        self.log_handler = LogHandler(self.logs_text)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        log.addHandler(self.log_handler)
        
    def update_logs(self):
        """Update logs in the GUI"""
        
        if self.log_handler:
            try:
                while True:
                    msg = self.log_handler.log_queue.get_nowait()
                    self.logs_text.configure(state="normal")
                    self.logs_text.insert("end", msg + "\n")
                    self.logs_text.see("end")
                    self.logs_text.configure(state="disabled")
            except queue.Empty:
                pass
        
        # Schedule next update
        self.after(100, self.update_logs)
        
    def clear_logs(self):
        """Clear the logs display"""
        
        self.logs_text.configure(state="normal")
        self.logs_text.delete("1.0", "end")
        self.logs_text.configure(state="disabled")
        
    def browse_file(self):
        """Browse for a file containing URLs"""
        
        filename = filedialog.askopenfilename(
            title="Select file with URLs",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, filename)
            
    def browse_directory(self):
        """Browse for download directory"""
        
        directory = filedialog.askdirectory(title="Select download directory")
        if directory:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, directory)
            
    def start_download(self):
        """Start the download process"""
        
        if self.download_thread and self.download_thread.is_alive():
            messagebox.showwarning("Download in progress", "A download is already in progress!")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL or select a file!")
            return
        
        # Disable download button
        self.download_button.configure(state="disabled", text="Downloading...")
        self.progress_label.configure(text="Starting download...")
        self.progress_bar.set(0)
        
        # Start download in separate thread
        self.download_thread = threading.Thread(target=self.download_worker, args=(url,), daemon=True)
        self.download_thread.start()
        
    def download_worker(self, url):
        """Worker thread for downloading"""
        
        try:
            # Build command-line arguments
            args = self.build_cli_args(url)
            
            # Import and call CLI
            from ..cli import _main
            
            # Run CLI in thread
            parser, exit_code, err_msg = _main(args)
            
            # Update UI based on result
            if exit_code == 0:
                self.after(0, lambda: self.download_complete("Download completed successfully!"))
            else:
                error_msg = err_msg if err_msg else "Download failed with unknown error"
                self.after(0, lambda: self.download_error(error_msg))
                
        except Exception as e:
            self.after(0, lambda err=str(e): self.download_error(err))
            
    def build_cli_args(self, url):
        """Build CLI arguments from GUI settings"""
        
        args = [url]
        
        # Type
        if self.type_var.get() != "auto":
            args.extend(["--type", self.type_var.get()])
        
        # Language
        lang = self.language_var.get()
        if lang:
            args.extend(["-lang", lang])
        
        # Format
        fmt = self.format_var.get()
        if fmt:
            args.extend(["--save-as", fmt])
        
        # Cover
        cover = self.cover_var.get()
        if cover:
            args.extend(["--cover", cover])
        
        # Replace
        if self.replace_var.get():
            args.append("--replace")
        
        # Use alternative details
        if self.use_alt_details_var.get():
            args.append("--use-alt-details")
        
        # No oneshot
        if self.no_oneshot_var.get():
            args.append("--no-oneshot-chapter")
        
        # Compressed images
        if self.use_compressed_var.get():
            args.append("--use-compressed-image")
        
        # Chapter range
        start_chapter = self.start_chapter_entry.get().strip()
        if start_chapter:
            args.extend(["--start-chapter", start_chapter])
        
        end_chapter = self.end_chapter_entry.get().strip()
        if end_chapter:
            args.extend(["--end-chapter", end_chapter])
        
        # Path
        path = self.path_entry.get().strip()
        if path:
            args.extend(["--path", path])
        
        # Proxy
        proxy = self.proxy_entry.get().strip()
        if proxy:
            args.extend(["--proxy", proxy])
        
        # Timeout
        timeout = self.timeout_entry.get().strip()
        if timeout:
            args.extend(["--timeout", timeout])
        
        # Delay
        delay = self.delay_entry.get().strip()
        if delay:
            args.extend(["--delay-requests", delay])
        
        # DNS over HTTPS
        dns = self.dns_var.get()
        if dns != "none":
            args.extend(["--dns-over-https", dns])
        
        # Force HTTPS
        if self.force_https_var.get():
            args.append("--force-https")
        
        # No track
        if self.no_track_var.get():
            args.append("--no-track")
        
        # Log level
        log_level = self.log_level_var.get()
        if log_level:
            args.extend(["--log-level", log_level])
        
        return args
        
    def download_complete(self, message):
        """Called when download completes"""
        
        self.progress_bar.set(1.0)
        self.progress_label.configure(text=message)
        self.download_button.configure(state="normal", text="Download")
        messagebox.showinfo("Success", message)
        
    def download_error(self, error_msg):
        """Called when download fails"""
        
        self.progress_bar.set(0)
        self.progress_label.configure(text="Download failed")
        self.download_button.configure(state="normal", text="Download")
        messagebox.showerror("Error", f"Download failed: {error_msg}")
        
    def login(self):
        """Handle login"""
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        # Build login arguments
        args = [
            "https://mangadex.org",  # Dummy URL
            "--login",
            "--login-username", username,
            "--login-password", password,
            "--login-method", self.login_method_var.get()
        ]
        
        if self.login_cache_var.get():
            args.append("--login-cache")
        
        # Run login in thread
        def login_worker():
            try:
                from ..cli import _main
                parser, exit_code, err_msg = _main(args)
                
                if exit_code == 0:
                    self.after(0, lambda: self.login_complete())
                else:
                    error_msg = err_msg if err_msg else "Login failed"
                    self.after(0, lambda msg=error_msg: self.login_error(msg))
            except Exception as e:
                self.after(0, lambda err=str(e): self.login_error(err))
        
        threading.Thread(target=login_worker, daemon=True).start()
        self.auth_status_label.configure(text="Logging in...")
        
    def login_complete(self):
        """Called when login completes"""
        
        self.auth_status_label.configure(text="Logged in successfully!")
        messagebox.showinfo("Success", "Logged in successfully!")
        
    def login_error(self, error_msg):
        """Called when login fails"""
        
        self.auth_status_label.configure(text="Login failed")
        messagebox.showerror("Error", f"Login failed: {error_msg}")
        
    def logout(self):
        """Handle logout"""
        def logout_worker():
            try:
                from ..network import Net
                if Net.mangadex.check_login():
                    Net.mangadex.logout()
                self.after(0, lambda: self.logout_complete())
            except Exception as e:
                self.after(0, lambda err=str(e): self.logout_error(err))

        threading.Thread(target=logout_worker, daemon=True).start()
        self.auth_status_label.configure(text="Logging out...")

    def logout_complete(self):
        self.auth_status_label.configure(text="Not logged in")
        messagebox.showinfo("Success", "Logged out successfully!")

    def logout_error(self, error_msg):
        self.auth_status_label.configure(text="Logout failed")
        messagebox.showerror("Error", f"Logout failed: {error_msg}")
    
    def start_search(self):
        """Start the manga search"""
        
        title_query = self.search_entry.get().strip()
        author_query = self.author_entry.get().strip()
        
        if not title_query and not author_query:
            messagebox.showerror("Error", "Please enter at least a title or author name to search!")
            return
        
        # Clear previous results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        self.search_results = []
        
        # Disable search button
        self.search_button.configure(state="disabled", text="Searching...")
        
        # Create search status message
        search_terms = []
        if title_query:
            search_terms.append(f"title: '{title_query}'")
        if author_query:
            search_terms.append(f"author: '{author_query}'")
        status_msg = f"Searching for {' and '.join(search_terms)}..."
        self.search_status_label.configure(text=status_msg)
        
        # Start search in separate thread
        search_thread = threading.Thread(target=self.search_worker, args=(title_query, author_query), daemon=True)
        search_thread.start()
    
    def search_worker(self, title_query, author_query):
        """Worker thread for searching manga"""
        
        try:
            # Create iterator for manga search
            # If only author is provided, search with empty title to get more results
            search_title = title_query if title_query else ""
            
            # Prepare filters for author search
            filters = {}
            if author_query:
                filters["author_name"] = author_query
            
            iterator = IteratorManga(search_title, **filters)
            
            results = []
            count = 0
            max_results = 20  # Limit displayed results
            
            # Fetch manga results
            for manga in iterator:
                results.append(manga)
                count += 1
                if count >= max_results:
                    break
            
            # Update UI with results
            self.after(0, lambda: self.display_search_results(results))
            
        except Exception as e:
            self.after(0, lambda err=str(e): self.search_error(err))
    
    def display_search_results(self, results):
        """Display search results in the GUI"""
        
        if not results:
            self.search_status_label.configure(text="No results found")
            self.search_button.configure(state="normal", text="Search")
            messagebox.showinfo("No Results", "No manga found matching your search query.")
            return
        
        self.search_results = results
        self.search_status_label.configure(text=f"Found {len(results)} results")
        
        # Display each result
        for idx, manga in enumerate(results):
            self.create_manga_result_widget(manga, idx)
        
        self.search_button.configure(state="normal", text="Search")
    
    def create_manga_result_widget(self, manga, idx):
        """Create a widget to display a single manga result"""
        
        # Container for each manga result
        result_frame = ctk.CTkFrame(self.search_results_frame)
        result_frame.pack(padx=5, pady=5, fill="x")
        
        # Left side: Cover image
        cover_frame = ctk.CTkFrame(result_frame, width=150, height=200)
        cover_frame.pack(side="left", padx=10, pady=10)
        cover_frame.pack_propagate(False)
        
        if PIL_AVAILABLE and manga.cover:
            # Load cover image in a thread
            threading.Thread(
                target=self.load_cover_image, 
                args=(manga.id, manga.cover, cover_frame), 
                daemon=True
            ).start()
        else:
            # Placeholder if PIL is not available
            no_image_label = ctk.CTkLabel(cover_frame, text="No Image\nAvailable")
            no_image_label.pack(expand=True)
        
        # Right side: Manga details
        details_frame = ctk.CTkFrame(result_frame)
        details_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            details_frame, 
            text=manga.title, 
            font=("Arial", 14, "bold"),
            wraplength=600,
            justify="left"
        )
        title_label.pack(anchor="w", padx=5, pady=(5, 2))
        
        # Authors
        if manga.authors:
            authors_text = "Authors: " + ", ".join(manga.authors)
            authors_label = ctk.CTkLabel(details_frame, text=authors_text, wraplength=600, justify="left")
            authors_label.pack(anchor="w", padx=5, pady=2)
        
        # Status and Year
        status_text = f"Status: {manga.status}"
        if hasattr(manga, 'year') and manga.year:
            status_text += f" | Year: {manga.year}"
        status_label = ctk.CTkLabel(details_frame, text=status_text)
        status_label.pack(anchor="w", padx=5, pady=2)
        
        # Genres
        if manga.genres:
            genres_text = "Genres: " + ", ".join(manga.genres[:5])  # Limit to 5 genres
            if len(manga.genres) > 5:
                genres_text += "..."
            genres_label = ctk.CTkLabel(details_frame, text=genres_text, wraplength=600, justify="left")
            genres_label.pack(anchor="w", padx=5, pady=2)
        
        # Description (truncated)
        if manga.description:
            desc_text = manga.description[:200] + "..." if len(manga.description) > 200 else manga.description
            desc_label = ctk.CTkLabel(
                details_frame, 
                text=f"Description: {desc_text}",
                wraplength=600,
                justify="left"
            )
            desc_label.pack(anchor="w", padx=5, pady=2)
        
        # Download button
        download_btn = ctk.CTkButton(
            details_frame,
            text="Download This Manga",
            command=lambda m=manga: self.download_from_search(m)
        )
        download_btn.pack(anchor="w", padx=5, pady=10)
    
    def load_cover_image(self, manga_id, cover, cover_frame):
        """Load and display manga cover image"""
        
        try:
            # Get cover URL
            cover_url = get_cover_art_url(manga_id, cover, "256px")
            
            if not cover_url:
                return
            
            # Download image
            response = Net.mangadex.get(cover_url, stream=True)
            response.raise_for_status()
            
            # Load image with PIL
            image_data = BytesIO(response.content)
            pil_image = Image.open(image_data)
            
            # Resize to fit the frame
            pil_image.thumbnail((150, 200), Image.Resampling.LANCZOS)
            
            # Convert to CTkImage for proper HighDPI support
            ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(150, 200))
            
            # Display in GUI (must be done in main thread)
            def display():
                # Clear existing widgets
                for widget in cover_frame.winfo_children():
                    widget.destroy()
                
                # Create label with CTkImage
                img_label = ctk.CTkLabel(cover_frame, image=ctk_image, text="")
                img_label.image = ctk_image  # Keep a reference
                img_label.pack(expand=True)
            
            self.after(0, display)
            
        except Exception as e:
            log.debug(f"Failed to load cover image: {e}")
            # If loading fails, we just don't show an image
    
    def download_from_search(self, manga):
        """Initiate download from a search result"""
        
        # Switch to download tab
        self.tabview.set("Download")
        
        # Fill in the URL field with manga URL
        manga_url = f"https://mangadex.org/title/{manga.id}"
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, manga_url)
        
        # Auto-start download or just show a message
        messagebox.showinfo(
            "Ready to Download", 
            f"Manga '{manga.title}' URL has been loaded. Click Download to start."
        )
    
    def search_error(self, error_msg):
        """Called when search fails"""
        
        self.search_status_label.configure(text="Search failed")
        self.search_button.configure(state="normal", text="Search")
        messagebox.showerror("Error", f"Search failed: {error_msg}")

def main():
    """Main entry point for GUI"""
    app = MangaDexDownloaderGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
