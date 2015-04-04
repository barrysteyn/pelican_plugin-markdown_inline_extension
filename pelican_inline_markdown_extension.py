# -*- coding: utf-8 -*-
"""
Pelican Inline Markdown Extension
==================================
An extension for the Python Markdown module that enables
the Pelican python blog add inline patterns. This extension
gives Pelican the ability to use Mathjax as a "first class
citizen" of the blog
"""

import markdown
import re

from markdown.util import etree
from markdown.util import AtomicString

class PelicanInlineMarkdownExtensionPattern(markdown.inlinepatterns.Pattern):
    """Inline markdown processing that matches mathjax"""

    def __init__(self, pelican_markdown_extension, tag, pattern):
        super(PelicanInlineMarkdownExtensionPattern,self).__init__(pattern)
        self.tag = tag
        self.config = pelican_markdown_extension.getConfig('config')

    def handleMatch(self, m):
        node = markdown.util.etree.Element(self.tag)
        tag_class = self.config.get(m.group('prefix'), 'pelican-inline')
        node.set('class', tag_class)
        node.text = markdown.util.AtomicString(m.group('text'))

        # If mathjax was successfully matched, then JavaScript needs to be added
        # for rendering. The boolean below indicates this
        return node

class PelicanInlineMarkdownExtension(markdown.Extension):
    """A markdown extension enabling mathjax processing in Markdown for Pelican"""
    def __init__(self, config):

        try:
            # Needed for markdown versions >= 2.5
            self.config['config'] = ['{}', 'config for markdown extension']
            super(PelicanInlineMarkdownExtension,self).__init__(**config)
        except AttributeError:
            # Markdown versions < 2.5
            config['config'] = [config['config'], 'config for markdown extension']
            super(PelicanInlineMarkdownExtension, self).__init__(config)

    def extendMarkdown(self, md, md_globals):
        # Regex to detect mathjax
        config = self.getConfig('config')
        patterns = []

        # The following mathjax settings can be set via the settings dictionary
        for key in config:
            patterns.append(re.escape(key))

        inline_regex = r'(?P<prefix>%s)(?P<text>.+?)\2' % ('|'.join(patterns))

        # Process after escapes
        md.inlinePatterns.add('texthighlight_inlined', PelicanInlineMarkdownExtensionPattern(self, 'span', inline_regex), '>escape')
