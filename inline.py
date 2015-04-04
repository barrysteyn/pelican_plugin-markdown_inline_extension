# -*- coding: utf-8 -*-
"""
Markdown Inline Extension For Pelican
=====================================
Extends pelican python's markdown module
and allows for customized inline html
"""

import os
import sys

from pelican import signals

try:
    from . pelican_inline_markdown_extension import PelicanInlineMarkdownExtension
except ImportError as e:
    PelicanInlineMarkdownExtension = None
    print("\nMarkdown is not installed - inline markdown extension disabled\n")

def process_settings(pelicanobj):
    """Sets user specified settings (see README for more details)"""

    # Default settings
    inline_settings = {}
    inline_settings['config'] = {'[*]':('', 'pelican-inline')}

    # Get the user specified settings
    try:
        settings = pelicanobj.settings['MD_INLINE']
    except:
        settings = None

    # If settings have been specified, add them to the config
    if isinstance(settings, dict):
        inline_settings['config'].update(settings)

    return inline_settings

def inline_markdown_extension(pelicanobj, config):
    """Instantiates a customized markdown extension"""

    # Instantiate markdown extension and append it to the current extensions
    try:
        pelicanobj.settings['MD_EXTENSIONS'].append(PelicanInlineMarkdownExtension(config))
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write("\nError - the pelican markdown extension failed to configure. Inline markdown extension is non-functional.\n")
        sys.stderr.flush()

def pelican_init(pelicanobj):
    """Loads settings and instantiates the Python markdown extension"""

    # If there was an error loading markdown, then do not process any further 
    if not PelicanInlineMarkdownExtension:
        return

    # Process settings
    config = process_settings(pelicanobj)

    # Configure Markdown Extension
    inline_markdown_extension(pelicanobj, config)

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
