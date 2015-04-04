# -*- coding: utf-8 -*-
"""
Math Render Plugin for Pelican
==============================
This plugin allows your site to render Math. It uses
the MathJax JavaScript engine.

For markdown, the plugin works by creating a Markdown
extension which is used during the markdown compilation stage.
Math therefore gets treated like a "first class citizen" in Pelican

For reStructuredText, the plugin instructs the rst engine
to output Mathjax for for math.

The mathjax script is automatically inserted into the HTML.

Typogrify Compatibility
-----------------------
This plugin now plays nicely with Typogrify, but it requires
Typogrify version 2.04 or above.

User Settings
-------------
Users are also able to pass a dictionary of settings in the settings file which
will control how the MathJax library renders things. This could be very useful
for template builders that want to adjust the look and feel of the math.
See README for more details.
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
    inline_settings['config'] = {'[*]':'pelican-inline'}

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
    """Instantiates a customized markdown extension for handling mathjax
    related content"""

    # Instantiate markdown extension and append it to the current extensions
    try:
        pelicanobj.settings['MD_EXTENSIONS'].append(PelicanInlineMarkdownExtension(config))
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write("\nError - the pelican markdown extension failed to configure. Inline markdown extension is non-functional.\n")
        sys.stderr.flush()

def pelican_init(pelicanobj):
    """Loads the mathjax script according to the settings. Instantiate the Python
    markdown extension, passing in the mathjax script as config parameter
    """

    # If there was am error loading markdown, then do not process any further 
    if not PelicanInlineMarkdownExtension:
        return

    # Process settings
    settings = process_settings(pelicanobj)

    # Configure Markdown Extension
    inline_markdown_extension(pelicanobj, settings)

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
