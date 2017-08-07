# Release Notes

## [Unreleased]

## v2.4.3
 - Enabled plugin in `.vue` file scope

## v2.4.2
 - Fixed automatic braces when inside a quote i.e. `<h1 class="|">` - #5

## v2.4.1
 - Added support for wrapping a selection with `{!! !!}`  - #12

## v2.4.0
 - Restrict plugin keybinds to only take effect in PHP and blade files #9
 - Comment syntax now surrounds pre-existing selections properly - #10

## v2.3.0
 - Surround selection by typing braces after making a selection
 - Convert a double brace `{{` to L5 unescaped without it being weird
 - Bugfix for #4
_Thanks @grantholle for this new feature!_

## v2.2.0
 - 'Format File' command to format an entire file at once

## v2.1.0
 - Added Laravel 5 unescaped tag support `{!!  !!}`

## v2.0.0
 - Added multi-cursor support
 - Added support for blade comments `{{-- --}}`
