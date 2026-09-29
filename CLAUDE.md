# Launch film kit

A method for making launch motion films for real companies with Claude Code. `README.md` has the step-by-step; this
file holds the rules. "The director" is the person who reviews the film and gives notes.

## When someone asks how to use this repo

Walk them through making a film, one step at a time, and do the steps they want done:

1. **Run folder:** `scripts/new-run.sh <name>` makes `~/runs/<name>-01/`. Add a sound library folder as a second
   argument if they have one.
2. **Brand kit:** build `brand/` with them from `templates/brand-kit.md`. Capture the company's pages and text, quote
   its claims word for word, copy colours and type from the live CSS, and collect the logo, fonts and product
   screenshots. Downloads need their OK.
3. **Build session:** give them the launch command and the prompt from `prompts/launch-film.md`, with their details
   filled in. The film is built by that fresh session, not this one (rule 6).
4. **Stops:** at the pitch and at the rough cut, help them read the frames or the cut and put their notes in their
   own words (rule 8).
5. **Compare:** when the final is in, run `scripts/compare.py` against a reference film they rate and report the
   numbers plainly (rule 5).

If they want to change the rules, edit this file and `prompts/launch-film.md` together, so the rules the build session
gets stay in step with these.

## Rules for every film

1. **Everything is a motion piece.** Motion graphics come first: big kinetic type, one idea at a time. A film can show
   the product and still be a motion piece, but never brief or storyboard it as a product demo. When a film shows the
   product, it shows a full mockup of a proper platform, designed for the film rather than copied from screenshots.
   The mockup shows only features the product really has, and the camera moves through it as if through an actual
   product. No static browser frames.
2. **Readable, and never a slideshow.** There's no set length. A film is slow enough to read, but the motion carries
   the timing: it must never look like a PowerPoint. The music drives from the first second.
3. **Sound is the build session's call.** It makes the music and effects its own way. If the director has a sound
   library, it goes in the run folder's `sfx/` as sounds they like, not a limit. Sounds the director doesn't want are
   named in the prompt.
4. **Claims.** Every claim on screen traces to the run's `brand/`: no invented stats, customers or real people.
5. **Five stages.** The director approves the pitch and the rough cut before anything is polished.
   1. **Prep** (a working session, or you): research the company and build `brand/` from `templates/brand-kit.md`.
      Screenshots show what the product does; they're reference for the mockup, not layouts to copy.
   2. **Pitch** (the build session): two or three routes, each shown as a few frames rendered in the film's real
      look, with a line on the story, a line on the sound, and questions for the director. They pick one.
   3. **Storyboard and rough cut:** a frame for every beat with its words and timing, and a rough cut at real speed
      with temporary sound, rendered quickly without motion blur. Pace, readability and tone are settled here, not at
      the end.
   4. **Build:** the final film, with motion blur and the full sound.
   5. **Compare:** before the director watches, put the film next to a reference film they rate, using
      `scripts/compare.py`: contact sheets, pace and loudness over time. If it's weaker, it isn't done.
6. **One fresh build session per film.** It storyboards and builds the film:
   - in its own run folder, containing only `brand/` (and `sfx/`);
   - started with `--safe-mode` and maximum effort;
   - given the prompt in `prompts/launch-film.md`.

   Never build a film at the end of a long working session; craft drops as a session's context fills. A big change
   starts a fresh session from the last good cut. A `--safe-mode` session loads no CLAUDE.md and no skills, so rules
   1–4 and 7 travel in the prompt.
7. **Custom motion.** The build session writes its own engine and every move itself: no Remotion or animation
   libraries. Data such as map outlines is fine.
8. **Notes carry the director's words.** Notes to a build session quote the director and change only what they name;
   everything else stays as it is. Anything the working session wants to add goes to the director first, marked as its
   own.

## Why these rules

Each one comes from a film that went wrong:

- A film storyboarded as a product walkthrough came out slow, with long holds on rebuilt app screens and music that
  barely started.
- A fixed 30 seconds made a good film too fast to read.
- A reading-time formula applied to every label turned the product section into a slideshow.
- Screens copied from screenshots looked flat; a designed mockup of the platform didn't.
- Widening "no marimba" into a ban on anything bell-like left a handful of sounds repeating.
- Notes that added the reviewer's own ideas changed parts nobody had asked to change.
- A revision built deep into a long session regressed.

## Working rules

- Downloads, pushes and anything other people will see need the director's OK first.
