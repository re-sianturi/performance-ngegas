# Delivering Artifacts to User

## Overview

After pipeline completion (or after Step 08 LP is done), the user may request to receive the deliverables directly in the chat. This document covers the workflow for packaging and sending HTML landing pages and other artifacts to the user via Telegram.

## File Locations

All landing pages are stored in per-segment run folders:

```
~/.hermes/runs/performance-ngegas/
├── 2026-06-11_010541_segment-01-muslim-taqwa/
│   └── 08-lp/
│       ├── primary.html
│       └── challenger.html
├── 2026-06-11_011059_segment-02-diabetes-ginjal/
│   └── 08-lp/
│       ├── primary.html
│       └── challenger.html
└── ...
```

## Workflow: Pack and Send

### 1. Gather Files

List all `primary.html` and `challenger.html` files across segment run folders:

```python
import os

runs_dir = os.path.expanduser("~/.hermes/runs/performance-ngegas")
segments = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]

for seg in segments:
    lp_dir = os.path.join(runs_dir, seg, "08-lp")
    if os.path.exists(lp_dir):
        files = os.listdir(lp_dir)
        print(f"{seg}: {files}")
```

### 2. Package into ZIP

**Important:** The `zip` command is not always available. Use Python `zipfile` as fallback.

```python
import os
import zipfile
import shutil

files_to_pack = [
    "seg01-muslim-taqwa-primary.html",
    "seg01-muslim-taqwa-challenger.html",
    # ... all files
]

# Copy files to /tmp with descriptive names first
for src_path, label in file_map:
    dst = os.path.join("/tmp", f"{label}.html")
    shutil.copy(src_path, dst)

# Create ZIP
zip_path = "/tmp/performance-ngegas-lp.zip"
with zipfile.ZipFile(zip_path, 'w') as zf:
    for f in files_to_pack:
        full_path = os.path.join("/tmp", f)
        if os.path.exists(full_path):
            zf.write(full_path, f)

print(f"Created {zip_path} ({os.path.getsize(zip_path)} bytes)")
```

### 3. Send to Telegram

Use `send_message` with `MEDIA:` prefix. Always discover targets first.

```python
# Step 1: Discover targets
send_message(action="list")

# Step 2: Send ZIP
send_message(
    action="send",
    message="MEDIA:/tmp/performance-ngegas-lp.zip",
    target="telegram:#Nobody"  # or user's actual chat target
)
```

### 4. Supported File Types

| File Type | Telegram Behavior |
|-----------|-----------------|
| `.html` | Sent as document attachment (not previewable inline) |
| `.zip` | Sent as document attachment |
| `.png`, `.jpg`, `.webp` | Sent as inline photos |
| `.pdf` | Sent as document with preview |

### 5. HTML Files in Telegram

HTML files are sent as document attachments. Users must:
1. Download the ZIP
2. Extract locally
3. Open HTML files in a browser

**Note:** Telegram does not render HTML inline. Always explain this to the user when sending HTML.

## Pitfalls

1. **Don't send raw HTML as text.** HTML code pasted as chat text is unreadable. Always package as ZIP or send individual files as `MEDIA:`.
2. **Use descriptive filenames.** `seg01-muslim-taqwa-primary.html` > `primary.html` (which is ambiguous across segments).
3. **Verify files exist before sending.** Always `ls` or `os.path.exists()` check before creating ZIP.
4. **ZIP command may not be available.** Always prefer Python `zipfile` over shell `zip` for portability.
5. **Absolute paths required.** `MEDIA:` prefix requires absolute paths (`/tmp/...` not `tmp/...`).
6. **Always send ZIP, not individual HTML files.** A batch of 6 segments × 2 variants = 14 files. Sending individually is noisy. Package into one ZIP.
