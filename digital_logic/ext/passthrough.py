"""
This extension adds passthrough Blocks to Python-Markdown. Passthrough blocks
are not transformed by the markdown processor at all.
    >>> import markdown
    >>> text = '''
    ... A paragraph before a *passthrough* block:
    ...
    ... +++++
    ... *passed through*
    ... +++++
    ... '''
    >>> html = markdown.markdown(text, extensions=['digital_logic.ext.passthrough'])
    >>> html
    '<p>A paragraph before a <em>passthrough</em> block:</p>\\n*passed through*'
    >>> markdown.markdown(text, extensions=['digital_logic.ext.passthrough'], safe_mode='replace')
    '<p>A paragraph before a <em>passthrough</em> block:</p>\\n*passed through*'
"""

import re

import markdown

# Global vars
PASSTHROUGH_BLOCK_RE = re.compile( \
    r'(?P<passthrough>^\+{5,})[ ]*\n(?P<content>.*?)(?P=passthrough)[ ]*$',
    re.MULTILINE | re.DOTALL
)
PASSTHROUGH_MARKER = '<!-- hyde.passthrough.placeholder -->'


class PassthroughExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        """ Add PassthroughBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('passthrough_block',
                             PassthroughBlockPreprocessor(md),
                             ">normalize_whitespace")

        md.postprocessors.add('passthrough_clean',
                              PassthroughBlockPostProcessor(),
                              "_end")


class PassthroughBlockPostProcessor(markdown.postprocessors.Postprocessor):
    def run(self, text):
        return text.replace(PASSTHROUGH_MARKER, '')


class PassthroughBlockPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, md):
        markdown.preprocessors.Preprocessor.__init__(self, md)

    def getConfig(self, key):
        if key in self.config:
            return self.config[key][0]
        else:
            return None

    def run(self, lines):
        """ Match and store passthrough blocks in the HtmlStash. """

        text = "\n".join(lines)
        while 1:
            m = PASSTHROUGH_BLOCK_RE.search(text)
            if m:
                content = m.group('content')
                content = PASSTHROUGH_MARKER + content
                placeholder = self.markdown.htmlStash.store(content, safe=True)
                text = '%s\n%s\n%s' % (
                text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")


def makeExtension(**kwargs):
    return PassthroughExtension(**kwargs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
