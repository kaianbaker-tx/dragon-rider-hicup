# Dragon Rider Hicup

Kaian is 10. He reads everything you write, and he talks to you with
voice-to-text, so his spelling will be off - work out what he meant and
keep going instead of asking him to spell it again.

## How to talk to him

- Short sentences. One idea at a time.
- Say what you are about to do, then do it, then say what changed.
- When something breaks, say what broke in plain words and fix it.
- Never dump a wall of code at him. Explain the one line that matters.
- `game-save "what changed"` after anything that works, using HIS words.
  `game-undo` goes back to an earlier save. Nothing is ever lost.

## This game

- Godot 4.7, single web export, published to GitHub Pages.
- Art and sounds come from the Kenney library. Use `kenney-find <word>`
  to search it and `kenney-find <word> --grab` to copy files into
  `assets/kenney/`. Never hand-copy from ~/GameAssets.
- `share-game` exports the web build into `docs/` and pushes. That is the
  only way the site updates.
- Keep `variant/thread_support=false` in export_presets.cfg or the web
  build shows a black screen on GitHub Pages.

## Rules

- Commit small and often, with messages he could read back later.
- Never commit anything from `shots/` bigger than a screenshot.
- If he asks for something that would take hours, build the smallest
  version that works first and show him that.
