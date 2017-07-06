import sublime
import sublime_plugin


class BladeSpacerFormatFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()

        # Run the text command
        view.run_command('blade_spacer_format')


class BladeSpacerFormatCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # triple-brace
        self.spaceTag(edit, '{{{')
        self.spaceTag(edit, '}}}', False)

        # L5
        self.spaceTag(edit, '{!!')
        self.spaceTag(edit, '!!}', False)

        # comments
        self.spaceTag(edit, '{{--')
        self.spaceTag(edit, '--}}', False)

        # double-brace
        self.spaceTag(edit, '{{')
        self.spaceTag(edit, '}}', False)

    def spaceTag(self, edit, tag, begin=True):

        regions = self.view.find_all(tag, sublime.LITERAL)
        offset = 0

        for region in regions:
            region.a += offset
            region.b += offset

            # is this a begin tag, or an end tag?
            if begin is True:
                pos = region.b
                insert_at = pos
                # If it's a double, is it valid?
                if self.validSequence(tag, self.view.substr(pos)):
                    continue

            else:
                pos = region.a - 1
                insert_at = region.a
                if self.validSequence(tag, self.view.substr(pos), '}'):
                    continue

            # insert spaces if we made it this far
            if(self.view.substr(pos) != ' '):
                self.view.insert(edit, insert_at, ' ')
                offset += 1

    def validSequence(self, tag, char, check='{'):
        return (tag == check * 2 and (char == check or char == '-'))


# Handles {!! !!} style entries
class BladeSpacerFiveCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for sel in self.view.sel():

            last = sel.end()
            endOfLine = self.view.find_by_class(
                last, True, sublime.CLASS_LINE_END)
            lineStr = self.view.substr(sublime.Region(last, endOfLine))

            # Insert an exclamation like usual keypress
            self.view.insert(edit, last, "!")

            # This is a new set of braces
            if (lineStr[0] == '}'):
                # Add space and ending
                self.view.insert(edit, last + 1, "  !!")

                # move cursor to middle
                self.view.sel().subtract(sublime.Region(last + 5, last + 5))
                self.view.sel().add(sublime.Region(last + 2, last + 2))

            # Otherwise we're changing an already existing set
            else:
                closingPos = lineStr.find('}')
                insertPos = last + closingPos + 1
                self.view.erase(edit, sublime.Region(insertPos, insertPos + 1))
                self.view.insert(edit, insertPos, '!!')


# This is only called when there is a selection, and the preceding text
# contains a string like `{{ `
class BladeSpacerFiveSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Surround the selection with dashes
        self.view.run_command(
            'insert_snippet', {"contents": "!${0:$SELECTION}!"})

        for sel in self.view.sel():

            begin = sel.begin()
            end = sel.end()
            before = self.view.substr(sublime.Region(begin, begin - 3))
            # if typing some blade comments with this selection, add spaces
            if before == "{!!":
                # add new spaces
                self.view.insert(edit, begin, ' ')
                self.view.insert(edit, end + 1, ' ')


# Called when there is NO selection made and preceding text looks like `{{ -`
class BladeSpacerCommentCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for sel in self.view.sel():

            last = sel.end()

            # Insert a dash like usual keypress
            self.view.insert(edit, last, '-')

            # Erase the space preceeding char before last
            self.view.erase(edit, sublime.Region(last - 1, last - 2))

            # Add two spaces and two dashes at end
            pos = last
            self.view.insert(edit, pos + 1, ' --')

            # move cursor to middle
            middle = pos + 1

            self.view.sel().subtract(sublime.Region(pos, pos))
            self.view.sel().add(sublime.Region(middle, middle))


# This is only called when there is a selection, and the preceding text
# contains a string like `{{ `
class BladeSpacerCommentSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Surround the selection with dashes
        self.view.run_command(
            'insert_snippet', {"contents": "-${0:$SELECTION}-"})

        for sel in self.view.sel():

            begin = sel.begin()
            end = sel.end()
            before = self.view.substr(sublime.Region(begin, begin - 4))
            # if typing some blade comments with this selection, add spaces
            if before == "{ --":
                # remove the extra spaces
                self.view.erase(edit, sublime.Region(begin - 3, begin - 2))
                self.view.erase(edit, sublime.Region(end + 1, end + 2))
                # add new spaces
                self.view.insert(edit, begin - 1, ' ')
                self.view.insert(edit, end, ' ')

# Handles the general {{ }} and {{{ }}}
class BladeSpacerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # insert any closing brackets like sublime normally does
        self.view.run_command(
            'insert_snippet', {"contents": "{${0:$SELECTION}}"})

        for sel in self.view.sel():

            # if we're not selecting text
            if (sel.empty()):
                last = sel.end()
                lastChar = self.view.substr(last - 1)
                charBeforeLast = self.view.substr(last - 2)
                charBeforeThat = self.view.substr(last - 3)
                charAfter = self.view.substr(last + 1)

                # did we type two curly braces?
                if(lastChar == '{' and charBeforeLast == '{'):
                    # If this is something like {{{}  }}
                    if(charBeforeThat == '{'):
                        endOfLine = self.view.find_by_class(
                            last, True, sublime.CLASS_LINE_END)
                        lineStr = self.view.substr(
                            sublime.Region(last, endOfLine))
                        # since we automatically add a curly bracket, we need
                        # to check beyond this
                        firstCurly = lineStr.find('}')
                        nextCurly = lineStr.find('}', firstCurly + 1)

                        # check to see if we're adding brackets to an existing
                        # set, fix if needed
                        if (nextCurly != -1):
                            self.view.erase(
                                edit, sublime.Region(last, last + 1))
                            self.view.insert(
                                edit, last + (nextCurly - firstCurly), '}')

                    else:
                        # If we're typing this in the middle of some quotes,
                        # add an additional end curly brace, since sublime
                        # doesn't auto-close braces inside quotes all the time
                        if (charBeforeThat == '"' and charAfter == '"'):
                            self.view.insert(edit, last + 1, '}')

                        self.addSpaces(edit, last)

                # triple {{{ }}}
                elif(lastChar == '{' and
                        charBeforeLast == ' ' and
                        charBeforeThat == '{'):
                    # erase previous space
                    self.view.erase(edit, sublime.Region(last - 1, last - 2))

                    # erase latter space
                    self.view.erase(edit, sublime.Region(last, last + 1))

                    # add two spaces and center
                    self.addSpaces(edit, last - 1)
            # We are selecting text, so mind the selection
            else:
                start = sel.begin()
                end = sel.end()
                charBeforeStart = self.view.substr(start - 1)
                charBeforeThat = self.view.substr(start - 2)
                charEvenBeforeThat = self.view.substr(start - 3)
                charAfterEnd = self.view.substr(end)
                charAfterThat = self.view.substr(end + 1)
                charEvenAfterThat = self.view.substr(end + 2)

                # Double {{ }}
                if (charBeforeThat == '{' and charBeforeStart == '{' and
                        charAfterEnd == '}' and charAfterThat == '}'):
                    # put a space on either side of the selection
                    self.view.insert(edit, start, ' ')
                    self.view.insert(edit, end + 1, ' ')

                # more than double, like {{{ }}}
                elif(charEvenBeforeThat == '{' and
                        charBeforeThat == ' ' and
                        charBeforeStart == '{' and
                        charAfterEnd == '}' and
                        charAfterThat == ' ' and
                        charEvenAfterThat == '}'):
                    # erase previous space
                    self.view.erase(edit, sublime.Region(start - 1, start - 2))

                    # erase latter space
                    self.view.erase(edit, sublime.Region(end, end + 1))

                    # rewrap the selection
                    self.view.insert(edit, start - 1, ' ')
                    self.view.insert(edit, end, ' ')

    def addSpaces(self, edit, pos):
        # subtract current region from selection so we don't end up with
        # two selections in some cases
        self.view.sel().subtract(sublime.Region(pos, pos))

        # add 2 spaces
        self.view.insert(edit, pos, '  ')

        # move cursor to middle
        middle = pos + 1

        self.view.sel().add(sublime.Region(middle, middle))
