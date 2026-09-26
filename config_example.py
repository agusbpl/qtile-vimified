"""
config_example.py — Minimal example integrating qtile-vimified into your Qtile configuration.
"""

from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy
from whichkey import setup_whichkey, make_switch_chord

# 1. Define your desktop color palette (or import from theme.py)
colors = {
    "bg": "#130626",
    "bg_alt": "#2d174d",
    "fg": "#e1d5f5",
    "selected": "#b62795",
    "active": "#e542a3",
    "urgent": "#ff8ba4",
}

# 2. Add your Vim modal submaps (KeyChords)
keys = [
    # Master Hub (ALT + ENTER) -> Springboard to any submap
    KeyChord(["mod1"], "Return", [
        Key([], "s", make_switch_chord("System"), desc="+System & Hardware..."),
        Key([], "p", make_switch_chord("Programming"), desc="+Programming & Dev..."),
        Key([], "o", make_switch_chord("Office"), desc="+Office & Documents..."),
        Key([], "l", make_switch_chord("Learning"), desc="+Learning & Data..."),
        Key([], "i", make_switch_chord("IA"), desc="+AI & Assistants..."),
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

    # Resize (ALT + D) -> Modal persistent dimensions
    KeyChord(["mod1"], "d", [
        Key([], "h", lazy.layout.grow_left(), desc="Grow Left"),
        Key([], "l", lazy.layout.grow_right(), desc="Grow Right"),
        Key([], "j", lazy.layout.grow_down(), desc="Grow Down"),
        Key([], "k", lazy.layout.grow_up(), desc="Grow Up"),
        Key([], "n", lazy.layout.normalize(), desc="Reset Sizes"),
    ], name="Resize", mode=True),
]

# 3. Initialize Which-Key HUD overlay (hooks enter_chord / leave_chord automatically)
whichkey_hud = setup_whichkey(colors, fontsize=14)
