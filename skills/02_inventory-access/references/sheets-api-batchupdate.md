---
type: Document
title: "Google Sheets API v4 — batchUpdate Field-Name Gotchas"
description: "# Google Sheets API v4 — batchUpdate Field-Name Gotchas"
tags: ["batchupdate", "sheets"]
generated:
  by: agent:hermes
  at: 2026-09-14
  confidence: auto-low-confidence
stale_after: 2027-09-14
status: stable
---

# Google Sheets API v4 — batchUpdate Field-Name Gotchas

Common 400 errors when using `spreadsheets.batchUpdate` with `urllib`/raw JSON.
The Python SDK struct field names differ from the JSON field names.

## repeatCell — format field paths

**Correct JSON field paths:**
- `userEnteredFormat.textFormat.bold` (NOT `userEnteredFormat.bold`)
- `userEnteredFormat.textFormat.foregroundColor` (NOT `userEnteredFormat.foregroundColor`)
- `userEnteredFormat.wrapStrategy` (NOT `userEnteredFormat.wrapping`)
- `userEnteredFormat.backgroundColor` (correct)

**Example:**
```json
{
  "repeatCell": {
    "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 9},
    "cell": {
      "userEnteredFormat": {
        "textFormat": {"bold": true, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "backgroundColor": {"red": 0.15, "green": 0.35, "blue": 0.7},
        "wrapStrategy": "CLIP"
      }
    },
    "fields": "userEnteredFormat(textFormat,backgroundColor,wrapStrategy)"
  }
}
```

**Wrong field names that produce 400:**
- `userEnteredFormat.bold` → `Unknown name "bold"`
- `userEnteredFormat.wrapping` → `Unknown name "wrapping"`
- `userEnteredFormat.foregroundColor` → `Unknown name "foregroundColor"`

## updateDimensionProperties — DimensionRange fields

`DimensionRange` accepts ONLY these fields:
- `sheetId`
- `dimension` ("ROWS" or "COLUMNS")
- `startIndex` (zero-based, inclusive)
- `endIndex` (zero-based, exclusive)

**Do NOT include** `startRowIndex`, `endRowIndex`, `startColumnIndex`, `endColumnIndex` —
these are NOT part of `DimensionRange`. The API returns:
`Invalid JSON payload received. Unknown name "startRowIndex" at 'update_dimension_properties.range'`

For columns: `"dimension": "COLUMNS", "startIndex": 3, "endIndex": 4`
For rows: `"dimension": "ROWS", "startIndex": 1, "endIndex": 1000`

The `fields` parameter is **mandatory** — use `"pixelSize"` or `"*"`. Omit it and
you get `At least one field must be listed in 'fields'`.

## setDataValidation — dropdown values

Each value in `ONE_OF_LIST` needs a `userEnteredValue` key:
```json
"values": [{"userEnteredValue": "Option 1"}, {"userEnteredValue": "Option 2"}]
```

Without the `userEnteredValue` wrapper, the dropdown silently gets no options.

## values.update — URL-encode sheet names with spaces

When the sheet tab name contains spaces (e.g., "Time Record"), the range in the
`values.get`/`values.update` URL must be URL-encoded:
```python
import urllib.parse
range_encoded = urllib.parse.quote("Time Record!A1:I1")
```
Without encoding, Python's `urllib.request` raises:
`InvalidURL: URL can't contain control characters`

## Token refresh fallback

When the Google OAuth access token expires, the `google-auth` library's
`Credentials.refresh()` can fail with `invalid_grant` even when the refresh
token is still valid (transient errors, clock skew, library quirks). Before
declaring the token revoked and forcing re-authorization, retry with a direct
`urllib` POST to `https://oauth2.googleapis.com/token`:
```python
data = urllib.parse.urlencode({
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "refresh_token": creds.refresh_token,
    "grant_type": "refresh_token",
}).encode()
req = urllib.request.Request(token_uri, data=data, method="POST")
```
This succeeds when the library fails. Do NOT delete the token file — the
refresh token is usually still valid.

## Mobile optimization checklist

When creating a sheet for mobile-first data entry (iOS/Android):

1. **Shorten header text** — "Scheduled Time" → "Sched", "Session Results" → "Results", "Client Name" → "Client". Full words wrap on 320px screens and push row height.
2. **Widen dropdown columns** — dropdown options like "In-Home - Group" need 200+px width. Default 100px truncates the text.
3. **Set `wrapStrategy: CLIP`** on all data cells — prevents text wrapping that causes rows to grow to 3x normal height. This is the #1 cause of scrolling fatigue on mobile.
4. **Compact row heights** — 25px data rows, 35px header rows. Default 21px is fine but you can tune.
5. **Freeze header row** — essential so the header stays visible while scrolling through 9 columns.
6. **Add a basic filter** (`setBasicFilter`) — dropdown arrows on filter headers make dropdown columns tappable on mobile. Without it, iOS sometimes doesn't show the dropdown arrow reliably.
7. **Test column count** — 9 columns at ~140px each = ~1260px visible width. iPhone SE in portrait shows ~3-4 columns. Users WILL scroll horizontally. This is acceptable but design column widths to minimize it.
