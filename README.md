# Lift Log

A static dashboard for my weight-training history. It loads the newest CSV from
this public Google Drive folder:

https://drive.google.com/drive/folders/1Z4XPVw74dzL7jtgqiXExs_6G8nJBfBU5

A GitHub Action downloads the folder every 6 hours, picks the newest CSV, and
commits it as `data/latest.csv`. The page then reads that file automatically, so
it stays up to date without needing a Google API key.

## Publishing to GitHub Pages

1. Create a repository called `weights` under the `diarmuid` account.
2. Push this folder to its `main` branch:

   ```bash
   git add .
   git commit -m "Publish lift log"
   git branch -M main
   git remote add origin https://github.com/diarmuid/weights.git
   git push -u origin main
   ```

3. In the repository, open **Settings → Pages** and set **Source** to
   **Deploy from a branch**, branch **main**, folder **/ (root)**.
4. The site will be published at:

   https://diarmuid.github.io/weights/

Allow a few minutes for the first deployment.

## How updates work

- The workflow is in `.github/workflows/sync-drive.yml`.
- It runs on a schedule (every 6 hours) and can be started manually from the
  **Actions** tab.
- It needs no secrets, but the Drive folder must remain shared as
  **Anyone with the link**.
- If the repository blocks workflow pushes, go to **Settings → Actions →
  General → Workflow permissions** and allow **Read and write permissions**.

## Running the sync locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python sync_drive.py
```

To preview the page locally, serve the folder instead of opening the file
directly (browsers block relative `fetch` requests from `file://` URLs):

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/.

## Manual overrides

- Open the page with `?csv=<link>` to load a specific CSV.
- Use the **Data source** panel to paste a Drive link or choose a local file.
- `index.html` also contains a built-in snapshot used as a last-resort fallback.