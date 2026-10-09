#!/usr/bin/env python3
"""
Blog Publishing & Sync Automation for abhyudaymishr.github.io
Pipeline:
  Blog Ideas (Apple Notes)
       ↓
  Write or Edit note
       ↓
  Add "#Publish" or "#Update" tag
       ↓
  Mac Shortcut (or run scripts/publish.sh)
       ↓
  Updates existing post OR creates new: _posts/YYYY-MM-DD-my-blog-post.md
       ↓
  git push
       ↓
  GitHub Actions CI/CD
       ↓
  abhyudaymishr.github.io/blog
"""

import sys
import os
import re
import argparse
import subprocess
import datetime
from html.parser import HTMLParser
from pathlib import Path

# Paths
REPO_DIR = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_DIR / "_posts"


class HTMLToMarkdown(HTMLParser):
    """Converts Apple Notes HTML export into clean Markdown."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.in_title_h1 = False
        self.title = None
        self.list_stack = []
        self.ol_counters = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.result.append(f"\n\n{'#' * level} ")
        elif tag == 'b' or tag == 'strong':
            self.result.append('**')
        elif tag == 'i' or tag == 'em':
            self.result.append('*')
        elif tag == 'code':
            self.result.append('`')
        elif tag == 'pre':
            self.result.append('\n```\n')
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            self.result.append("[")
            self._current_href = href
        elif tag == 'ul':
            self.list_stack.append('ul')
            self.result.append('\n')
        elif tag == 'ol':
            self.list_stack.append('ol')
            self.ol_counters.append(1)
            self.result.append('\n')
        elif tag == 'li':
            indent = '  ' * (len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1] == 'ol':
                num = self.ol_counters[-1]
                self.ol_counters[-1] += 1
                self.result.append(f"\n{indent}{num}. ")
            else:
                self.result.append(f"\n{indent}- ")
        elif tag in ('p', 'div'):
            self.result.append('\n')
        elif tag == 'br':
            self.result.append('\n')

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.result.append('\n\n')
        elif tag == 'b' or tag == 'strong':
            self.result.append('**')
        elif tag == 'i' or tag == 'em':
            self.result.append('*')
        elif tag == 'code':
            self.result.append('`')
        elif tag == 'pre':
            self.result.append('\n```\n')
        elif tag == 'a':
            href = getattr(self, '_current_href', '')
            self.result.append(f"]({href})")
            self._current_href = None
        elif tag == 'ul':
            if self.list_stack:
                self.list_stack.pop()
            self.result.append('\n')
        elif tag == 'ol':
            if self.list_stack:
                self.list_stack.pop()
            if self.ol_counters:
                self.ol_counters.pop()
            self.result.append('\n')

    def handle_data(self, data):
        self.result.append(data)

    def get_markdown(self):
        text = ''.join(self.result)
        text = re.sub(r'\*{4,}', '**', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def slugify(text: str) -> str:
    """Turn a title string into a clean url-friendly slug."""
    text = text.strip().lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


def extract_title_and_body(raw_text: str):
    """
    Extracts title and cleans body.
    Supports markdown headers, Apple Notes titles, or raw text.
    Never treats publish or update tags as title.
    """
    cleaned_text = raw_text.replace('\u2028', '\n').replace('\u2029', '\n').strip()
    raw_lines = [line.rstrip() for line in cleaned_text.split('\n')]

    # Filter out empty lines and lines that are solely tags like #Publish, #Published, #Update
    lines = []
    for line in raw_lines:
        trimmed = line.strip()
        if re.match(r'^(#|\s*)*(publish(ed)?|update(d)?)(\s*\(.*?\))?\s*$', trimmed, re.IGNORECASE):
            continue
        lines.append(line)

    # Drop leading empty lines
    while lines and not lines[0].strip():
        lines.pop(0)

    if not lines:
        return "Untitled Note", ""

    first_line = lines[0].strip()

    # Check if first line is a markdown header
    if first_line.startswith('#'):
        title = re.sub(r'^#+\s*', '', first_line).strip()
        remaining_lines = lines[1:]
    else:
        title = first_line
        remaining_lines = lines[1:]

    title = title.strip('"\'')

    # Remove any stray publish or update tags anywhere in body
    body_text = '\n'.join(remaining_lines).strip()
    body_text = re.sub(r'(?i)#(publish(ed)?|update(d)?)\b(\s*\(.*?\))?[^\n]*', '', body_text).strip()
    body_text = re.sub(r'\n{3,}', '\n\n', body_text).strip()

    return title, body_text


def get_existing_posts():
    """
    Parses existing posts in _posts/ directory.
    Returns list of dicts with metadata for matching.
    """
    posts = []
    if not POSTS_DIR.exists():
        return posts

    for path in sorted(POSTS_DIR.glob("*.md")):
        content = path.read_text(encoding='utf-8')
        # Extract YAML front matter
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            continue
        fm_text = fm_match.group(1)

        title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
        date_match = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})["\']?\s*$', fm_text, re.MULTILINE)
        note_id_match = re.search(r'^note_id:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)

        title = title_match.group(1) if title_match else ""
        date = date_match.group(1) if date_match else ""
        note_id = note_id_match.group(1) if note_id_match else ""

        # Extract slug from filename (strip YYYY-MM-DD-)
        filename_slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', path.stem)

        posts.append({
            'file_path': path,
            'filename': path.name,
            'title': title,
            'date': date,
            'note_id': note_id,
            'slug': filename_slug,
        })

    return posts


def find_matching_post(note_id: str, title: str, existing_posts: list):
    """
    Searches for an existing post that matches this note:
    1. By note_id (highest confidence)
    2. By title slug match
    3. By filename slug match
    """
    target_slug = slugify(title)

    # 1. Match by note_id
    if note_id:
        for p in existing_posts:
            if p['note_id'] and p['note_id'] == note_id:
                return p

    # 2. Match by title slug
    if target_slug:
        for p in existing_posts:
            if p['title'] and slugify(p['title']) == target_slug:
                return p

    # 3. Match by filename slug
    if target_slug:
        for p in existing_posts:
            if p['slug'] and p['slug'] == target_slug:
                return p

    return None


def find_publishable_notes():
    """
    Queries Apple Notes for notes with tag '#Publish' or '#Update' (excluding already '#Published').
    Returns list of dicts: [{'id': ..., 'name': ..., 'text': ...}]
    """
    get_ids_script = '''
    tell application "Notes"
        set matched to (every note whose plaintext contains "#Publish" or plaintext contains "#publish" or plaintext contains "#Update" or plaintext contains "#update" or body contains "#Publish" or body contains "#publish" or body contains "#Update" or body contains "#update")
        set idList to {}
        repeat with n in matched
            set end of idList to (id of n as string)
        end repeat
        return idList
    end tell
    '''
    id_res = subprocess.run(['osascript', '-e', get_ids_script], capture_output=True, text=True)
    if id_res.returncode != 0 or not id_res.stdout.strip():
        return []

    raw_ids = [i.strip() for i in id_res.stdout.strip().split(", ") if i.strip()]
    notes = []

    for note_id in raw_ids:
        fetch_script = f'''
        tell application "Notes"
            set n to (note id "{note_id}")
            return (name of n as string) & "___DELIM___" & (plaintext of n as string)
        end tell
        '''
        f_res = subprocess.run(['osascript', '-e', fetch_script], capture_output=True, text=True)
        if f_res.returncode == 0 and "___DELIM___" in f_res.stdout:
            parts = f_res.stdout.split("___DELIM___", 1)
            note_text = parts[1]

            # STRICT CHECK: Must contain '#publish' or '#update' as a tag, NOT followed by 'ed' or 'd'
            if not re.search(r'#(publish|update)\b(?!ed|d)', note_text, re.IGNORECASE):
                continue

            notes.append({
                'id': note_id,
                'name': parts[0].strip(),
                'text': note_text
            })

    return notes


def mark_note_as_published(note_id: str, is_update: bool = False):
    """
    Updates the note in Apple Notes: replaces '#Publish' or '#Update' with
    '#Published (YYYY-MM-DD)' or '#Published (updated YYYY-MM-DD)'.
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    tag_replacement = f"#Published (updated {today_str})" if is_update else f"#Published ({today_str})"

    fetch_script = f'''
    tell application "Notes"
        set n to (note id "{note_id}")
        return body of n as string
    end tell
    '''
    f_res = subprocess.run(['osascript', '-e', fetch_script], capture_output=True, text=True)
    if f_res.returncode != 0:
        return

    cur_body = f_res.stdout
    # Regex replace only #publish or #update not followed by ed/d
    new_body = re.sub(r'(?i)#(publish|update)\b(?!ed|d)', tag_replacement, cur_body)

    escaped_body = new_body.replace('\\', '\\\\').replace('"', '\\"')

    update_script = f'''
    tell application "Notes"
        try
            set n to (note id "{note_id}")
            set body of n to "{escaped_body}"
            return "ok"
        on error errStr
            return errStr
        end try
    end tell
    '''
    subprocess.run(['osascript', '-e', update_script], capture_output=True, text=True)


def notify_mac(title: str, message: str):
    """Shows native macOS notification."""
    ascript = f'''
    display notification "{message}" with title "Blog Publisher" subtitle "{title}" sound name "Glass"
    '''
    subprocess.run(['osascript', '-e', ascript], capture_output=True, text=True)


def publish_post_content(raw_text: str, note_id: str = None, custom_date: str = None, dry_run: bool = False, push: bool = True):
    """
    Parses note content, creates or updates markdown file in _posts, commits, and pushes.
    """
    title, body = extract_title_and_body(raw_text)

    if not title:
        print("❌ Error: Could not determine post title.")
        return None

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    existing_posts = get_existing_posts()
    matching_post = find_matching_post(note_id, title, existing_posts)

    is_update = matching_post is not None

    if is_update:
        file_path = matching_post['file_path']
        post_date = matching_post['date'] or custom_date or today_str
        bound_note_id = note_id or matching_post.get('note_id', '')
        action_verb = "Updated"
        print(f"\n🔄 Existing Post Found (Updating In-Place):")
        print(f"   Original File: _posts/{matching_post['filename']}")
    else:
        post_date = custom_date or today_str
        slug = slugify(title) or f"post-{post_date}"
        filename = f"{post_date}-{slug}.md"
        file_path = POSTS_DIR / filename
        bound_note_id = note_id or ""
        action_verb = "Published"
        print(f"\n📝 New Post Prepared:")
        print(f"   Filename:      _posts/{filename}")

    print(f"   Title:         {title}")
    print(f"   Date:          {post_date}")
    if is_update:
        print(f"   Last Modified: {today_str}")

    escaped_title = title.replace('"', '\\"')

    # Build Front Matter
    front_matter_lines = [
        "---",
        f'title: "{escaped_title}"',
        f'date: {post_date}',
    ]
    if is_update:
        front_matter_lines.append(f'last_modified_at: {today_str}')
    if bound_note_id:
        front_matter_lines.append(f'note_id: "{bound_note_id}"')
    front_matter_lines.append("---")
    front_matter_lines.append(body + "\n")

    post_content = "\n".join(front_matter_lines)

    if dry_run:
        print(f"\n--- [DRY RUN PREVIEW ({action_verb.upper()})] ---")
        print(post_content[:400] + ("..." if len(post_content) > 400 else ""))
        print("---------------------------------------")
        return file_path.name

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    file_path.write_text(post_content, encoding='utf-8')
    print(f"✅ Saved: {file_path}")

    # Git operations
    if push:
        try:
            subprocess.run(["git", "add", str(file_path)], cwd=REPO_DIR, check=True)
            commit_msg = f"{action_verb}: {title}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, check=True)
            print(f"✅ Git committed: '{commit_msg}'")

            print("🚀 Pushing to GitHub (origin main)...")
            push_res = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True, text=True)
            if push_res.returncode == 0:
                print("✅ Successfully pushed to GitHub! CI/CD workflow triggered.")
                notify_mac(title, f"{action_verb} on abhyudaymishr.github.io/blog")
            else:
                print(f"⚠️ Git push failed: {push_res.stderr.strip()}")
                print("💡 Run `git push origin main` manually.")
                notify_mac("Post committed locally", "Run `git push` to deploy to GitHub.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}", file=sys.stderr)

    return file_path.name


def main():
    parser = argparse.ArgumentParser(description="Auto-publish & sync notes to abhyudaymishr.github.io/blog")
    parser.add_argument("--scan", action="store_true", help="Scan Apple Notes for notes with #Publish or #Update tag (Default)")
    parser.add_argument("--stdin", action="store_true", help="Read note content from stdin (for Mac Shortcuts input)")
    parser.add_argument("--file", type=str, help="Read note content from a specific file")
    parser.add_argument("--date", type=str, help="Override date (format: YYYY-MM-DD)")
    parser.add_argument("--no-push", action="store_true", help="Create or update post without git commit/push")
    parser.add_argument("--dry-run", action="store_true", help="Preview post without saving or pushing")

    args = parser.parse_args()

    # Mode 1: Read from STDIN
    if args.stdin:
        content = sys.stdin.read()
        if not content.strip():
            print("Error: No content received on STDIN.", file=sys.stderr)
            sys.exit(1)
        publish_post_content(content, custom_date=args.date, dry_run=args.dry_run, push=not args.no_push)
        return

    # Mode 2: Read from specific file
    if args.file:
        path = Path(args.file)
        if not path.is_file():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        content = path.read_text(encoding='utf-8')
        publish_post_content(content, custom_date=args.date, dry_run=args.dry_run, push=not args.no_push)
        return

    # Mode 3 (Default): Scan Apple Notes
    print("🔍 Scanning Apple Notes for notes tagged with #Publish or #Update...")
    notes = find_publishable_notes()

    if not notes:
        print("ℹ️ No notes found with the '#Publish' or '#Update' tag.")
        print("💡 In Apple Notes:")
        print("   • To publish a new post: Add '#Publish'")
        print("   • To update an existing post: Add '#Update' or '#Publish'")
        return

    print(f"📋 Found {len(notes)} note(s) ready to sync:")
    for note in notes:
        print(f"   • {note['name']}")

    for note in notes:
        existing_posts = get_existing_posts()
        is_update = find_matching_post(note['id'], note['name'], existing_posts) is not None
        filename = publish_post_content(note['text'], note_id=note['id'], custom_date=args.date, dry_run=args.dry_run, push=not args.no_push)
        if filename and not args.dry_run:
            mark_note_as_published(note['id'], is_update=is_update)
            status_text = "#Published (updated)" if is_update else "#Published"
            print(f"🏷️ Updated Apple Note tag to {status_text}")


if __name__ == "__main__":
    main()
