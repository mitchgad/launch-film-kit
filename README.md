# Launch film kit

A method for making launch motion films for real companies with Claude Code. Each film is planned with you, then
built from a brand kit by a fresh Claude session that writes its own engine and every move. This repo holds the rules,
the prompt, the templates and two scripts; each film lives in its own folder outside it.

## What you need

- [Claude Code](https://claude.com/claude-code), with the most capable model you have available.
- Node 20 or later, ffmpeg, and Python 3 with numpy and Pillow. The build session installs anything else its film
  needs, such as Playwright's Chromium for rendering.

## Making a film

1. **Set up a run folder.**

   ```bash
   scripts/new-run.sh acme
   ```

   This makes `~/runs/acme-01/` with an empty `brand/` folder. To include a sound library, pass its folder as a second
   argument; it's copied in as `sfx/`.
2. **Fill in the brand kit.** Follow `brand/README.md`: page captures and text, the company's claims word for word,
   colours and type from the live CSS, logo, fonts and product screenshots. Everything the film says has to come from
   here.
3. **Start a fresh build session** in the run folder:

   ```bash
   cd ~/runs/acme-01 && claude --safe-mode --effort max --permission-mode auto
   ```

   Paste the prompt from `prompts/launch-film.md` with your company's details filled in. `--safe-mode` keeps your own
   CLAUDE.md, skills and plugins out of the session, so the prompt carries the rules.
4. **Pick a route.** The session pitches two or three routes as rendered frames and asks its questions, then stops.
   Answer in its terminal.
5. **Approve the rough cut.** It stops again with a storyboard and a rough cut at real speed. This is the moment to
   fix pace, readability and tone.
6. **Get the final** in `out/`, with motion blur and the full sound.
7. **Compare it with a film you rate** before you call it done:

   ```bash
   python3 scripts/compare.py ~/runs/acme-01/out/film.mp4 --ref reference.mp4
   ```

   It prints pace and loudness for both films side by side, and writes a contact sheet of each to `compare/`.

## Giving notes

Quote what you want changed and name only that. The build session changes what it's asked to, so any extra idea in
the notes becomes a change. Type "Apply these notes:" before pasting them. For a big change, start a fresh session
from the last good cut instead of piling onto a long one.

## Files

| Path | What it is |
|---|---|
| `CLAUDE.md` | The rules for every film, and the failures behind them |
| `prompts/launch-film.md` | The build session's prompt |
| `templates/brand-kit.md` | What goes in a run's `brand/` folder |
| `scripts/new-run.sh` | Makes a run folder |
| `scripts/compare.py` | Measures a film against a reference: pace, loudness over time and contact sheets |
