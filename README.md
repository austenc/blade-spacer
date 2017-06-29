Laravel Blade Spacer
============

Automatically adds spaces to laravel blade syntax for readability.

Plugin for Sublime Text 3 that adds in spaces after the opening blade tag and before the closing tag. Doing it manually gets overly tedious sometimes so I wrote this plugin, cheers!

Installing
----------
### Easy Install (Package Control)
You can install this plugin through the [Package Control](https://packagecontrol.io/installation).

1. Press ⌘/Ctrl + ⇧ + P to open the command palette.
2. Type `Package Control: Install Package` and press enter. Then search for `Laravel Blade Spacer`.


### Manual Installation (Not Recommended)
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

_The cursor is represented by ` | ` in the examples:_

 * typing `{{` will yield `{{ | }}` -- notice the spaces and cursor position
 * should work with `{{{  }}}` and `{{-- Comments --}}` too!
 * Laravel5 syntax support `{!! | !!}`

 **Since 2.2.0**
 A command has been added to space every set of blade syntax tags in the currently open file. It is under the 'Blade Spacer: Format File' option in the command palette (`Ctrl+Shift+P` by default in windows / linux, and `Cmd+Shift+P` on mac).

Feedback welcome, [open an issue here](https://github.com/austenc/blade-spacer/issues). 
