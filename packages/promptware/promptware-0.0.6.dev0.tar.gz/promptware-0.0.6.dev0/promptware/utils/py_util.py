from __future__ import annotations

from hashlib import sha256
import re


def hash_url_to_filename(url, etag=None):
    """
    Convert `url` into a hashed filename in a repeatable way.
    If `etag` is specified, append its hash to the url's, delimited
    by a period.
    If the url ends with .h5 (Keras HDF5 weights) adds '.h5' to the name
    so that TF 2.0 can identify it as a HDF5 file
    (see https://github.com/tensorflow/tensorflow/blob/00fad90125b18b80f
    e054de1055770cfb8fe4ba3/tensorflow/python/keras/engine/network.py#L1380)
    """
    url_bytes = url.encode("utf-8")
    url_hash = sha256(url_bytes)
    filename = url_hash.hexdigest()

    if etag:
        etag_bytes = etag.encode("utf-8")
        etag_hash = sha256(etag_bytes)
        filename += "." + etag_hash.hexdigest()

    if url.endswith(".py"):
        filename += ".py"

    return filename


def _hash_python_lines(lines: list[str]) -> str:
    filtered_lines = []
    for line in lines:
        line = re.sub(r"#.*", "", line)  # remove comments
        if line:
            filtered_lines.append(line)
    full_str = "\n".join(filtered_lines)

    # Make a hash from all this code
    full_bytes = full_str.encode("utf-8")
    return sha256(full_bytes).hexdigest()
