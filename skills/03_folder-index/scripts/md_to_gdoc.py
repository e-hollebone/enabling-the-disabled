#!/usr/bin/env python3
"""
Simple markdown-to-Google-Docs converter for the Enable the Disabled project.

For each .md file in Drive:
  1. Download the markdown content
  2. Convert to properly formatted Google Docs (headings, bold, tables, bullets, checkboxes, links)
  3. Create or update the corresponding Google Doc
  4. Delete the .md file from Drive

All internal references (folder/file names, IDs in backticks) are replaced
with clickable Google Drive links.
"""

import os
import re
import sys
import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

PROFILE_DIR = os.path.expanduser("~/.hermes/profiles/fitness-strategist")
TOKEN_PATH = os.path.join(PROFILE_DIR, "google_token.json")
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

# Master ID registry for link replacement
REGISTRY = {
    # Folders
    "Enable the Disabled - Shaun Kehoe": "17Sav0cJmDafe8DDvHKKq0OT1awzQ0ik8",
    "Enable the Disabled - Admin": "1_YpciYU1uRS53ol74oqojUKlUKSQF4BJ",
    "Brand": "1A45rdYzyLYudsjQEBEm5FcXUDf6198ys",
    "Corporate": "1dRr76f_xiGQvmnaAAMmSf1IjYhlNeT-O",
    "Corporate (Admin)": "1tH7rTwRGkjaj8KrZheNAkyLBSEkCdM4x",
    "Operations": "1wgqw4-IReNIMFov73r5DCEpvt7Mm9q1y",
    "00_Fact-finding": "1reMboKf5TezQWDZ9E55H7v3LyxelA5oH",
    "07_Incorporation": "1w2On6DibxG5z0REfgLoBYUEkERwkgSAU",
    "08_Trademark": "1omvZoaW1v63lMHFEgrNcxI4e8xtpaTR8",
    "name search": "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",
    "01_Clients": "1H0dGCPgf3tT8bYDCp9prGWJT9ub9fgIt",
    "02_HR-Workforce": "1Y-mz3Dqsd1rBcY6lohx4cTNYefETcqW3",
    "03_Operations": "1PV6qMwgnj9ATjhWA9p9Tb0S9x4Bg1Hyb",
    "04_IT-Infrastructure": "1gNcp_RPinZ2ofaSnf5cE2URko-Q3AR1z",
    "08_Security (Shared)": "1oTb65y2-xWLmNGa5nZoMYqHqOdiZY_uB",
    "08_Security (Admin)": "14Ek0zgqHHpXuuBtoe7EJDRUwjpTRu_Iy",
    "09_Other": "1WagBxHIuwam9jXlUTN5Ejm0TxSktkFaz",
    "_archive": "1cezQT8LdBg8Z_YTLdSH1Sgsc2gKdmZHO",
    "originals": "1sqNlbb-cUM1noX_a__SZAsmcSnytz679",
    "word-versions": "1tT3kL3jv6Fa4sNwcsA7sYmmi8_luQYAh",
    "Incorporation (2nd)": "1TxWJJfsh1rm0lFzBTxpyHA56eLp5ncm5",
    # Google Docs
    "README - Enable the Disabled - Shaun Kehoe": "1fxnh1MP1sfKwmQhfvLI49DQHLtBXugrhp_AQLPeBBSQ",
    "README - Brand": "13669ge5ZZLWIj4I3O5EYfb0iGnw1LJE9Nb5hoAVlLsM",
    "README - Corporate (Shared)": "1WmrJ6JrXszf5hX9iFLi8iiwXG02-Y-C86qkrozuJNyQ",
    "README - Corporate (Admin)": "1xdsYGcqTVJm5NcrS1cLwg2J92WOsa4vVmDQdkPW93Ng",
    "README - Operations": "1ek6lhXbO5nmkS-oy90o2gN2qtsaEyULC3_qGHAHvC0Y",
    "README - _archive": "1InsOmBFWYI3_TP3z6CqFel3sYI_c3wDQfgKV0qAaCFg",
    "README - Incorporation #1": "1k05txlKg_cv-yi8KOLCOooS7qZSdKQUoSRVM3qV2_Rk",
    "README - name search": "1rj5CM6WPCyKZ4blOVg5Q4MUcnKhVzoSI5WgUMloaVBI",
    "README - Trademark": "10-1A6XRI13979YdI3q-4Zvkw0raOLvZs97XVDFa07Aw",
    "README - Incorporation #2": "132q5A6VQiJWQovht14qIsSIi0whe3YwdcPAB9hFbntA",
    "README - Fact-finding": "1eLuGBVo_qQt2nngyH7qtpwE74KmeDfM5Qtuvj5aWuVo",
    "README - 08_Security (Admin)": "1shUm9OVOh5x0gGieaM7FYLExOWRZ2Fw-SiogUfpX4gQ",
    "README - Enabling the Disabled - Admin": "1lYtQHGtDmXI7YNPs6kSSM-FBBRdEiMwPdkZUX7aRceE",
    "Incorporation Checklist": "1blBHVPCVXbg4lmgnOqhY2c1oEQdVapziMOHIZ8BJ2Hc",
    "Sister Co Name Research - batch 01 (Doc)": "1fiyu9wzokeAGVHjAtXPCdXycXqvSyR23Uzp5NWNpyyk",
    "Sister Co Name Research - batch 02 (Doc)": "14yTZN9m4f048wy_kfyYPkvykRCPQ41-kk9HPuqIqp3s",
    "Sister Co Name Research - combined (Doc 1)": "1XaM3bFgXBlHH6rMRe9bawar2LZphBOrXoZPUfVjmXE0",
    "Sister Co Name Research - combined (Doc 2)": "1zjBCxJfJQxmTFdUCLpRvjgXTw4TU4xJKIRTYa6AXMXc",
}


def drive_url(item_id, item_type):
    """Build a Drive URL from an ID and type."""
    if item_type == "folder":
        return f"https://drive.google.com/drive/folders/{item_id}"
    elif item_type == "doc":
        return f"https://docs.google.com/document/d/{item_id}/edit"
    elif item_type == "sheet":
        return f"https://docs.google.com/spreadsheets/d/{item_id}/edit"
    elif item_type == "pdf":
        return f"https://drive.google.com/file/d/{item_id}/view"
    else:
        return f"https://drive.google.com/file/d/{item_id}/view"


def replace_links(text):
    """Replace `Name` and `ID` backtick patterns with markdown links."""
    for name, item_id in REGISTRY.items():
        # Determine type
        is_doc = item_id.startswith("1") and 40 <= len(item_id) <= 50 and not item_id.startswith("1Y") and not item_id.startswith("1P") and not item_id.startswith("1tT") and not item_id.startswith("1s") and not item_id.startswith("1q0") and not item_id.startswith("1aj") and not item_id.startswith("1zS") and not item_id.startswith("1_T") and not item_id.startswith("1n") and not item_id.startswith("1Q") and not item_id.startswith("1m2") and not item_id.startswith("1s") and not item_id.startswith("1W") and not item_id.startswith("1m") and not item_id.startswith("1i")
        
        # Just use doc type for known doc IDs, folder for folder IDs
        item_type = "folder"
        if name.startswith("README") or name in ["Incorporation Checklist", "Sister Co Name Research - batch 01 (Doc)", "Sister Co Name Research - batch 02 (Doc)", "Sister Co Name Research - combined (Doc 1)", "Sister Co Name Research - combined (Doc 2)"]:
            item_type = "doc"
        elif name.endswith(".png") or name.endswith(".pdf"):
            item_type = "pdf"
        elif "Inventory" in name:
            item_type = "sheet"
        
        url = drive_url(item_id, item_type)
        
        # Replace `Name` with [Name](URL)
        escaped = re.escape(name)
        text = re.sub(
            rf'`({escaped})`',
            rf'[{name}]({url})',
            text
        )
        
        # Replace `ID` with [ID](URL)
        escaped_id = re.escape(item_id)
        text = re.sub(
            rf'`({escaped_id})`',
            rf'[{item_id}]({url})',
            text
        )
    
    return text


def get_creds():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_PATH, "w") as f:
                f.write(creds.to_json())
        else:
            print("ERROR: No valid credentials. Run setup.py first.")
            sys.exit(1)
    return creds


def download_md(drive, file_id):
    request = drive.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    content = fh.getvalue().decode("utf-8")
    return content


def md_to_html(md_text):
    """Convert markdown to HTML using the markdown library."""
    # Replace internal links first
    md_text = replace_links(md_text)
    
    # Configure markdown extensions
    md = markdown.Markdown(extensions=[
        "tables",
        "fenced_code",
        "toc",
        "nl2br",
        "sane_lists",
    ])
    
    html = md.convert(md_text)
    return html


def count_utf16(text):
    return len(text.encode("utf-16-le")) // 2


def create_formatted_doc(docs, title, parent_id, html_content):
    """Create a Google Doc with content formatted from HTML.
    
    Uses a simple approach: insert text with appropriate styles.
    For full fidelity, we'd parse the HTML, but for this project
    the markdown structure is well-defined.
    """
    # Create the document
    body = {"title": title}
    if parent_id:
        body["parents"] = [parent_id]
    doc = docs.documents().create(body=body).execute()
    doc_id = doc["documentId"]
    
    # For now, use a simple text insertion approach
    # Parse the HTML and generate Docs API requests
    requests = html_to_docs_requests(html_content)
    
    if requests:
        docs.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()
    
    return doc_id


def html_to_docs_requests(html):
    """Convert HTML to Google Docs API batchUpdate requests."""
    # Parse HTML using regex (simple approach for well-structured markdown output)
    requests = []
    cursor = 2  # Docs index starts at 2
    
    # Strip HTML tags and convert to styled text
    # This is a simplified parser - handles the common markdown-to-HTML patterns
    
    pos = 0
    while pos < len(html):
        # Find next HTML tag
        tag_start = html.find("<", pos)
        if tag_start == -1:
            # Remaining text
            text = html[pos:]
            if text.strip():
                text = unescape_html(text)
                requests.extend(insert_styled_text(cursor, text))
                cursor += count_utf16(text)
            break
        
        # Process text before tag
        text_before = html[pos:tag_start]
        if text_before.strip():
            text = unescape_html(text_before)
            requests.extend(insert_styled_text(cursor, text))
            cursor += count_utf16(text)
        
        # Find the tag
        tag_end = html.find(">", tag_start)
        if tag_end == -1:
            break
        
        tag_content = html[tag_start + 1:tag_end]
        pos = tag_end + 1
        
        # Parse tag
        if tag_content.startswith("/"):
            # Closing tag
            continue
        elif tag_content.startswith("br"):
            requests.append(insert_newline(cursor))
            cursor += 1
        elif tag_content.startswith("h1"):
            # Read until </h1>
            content_start = pos
            close_tag = html.find("</h1>", pos)
            if close_tag == -1:
                break
            content = html[content_start:close_tag].strip()
            content = strip_tags(content)
            content = unescape_html(content)
            text_utf16 = count_utf16(content)
            
            requests.append(insert_text(cursor, content))
            requests.append(insert_newline(cursor + text_utf16))
            end = cursor + text_utf16 + 1
            requests.append(set_named_style(cursor, end, "HEADING1"))
            cursor = end
            pos = close_tag + 5
        elif tag_content.startswith("h2"):
            content_start = pos
            close_tag = html.find("</h2>", pos)
            if close_tag == -1:
                break
            content = html[content_start:close_tag].strip()
            content = strip_tags(content)
            content = unescape_html(content)
            if content:
                text_utf16 = count_utf16(content)
                requests.append(insert_text(cursor, content))
                requests.append(insert_newline(cursor + text_utf16))
                end = cursor + text_utf16 + 1
                requests.append(set_named_style(cursor, end, "HEADING2"))
                cursor = end
            pos = close_tag + 5
        elif tag_content.startswith("h3"):
            content_start = pos
            close_tag = html.find("</h3>", pos)
            if close_tag == -1:
                break
            content = html[content_start:close_tag].strip()
            content = strip_tags(content)
            content = unescape_html(content)
            if content:
                text_utf16 = count_utf16(content)
                requests.append(insert_text(cursor, content))
                requests.append(insert_newline(cursor + text_utf16))
                end = cursor + text_utf16 + 1
                requests.append(set_named_style(cursor, end, "HEADING3"))
                cursor = end
            pos = close_tag + 5
        elif tag_content.startswith("p"):
            content_start = pos
            close_tag = html.find("</p>", pos)
            if close_tag == -1:
                break
            content = html[content_start:close_tag].strip()
            content = unescape_html(content)
            
            # Process inline formatting
            styled_parts = parse_inline_html(content)
            text_offset = cursor
            
            for part in styled_parts:
                part_text = part["text"]
                part_utf16 = count_utf16(part_text)
                
                if part_text:
                    requests.append(insert_text(cursor, part_text))
                    if part.get("bold"):
                        requests.append(set_text_style(cursor, cursor + part_utf16, {"bold": True}))
                    if part.get("italic"):
                        requests.append(set_text_style(cursor, cursor + part_utf16, {"italic": True}))
                    if part.get("code"):
                        requests.append(set_text_style(cursor, cursor + part_utf16, 
                            {"fontFamily": "Courier New", "fontSize": {"magnitude": 10, "unit": "PT"}}))
                    if part.get("link"):
                        requests.append(set_text_style(cursor, cursor + part_utf16, 
                            {"link": {"url": part["link"]}}))
                    cursor += part_utf16
            
            requests.append(insert_newline(cursor))
            cursor += 1
            pos = close_tag + 4
        elif tag_content.startswith("ul"):
            # Collect list items
            items = []
            list_end = html.find("</ul>", pos)
            if list_end == -1:
                break
            list_content = html[pos:list_end]
            
            # Extract <li> items
            li_pattern = r"<li>(.*?)</li>"
            for m in re.finditer(li_pattern, list_content, re.DOTALL):
                item_html = m.group(1).strip()
                item_text = strip_tags(item_html)
                item_text = unescape_html(item_text)
                if item_text:
                    styled_parts = parse_inline_html(item_text)
                    start = cursor
                    for part in styled_parts:
                        part_text = part["text"]
                        part_utf16 = count_utf16(part_text)
                        if part_text:
                            requests.append(insert_text(cursor, part_text))
                            if part.get("bold"):
                                requests.append(set_text_style(cursor, cursor + part_utf16, {"bold": True}))
                            if part.get("italic"):
                                requests.append(set_text_style(cursor, cursor + part_utf16, {"italic": True}))
                            if part.get("link"):
                                requests.append(set_text_style(cursor, cursor + part_utf16, {"link": {"url": part["link"]}}))
                            cursor += part_utf16
                    requests.append(insert_newline(cursor))
                    cursor += 1
                    
                    # Apply bullet to the paragraph
                    requests.append(create_bullets(start, cursor, "BULLET_DISC"))
            
            pos = list_end + 5
        elif tag_content.startswith("ol"):
            list_end = html.find("</ol>", pos)
            if list_end == -1:
                break
            list_content = html[pos:list_end]
            
            li_pattern = r"<li>(.*?)</li>"
            for m in re.finditer(li_pattern, list_content, re.DOTALL):
                item_html = m.group(1).strip()
                item_text = strip_tags(item_html)
                item_text = unescape_html(item_text)
                if item_text:
                    styled_parts = parse_inline_html(item_text)
                    start = cursor
                    for part in styled_parts:
                        part_text = part["text"]
                        part_utf16 = count_utf16(part_text)
                        if part_text:
                            requests.append(insert_text(cursor, part_text))
                            if part.get("link"):
                                requests.append(set_text_style(cursor, cursor + part_utf16, {"link": {"url": part["link"]}}))
                            cursor += part_utf16
                    requests.append(insert_newline(cursor))
                    cursor += 1
                    requests.append(create_bullets(start, cursor, "NUMBER"))
            
            pos = list_end + 5
        elif tag_content.startswith("code"):
            # Code block
            close_tag = html.find("</code>", pos)
            if close_tag == -1:
                break
            code_content = html[pos:close_tag]
            code_content = unescape_html(code_content)
            code_utf16 = count_utf16(code_content)
            requests.append(insert_text(cursor, code_content))
            requests.append(insert_newline(cursor + code_utf16))
            end = cursor + code_utf16 + 1
            requests.append(set_text_style(cursor, end, 
                {"fontFamily": "Courier New", "fontSize": {"magnitude": 10, "unit": "PT"}}))
            cursor = end
            pos = close_tag + 7
        elif tag_content.startswith("pre"):
            close_tag = html.find("</pre>", pos)
            if close_tag == -1:
                break
            code_content = html[pos:close_tag]
            # Strip inner <code> tags if present
            code_content = strip_tags(code_content)
            code_content = unescape_html(code_content)
            code_utf16 = count_utf16(code_content)
            requests.append(insert_text(cursor, code_content))
            requests.append(insert_newline(cursor + code_utf16))
            end = cursor + code_utf16 + 1
            requests.append(set_text_style(cursor, end, 
                {"fontFamily": "Courier New", "fontSize": {"magnitude": 10, "unit": "PT"}}))
            cursor = end
            pos = close_tag + 6
        elif tag_content.startswith("blockquote"):
            close_tag = html.find("</blockquote>", pos)
            if close_tag == -1:
                break
            quote_content = html[pos:close_tag]
            # Extract paragraph text
            para_match = re.search(r"<p>(.*?)</p>", quote_content, re.DOTALL)
            if para_match:
                quote_text = strip_tags(para_match.group(1))
                quote_text = unescape_html(quote_text)
            else:
                quote_text = strip_tags(quote_content)
                quote_text = unescape_html(quote_text)
            
            if quote_text:
                quote_utf16 = count_utf16(quote_text)
                requests.append(insert_text(cursor, quote_text))
                requests.append(insert_newline(cursor + quote_utf16))
                end = cursor + quote_utf16 + 1
                requests.append(set_text_style(cursor, end, {"italic": True}))
                requests.append(set_paragraph_style(cursor, end, {
                    "marginStart": {"magnitude": 20, "unit": "PT"}
                }))
                cursor = end
            pos = close_tag + 13
        elif tag_content.startswith("table"):
            # Parse table
            table_end = html.find("</table>", pos)
            if table_end == -1:
                break
            table_html = html[pos:table_end]
            
            # Extract rows
            rows = []
            tr_pattern = r"<tr>(.*?)</tr>"
            for tr_match in re.finditer(tr_pattern, table_html, re.DOTALL):
                row_html = tr_match.group(1)
                cells = []
                td_pattern = r"<t[dh]>(.*?)</t[dh]>"
                for td_match in re.finditer(td_pattern, row_html, re.DOTALL):
                    cell_text = strip_tags(td_match.group(1))
                    cell_text = unescape_html(cell_text)
                    cells.append(cell_text)
                rows.append(cells)
            
            if rows:
                num_cols = max(len(r) for r in rows)
                num_rows = len(rows)
                
                # Pad rows
                for row in rows:
                    while len(row) < num_cols:
                        row.append("")
                
                # Insert table
                requests.append({
                    "insertTable": {
                        "rows": num_rows,
                        "columns": num_cols,
                        "location": {"segmentId": "", "index": cursor},
                    }
                })
                
                # Fill cells
                for ri, row in enumerate(rows):
                    for ci, cell_text in enumerate(row):
                        cell_idx = cursor + 1 + ri * num_cols + ci + 1
                        if cell_text:
                            cell_utf16 = count_utf16(cell_text)
                            requests.append(insert_text(cell_idx, cell_text))
                            
                            # Bold first row (headers)
                            if ri == 0:
                                requests.append(set_text_style(cell_idx, cell_idx + cell_utf16, {"bold": True}))
                
                cursor = cursor + 1 + num_rows * num_cols + 1
            
            pos = table_end + 8
        elif tag_content.startswith("hr"):
            # Horizontal rule - insert a line break with border
            requests.append(insert_text(cursor, ""))
            requests.append(insert_newline(cursor))
            requests.append(set_paragraph_style(cursor, cursor + 1, {
                "borderStyle": {
                    "width": {"magnitude": 1, "unit": "PT"},
                    "dashStyle": "SOLID_MED",
                }
            }))
            cursor += 1
            pos = tag_end + 1
        elif tag_content.startswith("a "):
            # This is handled by parse_inline_html
            continue
        else:
            # Skip unknown tags
            continue
    
    return requests


def parse_inline_html(text):
    """Parse inline HTML (bold, italic, code, links) and return styled parts."""
    parts = []
    pos = 0
    
    # Pattern for inline elements
    inline_pattern = r'(<strong>|</strong>|<em>|</em>|<code>|</code>|<a\s+[^>]*>|</a>)'
    
    while pos < len(text):
        match = re.search(inline_pattern, text[pos:])
        if not match:
            # Remaining plain text
            remaining = text[pos:]
            if remaining:
                parts.append({"text": unescape_html(remaining)})
            break
        
        # Text before the match
        before = text[pos:pos + match.start()]
        if before:
            parts.append({"text": unescape_html(before)})
        
        tag = match.group(1)
        pos += match.end()
        
        if tag == "<strong>":
            # Find closing tag
            close = text.find("</strong>", pos)
            if close == -1:
                break
            inner = text[pos:close]
            inner = unescape_html(inner)
            parts.append({"text": inner, "bold": True})
            pos = close + len("</strong>")
        elif tag == "<em>":
            close = text.find("</em>", pos)
            if close == -1:
                break
            inner = text[pos:close]
            inner = unescape_html(inner)
            parts.append({"text": inner, "italic": True})
            pos = close + len("</em>")
        elif tag == "<code>":
            close = text.find("</code>", pos)
            if close == -1:
                break
            inner = text[pos:close]
            inner = unescape_html(inner)
            parts.append({"text": inner, "code": True})
            pos = close + len("</code>")
        elif tag.startswith("<a "):
            # Extract href
            href_match = re.search(r'href="([^"]*)"', tag)
            href = href_match.group(1) if href_match else ""
            
            close = text.find("</a>", pos)
            if close == -1:
                break
            inner = text[pos:close]
            inner = unescape_html(inner)
            parts.append({"text": inner, "link": href})
            pos = close + len("</a>")
    
    # Merge consecutive plain text parts
    merged = []
    for part in parts:
        if merged and not any(part.get(k) for k in ["bold", "italic", "code", "link"]):
            if not any(merged[-1].get(k) for k in ["bold", "italic", "code", "link"]):
                merged[-1]["text"] += part["text"]
            else:
                merged.append(part)
        else:
            merged.append(part)
    
    return merged


def strip_tags(text):
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text)


def unescape_html(text):
    """Convert HTML entities to characters."""
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&amp;", "&")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&#x27;", "'")
    text = text.replace("&#x2F;", "/")
    # Handle emoji entities
    text = re.sub(r'&#x([0-9A-Fa-f]+);', lambda m: chr(int(m.group(1), 16)), text)
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    return text


def insert_text(cursor, text):
    return {
        "insertText": {
            "location": {"segmentId": "", "index": cursor},
            "text": text,
        }
    }


def insert_newline(cursor):
    return {
        "insertText": {
            "location": {"segmentId": "", "index": cursor},
            "text": "\n",
        }
    }


def set_text_style(start, end, style):
    fields = ",".join(style.keys())
    return {
        "updateTextStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "fields": fields,
            "textStyle": style,
        }
    }


def set_named_style(start, end, style_type):
    return {
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "fields": "namedStyleType",
            "paragraphStyle": {"namedStyleType": style_type},
        }
    }


def set_paragraph_style(start, end, style):
    return {
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "fields": ",".join(style.keys()),
            "paragraphStyle": style,
        }
    }


def create_bullets(start, end, preset):
    return {
        "createParagraphBullets": {
            "range": {"startIndex": start, "endIndex": end},
            "bulletPreset": preset,
        }
    }


def update_doc_content(docs, doc_id, html_content):
    """Clear and repopulate a Google Doc with formatted content from HTML."""
    # Get current doc
    doc = docs.documents().get(documentId=doc_id).execute()
    
    # Find last index
    last_index = None
    for elem in doc.get("body", {}).get("content", []):
        if "endIndex" in elem:
            last_index = elem["endIndex"]
    
    requests = []
    
    # Clear existing content
    if last_index and last_index > 2:
        requests.append({
            "deleteContentRange": {
                "range": {"startIndex": 2, "endIndex": last_index - 1}
            }
        })
    
    # Generate formatting requests
    content_requests = html_to_docs_requests(html_content)
    requests.extend(content_requests)
    
    if requests:
        docs.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert .md files in Google Drive to properly formatted Google Docs"
    )
    parser.add_argument("--convert", action="store_true")
    parser.add_argument("--delete-md", action="store_true")
    parser.add_argument("--update-readmes", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    
    args = parser.parse_args()
    
    if args.all:
        args.convert = True
        args.delete_md = True
        args.update_readmes = True
    
    creds = get_creds()
    drive = build("drive", "v3", credentials=creds)
    docs = build("docs", "v1", credentials=creds)
    
    # === Step 1: Convert .md files to Google Docs ===
    if args.convert:
        print("=" * 60)
        print("STEP 1: Converting .md files to Google Docs")
        print("=" * 60)
        
        # Files to convert: (md_id, new_doc_id, parent_id, doc_title, is_new)
        files = [
            # Batch 01: update existing Doc
            ("1YFE8EqQyNJVKKLW6IrBfXNplgH3nLCSp", "1fiyu9wzokeAGVHjAtXPCdXycXqvSyR23Uzp5NWNpyyk",
             "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",
             "Sister Company Name Research - Enable the Disabled - 2026-09-09", False),
            # Batch 02: update existing Doc
            ("1ajDh20i9sgsrjvaogJY94urSaRpRmFGc", "14yTZN9m4f048wy_kfyYPkvykRCPQ41-kk9HPuqIqp3s",
             "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",
             "Sister Company Name Research - Enable the Disabled - 2026-09-09 - Batch 02", False),
            # Batch 03: need to create new Doc (no existing Doc for batch 03 alone)
            ("1q06wAaH_-0hAgrPoOJ0kN_inbwiBCoo-", None,
             "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",
             "Sister Company Name Research - Enable the Disabled - 2026-09-09 - Batch 03", True),
            # Combined in name search: update existing Doc (1zj...)
            ("1_PptdlLnVPNSSQePGayS0W4-C2Czimy_", "1zjBCxJfJQxmTFdUCLpRvjgXTw4TU4xJKIRTYa6AXMXc",
             "1eLqAzm2dZXpj7_YiHi6XGplIOFJT2f8G",
             "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09", False),
            # Combined in 07_Incorporation: update existing Doc (1XaM...)
            ("1zSUPQVjD42ES8LPbNmynR7C79zWBLnwl", "1XaM3bFgXBlHH6rMRe9bawar2LZphBOrXoZPUfVjmXE0",
             "1w2On6DibxG5z0REfgLoBYUEkERwkgSAU",
             "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09", False),
        ]
        
        for md_id, target_doc_id, parent_id, doc_title, is_new in files:
            try:
                md_content = download_md(drive, md_id)
                print(f"\n  Source .md: {doc_title}")
                print(f"  Size: {len(md_content)} chars")
                
                html_content = md_to_html(md_content)
                print(f"  HTML size: {len(html_content)} chars")
                
                if args.dry_run:
                    print(f"  [DRY RUN] Would {'create' if is_new else 'update'} doc: {doc_title}")
                else:
                    if is_new:
                        new_id = create_formatted_doc(docs, doc_title, parent_id, html_content)
                        print(f"  Created new Google Doc: {new_id}")
                        # Update registry
                        REGISTRY[f"Sister Co Name Research - batch 03 (Doc)"] = new_id
                    else:
                        update_doc_content(docs, target_doc_id, html_content)
                        # Move to correct parent if needed
                        doc_meta = drive.files().get(
                            fileId=target_doc_id, fields="parents"
                        ).execute()
                        current_parents = doc_meta.get("parents", [])
                        if parent_id not in current_parents:
                            drive.files().update(
                                fileId=target_doc_id,
                                addParents=parent_id,
                                removeParents=",".join(current_parents),
                                fields="id, parents"
                            ).execute()
                        print(f"  Updated Google Doc: {target_doc_id}")
                
            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
    
    # === Step 2: Delete .md files ===
    if args.delete_md:
        print("\n" + "=" * 60)
        print("STEP 2: Deleting original .md files from Drive")
        print("=" * 60)
        
        md_files = [
            ("1YFE8EqQyNJVKKLW6IrBfXNplgH3nLCSp", "Sister Company Name Research - Enable the Disabled - 2026-09-09.md"),
            ("1ajDh20i9sgsrjvaogJY94urSaRpRmFGc", "Sister Company Name Research - Enable the Disabled - 2026-09-09-Batch-02.md"),
            ("1q06wAaH_-0hAgrPoOJ0kN_inbwiBCoo-", "Sister Company Name Research Batch-03 - Enable the Disabled - 2026-09-09.md"),
            ("1_PptdlLnVPNSSQePGayS0W4-C2Czimy_", "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09.md (name search)"),
            ("1zSUPQVjD42ES8LPbNmynR7C79zWBLnwl", "Sister Company Name Research COMBINED - Enable the Disabled - 2026-09-09.md (07_Incorporation)"),
        ]
        
        for md_id, name in md_files:
            if args.dry_run:
                print(f"  [DRY RUN] Would delete: {name}")
            else:
                try:
                    drive.files().delete(fileId=md_id).execute()
                    print(f"  Deleted: {name}")
                except Exception as e:
                    print(f"  ERROR deleting {name}: {e}")
    
    # === Step 3: Reformat README docs ===
    if args.update_readmes:
        print("\n" + "=" * 60)
        print("STEP 3: Reformatting README docs from markdown body to proper Docs")
        print("=" * 60)
        
        readme_docs = [
            ("1fxnh1MP1sfKwmQhfvLI49DQHLtBXugrhp_AQLPeBBSQ", "README - Enable the Disabled - Shaun Kehoe"),
            ("1WmrJ6JrXszf5hX9iFLi8iiwXG02-Y-C86qkrozuJNyQ", "README - Corporate (Shared)"),
            ("13669ge5ZZLWIj4I3O5EYfb0iGnw1LJE9Nb5hoAVlLsM", "README - Brand"),
            ("1ek6lhXbO5nmkS-oy90o2gN2qtsaEyULC3_qGHAHvC0Y", "README - Operations"),
            ("1InsOmBFWYI3_TP3z6CqFel3sYI_c3wDQfgKV0qAaCFg", "README - _archive"),
            ("1eLuGBVo_qQt2nngyH7qtpwE74KmeDfM5Qtuvj5aWuVo", "README - Fact-finding"),
            ("1k05txlKg_cv-yi8KOLCOooS7qZSdKQUoSRVM3qV2_Rk", "README - Incorporation #1"),
            ("1rj5CM6WPCyKZ4blOVg5Q4MUcnKhVzoSI5WgUMloaVBI", "README - name search"),
            ("10-1A6XRI13979YdI3q-4Zvkw0raOLvZs97XVDFa07Aw", "README - Trademark"),
            ("132q5A6VQiJWQovht14qIsSIi0whe3YwdcPAB9hFbntA", "README - Incorporation #2"),
            ("1xdsYGcqTVJm5NcrS1cLwg2J92WOsa4vVmDQdkPW93Ng", "README - Corporate (Admin)"),
            ("1shUm9OVOh5x0gGieaM7FYLExOWRZ2Fw-SiogUfpX4gQ", "README - 08_Security (Admin)"),
            ("1lYtQHGtDmXI7YNPs6kSSM-FBBRdEiMwPdkZUX7aRceE", "README - Enabling the Disabled - Admin"),
            ("1blBHVPCVXbg4lmgnOqhY2c1oEQdVapziMOHIZ8BJ2Hc", "Incorporation Checklist"),
        ]
        
        for doc_id, doc_title in readme_docs:
            try:
                print(f"\n  Processing: {doc_title}")
                
                # Get current content (stored as markdown text)
                doc = docs.documents().get(documentId=doc_id).execute()
                
                md_text = ""
                for elem in doc.get("body", {}).get("content", []):
                    if "paragraph" in elem:
                        for para in elem["paragraph"].get("elements", []):
                            if "textRun" in para:
                                md_text += para["textRun"].get("content", "")
                    elif "table" in elem:
                        for row in elem["table"].get("tableRows", []):
                            for cell in row.get("tableCells", []):
                                for elem2 in cell.get("content", []):
                                    if "paragraph" in elem2:
                                        for para in elem2["paragraph"].get("elements", []):
                                            if "textRun" in para:
                                                md_text += para["textRun"].get("content", "")
                            md_text += "\n"
                
                if not md_text.strip():
                    print(f"    Skipping (empty)")
                    continue
                
                print(f"    Source: {len(md_text)} chars")
                
                if args.dry_run:
                    print(f"    [DRY RUN] Would reformat with proper Docs formatting")
                else:
                    html_content = md_to_html(md_text)
                    print(f"    HTML: {len(html_content)} chars")
                    update_doc_content(docs, doc_id, html_content)
                    print(f"    Reformatted: {doc_title}")
                
            except Exception as e:
                print(f"    ERROR: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
