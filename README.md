<!-- AI-assisted: written with ChatGPT (OpenAI). See docs/AI_USAGE.md. -->
# TRACE · Carolina Data Challenge 2026

The submitted TRACE pitch deck, published as a self-contained static presentation. It runs in a modern browser and does not need a server-side application or API.

## View

**Slides: [rattled.me/TRACE-CDC2026-Presentation](http://rattled.me/TRACE-CDC2026-Presentation/)**

That is the GitHub Pages site for this repository. You can also open `index.html` directly. Add `#N` to the URL to open slide N (for example `#6`). Google Fonts are optional; without a network connection the deck uses local fallback fonts.

## Controls

- `→`, `Space`, or click the right side: next slide (or the next click build, such as "They moved." on slide 3)
- `←` or click the left side: previous slide
- `N`: speaker cues (presenter screen only)
- `T`: rehearsal timer and pace bar
- `G`: slide overview
- `F`: fullscreen
- `Esc`: close an overlay

The presentation runs 5:00 or less (about 4:30 of timed slides), split into three speakers: the Problem (slides 2–7), the Data (8–10) and the Technical Architecture (11–16: route forecast, Reflex trained on Colab, real-news grounding, ONNX export). Slide 17 onward is untimed **Q&A backup** for the fourth teammate. Charts are rendered with matplotlib from the TRACE results files; regenerate them with `python charts/make_charts.py`.
