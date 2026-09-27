# AI-assisted: written with Claude Code (Anthropic). See docs/AI_USAGE.md.
# One-off: reorders bundle.js into the 5-minute, three-speaker talk plus a Q&A backup section.
import json

raw = open('bundle.js', encoding='utf-8').read()
pre = 'window.TRACE_DECK = '
assert raw.startswith(pre)
pack = json.loads(raw[len(pre):].rstrip().rstrip(';'))
C = pack['content']
S = {s['id']: s for s in C['slides']}

C['meta'].update(
    runtime_target_seconds=270,
    format_note='5:00 maximum, three speakers (Problem · Data · Technical architecture), then Q&A. '
                'Backup slides after the close are for Q&A only and are not timed.')
C['speakers'] = [
    {"slot": "S1", "name": "William Keffer", "section": "The Problem", "seconds": 0},
    {"slot": "S2", "name": "Ismail Gasmi", "section": "The Data", "seconds": 0},
    {"slot": "S3", "name": "Markandeya Yalamanchi", "section": "Technical Architecture", "seconds": 0},
    {"slot": "S4", "name": "Adrian Hito", "section": "Technical Q&A", "seconds": 0},
]


def sp(id, who, sec, act=None):
    s = S[id]
    s['speaker'] = who
    s['seconds'] = sec
    if act:
        s['act'] = act
    return s


# ---- S1: the problem ----
problem = [sp('title', 'S1', 0), sp('cold-1', 'S1', 10), sp('cold-2', 'S1', 8), sp('cold-3', 'S1', 7),
           sp('lag', 'S1', 14), sp('late-detection', 'S1', 16), sp('reframe', 'S1', 15, 'I')]
S['reframe']['cues'] = [
    "This swap is the innovation claim. Make it the loudest sentence.",
    "Hand off: 'To forecast where harm lands, you first need data nobody had joined up.'"]

# ---- S2: the data ----
ds = sp('data-spine', 'S2', 30, 'II')
ds['cues'] = [
    "Read two numbers, not six: the World Bank indicators and the UNODC seizure cases.",
    "World Bank data plays five roles: market size (GDP, population), route friction (WGI governance, ports, air traffic, logistics), "
    "vulnerability (youth unemployment, poverty, Gini, health spend), outcomes for validation (homicide, HIV), and a detection-bias "
    "control that is fitted but never shown.",
    "Every call is programmatic with explicit source IDs (2 and 3), paginated, nulls kept, provenance recorded."]
conf = sp('honesty-method', 'S2', 25, 'II')
conf['cues'] = [
    "Say the objection before a judge does: seizures measure enforcement as well as trafficking.",
    "Answer: no corridor rests on seizures alone; every edge gets a 0-100 score from six independent signals.",
    "Routes are allocated over 234 documented UNODC corridors; the public seizure file has no route fields."]
hero = sp('terminal-hero', 'S2', 20, 'II')
hero['cues'] = [
    "One sentence: all of it becomes one workspace, the Atlas.",
    "Hand off: 'On top of this data we built two models.'"]

# ---- S3: technical architecture ----
forecast = {"id": "forecast", "act": "III", "speaker": "S3", "seconds": 25, "theme": "atlas", "blocks": [
    {"type": "kicker", "text": "Model 1 · route forecast, backtested blind"},
    {"type": "lines", "scale": "m", "items": [
        "LightGBM hurdle: will a corridor be active next year, and how much moves.",
        "Trained through 2019, predicting 2020–2024 unseen."]},
    {"type": "chart", "src": "assets/charts/backtest.png",
     "alt": "Grouped bars: LightGBM hurdle beats same-as-last-year and PPML gravity on AUC (0.88 vs 0.82 vs 0.58), "
            "Spearman (0.58 vs 0.48 vs 0.38) and precision@20 (0.48 vs 0.42 vs 0.34).",
     "caption": "8,242 training corridor-years · 3,170 test corridor-years · 46 features incl. 13 World Bank indicators per end · SHAP drivers per corridor"},
    {"type": "source", "text": "Santos Silva & Tenreyro (2006) PPML · Ke et al. (2017) LightGBM · Lundberg & Lee (2017) SHAP"}],
    "cues": [
        "'Same as last year' is the honest baseline because routes are sticky. We beat it on all three measures.",
        "Most corridors are zero most years; that is why it is a hurdle model (classifier times regressor).",
        "Per-drug AUC if asked: meth 0.96, heroin 0.92, cannabis 0.89, cocaine 0.79."]}

reflex = {"id": "reflex", "act": "III", "speaker": "S3", "seconds": 35, "theme": "atlas", "blocks": [
    {"type": "kicker", "text": "Model 2 · Reflex, our own Jev-style news classifier"},
    {"type": "lines", "scale": "m", "items": ["Official data is years late. News is minutes late."]},
    {"type": "pipeline", "steps": [
        {"step": "INGEST", "title": "GDELT every 15 min",
         "text": "Drug stories worldwide, deduped. Seven typed questions per headline: event?, type, drug, origin, transit, destination, size."},
        {"step": "TRAIN", "title": "Fine-tuned on a Colab T4",
         "text": "An NLI cross-encoder (DeBERTa-v3-xsmall) scores each answer. Log-loss on 10,777 open + UNODC-derived examples, "
                 "then 2,351 blind-verified headlines. About 7 minutes."},
        {"step": "CALIBRATE", "title": "Temperature scaling",
         "text": "One temperature per question type, fitted on held-out data: 80% confident means right about 80% of the time."}]},
    {"type": "chart", "size": "s", "src": "assets/charts/reflex_training.png",
     "alt": "Held-out accuracy rises from 48.1% (untuned backbone) to 90.2% (Reflex v0.2); calibration error falls from 0.206 to 0.020.",
     "caption": "Held-out open-dataset questions · ECE 0.020 is within the 0.02–0.03 independent tests report for Jev"}],
    "cues": [
        "Why build it: Jev (TypeSafe) had a waitlist and we had no key, so we implemented the same typed-question interface on an open model. No TypeSafe code or weights.",
        "Two numbers: accuracy 48% to 90%, calibration error 0.21 to 0.02.",
        "Jev sits behind the same JevClassifier interface and swaps in once a key exists."]}

reflex_real = {"id": "reflex-real", "act": "III", "speaker": "S3", "seconds": 35, "theme": "atlas", "blocks": [
    {"type": "kicker", "text": "Tested on 92 real, published headlines it never saw"},
    {"type": "chart", "src": "assets/charts/reflex_real_news.png",
     "alt": "Field accuracy on 92 real headlines for the keyword baseline, Reflex v0.2 and Reflex plus grounding. "
            "Grounded Reflex: is_event 91, event type 88, drug 98, origin 96, destination 85, size 93.",
     "caption": "Per-field accuracy, % · 47 events from 5 continents + 45 hard negatives (pharma recalls, overdose statistics, drug-war film reviews)"},
    {"type": "chart", "size": "s", "src": "assets/charts/reflex_grounding.png",
     "alt": "Grounding cuts invented entities from 21.6% (keyword) and 4.9% (Reflex) to 0%, and false events from 15.4% and 12.8% to 5.1%.",
     "caption": "Grounding: every country, drug and size must be supported by the text, or it becomes 'not stated'"}],
    "cues": [
        "Every earlier test was synthetic; this is real news, labelled by hand, never used for tuning.",
        "Grounding means zero invented countries or drugs: a location must appear in the text (gazetteer, ports, 150k+ cities); "
        "a drug must match a synonym (shabu = meth, carfentanil = fentanyl).",
        "Anomaly flag: a confident seizure on a corridor our forecast gave under 10% is flagged on the map; the model announces its own miss."]}

deploy = {"id": "deploy", "act": "III", "speaker": "S3", "seconds": 22, "theme": "atlas", "blocks": [
    {"type": "kicker", "text": "Shipping it · ONNX export for a CPU server"},
    {"type": "statgrid", "compact": True, "items": [
        {"value": "98.7%", "label": "of headlines get identical Live Wire output after export",
         "source": "150 headlines, all 7 fields, ONNX vs PyTorch"},
        {"value": "3.6 s", "label": "model load, down from 58.9 s in PyTorch",
         "source": "137 MB ONNX model, laptop CPU"},
        {"value": "0.84", "label": "precision of events shown on real news, at 0.86 mean confidence",
         "source": "calibration holds out of the lab: ECE 0.052 after grounding"}]},
    {"type": "sub", "text": "Same answers, a fraction of the weight: Reflex runs without PyTorch, so the Live Wire can classify news on the deployed API instead of a GPU notebook."},
    {"type": "source", "text": "backend/scripts/export_reflex_onnx.py · reflex/results/onnx_parity.json · reflex/results/real_news_v1.json"}],
    "cues": [
        "Honest limits, if time: one annotator; 92 rows means wide error bars; false events 5.1% against a 5% target.",
        "Hand to the close."]}

close = sp('close', 'S3', 8, 'IV')
close['cues'] = ["Pause before the last line. Then stop.", "Next slide is the QR; open the floor to questions."]
hand = sp('handoff', 'S3', 0, 'IV')
hand['blocks'][2]['items'] = ["Questions?"]
hand['cues'] = ["Leave the QR up during Q&A so judges can open the live site.",
                "Q&A lead: backup slides follow (→), or press G for the overview."]

qa_div = {"id": "qa-backup", "act": "V", "speaker": "S4", "seconds": 0, "theme": "void", "layout": "center", "blocks": [
    {"type": "kicker", "text": "Q&A backup"},
    {"type": "lines", "scale": "m", "items": ["Backtest by drug · Afghanistan test · methods · impact · roadmap"]}],
    "cues": ["Only for answering questions. Jump with G (overview) to the slide you need."]}
backup = [sp(i, 'S4', 0, 'V') for i in
          ['backtest', 'afghan', 'methods', 'transit', 'impact', 'social-good', 'model', 'six-screens', 'commands', 'roadmap']]

C['slides'] = problem + [ds, conf, hero, forecast, reflex, reflex_real, deploy, close, hand, qa_div] + backup
for s in C['speakers']:
    s['seconds'] = sum(x['seconds'] for x in C['slides'] if x['speaker'] == s['slot'])
print('talk seconds', sum(s['seconds'] for s in C['slides']), 'slides', len(C['slides']))
print([(s['section'], s['seconds']) for s in C['speakers']])
open('bundle.js', 'w', encoding='utf-8').write(pre + json.dumps(pack, ensure_ascii=False, separators=(',', ':')) + ';')
