# Output Formats — Diagram, Interactive HTML, Explainer Video

Read this when the user asks for one of these formats, or when the subject has
3 or more interacting parts and a diagram would obviously beat prose. STE text
remains the default; every format below costs more to make than the one before
it. All text inside any format — labels, captions, page copy, narration —
follows the same STE rules and guard rails from SKILL.md.

Contents:
- Which format to use
- Diagram
- Interactive HTML page
- Explainer video

## Which format to use

- The user names a format → use that format.
- No format named → use STE text. Add a diagram only when the subject has 3+
  interacting parts and a diagram would obviously beat prose.
- HTML page or video → only when the user asks. A one-line offer at the end of
  a text answer is allowed.

## Diagram

- Use Mermaid by default: GitHub, many editors, and many chat tools render it.
  Use SVG only when the layout must be free-form (geometry, memory layout).
- One idea per diagram. More than ~12 boxes → split into two diagrams.
- Name things exactly as the text names them — the synonym-rotation rule
  applies across text and diagram.
- Labels: 1 to 4 words. Every arrow gets a verb: "sends", "reads", "retries".
- Put one sentence below the diagram telling the reader where to start.

## Interactive HTML page

- Keep the page's HTML, CSS, and JavaScript in one file.
- Use a CDN library only when the user accepts an external network dependency.
- The reader does something, not only reads: step through a process, move a
  slider, toggle two states, or see the result of an input.
- Main idea at the top; details below.
- Must work on a phone screen, and in light mode and dark mode.
- No real data, keys, or personal information unless the user supplies them
  for this purpose.

## Explainer video

Build a 3Blue1Brown-style video with Manim:

1. Write a script first. Divide it into scenes. For each scene, write the
   narration in STE and describe the animation.
2. Write the Manim code: one class per scene, each scene about 10–40 seconds.
3. Narration audio:
   - If the user provides a text-to-speech API key, use it, reading the key
     from an environment variable — never write it into a file.
   - Otherwise use a free local TTS tool and tell the user which one.
4. Pair each audio clip with its scene; make each scene as long as its audio.
5. Render and join the scenes (for example with `ffmpeg`).
6. Give the user the video path and the command that re-renders it.

Render at low quality first (`manim -ql`) to catch errors fast; render high
quality only at the end.
