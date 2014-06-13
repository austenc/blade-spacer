blade-spacer
============

Automatically adds spaces to laravel blade syntax for readability.

Plugin for Sublime Text 3 that adds in spaces after the opening blade tag and before the closing tag. Doing it manually gets overly tedious sometimes so I wrote this plugin, cheers!

Installing
----------
**Without Git:** Download the latest source from `GitHub <http://github.com/austenc/blade-spacer>`. Copy the whole directory into the Packages directory.

**With Git:** Clone the repository in your Sublime Text Packages directory:

    git clone git://github.com/austenc/blade-spacer.git

The "Packages" packages directory is located at:

* OS X::

    ~/Library/Application Support/Sublime Text 3/Packages/

* Linux::

    ~/.Sublime Text 3/Packages/

* Windows::

    %APPDATA%/Sublime Text 3/Packages/

How it works
----------

Sublime text already handles the auto-closing of braces. This plugin automatically adds spaces between double (or triple) curly braces in blade files for readability.

The cursor in the example will be represented by ` | `

So typing `{{` will yield `{{ | }}` (notice the spaces and cursor position. Naturally `{{{` will also yield `{{{ | }}}` like one would expect. 
