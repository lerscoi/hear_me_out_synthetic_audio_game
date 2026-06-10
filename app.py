"""
Synthetic Audio Detection Game.
Hosted in Streamlit
"""
import argparse
from pathlib import Path

import streamlit as st

from config import THEME_CSS, TEXTS, DEFAULT_LIVES, EXPORT_DIR_DEFAULT
from export import push_result
from logic import (
    GameState,
    load_database,
    generate_trial_pair,
    handle_answer,
    submit_leaderboard_entry,
    reset_game_state
)


# Initialization
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--export_dir", default=EXPORT_DIR_DEFAULT)
    try:
        args, _ = parser.parse_known_args()
    except SystemExit:
        args = parser.parse_args([])
    return args

def has_export_configured() -> bool:
    """Return True if GitHub export secrets are present and usable."""
    try:
        return "github" in st.secrets and bool(st.secrets["github"].get("token"))
    except Exception:
        return False

ARGS = get_args()
EXPORT_DIR = Path(ARGS.export_dir)

st.set_page_config(
    page_title=TEXTS["page_title"],
    page_icon=TEXTS["page_icon"],
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(THEME_CSS, unsafe_allow_html=True)

if "game" not in st.session_state:
    st.session_state.game = GameState()

ss = st.session_state.game

# Screen Renderers
def render_landing_screen():
    """Renders the Landing/Home screen."""
    st.markdown(f'<div class="badge">{TEXTS["how_to_play_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{TEXTS["hero_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{TEXTS["hero_sub"]}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    username = st.text_input("Your name:", placeholder="Enter a username:", key="name_input", label_visibility="collapsed")

    db_ok, _, _ = load_database(EXPORT_DIR)
    ss.db_loaded = db_ok

    if not db_ok:
        st.warning(TEXTS["error_no_db"].format(EXPORT_DIR))

    start_disabled = not (username.strip() and db_ok)

    if st.button(TEXTS["btn_start"], disabled=start_disabled):
        ss.username = username.strip()
        reset_game_state(ss)
        ss.screen = "game"
        st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="trial-label">{TEXTS["how_to_play_label"]}</div>', unsafe_allow_html=True)
    for rule in TEXTS["rules"]:
        st.markdown(f'<div style="color:#8888aa;font-size:1.25rem;padding:0.2rem 0;">{rule}</div>', unsafe_allow_html=True)

    if ss.leaderboard:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown(f'<div class="trial-label">{TEXTS["leaderboard_label"]}</div>', unsafe_allow_html=True)
        render_leaderboard()


def render_game_screen():
    """Renders the active gameplay screen."""
    lives_str = '♥' * ss.lives + '♡' * (DEFAULT_LIVES - ss.lives)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{ss.score}</div><div class="stat-lbl">Score</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{ss.trials}</div><div class="stat-lbl">Rounds</div></div>', unsafe_allow_html=True)
    with col3:
        color = '#dd4444' if ss.lives == 1 else '#a0a0ff'
        st.markdown(f'<div class="stat-box"><div class="stat-val" style="color:{color};letter-spacing:4px;">{lives_str}</div><div class="stat-lbl">Lives</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if ss.current_pair is None:
        pair = generate_trial_pair(ss.bonafide_entries, ss.spoof_entries)
        if pair is None:
            st.error(TEXTS["error_load_audio"])
            if st.button("QUIT"):
                submit_leaderboard_entry(ss)
                ss.screen = "consent" if has_export_configured() else "results"
                st.rerun()
            return
        ss.current_pair = pair

    pair = ss.current_pair
    st.markdown(f'<div class="trial-label">{TEXTS["round_label"].format(ss.trials + 1)}</div>', unsafe_allow_html=True)

    for letter in ['A', 'B']:
        entry = pair[letter]
        audio_bytes = entry[1]
        st.markdown(f'<div class="clip-card"><div class="clip-letter">Clip {letter}</div>', unsafe_allow_html=True)
        st.audio(audio_bytes, format='audio/wav')
        st.markdown('</div>', unsafe_allow_html=True)

    if not ss.answered:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(TEXTS["btn_clip_a"], key="btn_A"):
                handle_answer(ss, 'A')
                st.rerun()
        with col2:
            if st.button(TEXTS["btn_clip_b"], key="btn_B"):
                handle_answer(ss, 'B')
                st.rerun()
    else:
        real = pair['real']
        fake_letter = 'B' if real == 'A' else 'A'
        fake_entry = pair[fake_letter]
        fake_lbl = fake_entry[0]
        fake_pipeline = fake_entry[2] if len(fake_entry) > 2 else ''
        pipeline_note = f' ({fake_pipeline})' if fake_pipeline and fake_pipeline != 'no_manipulation' else ''

        if ss.answer_correct:
            msg = TEXTS["feedback_correct"].format(fake_letter, fake_lbl, pipeline_note)
            st.markdown(f'<div class="feedback-correct">{msg}</div>', unsafe_allow_html=True)
        else:
            life_text = ss.lives if ss.lives > 0 else 0
            note = TEXTS["lives_lost_note"].format(life_text, "life" if life_text == 1 else "lives") if ss.lives > 0 else TEXTS["game_over_note"]
            msg = TEXTS["feedback_wrong"].format(fake_letter, fake_lbl, pipeline_note, note)
            st.markdown(f'<div class="feedback-wrong">{msg}</div>', unsafe_allow_html=True)

        if ss.lives <= 0:
            if st.button("SEE RESULTS ->"):
                submit_leaderboard_entry(ss)
                ss.screen = "consent" if has_export_configured() else "results"
                st.rerun()
        else:
            if st.button(TEXTS["btn_next"]):
                ss.current_pair = None
                ss.answered = False
                st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button(TEXTS["btn_quit"], key="quit_btn"):
        submit_leaderboard_entry(ss)
        ss.screen = "consent" if has_export_configured() else "results"
        st.rerun()


def render_consent_screen():
    """Renders the data sharing consent screen."""
    st.markdown(f'<div class="badge">{TEXTS["consent_badge"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title" style="font-size:clamp(1.5rem,6vw,2.2rem);">{TEXTS["consent_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{TEXTS["consent_intro"]}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="trial-label">{TEXTS["consent_data_label"]}</div>', unsafe_allow_html=True)
    for item in TEXTS["consent_data_items"]:
        st.markdown(f'<div class="consent-item">{item}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    for line in (
        TEXTS["consent_no_pii"],
        TEXTS["consent_purpose"],
        TEXTS["consent_withdraw"],
        TEXTS["consent_access"],
    ):
        st.markdown(f'<div class="consent-legal">{line}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(TEXTS["btn_consent_yes"]):
            with st.spinner("Submitting..."):
                ss.export_success = push_result(ss, st.secrets)
            ss.screen = "results"
            st.rerun()
    with col2:
        if st.button(TEXTS["btn_consent_no"]):
            ss.export_success = None
            ss.screen = "results"
            st.rerun()


def render_results_screen():
    """Renders the final results screen."""
    acc = round(ss.correct / ss.trials * 100) if ss.trials > 0 else 0

    st.markdown('<div class="badge">GAME OVER</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{ss.score}<br><span style="font-size:1rem;color:#666688;">points</span></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{ss.trials}</div><div class="stat-lbl">Rounds</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{acc}%</div><div class="stat-lbl">Accuracy</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-val">{ss.lives}</div><div class="stat-lbl">Lives left</div></div>', unsafe_allow_html=True)

    # Export status feedback
    if ss.export_success is True:
        st.markdown(f'<div class="feedback-correct">{TEXTS["consent_success"]}</div>', unsafe_allow_html=True)
    elif ss.export_success is False:
        st.markdown(f'<div class="feedback-wrong">{TEXTS["consent_fail"]}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<div class="trial-label">{TEXTS["leaderboard_label"]}</div>', unsafe_allow_html=True)

    my_ts = ss.leaderboard[-1]['ts'] if ss.leaderboard else None
    render_leaderboard(my_ts=my_ts)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button(TEXTS["btn_play_again"]):
        reset_game_state(ss)
        ss.screen = "landing"
        st.rerun()


def render_leaderboard(my_ts: float | None = None):
    """Helper to render the leaderboard HTML."""
    lb = ss.leaderboard[:20]
    for i, entry in enumerate(lb):
        is_me = my_ts is not None and entry['ts'] == my_ts
        cls = 'leaderboard-row me' if is_me else 'leaderboard-row'
        medal = ['🥇', '🥈', '🥉'][i] if i < 3 else f'#{i+1}'
        st.markdown(
            f'<div class="{cls}">'
            f'<span class="rank-num">{medal}</span>'
            f'<span class="lb-name">{entry["name"]}</span>'
            f'<span class="lb-score">{entry["score"]}pts</span>'
            f'<span class="lb-acc">{entry["acc"]}%</span>'
            f'</div>',
            unsafe_allow_html=True
        )

# Main Loop
def main():
    if not ss.db_loaded:
        ok, bf, sp = load_database(EXPORT_DIR)
        if ok:
            ss.bonafide_entries = bf
            ss.spoof_entries = sp
            ss.db_loaded = True

    if ss.screen == 'landing':
        render_landing_screen()
    elif ss.screen == 'game':
        render_game_screen()
    elif ss.screen == 'consent':
        render_consent_screen()
    elif ss.screen == 'results':
        render_results_screen()


if __name__ == "__main__":
    main()