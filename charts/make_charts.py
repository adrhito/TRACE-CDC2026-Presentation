# AI-assisted: written with Claude Code (Anthropic). See docs/AI_USAGE.md.
# Renders the deck's data charts with matplotlib. Numbers are copied from the TRACE repo:
#   backtest  -> docs/METHODS_EXPLAINED.md section 3 (backend/trace_backend/model/train.py backtest)
#   reflex    -> backend/trace_backend/reflex/results/eval_v0.2.json, real_news_v1.json, onnx_parity.json
# Run: python charts/make_charts.py  (writes assets/charts/*.png)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "charts")
INK, MID, FAINT, LINE = "#1F1C18", "#575047", "#B8B0A5", "#DDD7CE"
ACCENT, VIOLET = "#C5563A", "#8B5FA8"
plt.rcParams.update({
    "font.family": ["Consolas", "DejaVu Sans Mono"], "font.size": 13,
    "text.color": INK, "axes.labelcolor": MID, "xtick.color": MID, "ytick.color": MID,
    "axes.edgecolor": LINE, "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "figure.dpi": 200, "savefig.transparent": True,
})


def label_bars(ax, bars, fmt):
    for b in bars:
        v = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, v + 0.015, fmt(v), ha="center", va="bottom",
                fontsize=11, color=INK)


def grouped(ax, groups, series, fmt, ymax=1.0):
    n = len(series)
    w = 0.8 / n
    for i, (name, vals, color) in enumerate(series):
        xs = [g + (i - (n - 1) / 2) * w for g in range(len(groups))]
        label_bars(ax, ax.bar(xs, vals, w * 0.92, color=color, label=name), fmt)
    ax.set_xticks(range(len(groups)), groups)
    ax.set_ylim(0, ymax)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0, labelsize=13, labelcolor=INK)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=n, fontsize=12)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# 1. Route-forecast backtest: trained on target years <= 2019, tested blind on 2020-2024
fig, ax = plt.subplots(figsize=(8.6, 4.0))
grouped(ax, ["AUC\nactive next year?", "Spearman\nvolume ranking", "Precision@20\ngrowth calls"], [
    ("LightGBM hurdle (ours)", [0.881, 0.578, 0.48], ACCENT),
    ("Same as last year", [0.815, 0.477, 0.42], FAINT),
    ("PPML gravity", [0.583, 0.378, 0.34], "#D9D2C7"),
], lambda v: f"{v:.2f}")
save(fig, "backtest.png")

# 2. Reflex training: untuned NLI backbone vs Reflex v0.2 after Colab T4 fine-tune
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.8), gridspec_kw={"width_ratios": [1, 1]})
for ax, title, vals, fmt, ymax in [
    (a1, "Held-out accuracy  (higher is better)", [0.481, 0.902], lambda v: f"{v*100:.1f}%", 1.1),
    (a2, "Calibration error, ECE  (lower is better)", [0.206, 0.020], lambda v: f"{v:.3f}", 0.25),
]:
    bars = ax.bar(["Untuned\nbackbone", "Reflex v0.2"], vals, 0.55, color=[FAINT, ACCENT])
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + ymax * 0.015, fmt(b.get_height()),
                ha="center", va="bottom", fontsize=13, color=INK)
    ax.set_ylim(0, ymax)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0, labelsize=12, labelcolor=INK)
    ax.set_title(title, fontsize=12, color=MID, pad=10)
save(fig, "reflex_training.png")

# 3. Real-news benchmark: 92 published headlines, labelled by hand, never used for tuning
fields = ["is_event", "event type", "drug", "origin", "destination", "size"]
fig, ax = plt.subplots(figsize=(10.5, 4.0))
grouped(ax, fields, [
    ("Keyword baseline", [0.815, 0.739, 0.739, 0.891, 0.543, 0.429], FAINT),
    ("Reflex v0.2", [0.870, 0.880, 0.924, 0.924, 0.804, 0.786], VIOLET),
    ("Reflex + grounding (shipped)", [0.913, 0.880, 0.978, 0.957, 0.848, 0.929], ACCENT),
], lambda v: f"{v*100:.0f}", ymax=1.08)
save(fig, "reflex_real_news.png")

# 4. Grounding guardrails: what reaches the Live Wire that should not
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.4))
for ax, title, vals, fmt, ymax in [
    (a1, "Invented countries/drugs", [19 / 88, 5 / 102, 0.0], lambda v: f"{v*100:.1f}%", 0.26),
    (a2, "False events on non-events", [0.154, 0.128, 0.051], lambda v: f"{v*100:.1f}%", 0.19),
]:
    bars = ax.bar(["Keyword", "Reflex", "Reflex +\ngrounding"], vals, 0.6, color=[FAINT, VIOLET, ACCENT])
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + ymax * 0.02, fmt(b.get_height()),
                ha="center", va="bottom", fontsize=12, color=INK)
    ax.set_ylim(0, ymax)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0, labelsize=11, labelcolor=INK)
    ax.set_title(title, fontsize=12, color=MID, pad=10)
save(fig, "reflex_grounding.png")
print("ok")
