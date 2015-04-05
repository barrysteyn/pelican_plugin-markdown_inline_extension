Markdown Inline Extension For Pelican
=====================================
This plugin lets you customize inline html
within markdown by extending pythons markdown module

Installation
------------
To enable, ensure that the `md_inline_extension` plugin is accessible.
Then add the following to settings.py:

    PLUGINS = ["md_inline_extension"]

Usage
-----
By default, any markdown text inside `[*]...[*]` will get wrapped in
`span` tags with a class of `pelican-inline`. For example:

`[*]Lorem ipsum dolor sit amet, consectetur adipiscing elit[*]` will
become `<span class="pelican-inline">Lorem ipsum dolor sit amet, consectetur adipiscing elit</span>`

You can create your own inline patterns and associate them with
arbitrary classes and styles by using the `MD_INLINE` dictionary in settings.
The dictionary takes a pattern as key and expects either a string or a tuple
as a value. If a string is provided, then that will be the css class. If
a tuple is provided, then the first value will be the style, and the second
value (if exsists) will be the class. For example:

```
MD_INLINE = {
    '+=+': ('color:red', 'my-test-class'),
    '|-|': ('style,),
    '&^': 'my-other-text-class',
}
```

The above defines three new inline patterns:

 1. **+=+**: Text within `+=+` will be wrapped in `span` tags like so
: `<span style="color:red" class="my-test-class">...</span>`
 2. **|-|**: Text within `|-|` will be wrapped in
`<span style="color:blue">...</span>`. Note - no class is present
 3. **&^**: Text within `&^` will be wrapped in
`<span class="my-other-text-class">...</span>`. Note - no style present
