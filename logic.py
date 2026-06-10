"""
Game Logic for the Real vs Fake Audio Detection Game.
Handles data loading, parsing, state management, and scoring.
"""
import csv
import io
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import soundfile as sf

from config import (
    DEFAULT_LIVES,
    CSV_LABEL_FILE,
    CSV_FALLBACK_FILE,
    AUDIO_SUBDIR
)

class GameState:
    """Encapsulates the entire state of the game session."""
    def __init__(self):
        self.screen: str = "landing"
        self.username: str = ""
        self.lives: int = DEFAULT_LIVES
        self.score: int = 0
        self.trials: int = 0
        self.correct: int = 0
        self.current_pair: Optional[Dict[str, Any]] = None
        self.answered: bool = False
        self.answer_correct: Optional[bool] = None
        self.answer_which: Optional[str] = None
        self.leaderboard: List[Dict[str, Any]] = []
        self.db_loaded: bool = False
        self.session_id: str = str(uuid4())
        self.rounds: List[Dict] = []
        self.export_success: Optional[bool] = None

        # Data caches
        self.bonafide_entries: List[Dict] = []
        self.spoof_entries: List[Dict] = []

# Data Loading Helpers
def parse_id_mapping(csv_path: Path) -> Tuple[List[Dict], List[Dict]]:
    bonafide, spoof = [], []
    SPOOF_LABELS = {'synthetic', 'partial synthetic', 'spoof'}

    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                entry = {k.strip(): v.strip() for k, v in row.items()}
                lbl = entry.get('effective_label', '')
                if lbl == 'bonafide':
                    bonafide.append(entry)
                elif lbl in SPOOF_LABELS:
                    spoof.append(entry)
    except Exception as e:
        raise RuntimeError(f"Could not parse CSV {csv_path}: {e}")

    return bonafide, spoof


def find_audio_file(export_dir: Path, obf_id: str, split: str) -> Optional[Path]:
    """Locate audio file for a given ID in train/test folders."""
    extensions = ['.wav', '.WAV', '.flac', '.mp3']

    for s in (split, 'train', 'test'):
        for ext in extensions:
            p = export_dir / AUDIO_SUBDIR / s / (obf_id + ext)
            if p.exists():
                return p

    return None


def load_audio_bytes(path: Path) -> Optional[bytes]:
    """Load audio file and return raw bytes buffer."""
    try:
        audio, sr = sf.read(str(path), dtype='float32', always_2d=False)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        buf = io.BytesIO()
        sf.write(buf, audio, sr, format='WAV')
        return buf.getvalue()
    except Exception:
        return None


def load_database(export_dir: Path) -> Tuple[bool, List[Dict], List[Dict]]:
    """
    Load and validate the audio database.
    Returns (success, bonafide_entries, spoof_entries).
    """
    csv_candidates = [
        export_dir / CSV_LABEL_FILE,
        export_dir / CSV_FALLBACK_FILE
    ]

    csv_path = next((p for p in csv_candidates if p.exists()), None)

    if not csv_path:
        return False, [], []

    try:
        bonafide_raw, spoof_raw = parse_id_mapping(csv_path)
    except Exception:
        return False, [], []

    bonafide_valid = []
    for e in bonafide_raw:
        p = find_audio_file(export_dir, e['obfuscated_id'], e.get('split', 'train'))
        if p:
            bonafide_valid.append({**e, 'path': p})

    spoof_valid = []
    for e in spoof_raw:
        p = find_audio_file(export_dir, e['obfuscated_id'], e.get('split', 'train'))
        if p:
            spoof_valid.append({**e, 'path': p})

    has_data = bool(bonafide_valid and spoof_valid)
    return has_data, bonafide_valid, spoof_valid

# Game Logic
def generate_trial_pair(bonafide_list: List[Dict], spoof_list: List[Dict]) -> Optional[Dict[str, Any]]:
    """
    Generate a new pair of audio clips for a trial.
    Pair dict includes bonafide_id and spoof_id for per-round logging.
    """
    b_entry = random.choice(bonafide_list)
    s_entry = random.choice(spoof_list)

    b_audio = load_audio_bytes(b_entry['path'])
    s_audio = load_audio_bytes(s_entry['path'])

    if b_audio is None or s_audio is None:
        return None

    s_lbl = s_entry.get('effective_label', 'synthetic')
    s_pipeline = s_entry.get('pipeline', '')
    b_id = b_entry.get('obfuscated_id', '')
    s_id = s_entry.get('obfuscated_id', '')

    if random.random() < 0.5:
        return {
            'A': ('bonafide', b_audio),
            'B': (s_lbl, s_audio, s_pipeline),
            'real': 'A',
            'bonafide_id': b_id,
            'spoof_id': s_id,
        }
    else:
        return {
            'A': (s_lbl, s_audio, s_pipeline),
            'B': ('bonafide', b_audio),
            'real': 'B',
            'bonafide_id': b_id,
            'spoof_id': s_id,
        }

def handle_answer(state: GameState, chosen: str) -> None:
    """Process user answer, update score/lives, log round data, and set feedback flags."""
    if not state.current_pair:
        return

    pair = state.current_pair
    correct = (chosen == pair['real'])

    state.answered = True
    state.answer_correct = correct
    state.answer_which = chosen
    state.trials += 1

    # Per-round data
    fake_letter = 'B' if pair['real'] == 'A' else 'A'
    fake_entry = pair[fake_letter]
    state.rounds.append({
        'round': state.trials,
        'real_letter': pair['real'],
        'user_choice': chosen,
        'correct': correct,
        'fake_label': fake_entry[0],
        'fake_pipeline': fake_entry[2] if len(fake_entry) > 2 else '',
        'bonafide_id': pair.get('bonafide_id', ''),
        'spoof_id': pair.get('spoof_id', ''),
    })

    if correct:
        state.score += 10
        state.correct += 1
    else:
        state.lives -= 1


def submit_leaderboard_entry(state: GameState) -> None:
    """Add current player to leaderboard and sort."""
    entry = {
        'name': state.username,
        'score': state.score,
        'trials': state.trials,
        'correct': state.correct,
        'acc': round(state.correct / state.trials * 100) if state.trials > 0 else 0,
        'ts': time.time(),
    }
    state.leaderboard.append(entry)
    state.leaderboard.sort(key=lambda x: (-x['score'], -x['acc']))


def reset_game_state(state: GameState) -> None:
    """Reset game variables for a new round, including a fresh session ID."""
    state.lives = DEFAULT_LIVES
    state.score = 0
    state.trials = 0
    state.correct = 0
    state.current_pair = None
    state.answered = False
    state.answer_correct = None
    state.answer_which = None
    state.rounds = []
    state.session_id = str(uuid4())
    state.export_success = None