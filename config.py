"""
Configuration and Styling for the Real vs Fake Audio Game.
Contains all CSS themes, constants, and static text.
"""
# Constants
DEFAULT_LIVES = 3
EXPORT_DIR_DEFAULT = "game_database"
CSV_LABEL_FILE = "labels/id_mapping.csv"
CSV_FALLBACK_FILE = "id_mapping.csv"
AUDIO_SUBDIR = "audio"


# CSS Styles 
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

/* Base Reset */
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #2b252d;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}
[data-testid="stAppViewContainer"] { padding: 0; }
[data-testid="block-container"] { padding: 1.5rem 1rem 3rem; max-width: 540px; margin: 0 auto; }

/* Typography */
h1, h2, h3 { 
    font-family: 'Space Mono', monospace; 
    letter-spacing: -1px; 
}

.badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    padding: 2px 8px;
    border-radius: 2px;
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    color: #7878aa;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: clamp(3rem, 10vw, 5rem);
    font-weight: 1000;
    line-height: 1.05;
    margin: 0.5rem 0 0.25rem;
    background: linear-gradient(135deg, #e0e0ff 0%, #a0a0ff 50%, #6060cc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 2rem;
    color: #8888aa;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

/* Stats */
.stat-box {
    flex: 1;
    background: #111120;
    border: 1px solid #222240;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    text-align: center;
}
.stat-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #a0a0ff;
    line-height: 1;
}
.stat-lbl {
    font-size: 1rem;
    color: #666688;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Trial & Clips */
.trial-label {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    color: #555577;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

.clip-card {
    background: #0f0f1e;
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.clip-letter {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #4444aa;
    margin-bottom: 0.25rem;
}

/* Feedback */
.feedback-correct {
    background: #0a1f0a;
    border: 1px solid #1a4a1a;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #44dd44;
    font-family: 'Space Mono', monospace;
    font-size: 1.25rem;
    margin: 0.75rem 0;
}
.feedback-wrong {
    background: #1f0a0a;
    border: 1px solid #4a1a1a;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #dd4444;
    font-family: 'Space Mono', monospace;
    font-size: 1.25rem;
    margin: 0.75rem 0;
}

/* Consent */
.consent-item {
    color: #8888aa;
    font-size: 0.85rem;
    padding: 0.2rem 0;
}
.consent-legal {
    color: #555577;
    font-size: 0.78rem;
    line-height: 1.5;
    padding: 0.15rem 0;
}

/* Leaderboard */
.leaderboard-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid #111128;
    font-family: 'Space Mono', monospace;
    font-size: 1.25rem;
}
.leaderboard-row.me {
    background: #111128;
    border-radius: 6px;
    color: #a0a0ff;
}
.rank-num { color: #444466; min-width: 2rem; }
.lb-name { flex: 1; color: #ccccee; }
.lb-score { color: #a0a0ff; }
.lb-acc { color: #666688; font-size: 1rem; }

/* UI Elements */
.divider {
    border: none;
    border-top: 1px solid #1a1a30;
    margin: 1.5rem 0;
}

.stButton > button {
    width: 100%;
    background: #1a1a3a;
    border: 1px solid #5050cc;
    color: #c0c0ff;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    font-weight: 1000;
    border-radius: 8px;
    padding: 0.75rem;
    transition: all 0.15s;
    letter-spacing: 1px;
}
.stButton > button:hover {
    background: #2a2a5a;
    border-color: #5050cc;
    color: #ffffff;
}

div[data-testid="stTextInput"] input {
    background: #e0e0ff;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    color: #2b252d;
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    padding: 0.6rem 0.8rem;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #5050cc;
    box-shadow: 0 0 0 2px rgba(80,80,204,0.2);
}

audio { filter: invert(0.85) hue-rotate(180deg); width: 100%; border-radius: 6px; }

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
</style>
"""

# Text Resources
TEXTS = {
    "page_title": "Hear Me Out!",
    "page_icon": "🎙️",
    "hero_title": "Hear Me Out!",
    "hero_sub": "Synthetic voices sound more and more natural.<br> Can YOU tell the difference?<br>Listen to two clips and pick the real one.",
    "rules": [
        "🎧 Listen to both clips",
        "✅ Pick the authentic (human-voiced) clip",
        f"❌ {DEFAULT_LIVES} wrong answers and it's game over",
    ],
    "feedback_correct": "✓ Correct!<br>Clip {} was <b>{}</b>{}.",
    "feedback_wrong": "✗ Wrong.<br>Clip {} was <b>{}</b>{}<br>{}.",
    "lives_lost_note": "💔 {} {} left.",
    "game_over_note": "💀 Game over!",
    "leaderboard_label": "LEADERBOARD",
    "how_to_play_label": "HOW TO PLAY",
    "round_label": "ROUND {} - WHICH IS REAL?",
    "btn_start": "START GAME ->",
    "btn_next": "NEXT ROUND ->",
    "btn_quit": "QUIT & SEE SCORE",
    "btn_play_again": "PLAY AGAIN",
    "btn_clip_a": "🅰  Clip A is real",
    "btn_clip_b": "🅱  Clip B is real",
    "error_no_db": "⚠️ No audio database found in `{}`. Expected `labels/id_mapping.csv` and `audio/train/` or `audio/test/` folders.",
    "error_load_audio": "Could not load audio pair. Check your export directory.",

    # Consent screen
    "consent_badge": "BEFORE YOU GO",
    "consent_title": "Help our research?",
    "consent_intro": "Would you like to share your anonymous session data to support voice deepfake detection research?",
    "consent_data_label": "WHAT WE COLLECT",
    "consent_data_items": [
        "🔑 A random session ID (generated at game start, not linked to your name)",
        "📊 Score, accuracy, and number of rounds played",
        "🔍 Per-round: which clip was real, your choice, and the synthesis pipeline of the fake clip",
    ],
    "consent_no_pii": "Your username is never stored. No personal data is collected.",
    "consent_purpose": "Data is used solely for academic research on deepfake audio detection.",
    "consent_withdraw": "Because submissions are fully anonymous, they cannot be identified or retracted after sending.",
    "consent_access": "Results are stored in a private repository accessible only to the research team.",
    "btn_consent_yes": "YES, SHARE RESULTS ->",
    "btn_consent_no": "NO THANKS ->",
    "consent_success": "✓ Results shared. Thank you for contributing!",
    "consent_fail": "Your results were not saved. Thank you for playing!",
}