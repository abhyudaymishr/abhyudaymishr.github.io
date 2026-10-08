# Blog Automation Pipeline: Apple Notes ➔ Mac Shortcut ➔ GitHub Pages

This automation connects your everyday writing notes to your published Jekyll blog on [abhyudaymishr.github.io/blog](https://abhyudaymishr.github.io/blog).

## The Flow
```text
  Blog Ideas (Apple Notes)
            ↓
      Write normally
            ↓
     Add "#Publish" tag
            ↓
       Mac Shortcut
            ↓
  Creates: _posts/YYYY-MM-DD-my-blog-post.md
            ↓
         git push
            ↓
    GitHub Actions CI/CD
            ↓
  abhyudaymishr.github.io/blog
```

---

## 1. How to Write & Publish
1. Open **Apple Notes** (on Mac, iPhone, or iPad).
2. Write in your **Blog Ideas** folder or any note.
   - **First line**: Becomes the Post Title (e.g., `# Why Qudits Matter` or just `Why Qudits Matter`).
   - **Body**: Write your thoughts normally in markdown or standard text.
3. When ready to publish, simply add `#Publish` anywhere in the note.
4. Trigger your **Mac Shortcut** (or run `scripts/publish.sh`).
5. What happens automatically:
   - Finds the note with `#Publish`.
   - Extracts the title, creates the clean URL slug, and formats the Jekyll front matter.
   - Saves `_posts/YYYY-MM-DD-<slug>.md`.
   - Updates the note tag in Apple Notes to `#Published (YYYY-MM-DD)` so it never duplicates.
   - Runs `git add`, `git commit -m "Publish: <title>"`, and `git push origin main`.
   - GitHub Actions automatically builds Jekyll and deploys to `abhyudaymishr.github.io/blog`.
   - Displays a native macOS notification confirming publication.

---

## 2. Setting Up the Mac Shortcut in 30 Seconds

1. Open the **Shortcuts** app on your Mac (`Cmd + Space` ➔ type `Shortcuts`).
2. Click **"+"** to create a new shortcut.
3. Name it: **Publish Blog**.
4. In the right search bar, search for **"Run Shell Script"** and drag it in.
5. In the script box, enter:
   ```bash
   /bin/zsh /Users/abhyuday/abhyudaymishr.github.io/scripts/publish.sh
   ```
6. (Optional Convenience Settings):
   - Check **"Use as Quick Action"** / **"Pin in Menu Bar"** to publish with 1 click from your macOS top menu bar.
   - Add a keyboard shortcut (e.g. `Cmd + Shift + P`).
   - You can also say: *"Hey Siri, Publish Blog"*.

---

## 3. Alternative Trigger: Standalone Mac App
We have also pre-compiled a double-clickable macOS helper:
`scripts/Publish Blog.app`
Double-clicking it runs the publication cycle and shows a notification.

---

## 4. Manual Terminal Commands
If you ever prefer running from terminal:
```bash
# Auto-scan Apple Notes for #Publish tag and publish:
./scripts/publish.sh

# Preview without saving or pushing:
./scripts/publish.sh --dry-run

# Create post without git push:
./scripts/publish.sh --no-push
```

---

## 5. CI/CD (GitHub Actions)
The repository includes `.github/workflows/deploy.yml`.
Whenever a new post is pushed to `main`, GitHub Actions automatically builds the Jekyll site and deploys it to GitHub Pages.
