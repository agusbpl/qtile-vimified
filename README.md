# ⚡ qtile-vimified

<p align="center">
  <strong>Vim-style modal submaps, HJKL window navigation, and real-time Which-Key HUD for Qtile on Arch Linux.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Arch%20Linux%20%2F%20Qtile-blue?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/badge/UI-Qtile%20Native%20Popup-purple?style=flat-square" alt="Qtile Popup">
  <img src="https://img.shields.io/badge/Core-Python%203.14-yellow?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/Performance-Zero%20Latency%20(%3C1ms)-brightgreen?style=flat-square" alt="Performance">
  <img src="https://img.shields.io/badge/License-MIT-orange?style=flat-square" alt="License">
</p>

---

## 💡 Overview

**`qtile-vimified`** brings the full modal workflow, directional window management, and real-time **Which-Key HUD** experience from [`omarchy-vimified`](https://github.com/agusbpl/omarchy-vimified) to **Qtile on Arch Linux**.

Instead of memorizing dozens of complex multi-key combinations or relying on mouse navigation:
1. **Navigate Windows with `HJKL`:** Move focus and swap tiling windows intuitively using familiar Vim directional keys (`SUPER + H/J/K/L`).
2. **Modal Submaps (KeyChords):** Access system functions, developer tools, AI workflows, university platforms, and documents through cleanly categorized modes triggered by `ALT + <key>`.
3. **The Master Hub (`ALT + ENTER`):** A centralized springboard ("El Alt de los Alts") providing immediate visual access to every submap on your machine.
4. **Native Which-Key HUD Overlay:** An instant, zero-latency heads-up display rendered in the top-right corner. It dynamically auto-sizes to content, uses high-contrast typography, adapts to your active desktop palette (`theme.py`), and uses Qtile internal windows (never intercepts clicks or steals focus).

---

## 🖥️ Visual Architecture

```text
               ┌──────────────────────────────┐
               │        Qtile Manager         │
               │   (config.py / KeyChords)    │
               └──────────────┬───────────────┘
                              │
                    ALT + Key │ Super + HJKL
                              ▼
     ┌────────────────────────────────────────────────────────┐
     │                 qtile-vimified (Core)                  │
     │  • HJKL Directional Navigation & Window Swapping       │
     │  • Master Hub Springboard (ALT + ENTER)                │
     │  • enter_chord / leave_chord Lifecycle Hooks           │
     └─────────────────────────┬──────────────────────────────┘
                               │ Event hook payload
                               ▼
     ┌────────────────────────────────────────────────────────┐
     │          Which-Key HUD (whichkey.py / Popup)           │
     │  • Pure Terminal Aesthetic (Square corners, 1px border)│
     │  • Dynamic 1- or 2-Column Responsive Card Grid         │
     │  • Zero-latency Pango Markup Renderer                  │
     │  • Non-focus-stealing Internal X11 Window              │
     └────────────────────────────────────────────────────────┘
```

### HUD Preview (Terminal / Which-Key Aesthetic)

```text
 ┌─ :: SYSTEM & HARDWARE :: ────────────────── [ALT + S] ──┐
 │                                                         │
 │   [ f ] TUI File Browser      [ m ] Monitor (Btop)      │
 │   [ F ] GUI File Browser      [ e ] Edit Qtile Config   │
 │   [ n ] Network Manager       [ b ] Bluetooth Menu      │
 │   [ c ] Activate Camera       [ r ] Record Video Script │
 │   [ s ] Screenshot            [ q ] Shutdown System     │
 │   [ v ] +Volume Control...    [ l ] +Brightness...      │
 ├─────────────────────────────────────────────────────────┤
 │   [ ESC ] exit                                          │
 └─────────────────────────────────────────────────────────┘
```

---

## ⌨️ Default Submaps & Keybindings

### 1. Vim Directional Window Management

| Shortcut | Action | Description |
| :--- | :--- | :--- |
| `SUPER + H` | **Focus Left** | Move focus to the window on the left |
| `SUPER + J` | **Focus Down** | Move focus to the window below |
| `SUPER + K` | **Focus Up** | Move focus to the window above |
| `SUPER + L` | **Focus Right** | Move focus to the window on the right |
| `SUPER + SHIFT + H` | **Swap Left** | Swap active window with the one on the left |
| `SUPER + SHIFT + J` | **Swap Down** | Swap active window with the one below |
| `SUPER + SHIFT + K` | **Swap Up** | Swap active window with the one above |
| `SUPER + SHIFT + L` | **Swap Right** | Swap active window with the one on the right |
| `SUPER + CTRL + H/J/K/L` | **Grow Window** | Grow active window dimensions |

---

### 2. The Master Hub & Submaps

Press `ALT + <Key>` to enter a modal submap. The Which-Key HUD will immediately appear in the top-right corner. Press any listed key to execute its action, or press `Escape` to exit back to normal mode.

| Trigger | Submap Name | Content & Actions |
| :--- | :--- | :--- |
| `ALT + ENTER` | **⚡ Master Hub** | Springboard linking directly into all submaps (`s`, `p`, `o`, `l`, `i`, `u`, `n`, `f`, `e`, `d`, `m`, `t`) |
| `ALT + F` | **🖥️ Frames** | **Unified Window Management:** Fullscreen (`f`), Float/Tile (`t`), Split (`s`), Sticky (`p`), Normalize (`n`), Next Layout (`m`), Close (`w`), Toggle Bar (`b`) |
| `ALT + E` | **🗂️ Workspaces** | **Workspace Jump & Window Move:** Jump to 1..10, Move window to 1..10 (`SHIFT + 1..10`), Next workspace (`TAB`) |
| `ALT + D` | **📐 Resize / Dimensions** | Modal micro-adjustments (**D**imensions: `h`/`l` width, `j`/`k` height, `n` normalize) |
| `ALT + S` | **⚙️ System & Hardware** | Ranger (`f`), PCManFM (`F`), Btop (`m`), Edit Qtile (`e`), Network (`n`), Bluetooth (`b`), Camera (`c`), Record video (`r`), Screenshot (`s`), Shutdown (`q`), Volume (`v`), Brightness (`b`/`l`) |
| `ALT + P` | **💻 Programming & Dev** | Antigravity AI (`a`), Zed (`e`), Terminal (`t`), JupyterLab (`j`), LazyGit (`g`), GitHub Web (`G`), Google Colab (`c`), Discord (`d`) |
| `ALT + L` | **📚 Learning & Data** | Python, Pandas, Polars, PyTorch, Scikit-Learn, Hugging Face, SQL, PostgreSQL, Airflow, Metabase, local cheatsheets |
| `ALT + O` | **📝 Office & Documents** | Obsidian notes (`n`), OnlyOffice (`o`), Docs (`d`), Sheets (`s`), Okular/Zathura PDF (`p`/`z`), DeepL (`t`), WordReference (`w`), Wikipedia (`W`), Excalidraw (`e`) |
| `ALT + I` | **🤖 AI & Assistants** | Brain (`b`), Gemini (`a`), Claude (`c`), ChatGPT (`g`), Perplexity (`p`), DeepSeek (`d`), Mistral (`m`), Kimi (`k`), NotebookLM (`n`), OpenCode (`o`), Grok (`x`), Phind (`f`) |
| `ALT + U` | **🎓 UNLP Universidad** | AU24 (`a`), LINTI (`l`), IDEAS (`i`), mfi - info (`m`) |
| `ALT + N` | **🌐 Navigation & Web** | Browser (`b`), YouTube (`y`), YouTube Studio (`s`), Telegram (`t`), WhatsApp Web (`w`), Gmail (`m`) |
| `ALT + M` | **🎵 Media Player** | Play/Pause (`Space`), Next track (`l`), Previous track (`h`), Volume (`k`/`j`), Mute (`m`), cmus Player (`c`) |
| `ALT + T` | **🗣️ Text to Speech** | Piper TTS Spanish (`p`), Piper TTS English (`e`) |

---

## 🚀 Installation & Setup

1. Copy `whichkey.py` to your Qtile configuration directory:
   ```bash
   cp whichkey.py ~/.config/qtile/whichkey.py
   ```

2. In your `~/.config/qtile/config.py`:
   ```python
   from whichkey import setup_whichkey, make_switch_chord

   # (Define your KeyChords as usual, with name="...")

   # At the end of config.py:
   setup_whichkey(colors)
   ```

3. Reload Qtile (`SUPER + CTRL + R` or `qtile cmd-obj -o cmd -f reload_config`).

---

## 🧬 Principles & Design Rationale

- **Anti-Tofu (Rule A):** Zero raw Unicode emojis in HUD headers and labels. Clean ASCII and styled badges ensure identical rendering on any Linux installation without missing glyph blocks (`▯`).
- **Anti-Crowding & No Clipping (Rule B):** Dynamic mathematical calculation of text width and height using Pango text layout. The HUD automatically scales its dimensions and right-aligns beneath the top bar.
- **Zero Latency:** Implemented directly via Qtile's internal `Popup` drawer, consuming less than 1ms per render and zero background CPU/RAM overhead.
