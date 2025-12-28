from __future__ import annotations
import os
import sys
import time
import random
import platform
import subprocess
import shutil
import webbrowser

#!/usr/bin/env python3
"""
gurt.py - A small "cool" CLI app with fun utilities.

Features:
 - Color banner with gradient
 - Random ASCII art generator
 - System info (platform, python, uptime)
 - Surprise web opener (uses $BROWSER <url> if set)
 - Tiny guess-the-number game

Drop this file into your workspace and run: python3 gurt.py
"""


# --- ANSI helpers ---
CSI = "\x1b["
RESET = CSI + "0m"
BOLD = CSI + "1m"
HIDE = CSI + "?25l"
SHOW = CSI + "?25h"

def fg_rgb(r: int, g: int, b: int) -> str:
    return f"{CSI}38;2;{r};{g};{b}m"

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# --- Banner / visual ---
BANNER_TEXT = "G U R T"

def gradient_text(text: str, start=(120, 0, 255), end=(0, 200, 255)) -> str:
    out = []
    n = max(1, len(text) - 1)
    for i, ch in enumerate(text):
        r = int(start[0] + (end[0] - start[0]) * (i / n))
        g = int(start[1] + (end[1] - start[1]) * (i / n))
        b = int(start[2] + (end[2] - start[2]) * (i / n))
        out.append(fg_rgb(r, g, b) + ch)
    out.append(RESET)
    return "".join(out)

def print_banner() -> None:
    width = shutil.get_terminal_size((80, 20)).columns
    title = gradient_text(BANNER_TEXT, (255, 100, 0), (0, 200, 255))
    subtitle = fg_rgb(200, 200, 200) + "a tiny playground of silly and useful tricks" + RESET
    pad = max(0, (width - len(BANNER_TEXT)) // 2)
    print("\n" * 1 + " " * pad + BOLD + title + RESET)
    print(" " * max(0, (width - len(subtitle)) // 2) + subtitle + "\n")

# --- ASCII art generator ---
ARTS = [
    r"""
      .-'''-.
     / .===. \
     \/ 6 6 \/
     ( \___/ )
 ___ooo__V__ooo___
""",
    r"""
   (\_/)
   ( •_•)
  / >🍪   -- cookie bot
""",
    r"""
   ____  /|
  / . .\/ /
  \  ---|/
   \  /
__/_/__
""",
    r"""
   _____
  /     \
 | () () |
  \  ^  /
   |||||
   |||||
"""
]

def show_ascii_art() -> None:
    art = random.choice(ARTS).strip("\n")
    # colorize each line slightly differently
    lines = art.splitlines()
    for i, line in enumerate(lines):
        r = (50 + i * 30) % 256
        g = (100 + i * 20) % 256
        b = (200 - i * 15) % 256
        print(fg_rgb(r, g, b) + line + RESET)
    print()

# --- System info ---
def run_cmd_output(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return ""

def show_system_info() -> None:
    print(BOLD + "System Info" + RESET)
    print("Platform: ", platform.system(), platform.release(), platform.machine())
    print("Python:   ", platform.python_version())
    # Try uname
    uname = run_cmd_output(["uname", "-a"])
    if uname:
        print("Uname:    ", uname)
    # Try uptime (Linux)
    uptime = run_cmd_output(["uptime", "-p"])
    if uptime:
        print("Uptime:   ", uptime)
    else:
        # fallback: read /proc/uptime if present
        try:
            with open("/proc/uptime", "r") as f:
                secs = float(f.readline().split()[0])
                mins = int(secs // 60)
                hrs = mins // 60
                days = hrs // 24
                print(f"Uptime:   {days}d {hrs%24}h {mins%60}m")
        except Exception:
            pass
    # Disk usage
    total, used, free = shutil.disk_usage(".")
    def fmt(n): return f"{n/1024**3:.2f} GiB"
    print("Disk (cwd):", fmt(total), "used:", fmt(used), "free:", fmt(free))
    print()

# --- Surprise web opener ---
SURPRISES = [
    "https://thisworddoesnotexist.com/",
    "https://web.archive.org/web/20200202020202/https://www.retrojunk.com/",
    "https://patatap.com/",
    "https://shadertoy.com/",
    "https://pointerpointer.com/"
]

def open_surprise() -> None:
    url = random.choice(SURPRISES)
    browser_cmd = os.environ.get("BROWSER")
    print(BOLD + "Opening surprise:" + RESET, url)
    time.sleep(0.3)
    if browser_cmd:
        try:
            # If BROWSER is a single command name with args, keep it simple.
            subprocess.run([browser_cmd, url], check=False)
            return
        except Exception:
            pass
    # fallback to python webbrowser
    try:
        webbrowser.open(url)
    except Exception:
        print("Couldn't open browser. Try visiting:", url)
    print()

# --- Tiny game ---
def guess_number() -> None:
    print(BOLD + "Guess the Number" + RESET)
    low, high = 1, 100
    secret = random.randint(low, high)
    attempts = 0
    print(f"I'm thinking of a number between {low} and {high}. Try to guess!")
    while True:
        try:
            s = input("> ").strip()
            if s.lower() in ("q", "quit", "exit"):
                print("Aborted.")
                return
            guess = int(s)
            attempts += 1
            if guess < secret:
                print("Higher.")
            elif guess > secret:
                print("Lower.")
            else:
                print(f"Nice! {secret} in {attempts} attempts.")
                return
        except ValueError:
            print("Type a number or 'q' to quit.")

# --- Menu loop ---
def main_loop() -> None:
    try:
        while True:
            clear()
            print_banner()
            print("Menu:")
            print("  1) Random ASCII art")
            print("  2) System info")
            print("  3) Surprise web (uses $BROWSER if set)")
            print("  4) Guess the number")
            print("  q) Quit")
            choice = input("\nChoose: ").strip().lower()
            if choice in ("1", "a", "art"):
                clear()
                print_banner()
                show_ascii_art()
                input("Press Enter to continue...")
            elif choice in ("2", "s", "sys"):
                clear()
                print_banner()
                show_system_info()
                input("Press Enter to continue...")
            elif choice in ("3", "w", "web", "surprise"):
                open_surprise()
                input("Press Enter to continue...")
            elif choice in ("4", "g", "game"):
                clear()
                print_banner()
                guess_number()
                input("Press Enter to continue...")
            elif choice in ("q", "quit", "exit"):
                print("Goodbye.")
                break
            else:
                print("Unknown choice.")
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nInterrupted. Bye.")

if __name__ == "__main__":
    main_loop()