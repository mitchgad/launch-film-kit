# The build session's prompt

Paste this as the first message of a fresh build session (CLAUDE.md, rules 5 and 6). A `--safe-mode` session loads
no CLAUDE.md and no skills, so the film rules travel in the prompt.

## Start the session

```bash
cd ~/runs/<name>-NN && claude --safe-mode --effort max --permission-mode auto
```

- Add `--model <id>` to pick the model; use the most capable one you have.
- On a Mac, `caffeinate -is` in front of `claude` stops the machine sleeping during long renders.
- `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in front keeps the session from saving memories between films.

## The prompt

Fill in BRAND and URL. Keep or delete the bracketed parts, then remove the brackets.

```text
Make a motion graphics launch film for BRAND (URL). Their brand, product and claims are in ./brand; use only claims that appear there. [You can use their footage in ./brand/assets/FILE if it helps.]

The rules:
- It's a motion piece from the first frame to the last, even where it shows the product. When it shows the product, build a full mockup of a proper platform, designed for the film rather than copied from the screenshots, showing only features the product really has, and move through it as if through an actual product. No static browser frames.
- There's no set length. Make it slow enough to read, but let the motion carry the timing: it must never look like a PowerPoint. The music drives from the first second.
- Do the sound your own way. [My sound library is in ./sfx if it helps. I like SOUNDS YOU LIKE.] [No SOUNDS YOU DON'T WANT.]
- Write your own engine and every move yourself: no Remotion or animation libraries.
- 1920×1080, 60 fps.

Work in three stages, and stop after each of the first two so I can answer:
1. Pitch two or three routes. Show each as three or four frames rendered in the film's real look, with a line on the story and a line on the sound, and ask me what you need to know. Put it in ./pitch/.
2. When I've picked one, make a storyboard with a frame for every beat, its words and its timing, and a rough cut at real speed with temporary sound, rendered quickly without motion blur. Put it in ./storyboard/.
3. When I approve, build the final film with motion blur and the full sound, and put it in ./out/.

Go all out.
```

## During the run

- **At each stop:** look at the frames or the cut, and answer in the session's terminal.
- **Notes:** quote what you want changed and name only that (CLAUDE.md, rule 8). Type a lead-in such as "Apply these
  notes:" before pasting them, so the session reads them as an instruction.
- **Big changes:** start a fresh session from the last good cut rather than piling onto a long one.

## Before you call it done

Run `scripts/compare.py` against a reference film you rate (CLAUDE.md, rule 5, stage 5).
