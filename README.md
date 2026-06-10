# Hear Me Out 🙉

**Listen for the fake! Fool you 3 times, you're out!**

This is a minigame that tests synthetic speech detection skills. The main purpose is to bring awareness to how realistic artificial audio can sound, and how easily it is to be deceived when additional processing steps are layered on top. Listeners can test their detection capabilities and learn from their mistakes.

## How It Works

Each round presents two audio clips - one genuine, one synthetic. You have to listen to both and pick the real one. Get it wrong and you lose a life. You have **3 lives** before game over. Scores are tracked on a session leaderboard. 

## Project Structure

```
├── game database
  ├──  labels/     # Utterance labels and processing steps
  ├── audio/       # Utterances to load
├── app.py         # Streamlit UI and screen renderers
├── config.py      # Constants, CSS theme, and text strings
├── logic.py       # Data loading, game state, and scoring
├── export.py      # Anonymous result export to GitHub
└── pyproject.toml # Project dependencies (managed by uv)
```

## Setup

### Requirements

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the project root:

```bash
uv sync
```

### Running

```bash
uv run streamlit run app.py
```

## Assets
**LLAMAPARTIALSPOOF**        
Luong, H.-T., Li, H., Zhang, L., Lee, K. A., & Chng, E. S. (2024, November 26). 
LlamaPartialSpoof (1.0.b). Zenodo. https://doi.org/10.5281/zenodo.14214149 

**THE INTERNATIONAL SOUNDSCAPE DATABASE**  
Mitchell, A., Oberman, T., Aletta, F., Erfanian, M., Kachlicka, 
M., Lionello, M., Fang, X., & Kang, J. (2024). The International 
Soundscape Database: An integrated multimedia database of urban 
soundscape surveys -- questionnaires with acoustical and contextual
information (1.0.1-alpha.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10672568
