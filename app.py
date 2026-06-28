"""
app.py — Lexical Complexity Profiler
A research tool for second language acquisition and educational technology.

Methodology:
  Word frequency data: wordfreq library (Speer, 2022), which draws on
  real-world corpora including Wikipedia, Reddit, OpenSubtitles, and news.

  CEFR-level approximation uses calibrated Zipf-frequency thresholds:
    A1: Zipf > 5.5  (core, most frequent vocabulary)
    A2: Zipf 4.5–5.5
    B1: Zipf 3.5–4.5
    B2: Zipf 2.5–3.5
    C1: Zipf 1.5–2.5
    C2: Zipf ≤ 1.5

  Two correction layers are applied:
  1. A1 overrides: concrete teaching vocabulary (cat, dog, etc.) that is
     genuinely A1 but under-scored by corpus frequency.
  2. Academic Word List (Coxhead, 2000): 570 headwords flagged as ≥ B2
     regardless of their raw frequency score.

  Known limitation: frequency-based CEFR mapping diverges from official
  CEFR word lists (e.g. Cambridge English Vocabulary Profile) for
  topic-specific vocabulary. Use results as a comparative and indicative
  measure, not a definitive level assignment.
"""

import re
import streamlit as st
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from wordfreq import zipf_frequency
from collections import Counter, defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io

from wordlists import AWL_WORDS, A1_OVERRIDES

# ── NLTK resource setup ─────────────────────────────────────────────────────

@st.cache_resource
def load_nlp():
    pkgs = [
        "punkt", "punkt_tab", "wordnet",
        "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng",
    ]
    for p in pkgs:
        nltk.download(p, quiet=True)
    return WordNetLemmatizer()

# ── CEFR mapping ─────────────────────────────────────────────────────────────

LEVELS        = ["A1", "A2", "B1", "B2", "C1", "C2", "Off-list"]
LEVEL_COLOURS = {
    "A1":       "#22c55e",
    "A2":       "#86efac",
    "B1":       "#facc15",
    "B2":       "#fb923c",
    "C1":       "#f87171",
    "C2":       "#dc2626",
    "Off-list": "#94a3b8",
}

def zipf_to_cefr(score: float) -> str:
    if score >= 5.5:  return "A1"
    if score >= 4.5:  return "A2"
    if score >= 3.5:  return "B1"
    if score >= 2.5:  return "B2"
    if score >= 1.5:  return "C1"
    if score >  0.0:  return "C2"
    return "Off-list"

def get_level(lemma: str, zipf: float) -> str:
    """Apply correction layers on top of the raw Zipf→CEFR mapping."""
    if lemma in A1_OVERRIDES:
        return "A1"
    if lemma in AWL_WORDS:
        raw = zipf_to_cefr(zipf)
        # AWL words are B2 minimum; only override upward
        if raw in ("A1", "A2", "B1"):
            return "B2"
        return raw
    return zipf_to_cefr(zipf)

def get_wordnet_pos(tag: str):
    if tag.startswith("J"): return wordnet.ADJ
    if tag.startswith("V"): return wordnet.VERB
    if tag.startswith("R"): return wordnet.ADV
    return wordnet.NOUN

CONTENT_TAGS = {
    "NN","NNS","VB","VBD","VBG","VBN","VBP","VBZ",
    "JJ","JJR","JJS","RB","RBR","RBS",
}
SKIP_TAGS = {"NNP","NNPS","CD","SYM","LS","POS",".",",",":","''","``","#","$"}

def is_analyzable(token: str, pos: str) -> bool:
    if pos in SKIP_TAGS:
        return False
    if not re.match(r"^[a-zA-Z](?:[a-zA-Z'-]*[a-zA-Z])?$", token):
        return False
    return len(token) >= 2

# ── Core analysis ─────────────────────────────────────────────────────────────

def analyze(text: str, lemmatizer) -> list[dict]:
    tokens  = nltk.word_tokenize(text)
    tagged  = nltk.pos_tag(tokens)
    results = []
    for token, pos in tagged:
        if not is_analyzable(token, pos):
            continue
        lemma = lemmatizer.lemmatize(token.lower(), get_wordnet_pos(pos))
        zipf  = zipf_frequency(lemma, "en")
        level = get_level(lemma, zipf)
        results.append({
            "token":      token,
            "lemma":      lemma,
            "pos":        pos,
            "zipf":       round(zipf, 2),
            "level":      level,
            "is_content": pos in CONTENT_TAGS,
        })
    return results

def compute_stats(records: list[dict]) -> dict:
    total = len(records)
    if not total:
        return {}

    lemmas        = [r["lemma"] for r in records]
    types         = len(set(lemmas))
    content_count = sum(1 for r in records if r["is_content"])

    # Corrected TTR (CTTR) — less biased against long texts
    cttr = types / (2 * total) ** 0.5

    level_counts = Counter(r["level"] for r in records)
    level_pcts   = {lv: round(level_counts.get(lv, 0) / total * 100, 1)
                    for lv in LEVELS}

    zipf_vals = [r["zipf"] for r in records if r["zipf"] > 0]
    mean_zipf = round(sum(zipf_vals) / len(zipf_vals), 2) if zipf_vals else 0

    return {
        "total_tokens":  total,
        "unique_types":  types,
        "cttr":          round(cttr, 3),
        "lex_density":   round(content_count / total * 100, 1),
        "level_counts":  level_counts,
        "level_pcts":    level_pcts,
        "mean_zipf":     mean_zipf,
    }

def group_by_level(records: list[dict]) -> dict[str, list]:
    """For each level, return unique lemmas sorted by frequency in text."""
    buckets: dict[str, Counter] = defaultdict(Counter)
    for r in records:
        buckets[r["level"]][r["lemma"]] += 1
    return {lv: buckets[lv].most_common() for lv in LEVELS}

# ── Chart ─────────────────────────────────────────────────────────────────────

def make_bar_chart(level_pcts: dict) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 3.2))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    labels = LEVELS
    values = [level_pcts.get(lv, 0) for lv in labels]
    colors = [LEVEL_COLOURS[lv] for lv in labels]

    bars = ax.bar(labels, values, color=colors, edgecolor="#1e293b",
                  linewidth=0.8, zorder=2)

    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val:.1f}%",
                ha="center", va="bottom",
                fontsize=9,
            )

    ax.set_ylabel("% of tokens", fontsize=10)
    ax.set_ylim(0, max(values) * 1.2 if any(values) else 10)
    ax.tick_params(labelsize=10)
    ax.spines[:].set_visible(False)
    ax.yaxis.grid(True, linewidth=0.6, zorder=0, alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_title("Vocabulary Level Distribution", fontsize=12, pad=10)

    return fig

# ── Streamlit UI ──────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="LexComplex",
        page_icon="📊",
        layout="wide",
    )

    # Only structural styles — no colour overrides so Streamlit's own
    # light/dark theme toggle works correctly.
    st.markdown("""
    <style>
    .section-header {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin: 24px 0 8px;
        opacity: 0.6;
    }
    .word-pill {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 99px;
        font-size: 12px;
        margin: 2px 3px;
        font-family: 'Courier New', monospace;
    }
    .note-box {
        border-left: 3px solid #6d28d9;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        opacity: 0.8;
        margin: 12px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── header ──
    st.markdown("## 📊 LexComplex")
    st.markdown(
        "<span style='font-size:14px;opacity:0.6;'>"
        "Vocabulary-level analysis for SLA research and materials development"
        "</span>",
        unsafe_allow_html=True,
    )

    lemmatizer = load_nlp()

    # ── sidebar: mode and options ──
    with st.sidebar:
        st.markdown("### ⚙️ Options")

        mode = st.radio(
            "Input mode",
            ["Single text", "Compare two texts"],
            help="Compare mode profiles both texts side by side.",
        )

        st.markdown("---")
        st.markdown("**Display options**")
        show_wordlists = st.checkbox("Show word lists per level", value=True)
        max_words_shown = st.slider(
            "Max words shown per level", 10, 100, 30, 5
        )

        st.markdown("---")
        st.markdown(
            "<div class='note-box'>"
            "<b>Methodology note</b><br>"
            "CEFR levels are approximated from corpus frequency "
            "(Zipf scores via wordfreq) with two corrections: A1 overrides "
            "for common concrete vocabulary, and Academic Word List "
            "(Coxhead, 2000) floor of B2 for academic terms.<br><br>"
            "This is a research approximation. For definitive CEFR word "
            "levels, consult the Cambridge English Vocabulary Profile."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── text input ──
    if mode == "Single text":
        col_in, col_up = st.columns([3, 1])
        with col_in:
            user_text = st.text_area(
                "Paste text here",
                height=200,
                placeholder="Paste any text — a game excerpt, textbook passage, dialogue transcript…",
                label_visibility="collapsed",
            )
        with col_up:
            uploaded = st.file_uploader(
                "Or upload a .txt file",
                type=["txt"],
                label_visibility="visible",
            )
            if uploaded:
                user_text = uploaded.read().decode("utf-8", errors="ignore")
                st.success(f"Loaded {len(user_text):,} characters")

        run = st.button("▶  Run analysis", use_container_width=False)

        if run and user_text and user_text.strip():
            with st.spinner("Analysing…"):
                records = analyze(user_text, lemmatizer)
                if not records:
                    st.warning("No analysable words found. Check your input.")
                    return
                stats = compute_stats(records)
                by_level = group_by_level(records)
            _render_single(stats, by_level, show_wordlists, max_words_shown)

        elif run:
            st.warning("Please enter some text first.")

    else:  # compare two texts
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("<div class='section-header'>Text A</div>", unsafe_allow_html=True)
            label_a = st.text_input("Label for Text A", value="Text A")
            text_a  = st.text_area("Text A", height=180, label_visibility="collapsed",
                                    placeholder="Paste first text…")
        with col_b:
            st.markdown("<div class='section-header'>Text B</div>", unsafe_allow_html=True)
            label_b = st.text_input("Label for Text B", value="Text B")
            text_b  = st.text_area("Text B", height=180, label_visibility="collapsed",
                                    placeholder="Paste second text…")

        run = st.button("▶  Compare texts", use_container_width=False)

        if run and text_a.strip() and text_b.strip():
            with st.spinner("Analysing both texts…"):
                rec_a = analyze(text_a, lemmatizer)
                rec_b = analyze(text_b, lemmatizer)
                if not rec_a or not rec_b:
                    st.warning("Could not parse one or both texts.")
                    return
                stats_a = compute_stats(rec_a)
                stats_b = compute_stats(rec_b)
                by_level_a = group_by_level(rec_a)
                by_level_b = group_by_level(rec_b)
            _render_compare(
                stats_a, stats_b, by_level_a, by_level_b,
                label_a, label_b, show_wordlists, max_words_shown,
            )
        elif run:
            st.warning("Please enter text in both panels.")


# ── rendering helpers ─────────────────────────────────────────────────────────

def _render_metrics(stats: dict, label: str = ""):
    prefix = f"**{label}** — " if label else ""
    st.markdown(
        f"{prefix}{stats['total_tokens']:,} tokens · "
        f"{stats['unique_types']:,} unique lemmas",
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Lexical Density",  f"{stats['lex_density']}%",
              help="Content words / total words × 100. Higher = more information-dense.")
    m2.metric("Corrected TTR",    f"{stats['cttr']}",
              help="Unique lemmas / √(2 × total). Measures lexical variety, corrected for text length.")
    m3.metric("Mean Zipf Score",  f"{stats['mean_zipf']}",
              help="Average corpus frequency of all tokens (1=very rare, 7=extremely common). Lower = harder text.")
    m4.metric("C1+ Coverage",
              f"{stats['level_pcts'].get('C1', 0) + stats['level_pcts'].get('C2', 0) + stats['level_pcts'].get('Off-list', 0):.1f}%",
              help="Proportion of tokens at C1, C2, or off-list. Useful as a difficulty ceiling indicator.")


def _render_chart(stats: dict):
    fig = make_bar_chart(stats["level_pcts"])
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=130, bbox_inches="tight",
                transparent=True)
    st.image(buf.getvalue(), use_container_width=True)
    plt.close(fig)


def _render_level_table(stats: dict):
    rows = []
    for lv in LEVELS:
        count = stats["level_counts"].get(lv, 0)
        pct   = stats["level_pcts"].get(lv, 0.0)
        rows.append({"Level": lv, "Tokens": count, "% of text": pct})
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_wordlists(by_level: dict, max_words: int):
    st.markdown("<div class='section-header'>Word lists by level</div>",
                unsafe_allow_html=True)
    for level in LEVELS:
        words = by_level.get(level, [])
        if not words:
            continue
        colour = LEVEL_COLOURS[level]
        with st.expander(f"{level}  —  {len(words)} unique lemmas"):
            pills = "".join(
                f"<span class='word-pill' style='background:{colour}22;"
                f"color:{colour};border:1px solid {colour}55;'>"
                f"{w} <span style='opacity:0.6'>×{n}</span></span>"
                for w, n in words[:max_words]
            )
            st.markdown(pills, unsafe_allow_html=True)
            if len(words) > max_words:
                st.caption(f"… and {len(words) - max_words} more")


def _render_single(stats, by_level, show_wordlists, max_words):
    st.markdown("---")
    _render_metrics(stats)
    _render_chart(stats)

    with st.expander("Level breakdown table", expanded=False):
        _render_level_table(stats)

    if show_wordlists:
        _render_wordlists(by_level, max_words)

    _render_download(stats, by_level)


def _render_compare(stats_a, stats_b, by_level_a, by_level_b,
                    label_a, label_b, show_wordlists, max_words):
    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**{label_a}**")
        _render_metrics(stats_a)
        _render_chart(stats_a)
    with col_b:
        st.markdown(f"**{label_b}**")
        _render_metrics(stats_b)
        _render_chart(stats_b)

    # Side-by-side level table
    st.markdown("<div class='section-header'>Level comparison</div>",
                unsafe_allow_html=True)
    rows = []
    for lv in LEVELS:
        rows.append({
            "Level":              lv,
            f"{label_a} tokens": stats_a["level_counts"].get(lv, 0),
            f"{label_a} %":      stats_a["level_pcts"].get(lv, 0.0),
            f"{label_b} tokens": stats_b["level_counts"].get(lv, 0),
            f"{label_b} %":      stats_b["level_pcts"].get(lv, 0.0),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Unique high-difficulty words in each text
    st.markdown("<div class='section-header'>High-difficulty vocabulary (C1+)</div>",
                unsafe_allow_html=True)
    c1plus = ["C1", "C2", "Off-list"]
    col_a2, col_b2 = st.columns(2)

    def hard_words(by_level):
        words = []
        for lv in c1plus:
            words.extend((w, n, lv) for w, n in by_level.get(lv, [])[:max_words])
        return sorted(words, key=lambda x: -x[1])

    with col_a2:
        st.markdown(f"*{label_a}*")
        for w, n, lv in hard_words(by_level_a)[:max_words]:
            colour = LEVEL_COLOURS[lv]
            st.markdown(
                f"<span class='word-pill' style='background:{colour}22;"
                f"color:{colour};border:1px solid {colour}55;'>"
                f"{w} ×{n} <span style='font-size:10px'>({lv})</span></span>",
                unsafe_allow_html=True,
            )
    with col_b2:
        st.markdown(f"*{label_b}*")
        for w, n, lv in hard_words(by_level_b)[:max_words]:
            colour = LEVEL_COLOURS[lv]
            st.markdown(
                f"<span class='word-pill' style='background:{colour}22;"
                f"color:{colour};border:1px solid {colour}55;'>"
                f"{w} ×{n} <span style='font-size:10px'>({lv})</span></span>",
                unsafe_allow_html=True,
            )

    if show_wordlists:
        col_a3, col_b3 = st.columns(2)
        with col_a3:
            st.markdown(f"**{label_a} — word lists**")
            _render_wordlists(by_level_a, max_words)
        with col_b3:
            st.markdown(f"**{label_b} — word lists**")
            _render_wordlists(by_level_b, max_words)


def _render_download(stats, by_level):
    st.markdown("<div class='section-header'>Export</div>",
                unsafe_allow_html=True)
    rows = []
    for level in LEVELS:
        for lemma, count in by_level.get(level, []):
            rows.append({"lemma": lemma, "level": level, "count": count})
    df = pd.DataFrame(rows)
    csv = df.to_csv(index=False).encode()
    st.download_button(
        "⬇  Download word list CSV",
        data=csv,
        file_name="lexical_profile.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
