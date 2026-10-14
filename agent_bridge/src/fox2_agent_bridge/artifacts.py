"""Canonical generated text. Raw/binary evidence must use its own byte contract."""
import json
import os
import tempfile
from pathlib import Path


def canonical_text(value: str) -> str:
    return '\n'.join(line.rstrip() for line in value.replace('\r\n', '\n').replace('\r', '\n').splitlines()).rstrip('\n') + '\n'


def text_hygiene(path: Path) -> None:
    raw = path.read_bytes()
    value = raw.decode('utf-8')
    if raw.startswith(b'\xef\xbb\xbf') or value != canonical_text(value):
        raise ValueError(f'noncanonical generated text: {path.name}')


def write_text(path: Path, value: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(canonical_text(value))
        text_hygiene(Path(temporary))
        os.replace(temporary, path)
        text_hygiene(path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path


def write_json(path: Path, value: object) -> Path:
    return write_text(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
