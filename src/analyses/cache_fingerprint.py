#!/usr/bin/env python3
"""Deterministic content fingerprints for resumable analysis caches.

This module has no executable output.  It centralizes cache signatures so a cache
is reused only when its input files, arrays, topology, and declared parameters are
identical to those used when the cache was written.
"""
from __future__ import annotations

from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Iterable, Mapping

import numpy as np


@lru_cache(maxsize=None)
def _file_sha256(path_text: str) -> str:
    """Return the SHA-256 digest of one immutable-on-run input file."""
    path = Path(path_text)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _update_array(digest: object, name: str, value: np.ndarray) -> None:
    """Add an array name, dtype, shape, and exact C-order bytes to a digest."""
    array = np.asarray(value)
    digest.update(name.encode("utf-8"))
    digest.update(str(array.dtype).encode("ascii"))
    digest.update(json.dumps(array.shape).encode("ascii"))
    if array.dtype.hasobject:
        payload = json.dumps(array.tolist(), ensure_ascii=False, sort_keys=True).encode("utf-8")
        digest.update(payload)
    else:
        contiguous = np.ascontiguousarray(array)
        digest.update(memoryview(contiguous).cast("B"))


def content_signature(
    label: str,
    *,
    files: Iterable[Path] = (),
    arrays: Mapping[str, np.ndarray] | None = None,
    parameters: Mapping[str, object] | None = None,
) -> str:
    """Build a stable SHA-256 signature for one cache contract."""
    digest = hashlib.sha256()
    digest.update(label.encode("utf-8"))
    for path in sorted((Path(item).resolve() for item in files), key=str):
        if not path.is_file():
            raise FileNotFoundError(f"Cache-signature input does not exist: {path}")
        digest.update(path.name.encode("utf-8"))
        digest.update(_file_sha256(str(path)).encode("ascii"))
    for name, value in sorted((arrays or {}).items()):
        _update_array(digest, name, value)
    normalized_parameters = json.dumps(
        parameters or {},
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
        default=str,
    )
    digest.update(normalized_parameters.encode("ascii"))
    return digest.hexdigest()


def cache_matches(container: object, expected_signature: str) -> bool:
    """Return whether an opened NumPy archive contains the expected signature."""
    try:
        return str(container["signature"].item()) == expected_signature
    except (KeyError, ValueError, AttributeError):
        return False
