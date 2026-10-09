#!/usr/bin/env python3
"""
Blog Publishing Automation for abhyudaymishr.github.io
Pipeline:
  Blog Ideas (Apple Notes)
       ↓
  Write normally
       ↓
  Add "#Publish" tag
       ↓
  Mac Shortcut (or run scripts/publish_note.py)
       ↓
  Creates: _posts/YYYY-MM-DD-my-blog-post.md
       ↓
  git push
       ↓
  GitHub (GitHub Actions CI/CD)
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
        self.list_stack = []  # 'ul' or 'ol'
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
            self.result.append(f"[")
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
        # Normalize double bold marks (Apple Notes sometimes nests <b><b>)
        text = re.sub(r'\*{4,}', '**', text)
        # Normalize multiple line breaks
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
    Never treats publish tags as title.
    """
    # Replace non-standard unicode line breaks from Apple Notes
    cleaned_text = raw_text.replace('\u2028', '\n').replace('\u2029', '\n').strip()
    raw_lines = [line.rstrip() for line in cleaned_text.split('\n')]
    
    # Filter out empty lines AND lines that are solely tags like #Publish or #Published
    lines = []
    for line in raw_lines:
        trimmed = line.strip()
        # If line is solely a publish tag (e.g. #Publish, #Published, #Published (2026-10-09))
        if re.match(r'^(#|\s*)*publish(ed)?(\s*\(.*?\))?\s*$', trimmed, re.IGNORECASE):
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

    # Strip quote marks if wrapped
    title = title.strip('"\'')

    # Remove any stray #Publish or #Published tags from body
    body_text = '\n'.join(remaining_lines).strip()
    body_text = re.sub(r'(?i)#publish(ed)?\b(\s*\(.*?\))?[^\n]*', '', body_text).strip()
    # Strip any consecutive blank lines
    body_text = re.sub(r'\n{3,}', '\n\n', body_text).strip()

    return title, body_text


def find_publishable_notes():
    """
    Queries Apple Notes for notes with tag '#Publish' (excluding already #Published).
    Returns list of dicts: [{'id': ..., 'name': ..., 'text': ...}]
    """
    # Query Apple Notes for notes containing #Publish or #publish
    get_ids_script = '''
    tell application "Notes"
        set matched to (every note whose plaintext contains "#Publish" or plaintext contains "#publish" or body contains "#Publish" or body contains "#publish")
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
            
            # STRICT CHECK: Must contain '#publish' as a standalone tag, NOT followed by 'ed'
            if not re.search(r'#publish\b(?!ed)', note_text, re.IGNORECASE):
                continue

            notes.append({
                'id': note_id,
                'name': parts[0].strip(),
                'text': note_text
            })

    return notes


def mark_note_as_published(note_id: str, post_filename: str):
    """
    Updates the note in Apple Notes: precisely replaces '#Publish' with '#Published (YYYY-MM-DD)'.
    Never touches '#Published'.
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    tag_replacement = f"#Published ({today_str})"
    
    # Fetch note body
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
    # Regex replace only #publish not followed by ed
    new_body = re.sub(r'(?i)#publish\b(?!ed)', tag_replacement, cur_body)

    # Escape quotes and backslashes for AppleScript
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


def publish_post_content(raw_text: str, custom_date: str = None, dry_run: bool = False, push: bool = True):
    """
    Parses note content, creates markdown file in _posts, commits, and pushes.
    """
    title, body = extract_title_and_body(raw_text)
    
    if not title:
        print("❌ Error: Could not determine post title.")
        return None

    post_date = custom_date or datetime.date.today().strftime("%Y-%m-%d")
    slug = slugify(title)
    if not slug:
        slug = f"post-{post_date}"

    filename = f"{post_date}-{slug}.md"
    file_path = POSTS_DIR / filename

    # Escape title quotes for YAML
    escaped_title = title.replace('"', '\\"')

    post_content = f"""---
title: "{escaped_title}"
date: {post_date}
---
{body}
"""

    print(f"\n📝 Post Prepared:")
    print(f"   Title:    {title}")
    print(f"   Date:     {post_date}")
    print(f"   Filename: _posts/{filename}")

    if dry_run:
        print("\n--- [DRY RUN PREVIEW] ---")
        print(post_content[:400] + ("..." if len(post_content) > 400 else ""))
        print("-------------------------")
        return filename

    # Ensure _posts exists
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    # Write file
    file_path.write_text(post_content, encoding='utf-8')
    print(f"✅ Created: {file_path}")

    # Git operations
    if push:
        try:
            # Stage
            subprocess.run(["git", "add", str(file_path)], cwd=REPO_DIR, check=True)
            
            # Commit
            commit_msg = f"Publish: {title}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, check=True)
            print(f"✅ Git committed: '{commit_msg}'")

            # Push
            print("🚀 Pushing to GitHub (origin main)...")
            push_res = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True, text=True)
            if push_res.returncode == 0:
                print("✅ Successfully pushed to GitHub! CI/CD workflow triggered.")
                notify_mac(title, f"Published to abhyudaymishr.github.io/blog")
            else:
                print(f"⚠️ Git push failed: {push_res.stderr.strip()}")
                print("💡 Check your GitHub authentication or run `git push origin main` manually.")
                notify_mac("Post committed locally", "Run `git push` to deploy to GitHub.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}", file=sys.stderr)

    return filename


def main():
    parser = argparse.ArgumentParser(description="Auto-publish notes to abhyudaymishr.github.io/blog")
    parser.add_argument("--scan", action="store_true", help="Scan Apple Notes for notes with #Publish tag (Default)")
    parser.add_argument("--stdin", action="store_true", help="Read note content from stdin (for Mac Shortcuts input)")
    parser.add_argument("--file", type=str, help="Read note content from a specific file")
    parser.add_argument("--date", type=str, help="Override date (format: YYYY-MM-DD)")
    parser.add_argument("--no-push", action="store_true", help="Create post file without git commit/push")
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

    # Mode 3 (Default): Scan Apple Notes for #Publish
    print("🔍 Scanning Apple Notes for notes tagged with #Publish...")
    notes = find_publishable_notes()

    if not notes:
        print("ℹ️ No notes found with the '#Publish' tag.")
        print("💡 In Apple Notes: Write your draft in 'Blog Ideas' and add '#Publish' when ready!")
        notify_mac("No notes to publish", "Add #Publish tag to your draft in Apple Notes.")
        return

    print(f"📋 Found {len(notes)} note(s) ready to publish:")
    for note in notes:
        print(f"   • {note['name']}")

    for note in notes:
        filename = publish_post_content(note['text'], custom_date=args.date, dry_run=args.dry_run, push=not args.no_push)
        if filename and not args.dry_run:
            mark_note_as_published(note['id'], filename)
            print(f"🏷️ Updated Apple Note tag to #Published")


if __name__ == "__main__":
    main()
