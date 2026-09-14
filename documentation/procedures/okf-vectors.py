#!/usr/bin/env python3
"""
okf-vectors.py — Lightweight local vector search for homelab documentation.

Replaces Typesense with a simple SQLite-backed vector store. Uses llama.cpp
on renfrew-embed:8080 for embedding generation. Stores document metadata +
embeddings locally; semantic search via cosine similarity.

Embeddings are 768-dim (nomic-embed-text-v1.5-Q4_K_M). Indexing is
incremental: a file is re-embedded only when its content hash (SHA-256)
changes.

Usage:
  python3 okf-vectors.py index                     # Incremental index (--force for full rebuild)
  python3 okf-vectors.py stale                     # List docs past their stale_after date
  python3 okf-vectors.py search "query"            # Semantic search
  python3 okf-vectors.py test                      # Run the unit test suite
  python3 okf-vectors.py search "query" --type Playbook --top-k 5 --exclude-stale

Search options:
  --top-k / --per-page  Number of results (both accepted)
  --type                One of: Playbook, Decision, Guide, Document, Template,
                        Inventory, Research, Proposal (plus "Note" for vault files)
  --status              Filter by status (e.g. stable, draft)
  --exclude-stale       Exclude docs whose stale_after date is in the past
  --keyword / --fts     FTS5 keyword pre-filter: rank only docs matching this
                        query (aliases; narrows candidates before cosine pass)
  --raw                 Output raw JSON

Frontmatter fields read: title, description, type, tags, status, stale_after,
generated (provenance) and verified (verification events). generated.by is
normalized to the canonical OKF values ('agent:hermes' or 'human:*').

Environment overrides (mainly for testing/alternate deployments):
  OKF_VECTORS_DB        Path to the SQLite database
  OKF_VECTORS_LLAMA_URL llama.cpp embeddings endpoint
"""

import argparse
import ast
import glob
import hashlib
import inspect
import json
import math
import os
import re
import sqlite3
import struct
import sys
import tempfile
import textwrap
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

# --- Metrics emission (homelab-metrics) ---
_METRICS_DB = os.environ.get("OKF_METRICS_DB", "/home/hermes/homelab/metrics/metrics.db")


def _emit_metric(event_type: str, metadata: dict | None = None):
    """Append a metric event to the metrics DB. Best-effort; never raises."""
    try:
        conn = sqlite3.connect(_METRICS_DB)
        try:
            conn.execute("""CREATE TABLE IF NOT EXISTS metric_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS metric_sources (
                source TEXT PRIMARY KEY,
                description TEXT,
                first_seen TEXT,
                last_seen TEXT
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS daily_counts (
                day TEXT NOT NULL,
                event_type TEXT NOT NULL,
                source TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (day, event_type, source)
            )""")
            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "INSERT INTO metric_events (event_type, source, timestamp, metadata) VALUES (?, ?, ?, ?)",
                (event_type, "hermes-agent", now, json.dumps(metadata or {})),
            )
            conn.execute(
                "INSERT INTO metric_sources (source, description, first_seen, last_seen) "
                "VALUES (?, ?, COALESCE((SELECT first_seen FROM metric_sources WHERE source = ?), ?), ?)"
                " ON CONFLICT(source) DO UPDATE SET last_seen = excluded.last_seen",
                ("hermes-agent", "Hermes Agent on renfrew-hermes", "hermes-agent", now, now),
            )
            day = now[:10]
            conn.execute(
                "INSERT INTO daily_counts (day, event_type, source, count) "
                "VALUES (?, ?, ?, 1) "
                "ON CONFLICT(day, event_type, source) DO UPDATE SET count = count + 1",
                (day, event_type, "hermes-agent"),
            )
            conn.commit()
        finally:
            conn.close()
    except Exception:
        pass  # metrics are best-effort — never break the caller

# --- Configuration ---

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # repo root (e.g. /home/hermes/homelab)

def _get_llama_url() -> str:
    return os.environ.get(
        "OKF_VECTORS_LLAMA_URL", "http://renfrew-embed.renfrew.hollebone.ca:8080/v1/embeddings"
    )

def _get_db_path() -> str:
    """Default to .okf-vectors.db in the repo root (where this script lives)."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    return os.environ.get(
        "OKF_VECTORS_DB", str(repo_root / ".okf-vectors.db")
    )

def _get_repo_root() -> str:
    """Root of the repo — the full tree is indexed, not just documentation/."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    return os.environ.get(
        "HOME_LAB_REPO_ROOT", str(repo_root)
    )

def _get_obsidian_vault_root() -> str | None:
    """Obsidian vault root — set env var to enable vault indexing."""
    return os.environ.get("OBSIDIAN_VAULT_ROOT")

# Module-level defaults (backward-compatible — functions read env at call time)
LLAMA_URL = _get_llama_url()
DB_PATH = _get_db_path()
REPO_ROOT = _get_repo_root()
OBSIDIAN_VAULT_ROOT = _get_obsidian_vault_root()

MAX_CONTENT_CHARS = 1000  # Per-doc content cap (renfrew-embed llama.cpp has --batch-size 2048)
BATCH_SIZE = 50  # Number of docs per embedding request batch
EMBEDDING_DIM = 768  # nomic-embed-text-v1.5 (Q4_K_M) produces 768-dim embeddings
HTTP_TIMEOUT = 60  # seconds, per embedding request
MAX_RETRIES = 3  # embedding API retry attempts (exponential backoff)
RETRY_BACKOFF = 2  # base seconds for exponential backoff

# Directories to skip when walking the repo
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", ".eggs", ".tox",
    ".mypy_cache", ".pytest_cache", ".okf-vectors.egg-info",
    "disaster-recovery",  # backup archives — not live docs
}

# File extensions that are never indexed as text
SKIP_EXTENSIONS = {
    ".lock", ".sum", ".mod", ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".pdf", ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".dat", ".db", ".sqlite",
    ".sqlite3", ".mp3", ".mp4", ".avi", ".mov", ".wav",
    ".pyc", ".pyo", ".o", ".a", ".lib", ".map", ".orig", ".bak",
    ".tmp", ".cache", ".rsc", ".iml", ".pid", ".master", ".herschel",
    ".coder", ".dns01", ".dns02", ".dns03", ".TAG", ".vars", ".template",
    ".tail", ".log", ".db-wal", ".db-shm",
}

# Image extensions that get metadata extraction instead of full text indexing
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp"}

# Metadata filenames (not indexed)
META_FILENAMES = {
    ".gitignore", ".gitattributes", ".dockerignore", ".eslintrc",
    ".prettierrc", ".editorconfig", ".nvmrc", ".npmignore", ".eslintignore",
    ".yamllint", "LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING",
    "AUTHORS", "AUTHORS.md", "CHANGELOG.md", "CHANGELOG", "HISTORY.md",
    "HISTORY", "CONTRIBUTORS", "CONTRIBUTORS.md", "CODE_OF_CONDUCT.md",
    "SECURITY.md", "gitkeep", "CACHEDIR.TAG", ".env",
}

# OKF ignore file — same syntax as .gitignore
OKF_IGNORE_FILE = Path(REPO_ROOT) / ".okfignore"
OKF_IGNORE_PATTERNS: list[str] = []


def _load_okfignore() -> list[str]:
    """Load .okfignore patterns."""
    if not OKF_IGNORE_FILE.exists():
        return []
    patterns = []
    for line in OKF_IGNORE_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


OKF_IGNORE_PATTERNS = _load_okfignore()


def is_okf_ignored(filepath: Path) -> bool:
    """Check if a file matches any .okfignore pattern."""
    try:
        rel = filepath.relative_to(REPO_ROOT)
    except ValueError:
        return False
    rel_str = str(rel)
    for pattern in OKF_IGNORE_PATTERNS:
        if pattern.endswith("/"):
            if rel_str.startswith(pattern) or pattern.rstrip("/") in rel.parts:
                return True
        elif pattern.startswith("*."):
            if rel_str.endswith(pattern[1:]):
                return True
        else:
            if pattern in rel_str or rel_str == pattern:
                return True
    return False


# OKF knowledge-base document types. "Note" is included for Obsidian vault
# files, which are indexed but never assigned an OKF type.
VALID_TYPES = [
    "Playbook",
    "Decision",
    "Guide",
    "Document",
    "Template",
    "Inventory",
    "Research",
    "Proposal",
    "Note",
]


def strip_markdown(content: str) -> str:
    """Strip markdown formatting to get plain text for content/embedding."""
    # Remove code blocks
    content = re.sub(r'```[a-z]*\n(.*?)```', '', content, flags=re.DOTALL)
    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)
    # Remove images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    # Remove links but keep link text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    # Remove markdown headers
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
    # Remove horizontal rules
    content = re.sub(r'^---\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*\*\*\*\s*$', '', content, flags=re.MULTILINE)
    # Remove blockquotes
    content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
    # Remove list markers
    content = re.sub(r'^[-*]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\d+\.\s+', '', content, flags=re.MULTILINE)
    # Remove bold/italic
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    content = re.sub(r'__([^_]+)__', r'\1', content)
    content = re.sub(r'_([^_]+)_', r'\1', content)
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()


def _parse_scalar(value: str):
    """Parse a scalar frontmatter value: string, inline list, or inline mapping."""
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        result = {}
        for part in inner.split(","):
            if ":" in part:
                key, _, val = part.partition(":")
                result[key.strip()] = val.strip().strip("\"'")
        return result
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_frontmatter(content: str):
    """Parse YAML frontmatter from markdown content. Returns (frontmatter_dict, body_str).

    This is a lightweight regex-based parser, not a full YAML implementation:
    it extracts first-level fields — scalars, quoted strings, inline/block
    lists, and inline or block nested mappings (e.g. ``generated``,
    ``verified``). Nested mappings are returned as dicts of their first-level
    sub-fields. Unsupported YAML features (anchors/aliases, multi-line block
    scalars via ``|``/``>``, lists-of-lists) are silently ignored.
    """
    frontmatter = {}
    body = content

    if content.startswith("---"):
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", content, re.DOTALL)
        if match:
            yaml_block = match.group(1)
            body = match.group(2)
            current_key = None
            pending_kind = None  # "list", "map", or None (unknown)
            pending_list: list = []
            pending_map: dict = {}
            for line in yaml_block.split("\n"):
                if not line.strip():
                    continue
                indent = len(line) - len(line.lstrip(" \t"))
                stripped = line.strip()
                if indent == 0:
                    # Flush any pending nested block before starting a new key.
                    if current_key is not None:
                        if pending_kind == "list" and pending_list:
                            frontmatter[current_key] = pending_list
                        elif pending_kind == "map" and pending_map:
                            frontmatter[current_key] = pending_map
                    current_key = None
                    pending_kind = None
                    pending_list = []
                    pending_map = {}
                    key_match = re.match(r"^([A-Za-z0-9_.\-]+):\s*(.*)$", stripped)
                    if not key_match:
                        continue
                    current_key = key_match.group(1)
                    raw_value = key_match.group(2).strip()
                    if raw_value:
                        frontmatter[current_key] = _parse_scalar(raw_value)
                        current_key = None
                    continue
                # Indented line — belongs to the current key's nested block.
                if current_key is None:
                    continue
                if pending_kind is None:
                    if stripped.startswith("- "):
                        pending_kind = "list"
                    elif ":" in stripped:
                        pending_kind = "map"
                    else:
                        continue  # continuation text we can't represent; ignore
                if pending_kind == "list":
                    if stripped.startswith("- "):
                        item = stripped[2:].strip()
                        if ":" in item:
                            pending_list.append(_parse_scalar("{" + item + "}"))
                        else:
                            pending_list.append(_parse_scalar(item))
                    elif pending_list and isinstance(pending_list[-1], dict):
                        # Continuation of the last list item (nested sub-field).
                        if ":" in stripped:
                            key, _, val = stripped.partition(":")
                            pending_list[-1][key.strip()] = val.strip().strip("\"'")
                elif pending_kind == "map" and ":" in stripped:
                    key, _, val = stripped.partition(":")
                    pending_map[key.strip()] = _parse_scalar(val.strip())
            # Flush trailing pending block at end of frontmatter.
            if current_key is not None:
                if pending_kind == "list" and pending_list:
                    frontmatter[current_key] = pending_list
                elif pending_kind == "map" and pending_map:
                    frontmatter[current_key] = pending_map

    return frontmatter, body


def extract_title(filepath: str, body: str, frontmatter: dict) -> str:
    """Extract a title from frontmatter, H1 header, or filename."""
    title = frontmatter.get('title', '')
    if title:
        return str(title)
    h1_match = re.match(r'^#\s+(.+)', body)
    if h1_match:
        return h1_match.group(1).strip()
    return Path(filepath).stem


def get_content_for_embedding(body: str) -> str:
    """Get plain text content for embedding, truncated to MAX_CONTENT_CHARS."""
    plain = strip_markdown(body)
    if len(plain) > MAX_CONTENT_CHARS:
        plain = plain[:MAX_CONTENT_CHARS]
    return plain


def as_str(value, default: str = "") -> str:
    """Coerce a parsed frontmatter value to a string."""
    if value is None:
        return default
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


def coerce_tags(value) -> list:
    """Coerce a parsed frontmatter tags value to a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(tag) for tag in value]
    if isinstance(value, str):
        return [value] if value else []
    return []


def content_hash(content: str) -> str:
    """SHA-256 of raw file content, used for incremental reindexing."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def normalize_generated_by(value) -> str:
    """Normalize frontmatter `generated.by` to canonical OKF values.

    Older auto-generated frontmatter used `agent:cron` or `hermes-agent/v2.1`;
    those are mapped to the canonical `agent:hermes`. Human provenance
    (`human:*`) is preserved as-is.
    """
    if isinstance(value, dict):
        value = value.get("by", "")
    v = str(value or "").strip()
    if not v:
        return ""
    if v.startswith("human:"):
        return v
    return "agent:hermes"


def format_verified(value) -> str:
    """Serialize frontmatter `verified` (a mapping or list of mappings) to a compact string."""
    if isinstance(value, list):
        return "; ".join(format_verified(item) for item in value if item)
    if isinstance(value, dict):
        by = str(value.get("by", "") or "").strip()
        at = str(value.get("at", "") or "").strip()
        if by and at:
            return f"{by} @ {at}"
        return by or at
    return str(value or "").strip()


def is_stale(stale_after: str) -> bool:
    """True if the doc's stale_after date is in the past.

    Accepts `YYYY-MM-DD` and ISO-8601 datetimes. Unparseable values are
    treated as not stale (don't guess).
    """
    raw = (stale_after or "").strip()
    if not raw:
        return False
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            return date.fromisoformat(raw) < datetime.now(timezone.utc).date()
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt < datetime.now(timezone.utc)
    except ValueError:
        return False


class EmbeddingServiceError(RuntimeError):
    """Raised when the llama.cpp embedding endpoint cannot be reached."""


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of texts via llama.cpp server.

    Retries with exponential backoff (up to MAX_RETRIES attempts). Raises
    EmbeddingServiceError if the endpoint is unreachable.
    """
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                _get_llama_url(),
                headers={"Content-Type": "application/json"},
                json={"input": texts},
                timeout=HTTP_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            return [item["embedding"] for item in data["data"]]
        except (requests.RequestException, ValueError, KeyError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                delay = RETRY_BACKOFF * (2 ** (attempt - 1))
                print(
                    f"  ⚠️  Embedding request failed (attempt {attempt}/{MAX_RETRIES}): {exc}"
                )
                print(f"     Retrying in {delay}s...")
                time.sleep(delay)
    raise EmbeddingServiceError(
        f"llama.cpp endpoint {_get_llama_url()} unreachable after {MAX_RETRIES} attempts: {last_error}"
    )


def init_db():
    """Initialize the SQLite vector database (with column migration)."""
    conn = sqlite3.connect(_get_db_path())
    conn.execute("""
        CREATE TABLE IF NOT EXISTS docs (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            content TEXT,
            type TEXT,
            tags TEXT,
            status TEXT,
            stale_after TEXT,
            generated TEXT,
            verified TEXT,
            content_hash TEXT,
            source_path TEXT,
            directory TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            doc_id TEXT PRIMARY KEY,
            vector BLOB,
            FOREIGN KEY (doc_id) REFERENCES docs(id)
        )
    """)
    # FTS5 keyword index mirroring docs (title/description/content/source_path)
    # so search can pre-filter candidates before the Python-side cosine similarity
    # pass. doc_id is UNINDEXED: stored so MATCH results can be mapped back to docs
    # rows, but not tokenized/searched.
    #
    # Migration: FTS5 tables don't support ALTER TABLE ADD COLUMN. If the existing
    # docs_fts table lacks source_path, drop and recreate it, then rebuild from the
    # docs table.
    existing_fts_cols = {
        row[1]
        for row in conn.execute("PRAGMA table_info(docs_fts)")
    } if conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='docs_fts'"
    ).fetchone()[0] > 0 else set()

    if "source_path" not in existing_fts_cols:
        conn.execute("DROP TABLE IF EXISTS docs_fts")
        conn.execute("""
            CREATE VIRTUAL TABLE docs_fts USING fts5(
                title,
                description,
                content,
                source_path,
                doc_id UNINDEXED
            )
        """)
        # Rebuild from existing docs
        conn.execute("""
            INSERT INTO docs_fts (doc_id, title, description, content, source_path)
            SELECT id, title, description, content, source_path FROM docs
        """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_type ON docs(type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_status ON docs(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_source_path ON docs(source_path)")
    # First run on a pre-FTS database: backfill docs_fts from existing rows so
    # --keyword works without a full re-embed. Later runs stay in sync via
    # index_docs(); this only fires while the virtual table is empty.
    if conn.execute("SELECT COUNT(*) FROM docs_fts").fetchone()[0] == 0 and \
            conn.execute("SELECT COUNT(*) FROM docs").fetchone()[0] > 0:
        conn.execute("""
            INSERT INTO docs_fts (doc_id, title, description, content)
            SELECT id, title, description, content FROM docs
        """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_type ON docs(type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_status ON docs(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_docs_source_path ON docs(source_path)")
    # Migrate databases created before the verified/content_hash columns existed.
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(docs)")}
    for column in ("verified", "content_hash"):
        if column not in existing_cols:
            conn.execute(f"ALTER TABLE docs ADD COLUMN {column} TEXT")
    conn.commit()
    return conn


def should_index_file(filepath: Path) -> bool:
    """Return True if a file should be included in the index."""
    # Skip by directory
    for part in Path(filepath).parts:
        if part in SKIP_DIRS:
            return False

    # Skip metadata files
    if Path(filepath).name in META_FILENAMES:
        return False

    # Skip by extension
    ext = Path(filepath).suffix.lower()
    if ext in SKIP_EXTENSIONS:
        return False

    # Skip .okfignore matches
    if is_okf_ignored(filepath):
        return False

    return True


def extract_image_metadata(filepath: Path) -> dict:
    """Extract metadata from an image file using PIL.

    Returns a dict with: width, height, format, mode, exif (dict or None).
    """
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        with Image.open(filepath) as img:
            info = {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "exif": None,
            }
            exif_data = img.getexif()
            if exif_data:
                exif = {}
                for tag_id, val in exif_data.items():
                    tag_name = TAGS.get(tag_id, str(tag_id))
                    # Only include serializable values
                    if isinstance(val, (str, int, float)):
                        exif[tag_name] = str(val)
                info["exif"] = exif if exif else None
            return info
    except Exception:
        return {"width": None, "height": None, "format": None, "mode": None, "exif": None}


def get_content_for_non_md(filepath: Path) -> str:
    """Get indexable content from a non-markdown text file.

    For code/config files: returns the first MAX_CONTENT_CHARS characters.
    For image files: returns a string describing extracted metadata.
    """
    ext = Path(filepath).suffix.lower()

    if ext in IMAGE_EXTENSIONS:
        meta = extract_image_metadata(filepath)
        parts = [f"Image: {filepath.name}"]
        if meta.get("width") and meta.get("height"):
            parts.append(f"Resolution: {meta['width']}x{meta['height']}")
        if meta.get("format"):
            parts.append(f"Format: {meta['format']}")
        if meta.get("mode"):
            parts.append(f"Mode: {meta['mode']}")
        if meta.get("exif"):
            for k, v in meta["exif"].items():
                parts.append(f"EXIF {k}: {v}")
        return " | ".join(parts)

    # For all other text files (code, config, scripts, etc.)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        if len(content) > MAX_CONTENT_CHARS:
            content = content[:MAX_CONTENT_CHARS]
        return content
    except Exception:
        return ""


def collect_docs():
    """Walk the full homelab repo + Obsidian vault, return list of doc dicts.

    Indexes every text file in the repo (not just documentation/), plus image
    files via metadata extraction. Skips build artifacts, backup archives,
    version-control internals, and binary files.
    """
    docs = []
    seen_paths = set()

    repo_root = Path(_get_repo_root())

    # --- Phase 1: walk the entire repo for text + image files ---
    for filepath in sorted(repo_root.rglob("*")):
        if not filepath.is_file():
            continue
        if not should_index_file(filepath):
            continue
        if filepath in seen_paths:
            continue
        seen_paths.add(filepath)

        rel_dir = str(filepath.parent.relative_to(repo_root))
        ext = filepath.suffix.lower()
        frontmatter = {}
        raw_content = ""

        if ext == ".md":
            # Markdown: parse frontmatter, index body
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
            except (OSError, UnicodeDecodeError):
                continue
            frontmatter, body = parse_frontmatter(raw_content)
            plain_content = get_content_for_embedding(body)
            title = extract_title(str(filepath), body, frontmatter)
            doc_type = as_str(frontmatter.get('type'), 'Document')
            description = as_str(frontmatter.get('description'))
        else:
            # Non-markdown text or image
            raw_content = get_content_for_non_md(filepath)
            if not raw_content:
                continue
            plain_content = raw_content
            title = filepath.stem.replace("-", " ").replace("_", " ").title()
            doc_type = "Code" if ext in (".py", ".sh", ".js", ".ts", ".go", ".rs", ".c", ".cpp", ".h", ".hpp", ".java", ".rb", ".pl", ".php", ".swift", ".kt", ".ps1", ".sql", ".dockerfile", ".makefile", ".cmake") else "Config" if ext in (".yaml", ".yml", ".json", ".toml", ".xml", ".csv", ".ini", ".cfg", ".conf", ".service", ".timer", ".socket", ".html", ".css", ".scss", ".jsx", ".tsx") else "Image" if ext in IMAGE_EXTENSIONS else "Document"
            description = f"{filepath.name} ({rel_dir})"

        doc_id = "homelab_" + hashlib.md5(str(filepath).encode()).hexdigest()[:16]

        docs.append({
            "id": doc_id,
            "title": title,
            "description": description,
            "content": plain_content,
            "type": doc_type,
            "tags": json.dumps([ext.lstrip(".")] if ext else []),
            "status": as_str(frontmatter.get('status'), 'unknown') if ext == ".md" else "active",
            "stale_after": as_str(frontmatter.get('stale_after')) if ext == ".md" else "",
            "generated": normalize_generated_by(frontmatter.get('generated')) if ext == ".md" else "",
            "verified": format_verified(frontmatter.get('verified')) if ext == ".md" else "",
            "content_hash": content_hash(raw_content),
            "source_path": str(filepath),
            "directory": rel_dir,
        })

    # Obsidian vault (optional — only if OBSIDIAN_VAULT_ROOT is set)
    vault_root = _get_obsidian_vault_root()
    if vault_root:
        md_files = glob.glob(f"{vault_root}/**/*.md", recursive=True)
        for filepath in sorted(md_files):
            if filepath in seen_paths:
                continue
            seen_paths.add(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            frontmatter, body = parse_frontmatter(content)
            plain_content = get_content_for_embedding(body)
            title = extract_title(filepath, body, frontmatter)
            doc_id = "obsidian_" + hashlib.md5(filepath.encode()).hexdigest()[:16]

            try:
                directory = str(Path(filepath).parent.relative_to(vault_root))
            except ValueError:
                directory = str(Path(filepath).parent)

            docs.append({
                "id": doc_id,
                "title": title,
                "description": as_str(frontmatter.get('description')),
                "content": plain_content,
                "type": "Note",
                "tags": json.dumps(coerce_tags(frontmatter.get('tags'))),
                "status": "active",
                "stale_after": "",
                "generated": "",
                "verified": format_verified(frontmatter.get('verified')),
                "content_hash": content_hash(content),
                "source_path": filepath,
                "directory": directory,
            })

    return docs


def index_docs(force: bool = False):
    """Index documents into the local vector database.

    Incremental by default: files whose SHA-256 content hash is unchanged are
    skipped, and only new/changed files are embedded. Pass force=True to
    delete all rows and rebuild the index from scratch.
    """
    print("=== OKF Vector Index — Indexing OKF repo ===")
    print(f"llama.cpp endpoint: {_get_llama_url()}")
    print(f"Database: {_get_db_path()}")

    docs = collect_docs()
    print(f"\nFound {len(docs)} documents")

    conn = init_db()

    if force:
        conn.execute("DELETE FROM embeddings")
        conn.execute("DELETE FROM docs")
        conn.execute("DELETE FROM docs_fts")
        conn.commit()
        existing_hashes = {}
    else:
        existing_hashes = {
            row[0]: row[1]
            for row in conn.execute("SELECT id, content_hash FROM docs")
        }

    to_embed = []
    unchanged = 0
    for doc in docs:
        if existing_hashes.get(doc["id"]) == doc["content_hash"]:
            unchanged += 1
            continue
        to_embed.append(doc)

    print(f"  {unchanged} unchanged (skipped), {len(to_embed)} to embed")

    # Embed + upsert new/changed docs in batches. Metadata rows are only
    # written after embeddings succeed, so a failed run leaves the previous
    # (searchable) state intact and the file is retried next run.
    for i in range(0, len(to_embed), BATCH_SIZE):
        batch = to_embed[i:i + BATCH_SIZE]
        texts = [doc["content"] for doc in batch]
        embeddings = generate_embeddings(texts)

        for doc, emb in zip(batch, embeddings):
            if len(emb) != EMBEDDING_DIM:
                print(
                    f"  ⚠️  {doc['source_path']}: embedding dim {len(emb)} "
                    f"!= expected {EMBEDDING_DIM}"
                )
            vec_bytes = struct.pack(f"{len(emb)}f", *emb)
            conn.execute("""
                INSERT OR REPLACE INTO docs
                    (id, title, description, content, type, tags, status,
                     stale_after, generated, verified, content_hash,
                     source_path, directory)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (doc["id"], doc["title"], doc["description"], doc["content"],
                  doc["type"], doc["tags"], doc["status"], doc["stale_after"],
                  doc["generated"], doc["verified"], doc["content_hash"],
                  doc["source_path"], doc["directory"]))
            conn.execute(
                "INSERT OR REPLACE INTO embeddings (doc_id, vector) VALUES (?, ?)",
                (doc["id"], vec_bytes)
            )
            # Keep the FTS5 keyword index in sync: delete any stale row for
            # this doc (incremental re-index of a changed file), then insert
            # the fresh title/description/content/source_path.
            conn.execute("DELETE FROM docs_fts WHERE doc_id = ?", (doc["id"],))
            conn.execute(
                "INSERT INTO docs_fts (doc_id, title, description, content, source_path) "
                "VALUES (?, ?, ?, ?, ?)",
                (doc["id"], doc["title"], doc["description"], doc["content"], doc["source_path"]),
            )
        conn.commit()

        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(to_embed) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"  Batch {batch_num}/{total_batches}: {len(batch)} embeddings")

    # Drop rows for files that no longer exist on disk.
    known_ids = [doc["id"] for doc in docs]
    if known_ids:
        placeholders = ", ".join("?" * len(known_ids))
        conn.execute(
            f"DELETE FROM embeddings WHERE doc_id NOT IN ({placeholders})", known_ids
        )
        conn.execute(
            f"DELETE FROM docs WHERE id NOT IN ({placeholders})", known_ids
        )
        conn.execute(
            f"DELETE FROM docs_fts WHERE doc_id NOT IN ({placeholders})", known_ids
        )
    else:
        conn.execute("DELETE FROM embeddings")
        conn.execute("DELETE FROM docs")
        conn.execute("DELETE FROM docs_fts")
    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    print(f"\n✅ Indexed {total} documents with {EMBEDDING_DIM}-dim embeddings")

    # Emit metric
    _emit_metric("okf_index", {"count": total})

    # Print type distribution
    cursor = conn.execute(
        "SELECT type, COUNT(*) FROM docs GROUP BY type ORDER BY COUNT(*) DESC"
    )
    print("\nType distribution:")
    for row in cursor:
        print(f"  {row[0]}: {row[1]}")

    conn.close()


def cosine_similarity(a, b) -> float:
    """Cosine similarity between two equal-length vectors.

    Returns 1.0 for identical vectors, 0.0 for orthogonal vectors, and 0.0
    for empty/mismatched-length inputs (treated as no similarity).
    """
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a > 0 and norm_b > 0:
        return dot / (norm_a * norm_b)
    return 0.0


def search_docs(query: str, top_k: int = 10,
                doc_type: str | None = None,
                status_filter: str | None = None,
                exclude_stale: bool = False,
                keyword: str | None = None):
    """Semantic search using cosine similarity, optionally pre-filtered by FTS5.

    When `keyword` is given, the FTS5 `docs_fts` virtual table (mirroring
    docs.title/description/content) is queried with MATCH first, and only the
    matching doc ids are fetched for the Python-side cosine similarity pass.
    This narrows the candidate set before any similarity computation, so
    keyword search stays fast as the corpus grows. A malformed FTS5 query
    falls back to the full scan rather than failing.

    Without `keyword`, behavior is unchanged: every row is fetched and ranked
    by cosine similarity Python-side. That full-scan fallback is the default
    and is fine at the current scale (a few thousand docs).
    """
    conn = init_db()

    # Optional FTS5 keyword pre-filter: restrict candidates to docs whose
    # title/description/content match the keyword query before the cosine pass.
    fts_ids: set[str] | None = None
    if keyword:
        try:
            fts_ids = {
                row[0]
                for row in conn.execute(
                    "SELECT doc_id FROM docs_fts WHERE docs_fts MATCH ?",
                    (keyword,),
                )
            }
        except sqlite3.OperationalError as exc:
            print(f"  ⚠️  FTS keyword query failed ({exc}); falling back to full scan")
            fts_ids = None

    # Generate query embedding
    print(f"Generating embedding for: \"{query}\"")
    query_emb = generate_embeddings([query])[0]

    if fts_ids is not None and not fts_ids:
        # FTS5 matched nothing — no candidates, skip the similarity pass.
        conn.close()
        return []

    # Fetch candidate docs with embeddings. The FTS5 match set (when present)
    # narrows candidates before similarity computation; doc_type narrows further.
    base_sql = """
        SELECT d.id, d.title, d.description, d.content, d.type, d.tags,
               d.status, d.stale_after, d.generated, d.verified,
               d.source_path, d.directory, e.vector
        FROM docs d JOIN embeddings e ON d.id = e.doc_id
    """
    conditions = []
    params: list = []
    if doc_type:
        conditions.append("d.type = ?")
        params.append(doc_type)
    if fts_ids is not None:
        placeholders = ", ".join("?" * len(fts_ids))
        conditions.append(f"d.id IN ({placeholders})")
        params.extend(sorted(fts_ids))
    if conditions:
        cursor = conn.execute(
            base_sql + " WHERE " + " AND ".join(conditions), params
        )
    else:
        cursor = conn.execute(base_sql)

    results = []
    for row in cursor:
        _doc_id, title, desc, content, doc_type_val, tags_json, \
            status, stale_after, generated, verified, source_path, directory, \
            vec_bytes = row

        # Check status filter
        if status_filter and status != status_filter:
            continue

        # Check stale filter
        stale = is_stale(stale_after)
        if exclude_stale and stale:
            continue

        # Deserialize stored vector. Use the actual stored length so search
        # survives embedding-model dimension changes.
        stored_emb = list(struct.unpack(f"{len(vec_bytes) // 4}f", vec_bytes))

        # Cosine similarity
        similarity = cosine_similarity(query_emb, stored_emb)

        # Parse tags
        tags = json.loads(tags_json) if tags_json else []

        results.append({
            "score": similarity,
            "title": title,
            "type": doc_type_val,
            "status": status,
            "stale": stale,
            "stale_after": stale_after,
            "generated": generated,
            "verified": verified,
            "tags": tags,
            "source_path": source_path,
            "directory": directory,
            "description": desc,
            "content_preview": content[:200] + "..." if len(content) > 200 else content,
        })

    # Sort by similarity descending
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:top_k]

    _emit_metric("okf_search", {"query": query, "top_k": top_k, "results": len(results)})

    conn.close()
    return results


def list_stale_docs() -> int:
    """List docs whose stale_after date is in the past. No llama.cpp needed."""
    conn = init_db()
    rows = conn.execute(
        "SELECT title, type, stale_after, source_path FROM docs"
    ).fetchall()
    conn.close()

    stale = [row for row in rows if is_stale(row[2])]
    total = len(rows)

    print("=== OKF Vector Index — Stale documents ===")
    if not stale:
        print("\n✅ No stale documents.")
        return 0
    pct = 100.0 * len(stale) / total if total else 0.0
    print(
        f"\n⚠️  {len(stale)} of {total} documents are past their stale_after "
        f"date ({pct:.1f}%)"
    )
    for title, doc_type, stale_after, source_path in sorted(stale, key=lambda r: r[2]):
        print(f"  [{doc_type}] {title} — stale after {stale_after}")
        print(f"    {source_path}")
    return len(stale)


def main():
    parser = argparse.ArgumentParser(description="OKF Vector Search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser(
        "index", help="Build/update the vector database (incremental)"
    )
    index_parser.add_argument(
        "--force", action="store_true",
        help="Full rebuild: delete all rows and re-embed every document",
    )

    subparsers.add_parser(
        "stale", help="List documents past their stale_after date"
    )

    subparsers.add_parser("test", help="Run the unit test suite")

    search_parser = subparsers.add_parser("search", help="Semantic search")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--top-k", "--per-page", dest="top_k", type=int, default=10,
        help="Number of results (alias: --per-page)",
    )
    search_parser.add_argument(
        "--type", choices=VALID_TYPES, help="Filter by document type"
    )
    search_parser.add_argument(
        "--status", help="Filter by status (e.g. stable, draft)"
    )
    search_parser.add_argument(
        "--exclude-stale", action="store_true",
        help="Exclude documents past their stale_after date",
    )
    search_parser.add_argument(
        "--keyword", "--fts", dest="keyword",
        help="FTS5 keyword pre-filter: rank only docs matching this query "
             "(alias: --fts)",
    )
    search_parser.add_argument(
        "--raw", action="store_true", help="Output raw JSON instead of formatted"
    )

    args = parser.parse_args()

    try:
        if args.command == "index":
            index_docs(force=args.force)
        elif args.command == "stale":
            list_stale_docs()
        elif args.command == "test":
            sys.exit(test())
        elif args.command == "search":
            results = search_docs(
                args.query,
                top_k=args.top_k,
                doc_type=args.type,
                status_filter=args.status,
                exclude_stale=args.exclude_stale,
                keyword=args.keyword,
            )

            if args.raw:
                print(json.dumps(results, indent=2))
            else:
                print(f"\n🔍 Semantic search: \"{args.query}\" ({len(results)} results)\n")
                for r in results:
                    badge = " ⚠️ STALE" if r["stale"] else ""
                    print(f"  [{r['type']}] 📄 {r['title']}{badge}")
                    if r['description']:
                        print(f"    {r['description']}")
                    print(f"    Score: {r['score']:.4f} | Status: {r['status']}")
                    if r['stale_after']:
                        print(f"    Stale after: {r['stale_after']}")
                    if r['generated']:
                        print(f"    Generated by: {r['generated']}")
                    if r['verified']:
                        print(f"    Verified: {r['verified']}")
                    if r['tags']:
                        print(f"    Tags: {', '.join(r['tags'])}")
                    print(f"    Path: {r['source_path']}")
                    print(f"    Preview: {r['content_preview'][:150]}")
                    print()
    except EmbeddingServiceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            "Is llama.cpp running? Check the embedding endpoint and try again.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception:
        # Best-effort metrics should never propagate failures to the caller.
        pass


# --- Tests ---
#
# Run with: python3 okf-vectors.py test
# (or import this module and call test()).


def test_parse_frontmatter_scalar():
    """Scalar frontmatter values (plain, quoted) parse to their string form."""
    content = (
        "---\n"
        "title: Test Doc\n"
        'description: "A quoted description"\n'
        "status: stable\n"
        "type: Guide\n"
        "---\n\n"
        "Body text"
    )
    fm, body = parse_frontmatter(content)
    assert fm["title"] == "Test Doc"
    assert fm["description"] == "A quoted description"
    assert fm["status"] == "stable"
    assert fm["type"] == "Guide"
    assert body.strip() == "Body text"


def test_parse_frontmatter_inline_list():
    """Inline list values (tags) parse to a list of strings."""
    content = '---\ntags: [proxmox, opnsense, "dns"]\n---\n\nBody'
    fm, _ = parse_frontmatter(content)
    assert fm["tags"] == ["proxmox", "opnsense", "dns"]


def test_parse_frontmatter_inline_mapping():
    """Inline mapping values ({by: ..., at: ...}) parse to a dict."""
    content = "---\ngenerated: {by: human:ehollebone, at: 2026-08-14}\n---\n\nBody"
    fm, _ = parse_frontmatter(content)
    assert fm["generated"] == {"by": "human:ehollebone", "at": "2026-08-14"}


def test_parse_frontmatter_block_mapping():
    """Block mappings (generated/verified) parse to dicts."""
    content = (
        "---\n"
        "generated:\n"
        "  by: agent:hermes\n"
        "  at: 2026-08-16\n"
        "verified:\n"
        "  by: human:ehollebone\n"
        "  at: 2026-08-14\n"
        "---\n\n"
        "Body"
    )
    fm, _ = parse_frontmatter(content)
    assert fm["generated"] == {"by": "agent:hermes", "at": "2026-08-16"}
    assert fm["verified"] == {"by": "human:ehollebone", "at": "2026-08-14"}


def test_parse_frontmatter_nested_mapping():
    """Nested structures: inline mapping with colon-bearing values, and a block
    list-of-dicts (verified history)."""
    content = (
        "---\n"
        "generated: {by: hermes-agent/v2.1, at: 2026-08-09T00:00:00Z}\n"
        "verified:\n"
        "  - by: human:ehollebone\n"
        "    at: 2026-08-14\n"
        "---\n\n"
        "Body"
    )
    fm, _ = parse_frontmatter(content)
    assert fm["generated"] == {
        "by": "hermes-agent/v2.1",
        "at": "2026-08-09T00:00:00Z",
    }
    assert fm["verified"] == [{"by": "human:ehollebone", "at": "2026-08-14"}]


def test_strip_markdown():
    """Markdown formatting is removed, leaving plain text."""
    md = """# Header

Some **bold** and *italic* text with [a link](https://example.com) and `code`.

- item one
- item two

> a quote

```python
print("hidden")
```
"""
    plain = strip_markdown(md)
    assert "Header" in plain
    assert "bold" in plain
    assert "italic" in plain
    assert "a link" in plain
    assert "**" not in plain
    assert "(https://example.com)" not in plain
    assert "print" not in plain  # fenced code block removed
    assert "item one" in plain
    assert "a quote" in plain
    assert "- item one" not in plain


def test_cosine_similarity_known_values():
    """Identical vectors score 1.0; orthogonal vectors score 0.0."""
    assert math.isclose(
        cosine_similarity([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0, rel_tol=1e-9
    )
    assert math.isclose(
        cosine_similarity([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]), 0.0, abs_tol=1e-12
    )
    assert cosine_similarity([1.0, 2.0], [1.0, 2.0]) > 0.9
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0  # zero vector
    assert cosine_similarity([1.0, 0.0], [1.0]) == 0.0  # length mismatch


def test_content_hash_changes():
    """Same content hashes identically; different content differs."""
    h1 = content_hash("same content")
    assert h1 == content_hash("same content")
    assert h1 != content_hash("different content")
    assert len(h1) == 64  # SHA-256 hex digest


def test_extract_title_from_frontmatter():
    """Title resolution: frontmatter > H1 > filename stem."""
    fm = {"title": "From Frontmatter"}
    assert (
        extract_title("/tmp/x/foo.md", "# H1 Title\nbody", fm) == "From Frontmatter"
    )
    assert extract_title("/tmp/x/foo.md", "# H1 Title\nbody", {}) == "H1 Title"
    assert extract_title("/tmp/x/foo.md", "no heading here", {}) == "foo"


def test_init_db_creates_tables():
    """init_db creates docs + embeddings tables with expected columns."""
    original_db = _get_db_path
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            def _patched():
                return os.path.join(tmpdir, "test.db")
            globals()["_get_db_path"] = _patched
            conn = init_db()
            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            assert "docs" in tables
            assert "embeddings" in tables
            doc_cols = {row[1] for row in conn.execute("PRAGMA table_info(docs)")}
            assert "verified" in doc_cols
            assert "content_hash" in doc_cols
            conn.close()
    finally:
        globals()["_get_db_path"] = original_db


def test() -> int:
    """Run every test_* function in this module. Returns exit code 0/1."""
    tests = sorted(
        (name, fn)
        for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    if not tests:
        print("No tests found")
        return 1

    module_file = os.path.abspath(__file__)
    total_asserts = 0
    failures: list[tuple[str, str]] = []

    # Precompute the source line range of every assert statement in each test
    # function. The tracer counts one execution per assert statement, which
    # handles multi-line (parenthesized) asserts and asserts inside loops.
    assert_ranges: dict[int, list[tuple[int, int]]] = {}
    for _name, fn in tests:
        try:
            tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        except (OSError, SyntaxError, TypeError):
            continue
        offset = fn.__code__.co_firstlineno - 1
        assert_ranges[id(fn.__code__)] = [
            (node.lineno + offset, node.end_lineno + offset)
            for node in ast.walk(tree)
            if isinstance(node, ast.Assert)
            and node.lineno is not None
            and node.end_lineno is not None
        ]

    for name, fn in tests:
        counter = [0]
        frame_last: dict[int, tuple[int, int] | None] = {}

        def tracer(frame, event, _arg, _counter=counter, _frame_last=frame_last):
            if (
                event == "line"
                and os.path.abspath(frame.f_code.co_filename) == module_file
            ):
                ranges = assert_ranges.get(id(frame.f_code))
                if ranges:
                    line_no = frame.f_lineno
                    active = next(
                        (r for r in ranges if r[0] <= line_no <= r[1]), None
                    )
                    fid = id(frame)
                    last = _frame_last.get(fid)
                    if active is not None and last != active:
                        _counter[0] += 1
                        _frame_last[fid] = active
                    elif active is None:
                        _frame_last[fid] = None
            return tracer

        sys.settrace(tracer)
        try:
            fn()
        except AssertionError as exc:
            failures.append((name, str(exc)))
            print(f"  ✗ {name}: FAILED — {exc}")
        except Exception as exc:  # noqa: BLE001 — any unexpected error fails the test
            failures.append((name, repr(exc)))
            print(f"  ✗ {name}: ERROR — {exc!r}")
        else:
            print(f"  ✓ {name} ({counter[0]} assertions)")
        finally:
            sys.settrace(None)
        total_asserts += counter[0]

    print(
        f"\n{len(tests) - len(failures)}/{len(tests)} tests passed, "
        f"{total_asserts} assertions executed"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    main()
