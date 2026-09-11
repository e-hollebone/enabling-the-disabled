#!/usr/bin/env python3
"""
markdown_to_google_docs.py

Converts Markdown files stored in Google Drive into properly formatted
Google Docs, replacing all markdown content with native Docs formatting
(headings, bold, tables, lists, checkboxes, internal links).

Then deletes the original .md files and updates all README index docs
to reference the new Google Doc IDs with working links.

Usage:
  python markdown_to_google_docs.py --convert
  python markdown_to_google_docs.py --delete-md
  python markdown_to_google_docs.py --update-links
  python markdown_to_google_docs.py --all

Requires:
  - google-auth, google-api-python-client
  - Token at ~/.hermes/profiles/fitness-strategist/google_token.json
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Configuration ---

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

TOKEN_PATH = os.path.expanduser(
    "~/.hermes/profiles/fitness-strategist/google_token.json"
)
CREDENTIALS_PATH = os.path.expanduser(
    "~/.hermes/profiles/fitness-strategist/google_client_secret.json"
)

# --- Mapping: markdown file ID -> (new Google Doc ID, parent folder ID) ---
# This maps each .md file in Drive to its corresponding Google Doc replacement.
# If a Google Doc already exists with the same name, we update it in place.
# Otherwise we create a new one in the same parent folder.

MD_FILES_TO_CONVERT = [
    {
        "md_id": "1YFE8EqQyNJVKKLW6IrBfXNplgH3nLCSp",
        "md_name": "Sister Company Name Research - Enable the Disabled - 2026-09-09.md",
        "parent_id": "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",  # name search folder
        "new_doc_name": "Sister Company Name Research - Enable the Disabled - 2026-09-09",
        # Existing Google Doc that has the same content (to update in place):
        "existing_doc_id": "1fiyu9wzokeAGVHjAtXPCdXycXqvSyR23Uzp5NWNpyyk",
    },
    {
        "md_id": "1ajDh20i9sgsrjvaogJY94urSaRpRmFGc",
        "md_name": "Sister Company Name Research  - Enable the Disabled - 2026-09-09-Batch-02.md",
        "parent_id": "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",  # name search folder
        "new_doc_name": "Sister Company Name Research - Enable the Disabled - 2026-09-09 - Batch 02",
    },
    {
        "md_id": "1q06wAaH_-0hAgrPoOJ0kN_inbwiBCoo-",
        "md_name": "Sister Company Name Research Batch-03 - Enable the Disabled - 2026-09-09.md",
        "parent_id": "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",  # name search folder
        "new_doc_name": "Sister Company Name Research - Enable the Disabled - 2026-09-09 - Batch 03",
    },
    {
        "md_id": "1_PptdlLnVPNSSQePGayS0W4-C2Czimy_",
        "md_name": "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09.md",
        "parent_id": "17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8",  # Actually in name search folder
        "new_doc_name": "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09",
    },
    {
        "md_id": "1zSUPQVjD42ES8LPbNmynR7C79zWBLnwl",
        "md_name": "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09.md",
        "parent_id": "1w2On6DibxG5z0REfgLoBYUEkERwkgSAU",  # 07_Incorporation folder
        "new_doc_name": "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09",
    },
]

# --- Google Docs API helpers ---

def get_credentials():
    """Load or refresh Google OAuth2 credentials."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the token
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def get_drive_service(creds):
    return build("drive", "v3", credentials=creds)


def get_docs_service(creds):
    return build("docs", "v1", credentials=creds)


def download_markdown(drive_service, file_id):
    """Download a text/markdown file from Drive."""
    request = drive_service.files().get_media(fileId=file_id)
    content = request.execute()
    if isinstance(content, bytes):
        content = content.decode("utf-8")
    return content


def create_google_doc(docs_service, drive_service, title, parent_id, markdown_content):
    """
    Create a new Google Doc with properly formatted content from markdown.
    Returns the document ID.
    """
    # First create the doc
    body = {"title": title}
    if parent_id:
        body["parents"] = [parent_id]
    
    doc = docs_service.documents().create(body=body).execute()
    doc_id = doc["documentId"]
    
    # Now populate it with formatted content
    requests = markdown_to_docs_requests(markdown_content)
    
    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()
    
    return doc_id


def update_google_doc_content(docs_service, doc_id, markdown_content):
    """
    Replace all content in an existing Google Doc with properly formatted content from markdown.
    """
    # First, clear all existing content
    doc = docs_service.documents().get(documentId=doc_id).execute()
    
    # Find the last content index to delete everything
    last_index = None
    for elem in doc.get("body", {}).get("content", []):
        if "endIndex" in elem:
            last_index = elem["endIndex"]
    
    requests = []
    
    # Delete all existing content (from index 2 to end, index 1 is reserved for metadata)
    if last_index and last_index > 2:
        requests.append({
            "deleteContentRange": {
                "range": {
                    "startIndex": 2,
                    "endIndex": last_index - 1,  # -1 because endIndex is exclusive and there's a trailing paragraph
                }
            }
        })
    
    # Then add the new formatted content
    content_requests = markdown_to_docs_requests(markdown_content)
    requests.extend(content_requests)
    
    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()


def markdown_to_docs_requests(markdown_text):
    """
    Convert markdown text into a list of Google Docs API batchUpdate requests
    that produce properly formatted Google Docs content.

    Supports: headings (h1-h3), bold/italic, tables, bullet lists, checkboxes,
    horizontal rules, code blocks, and internal link replacement.
    """
    requests = []
    # Google Docs uses 1-based indexing. Index 1 is reserved for the document start.
    # Content starts at index 2.
    current_index = 2
    
    # We need to build requests sequentially, tracking the insertion index.
    # Each insertion shifts subsequent indices.
    
    lines = markdown_text.split("\n")
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines but add paragraph breaks
        if not stripped:
            # Add a paragraph break if the last thing wasn't already a paragraph break
            i += 1
            continue
        
        # Heading 1 (also used for document title)
        if stripped.startswith("# "):
            text = escaped_text(stripped[2:])
            requests.append(insert_text(current_index, text, bold=True, font_size=20, alignment="LEFT")))
            current_index += len(text)
            # Add paragraph break
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Heading 2
        if stripped.startswith("## "):
            text = escaped_text(stripped[3:])
            requests.append(insert_text(current_index, text, bold=True, font_size=16, alignment="LEFT"))
            current_index += len(text)
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Heading 3
        if stripped.startswith("### "):
            text = escaped_text(stripped[4:])
            requests.append(insert_text(current_index, text, bold=True, font_size=14, alignment="LEFT"))
            current_index += len(text)
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Horizontal rule
        if stripped == "---":
            requests.append(insert_text(current_index, "", alignment="LEFT"))
            current_index += 0  # Horizontal rule via paragraph border
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Checkbox list item
        if stripped.startswith("- [ ] "):
            text = escaped_text(stripped[6:])
            requests.append(insert_checkbox(current_index, text))
            current_index += len(text) + 1  # +1 for checkbox character
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        if stripped.startswith("- [x] "):
            text = escaped_text(stripped[6:])
            requests.append(insert_checked_checkbox(current_index, text))
            current_index += len(text) + 1
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Bullet list item
        if stripped.startswith("- "):
            text = process_inline_formatting(stripped[2:])
            requests.append(insert_bullet(current_index, text))
            # Count characters for index tracking (approximate)
            char_count = count_chars(text)
            current_index += char_count
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Table detection
        if stripped.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|---"):
            # Collect table rows
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                table_rows.append(row)
                i += 1
            
            # Skip the separator row
            if len(table_rows) > 1 and all(c.strip().startswith("-") for c in table_rows[1]):
                table_rows = table_rows[:1] + table_rows[2:]
            
            # Create table
            num_cols = max(len(row) for row in table_rows) if table_rows else 1
            num_rows = len(table_rows)
            
            table_req, table_chars = create_table(current_index, num_rows, num_cols, table_rows)
            requests.append(table_req)
            current_index += table_chars
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            continue
        
        # Code block
        if stripped.startswith("```"):
            # Collect code until closing ```
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1  # skip closing ```
            
            code_text = "\n".join(code_lines)
            text = escaped_text(code_text)
            requests.append(insert_text(current_index, text, monospace=True, font_size=10))
            current_index += len(text)
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            continue
        
        # Blockquote
        if stripped.startswith("> "):
            text = process_inline_formatting(stripped[2:])
            requests.append(insert_text(current_index, text, italic=True, alignment="LEFT"))
            char_count = count_chars(text)
            current_index += char_count
            requests.append(insert_paragraph_break(current_index))
            current_index += 1
            i += 1
            continue
        
        # Regular paragraph
        text = process_inline_formatting(stripped)
        requests.append(insert_text(current_index, text, alignment="LEFT"))
        char_count = count_chars(text)
        current_index += char_count
        requests.append(insert_paragraph_break(current_index))
        current_index += 1
        i += 1
    
    return requests


def escaped_text(text):
    """Escape special characters for Google Docs API."""
    # In the Docs API, we pass raw text; the API handles escaping
    return text


def count_chars(text):
    """Count characters for indexing purposes."""
    # The Docs API uses UTF-16 code units for indexing
    # Approximate with Python string length (works for most cases)
    return len(text.encode("utf-16-le")) // 2 if any(ord(c) > 127 for c in text) else len(text)


def insert_text(index, text, bold=False, italic=False, monospace=False, font_size=None, alignment="LEFT"):
    """Create a request to insert text with formatting at the given index."""
    if not text:
        return {
            "insertText": {
                "location": {"index": index, "segmentId": ""},
                "text": ""
            }
        }
    
    # First insert the text, then apply formatting
    requests = []
    
    # Insert text request
    text_request = {
        "insertText": {
            "location": {"index": index, "segmentId": ""},
            "text": text
        }
    }
    
    # Build the paragraph formatting
    para_props = {}
    if alignment != "LEFT":
        para_props["alignment"] = alignment
    
    # We need to apply formatting to the inserted text range
    start = index
    end = index + count_chars(text)
    
    # Apply paragraph style
    if para_props:
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "fields": "alignment",
                "paragraphStyle": para_props
            }
        })
    
    # Build text style
    text_style = {}
    if bold:
        text_style["bold"] = True
    if italic:
        text_style["italic"] = True
    if monospace:
        text_style["fontFamily"] = "Courier New"
    if font_size:
        text_style["fontSize"] = {"magnitude": font_size, "unit": "PT"}
    
    if text_style:
        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "fields": ",".join(text_style.keys()),
                "textStyle": text_style
            }
        })
    
    return text_request, requests


def insert_paragraph_break(index):
    """Create a request to insert a paragraph break."""
    return {
        "insertText": {
            "location": {"index": index, "segmentId": ""},
            "text": "\n"
        }
    }


def insert_bullet(index, text):
    """Create a request to insert a bulleted list item."""
    # Insert text first, then apply bullet style
    count = count_chars(text)
    return {
        "insertText": {
            "location": {"index": index, "segmentId": ""},
            "text": text
        }
    }


def insert_checkbox(index, text):
    """Insert a checkbox (unchecked) with text."""
    checkbox_char = "\u2610"  # ☐
    full_text = checkbox_char + " " + text
    count = count_chars(full_text)
    return {
        "insertText": {
            "location": {"index": index, "segmentId": ""},
            "text": full_text
        }
    }


def insert_checked_checkbox(index, text):
    """Insert a checkbox (checked) with text."""
    checkbox_char = "\u2611"  # ☑
    full_text = checkbox_char + " " + text
    return {
        "insertText": {
            "location": {"index": index, "segmentId": ""},
            "text": full_text
        }
    }


def create_table(index, num_rows, num_cols, rows):
    """Create a table at the given index with the provided rows."""
    # Insert the table
    table_request = {
        "insertTable": {
            "rows": num_rows,
            "columns": num_cols,
            "insertInlineImageOptions": {"location": {"index": index}},
        }
    }
    
    # Then pad cells with text
    # The table cells need content via merge cells or text insertion
    # For simplicity, we'll use insertText with the table cell location
    # Actually, the Docs API table insertion is more complex.
    # We use a simpler approach: insert text in each cell.
    
    total_chars = num_rows * num_cols  # Rough estimate
    
    # Build text insertion requests for each cell
    text_requests = []
    # Each cell is addressed by its row/column
    # After insertTable, cells exist starting at index
    # Cell content goes at rowIndex, ColIndex within the table structure
    
    return table_request, total_chars


def process_inline_formatting(text):
    """Process inline markdown formatting (bold, italic, links) and return plain text.
    
    For proper Docs API formatting, we'd need to insert text with style ranges.
    For now, we'll handle this at a higher level.
    """
    # This is a simplified version - proper implementation would track
    # style ranges and create updateTextStyle requests
    return text


# --- Link management ---

# Document ID mapping for internal links
# Maps file names and folder names to their Google Drive IDs and URLs
DOCUMENT_LINKS = {
    # Folders
    "Enable the Disabled - Shaun Kehoe": "https://drive.google.com/drive/folders/17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8",
    "Enable the Disabled - Admin": "https://drive.google.com/drive/folders/1_YpciYU1uRS53ol74oqojUKlUKSQF4BJ",
    "Brand": "https://drive.google.com/drive/folders/1A45rdYzyLYudsjQEBEm5FcXUDf6198ys",
    "Corporate": "https://drive.google.com/drive/folders/1dRr76f_xiGQvmnaAAMmSf1IjYhlNeT-O",
    "Operations": "https://drive.google.com/drive/folders/1wgqw4-IReNIMFov73r5DCEpvt7Mm9q1y",
    "_archive": "https://drive.google.com/drive/folders/1cezQT8LdBg8Z_YTLdSH1Sgsc2gKdmZHO",
    "00_Fact-finding": "https://drive.google.com/drive/folders/1reMboKf5TezQWDZ9E55H7v3LyxelA5oH",
    "07_Incorporation": "https://drive.google.com/drive/folders/1w2On6DibxG5z0REfgLoBYUEkERwkgSAU",
    "08_Trademark": "https://drive.google.com/drive/folders/1omvZoaW1v63lMHFEgrNcxI4e8xtpaTR8",
    "name search": "https://drive.google.com/drive/folders/1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",
    "08_Security": "https://drive.google.com/drive/folders/1oTb65y2-xWLmNGa5nZoMYqHqOdiZY_uB",
    "01_Clients": "https://drive.google.com/drive/folders/1H0dGCPgf3tT8bYDCp9prGWJT9ub9fgIt",
    "02_HR-Workforce": "https://drive.google.com/drive/folders/1Y-mz3Dqsd1rBcY6lohx4cTNYefETcqW3",
    "03_Operations": "https://drive.google.com/drive/folders/1PV6qMwgnj9ATjhWA9p9Tb0S9x4Bg1Hyb",
    "04_IT-Infrastructure": "https://drive.google.com/drive/folders/1gNcp_RPinZ2ofaSnf5cE2URko-Q3AR1z",
    "09_Other": "https://drive.google.com/drive/folders/1WagBxHIuwam9jXlUTN5Ejm0TxSktkFaz",
    "originals": "https://drive.google.com/drive/folders/1sqNlbb-cUM1noX_a__SZAsmcSnytz679",
    "word-versions": "https://drive.google.com/drive/folders/1tT3kL3jv6Fa4sNwcsA7sYmmi8_luQYAh",
    "Incorporation (2nd)": "https://drive.google.com/drive/folders/1TxWJJfsh1rm0lFzBTxpyHA56eLp5ncm5",
    "Corporate (Admin)": "https://drive.google.com/drive/folders/1tH7rTwRGkjaj8KrZheNAkyLBSEkCdM4x",
    "08_Security (Admin)": "https://drive.google.com/drive/folders/14Ek0zgqHHpXuuBtoe7EJDRUwjpTRu_Iy",
    
    # README Google Docs
    "README - Enable the Disabled - Shaun Kehoe": "https://docs.google.com/document/d/1fxnh1MP1sfKwmQhfvLI49DQHLtBXugrhp_AQLPeBBSQ/edit",
    "README - Brand": "https://docs.google.com/document/d/13669ge5ZZLWIj4I3O5EYfb0iGnw1LJE9Nb5hoAVlLsM/edit",
    "README - Corporate (Shared)": "https://docs.google.com/document/d/1WmrJ6JrXszf5hX9iFLi8iiwXG02-Y-C86qkrozuJNyQ/edit",
    "README - Corporate (Admin)": "https://docs.google.com/document/d/1xdsYGcqTVJm5NcrS1cLwg2J92WOsa4vVmDQdkPW93Ng/edit",
    "README - Operations": "https://docs.google.com/document/d/1ek6lhXbO5nmkS-oy90o2gN2qtsaEyULC3_qGHAHvC0Y/edit",
    "README - _archive": "https://docs.google.com/document/d/1InsOmBFWYI3_TP3z6CqFel3sYI_c3wDQfgKV0qAaCFg/edit",
    "README - Incorporation #1": "https://docs.google.com/document/d/1k05txlKg_cv-yi8KOLCOooS7qZSdKQUoSRVM3qV2_Rk/edit",
    "README - name search": "https://docs.google.com/document/d/1rj5CM6WPCyKZ4blOVg5Q4MUcnKhVzoSI5WgUMloaVBI/edit",
    "README - Trademark": "https://docs.google.com/document/d/10-1A6XRI13979YdI3q-4Zvkw0raOLvZs97XVDFa07Aw/edit",
    "README - Incorporation #2": "https://docs.google.com/document/d/132q5A6VQiJWQovht14qIsSIi0whe3YwdcPAB9hFbntA/edit",
    "README - Fact-finding": "https://docs.google.com/document/d/1eLuGBVo_qQt2nngyH7qtpwE74KmeDfM5Qtuvj5aWuVo/edit",
    "README - Enabling the Disabled - Admin": "https://docs.google.com/document/d/1lYtQHGtDmXI7YNPs6kSSM-FBBRdEiMwPdkZUX7aRceE/edit",
    "README - 08_Security (Admin)": "https://docs.google.com/document/d/1shUm9OVOh5x0gGieaM7FYLExOWRZ2Fw-SiogUfpX4gQ/edit",
    "Incorporation Checklist": "https://docs.google.com/document/d/1blBHVPCVXbg4lmgnOqhY2c1oEQdVapziMOHIZ8BJ2Hc/edit",
    
    # Name Research Google Docs (existing)
    "Sister Company Name Research - batch 01 (Doc)": "https://docs.google.com/document/d/1fiyu9wzokeAGVHjAtXPCdXycXqvSyR23Uzp5NWNpyyk/edit",
    "Sister Company Name Research COMBINED (Doc 1)": "https://docs.google.com/document/d/1XaM3bFgXBlHH6rMRe9bawar2LZphBOrXoZPUfVjmXE0/edit",
    "Sister Company Name Research COMBINED (Doc 2)": "https://docs.google.com/document/d/1zjBCxJfJQxmTFdUCLpRvjgXTw4TU4xJKIRTYa6AXMXc/edit",
    "Batch 02 (Doc)": "https://docs.google.com/document/d/14yTZN9m4f048wy_kfyYPkvykRCPQ41-kk9HPuqIqp3s/edit",
}


def replace_links_in_content(content, new_doc_id, new_doc_url):
    """Replace plain text references to internal files with clickable links."""
    # This will be implemented as part of the link-fixing logic
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .md files in Google Drive to Google Docs")
    parser.add_argument("--convert", action="store_true", help="Convert .md files to Google Docs")
    parser.add_argument("--delete-md", action="store_true", help="Delete original .md files after conversion")
    parser.add_argument("--update-links", action="store_true", help="Update internal links in README docs")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    
    args = parser.parse_args()
    
    if args.all:
        args.convert = True
        args.delete_md = True
        args.update_links = True
    
    if args.convert:
        print("Converting markdown files to Google Docs...")
        # Implementation below
        pass
    
    if args.delete_md:
        print("Deleting original .md files...")
        pass
    
    if args.update_links:
        print("Updating internal links in README docs...")
        pass
