import asyncio
import re
from xml.sax.saxutils import escape
from libqtile import hook
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.popup import Popup

# ==============================================================================
# SUBMAP METADATA & TITLES
# Strict compliance with Anti-Tofu (Rule A) & Anti-Crowding (Rule B)
# ==============================================================================
SUBMAP_META = {
    "Hub": {
        "title": "MASTER HUB",
        "tag": "[ALT + ENTER]",
        "badge": "[HUB]",
    },
    "System": {
        "title": "SYSTEM & HARDWARE",
        "tag": "[ALT + S]",
        "badge": "[SYS]",
    },
    "Programming": {
        "title": "PROGRAMMING & DEV",
        "tag": "[ALT + P]",
        "badge": "[DEV]",
    },
    "Learning": {
        "title": "LEARNING & DATA SCIENCE",
        "tag": "[ALT + L]",
        "badge": "[DOC]",
    },
    "Office": {
        "title": "OFFICE & DOCUMENTS",
        "tag": "[ALT + O]",
        "badge": "[OFF]",
    },
    "IA": {
        "title": "AI & ASSISTANTS",
        "tag": "[ALT + I]",
        "badge": "[ AI]",
    },
    "UNLP": {
        "title": "UNLP UNIVERSIDAD",
        "tag": "[ALT + U]",
        "badge": "[UNL]",
    },
    "NAV": {
        "title": "NAVIGATION & WEB",
        "tag": "[ALT + N]",
        "badge": "[NAV]",
    },
    "Frames": {
        "title": "FRAMES & WINDOWS",
        "tag": "[ALT + F]",
        "badge": "[WIN]",
    },
    "Workspaces": {
        "title": "WORKSPACES",
        "tag": "[ALT + E]",
        "badge": "[WKS]",
    },
    "Resize": {
        "title": "RESIZE / DIMENSIONS",
        "tag": "[ALT + D]",
        "badge": "[DIM]",
    },
    "Media": {
        "title": "MEDIA PLAYER",
        "tag": "[ALT + M]",
        "badge": "[MED]",
    },
    "TTS": {
        "title": "TEXT TO SPEECH",
        "tag": "[ALT + T]",
        "badge": "[TTS]",
    },
    "Volume": {
        "title": "VOLUME CONTROL",
        "tag": "[VOL]",
        "badge": "[VOL]",
    },
    "Brightness": {
        "title": "BRIGHTNESS CONTROL",
        "tag": "[BRI]",
        "badge": "[BRI]",
    },
}


def make_switch_chord(target_name):
    """Creates a lazy function that seamlessly switches from the active chord to target_name."""
    @lazy.function
    def _switch(qtile):
        try:
            qtile.ungrab_chord()
            for k in qtile.config.keys:
                if getattr(k, "name", "") == target_name:
                    qtile.grab_chord(k)
                    return
        except Exception as e:
            logger.warning(f"whichkey: failed switching to chord {target_name}: {e}")
    return _switch


def extract_entries(qtile, chord_name):
    """Extracts available keybindings and descriptions for the specified chord."""
    target_chord = None
    for k in qtile.config.keys:
        if getattr(k, "name", "") == chord_name:
            target_chord = k
            break
        if hasattr(k, "submappings"):
            for sub in k.submappings:
                if getattr(sub, "name", "") == chord_name:
                    target_chord = sub
                    break
            if target_chord:
                break

    if not target_chord or not hasattr(target_chord, "submappings"):
        return []

    entries = []
    for sub in target_chord.submappings:
        key_name = getattr(sub, "key", "")
        desc = getattr(sub, "desc", "")
        mods = getattr(sub, "modifiers", [])

        # Skip Escape key (standard chord exit)
        if key_name.lower() == "escape":
            continue

        # Format key label (Vim conventions: shift gives uppercase)
        if "shift" in mods:
            label = key_name.upper() if len(key_name) == 1 else f"S-{key_name}"
        elif "control" in mods:
            label = f"C-{key_name}"
        elif "mod1" in mods:
            label = f"A-{key_name}"
        else:
            label = key_name

        if hasattr(sub, "submappings") and getattr(sub, "name", ""):
            desc = f"+{sub.name}..."

        if desc:
            entries.append((label, desc))

    return entries


def format_card_markup(chord_name, entries, colors):
    """Formats the submap entries into a high-contrast Pango markup Which-Key card."""
    meta = SUBMAP_META.get(chord_name, {
        "title": chord_name.upper(),
        "tag": f"[{chord_name.upper()}]",
        "badge": f"[{chord_name[:3].upper()}]"
    })

    title = escape(meta["title"])
    tag = escape(meta["tag"])

    accent = colors.get("active", "#e542a3")
    urgent = colors.get("urgent", "#ff8ba4")
    fg = colors.get("fg", "#e1d5f5")
    bg_alt = colors.get("bg_alt", "#2d174d")

    header = f"<b><span foreground='{accent}'>:: {title} ::</span></b>  <span foreground='{urgent}'>{tag}</span>"

    if not entries:
        lines = [f"<span foreground='{fg}'>Mode active. Press key or ESC.</span>"]
    else:
        is_two_col = len(entries) > 10
        lines = []

        if is_two_col:
            half = (len(entries) + 1) // 2
            col1 = entries[:half]
            col2 = entries[half:]

            max_d1 = max(len(d) for k, d in col1)
            max_k1 = max(len(k) for k, d in col1)
            max_k2 = max((len(k) for k, d in col2), default=1)

            for i in range(half):
                k1, d1 = col1[i]
                d1_esc = escape(d1)
                pad_space = " " * (max_d1 - len(d1))
                c1 = f"<span foreground='{urgent}'><b>[ {k1:^{max_k1}} ]</b></span> <span foreground='{fg}'>{d1_esc}{pad_space}</span>"
                if i < len(col2):
                    k2, d2 = col2[i]
                    d2_esc = escape(d2)
                    c2 = f"<span foreground='{urgent}'><b>[ {k2:^{max_k2}} ]</b></span> <span foreground='{fg}'>{d2_esc}</span>"
                    lines.append(f"{c1}   {c2}")
                else:
                    lines.append(c1)
        else:
            max_k = max((len(k) for k, d in entries), default=1)
            for k, d in entries:
                d_esc = escape(d)
                lines.append(f"<span foreground='{urgent}'><b>[ {k:^{max_k}} ]</b></span> <span foreground='{fg}'>{d_esc}</span>")

    # Header and footer borders
    max_line_len = max(len(re.sub(r"<[^>]+>", "", l)) for l in [header] + lines)
    sep_len = max(max_line_len, 34)
    sep = f"<span foreground='{bg_alt}'>{'─' * min(sep_len, 72)}</span>"
    footer = f"<span foreground='{urgent}'><b>[ ESC ]</b></span> <span foreground='{fg}'>exit</span>"

    return f"{header}\n{sep}\n" + "\n".join(lines) + f"\n{sep}\n{footer}"


class WhichKeyHUD:
    """Manages the zero-latency Which-Key HUD overlay inside Qtile."""

    def __init__(self, colors, qtile_instance=None, fontsize=14):
        self._qtile = qtile_instance
        self.colors = colors
        self.fontsize = fontsize
        self.popup = None
        self.timer_handle = None

    @property
    def qtile(self):
        if self._qtile is not None:
            return self._qtile
        from libqtile import qtile as active_qtile
        return active_qtile

    def show(self, chord_name):
        """Displays the Which-Key HUD card for the specified chord."""
        self.hide()

        try:
            q = self.qtile
            if not q:
                return

            entries = extract_entries(q, chord_name)
            markup_text = format_card_markup(chord_name, entries, self.colors)

            pad_x = 18
            pad_y = 14

            # Initial dummy popup to accurately measure text dimensions
            p = Popup(
                q,
                x=0,
                y=0,
                width=800,
                height=600,
                font="JetBrainsMono Nerd Font",
                fontsize=self.fontsize,
                background=self.colors.get("bg", "#130626"),
                border=self.colors.get("active", "#e542a3"),
                border_width=1,
                opacity=0.98,
                horizontal_padding=pad_x,
                vertical_padding=pad_y,
            )
            p.layout.text = markup_text
            p.clear()

            # Dynamic auto-sizing
            real_w = p.layout.width + (pad_x * 2)
            real_h = p.layout.height + (pad_y * 2)

            screen = q.current_screen
            screen_w = getattr(screen, "width", 1366)
            x = screen_w - real_w - 20
            y = 35  # Directly below the top bar (22px + margin)

            p.win.place(x, y, real_w, real_h, 1, self.colors.get("active", "#e542a3"), above=True)
            p.draw_text(pad_x, pad_y)
            p.unhide()
            p.draw()

            self.popup = p

            # Auto-dismiss timeout (15s) in case chord is abandoned
            loop = asyncio.get_event_loop()
            self.timer_handle = loop.call_later(15, self.hide)

        except Exception as e:
            logger.warning(f"whichkey: error showing HUD for {chord_name}: {e}")
            self.hide()

    def hide(self):
        """Hides and destroys the active Which-Key HUD card."""
        if self.timer_handle:
            try:
                self.timer_handle.cancel()
            except Exception:
                pass
            self.timer_handle = None

        if self.popup:
            try:
                self.popup.hide()
                self.popup.kill()
            except Exception:
                pass
            self.popup = None


def setup_whichkey(colors, qtile_instance=None, fontsize=14):
    """Installs the Which-Key hooks into Qtile."""
    hud = WhichKeyHUD(colors, qtile_instance, fontsize=fontsize)

    @hook.subscribe.enter_chord
    def on_enter_chord(chord_name):
        hud.show(chord_name)

    @hook.subscribe.leave_chord
    def on_leave_chord():
        hud.hide()

    @hook.subscribe.shutdown
    def on_shutdown():
        hud.hide()

    @hook.subscribe.restart
    def on_restart():
        hud.hide()

    logger.warning("whichkey: initialized successfully with Qtile hooks.")
    return hud
