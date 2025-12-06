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

"""GUI launcher for MangaDex Downloader"""

import sys


def main():
    """Main entry point for GUI"""
    try:
        import customtkinter
    except ImportError:
        print("=" * 60)
        print("ERROR: customtkinter is not installed")
        print("=" * 60)
        print("\nThe GUI requires customtkinter to be installed.")
        print("\nTo install it, run one of the following commands:\n")
        print("  pip install mangadex-downloader[optional]")
        print("  pip install customtkinter\n")
        print("For more information, see GUI_USAGE.md")
        print("=" * 60)
        sys.exit(1)
    
    from .app import main as app_main
    app_main()


if __name__ == "__main__":
    main()
