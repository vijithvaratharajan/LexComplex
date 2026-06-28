# LexComplex

A vocabulary-level profiler for second language acquisition research and materials development. Paste any English text, and LexComplex tells you how much of it falls at each CEFR level, how lexically dense it is, how varied its vocabulary is, and which words are likely to challenge a learner at a given proficiency stage.

**[Live app](https://your-app-url.streamlit.app)**

---

## What it does

LexComplex takes any English text, breaks it into individual words, and maps each word to a CEFR proficiency level (A1 through C2) using corpus frequency data. You can analyse a single text or compare two texts side by side, which makes it useful for tasks like evaluating whether a game's opening scene is appropriate for B1 learners, comparing a textbook passage to authentic material, or auditing a reading comprehension task for lexical difficulty.

The app runs entirely in the browser via Streamlit. No data is stored.

---

## Key concepts

**CEFR levels**
The Common European Framework of Reference for Languages divides language proficiency into six bands: A1 and A2 (beginner to elementary), B1 and B2 (intermediate to upper-intermediate), and C1 and C2 (advanced to mastery). Each band has associated vocabulary expectations. A1 learners are expected to know words like "house" and "eat." C1 learners encounter words like "pedagogy" and "mediate." LexComplex assigns every word in a text to one of these bands so you can see the overall vocabulary demand at a glance.

**Zipf frequency scores**
A Zipf score is a logarithmic measure of how often a word appears in real language use. The scale runs roughly from 1 (extremely rare) to 7 (the most common words in the language, such as "the" and "be"). LexComplex uses Zipf scores from the wordfreq library (Speer, 2022), which draws on large multilingual corpora including Wikipedia, news text, and subtitles. Higher Zipf scores correspond to easier vocabulary; lower scores indicate words a learner is less likely to have encountered.

The CEFR band thresholds used are:

| CEFR level | Zipf range      |
|------------|-----------------|
| A1         | above 5.5       |
| A2         | 4.5 to 5.5      |
| B1         | 3.5 to 4.5      |
| B2         | 2.5 to 3.5      |
| C1         | 1.5 to 2.5      |
| C2         | below 1.5       |

**The Academic Word List**
The Academic Word List (AWL; Coxhead, 2000) is a set of 570 word families that appear frequently across academic disciplines but are not among the most common words in general English. Words like "analyse," "establish," and "facilitate" belong here. Because these words are used widely in academic writing, their corpus frequency scores can be misleadingly high, making them appear easier than they are for a learner encountering them in an educational context. LexComplex applies the AWL as a correction layer, treating all AWL words as B2 minimum regardless of their raw frequency score.

**Lemmatisation**
Rather than counting "running," "ran," and "runs" as three separate words, LexComplex reduces each token to its base form, or lemma ("run"), before looking up its frequency. This gives a more accurate picture of the vocabulary a learner actually needs to know. Lemmatisation is handled by NLTK's WordNet lemmatiser, which uses part-of-speech context to make the right reduction (so "better" as an adjective becomes "good," not "better").

**Lexical density**
Lexical density measures the proportion of content words (nouns, main verbs, adjectives, and adverbs) relative to all words in a text. A text with high lexical density packs more information into fewer words. Academic writing typically runs around 40 to 55 percent. Casual conversation and simple textbooks run lower. A higher lexical density generally means a more demanding reading experience.

**Corrected Type-Token Ratio (CTTR)**
Type-token ratio (TTR) is the number of unique words divided by the total number of words in a text. A high TTR suggests a rich, varied vocabulary; a low TTR suggests repetition. The problem with raw TTR is that it shrinks naturally as texts get longer, making it unsuitable for comparing texts of different lengths. LexComplex uses the corrected version (CTTR), which divides unique words by the square root of twice the total word count, partially compensating for the length effect.

---

## Usage

**Single text mode**
Paste any text into the input box or upload a `.txt` file and click Run. The app returns a bar chart showing the CEFR distribution, four summary metrics, and expandable word lists for each level. You can download the full word-level data as a CSV.

**Compare mode**
Switch to Compare in the sidebar, paste two texts into the panels (for example, a game excerpt and a textbook passage), and run the analysis. The app shows both profiles side by side with a combined level table and a panel highlighting high-difficulty vocabulary (C1 and above) from each text.

**Sidebar options**
You can toggle the word lists on or off and set how many words to display per level. The methodology note in the sidebar explains the key limitations.

---

## Methodology note

LexComplex uses corpus frequency as a proxy for CEFR level. This is a well-established approach in computational vocabulary profiling (see Nation, 2001; Laufer & Nation, 1995) but it is an approximation, not a definitive level assignment. Two corrections are applied to address known divergences. First, an A1 override list covers common concrete vocabulary (words like "cat," "pencil," and "Monday") that appears infrequently in written corpora but is unambiguously basic for a language learner. Second, the Academic Word List applies a B2 floor to academic vocabulary whose corpus frequency would otherwise underestimate its difficulty for most learners.

The B2/C1 boundary is the least reliable region of the profiler. Many academic and technical words cluster in the Zipf 2.5 to 3.5 range regardless of their pedagogical level. For definitive CEFR word-level data, cross-reference results with the Cambridge English Vocabulary Profile.

---

## References

Coxhead, A. (2000). A new academic word list. *TESOL Quarterly, 34*(2), 213-238.

Laufer, B., & Nation, P. (1995). Vocabulary size and use: Lexical richness in L2 written production. *Applied Linguistics, 16*(3), 307-322.

Nation, I. S. P. (2001). *Learning vocabulary in another language*. Cambridge University Press.

Speer, R. (2022). rspeer/wordfreq: v3.0. Zenodo. https://doi.org/10.5281/zenodo.7199437

---

## Tech

- Python 3.10+
- [Streamlit](https://streamlit.io) for the interface
- [wordfreq](https://github.com/rspeer/wordfreq) for corpus frequency data
- [NLTK](https://www.nltk.org) for tokenisation and lemmatisation
- pandas and matplotlib for data handling and charts

## Run locally

```bash
git clone https://github.com/yourusername/lexcomplex.git
cd lexcomplex
pip install -r requirements.txt
streamlit run app.py
```

## License

MIT

## Author

Vijith Varatharajan
[ORCID: 0009-0007-8713-1343](https://orcid.org/0009-0007-8713-1343)
