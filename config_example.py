"""
config_example.py — Minimal example integrating qtile-vimified into your Qtile configuration.
"""

import os
from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy
from whichkey import setup_whichkey, make_switch_chord
from theme import colors

terminal = "alacritty"
code_editor = "zeditor"
text_editor = "nvim"

# Modal submaps (KeyChords)
keys = [
    # Master Hub (ALT + ENTER) -> Springboard to any submap
    KeyChord(["mod1"], "Return", [
        Key([], "s", make_switch_chord("System"), desc="+System & Hardware..."),
        Key([], "p", make_switch_chord("Programming"), desc="+Programming & Dev..."),
        Key([], "o", make_switch_chord("Office"), desc="+Office & Documents..."),
        Key([], "l", make_switch_chord("Learning"), desc="+Learning & Data..."),
        Key([], "i", make_switch_chord("IA"), desc="+AI & Assistants..."),
        Key([], "n", make_switch_chord("NAV"), desc="+Navigation & Web..."),
        Key([], "f", make_switch_chord("Frames"), desc="+Frames (Windows)..."),
        Key([], "e", make_switch_chord("Workspaces"), desc="+Workspaces..."),
        Key([], "d", make_switch_chord("Resize"), desc="+Resize (Dims)..."),
        Key([], "m", make_switch_chord("Media"), desc="+Media Player..."),
    ], name="Hub"),

    # Frames (ALT + F) -> Unified Window Management
    KeyChord(["mod1"], "f", [
        Key([], "f", lazy.window.toggle_fullscreen(), desc="Toggle Fullscreen"),
        Key([], "t", lazy.window.toggle_floating(), desc="Toggle Floating"),
        Key([], "s", lazy.layout.toggle_split(), desc="Toggle Split"),
        Key([], "n", lazy.layout.normalize(), desc="Normalize Sizes"),
        Key([], "m", lazy.next_layout(), desc="Cycle Layout"),
        Key([], "w", lazy.window.kill(), desc="Close Window"),
    ], name="Frames"),

    # System & Hardware (ALT + S)
    KeyChord(["mod1"], "s", [
        Key([], "f", lazy.spawn(terminal + " -e ranger"), desc="TUI File Browser"),
        Key(["shift"], "f", lazy.spawn("pcmanfm"), desc="GUI File Browser"),
        Key([], "l", lazy.spawn("localsend"), desc="LocalSend (LAN Share)"),
        Key([], "m", lazy.spawn(terminal + " -e btop"), desc="Monitor (Btop)"),
        Key([], "space", lazy.spawn("rofi -show drun"), desc="App Launcher"),
        Key([], "c", lazy.spawn(os.path.expanduser("~/Scripts/video_making/camera_activation.sh")), desc="Toggle Camera"),
        Key([], "r", lazy.spawn(os.path.expanduser("~/Scripts/video_making/video_start0.sh")), desc="Record Video"),
        Key(["shift"], "r", lazy.spawn(os.path.expanduser("~/Scripts/video_making/video_start0.sh")), desc="Record + Camera"),
        Key([], "d", lazy.spawn("arandr"), desc="Display Layout (ARandR)"),
        Key(["shift"], "v", lazy.spawn("pavucontrol"), desc="Audio Mixer (GUI)"),
        Key([], "q", lazy.spawn("shutdown now"), desc="Shutdown System"),
    ], name="System"),

    # Programming & Dev (ALT + P)
    KeyChord(["mod1"], "p", [
        Key([], "e", lazy.spawn(code_editor), desc="Code Editor (Zed)"),
        Key([], "v", lazy.spawn(terminal + " -e " + text_editor), desc="Neovim Editor"),
        Key([], "t", lazy.spawn(terminal), desc="Pure Terminal"),
        Key([], "i", lazy.spawn(terminal + " -e ipython"), desc="IPython Shell"),
        Key([], "j", lazy.spawn(terminal + " -e jupyter-lab"), desc="Jupyter Lab"),
        Key([], "s", lazy.spawn("sqlitebrowser"), desc="SQLite Browser GUI"),
        Key([], "g", lazy.spawn(terminal + " -e lazygit"), desc="Lazygit"),
    ], name="Programming"),

    # Office & Documents (ALT + O)
    KeyChord(["mod1"], "o", [
        Key([], "n", lazy.spawn("obsidian"), desc="Notes (Obsidian)"),
        Key([], "o", lazy.spawn("onlyoffice-desktopeditors"), desc="Office Suite"),
        Key(["shift"], "s", lazy.spawn(terminal + " -e sc-im"), desc="SC-IM Spreadsheet (TUI)"),
        Key([], "c", lazy.spawn(terminal + " -e qalc"), desc="Calculator (Qalculate)"),
        Key([], "p", lazy.spawn("okular"), desc="PDF Reader (Okular)"),
        Key([], "z", lazy.spawn("zathura"), desc="Zathura"),
    ], name="Office"),

    # Resize (ALT + D) -> Modal persistent dimensions
    KeyChord(["mod1"], "d", [
        Key([], "h", lazy.layout.grow_left(), desc="Grow Left"),
        Key([], "l", lazy.layout.grow_right(), desc="Grow Right"),
        Key([], "j", lazy.layout.grow_down(), desc="Grow Down"),
        Key([], "k", lazy.layout.grow_up(), desc="Grow Up"),
        Key([], "n", lazy.layout.normalize(), desc="Reset Sizes"),
    ], name="Resize", mode=True),
]

# Initialize Which-Key HUD overlay (hooks enter_chord / leave_chord automatically)
whichkey_hud = setup_whichkey(colors, fontsize=14)
