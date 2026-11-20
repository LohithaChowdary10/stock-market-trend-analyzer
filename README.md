# Stock Market Trend Analyzer — Streamlit

## Run locally
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. In the terminal, run:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Demo login
- Username: `demo`
- Password: `demo123`

## CSV format
A CSV file must include a `Close` column. A `Date` column is optional.

Example:
```csv
Date,Close
2025-01-01,100
2025-01-02,104
2025-01-03,101
```

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository and upload all files in this folder.
2. Go to https://share.streamlit.io/
3. Sign in with GitHub and click **Create app**.
4. Select the repository, branch, and `app.py` as the main file.
5. Click **Deploy**.

## Important notes
- Login/register in this learning demo uses Streamlit session state. It is not production authentication and accounts are not persisted across sessions.
- Analysis history is session-only.
- This version accepts CSV or built-in sample data. It does not fetch live market prices.
