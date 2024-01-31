"""
A Pelican plugin which minifies HTML pages.

Based on https://github.com/PhasecoreX/pelican-minify
"""

import logging
import os

from htmlmin import minify
from pelican import signals

# We need save unicode strings to files.
try:
    from codecs import open
except ImportError:
    pass

logger = logging.getLogger(__name__)


def minify_html(pelican):
    """Minify all HTML files.
    :param pelican: The Pelican instance.
    """
    options = pelican.settings.get("MINIFY", {})
    files_to_minify = []

    for dirpath, _, filenames in os.walk(pelican.settings["OUTPUT_PATH"]):
        files_to_minify += [
            os.path.join(dirpath, name)
            for name in filenames
            if name.endswith(".html") or name.endswith(".htm")
        ]

    for filepath in files_to_minify:
        create_minified_file(filepath, options)


def create_minified_file(filename, options):
    """Create a minified HTML file, overwriting the original.
    :param str filename: The file to minify.
    """
    with open(filename, encoding="utf-8") as uncompressed_f:
        uncompressed = uncompressed_f.read()

    with open(filename, "w", encoding="utf-8") as f:
        try:
            logger.debug("Minifying: %s" % filename)
            compressed = minify(uncompressed, **options)
            f.write(compressed)
        except Exception as ex:
            logger.critical("HTML Minification failed: %s" % ex)


def register():
    """Run the HTML minification stuff after all articles have been generated,
    at the very end of the processing loop.
    """
    signals.finalized.connect(minify_html)
