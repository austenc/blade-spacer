import sublime, sublime_plugin

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
                
    def spaceTag(self, edit, tag, begin = True):

        regions = self.view.find_all(tag, sublime.LITERAL)
        offset = 0

        for region in regions:
            region.a += offset
            region.b += offset

            # is this a begin tag, or an end tag?
            if(begin == True):
                pos       = region.b
                insert_at = pos
                # If it's a double, is it valid?
                if(tag == '{{' and (self.view.substr(pos) == '{' or self.view.substr(pos) == '-')):
                    continue

            else:
                pos       = region.a - 1
                insert_at = region.a
                if(tag == '}}' and (self.view.substr(pos) == '}' or self.view.substr(pos) == '-')):
                    continue
                    
            # insert spaces if we made it this far
            if(self.view.substr(pos) != ' '):
                self.view.insert(edit, insert_at, ' ')
                offset += 1


class BladeSpacerFiveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for sel in self.view.sel():

            last = sel.end()

            # Insert an exclamation like usual keypress
            self.view.insert(edit, last, "!")

            # Add space and ending
            self.view.insert(edit, last+1, "  !!")
            
            # move cursor to middle
            self.view.sel().subtract(sublime.Region(last+5, last+5))
            self.view.sel().add(sublime.Region(last+2, last+2))


class BladeSpacerCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for sel in self.view.sel():

            last = sel.end()

            # Insert a dash like usual keypress
            self.view.insert(edit, last, '-')

            # Erase the space preceeding char before last
            self.view.erase(edit, sublime.Region(last-1, last-2))

            # Add two spaces and two dashes at end
            pos = last
            self.view.insert(edit, pos+1, ' --')
            
            # move cursor to middle
            middle = pos+1

            self.view.sel().subtract(sublime.Region(pos, pos))            
            self.view.sel().add(sublime.Region(middle, middle))


class BladeSpacerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # insert any closing brackets like sublime normally does
        self.view.run_command('insert_snippet', {"contents": "{${0:$SELECTION}}"})

        for sel in self.view.sel():
            size = sel.size()

            # if we're not selecting text
            if (size == 0):
                last           = sel.end()
                lastChar       = self.view.substr(last-1)
                charBeforeLast = self.view.substr(last-2)
                charBeforeThat = self.view.substr(last-3)

                # did we type two curly braces?
                if(lastChar == '{' and charBeforeLast == '{'):
                    # If this is something like {{{}  }}
                    if(charBeforeThat == '{'):
                        # remove following 2 spaces and add usual spacing
                        self.view.erase(edit, sublime.Region(last+1, last+3))
                        self.addSpaces(edit, last)
                    else:
                        self.addSpaces(edit, last)

                # triple {{{ }}}
                elif(lastChar == '{' and charBeforeLast == ' ' and charBeforeThat == '{'):
                    # erase previous space
                    self.view.erase(edit, sublime.Region(last-1, last-2))
                    
                    # erase latter space
                    self.view.erase(edit, sublime.Region(last, last+1))

                    # add two spaces and center
                    self.addSpaces(edit, last-1)
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
                if (charBeforeThat == '{' and charBeforeStart == '{' and charAfterEnd == '}' and charAfterThat == '}'):
                    # put a space on either side of the selection
                    self.view.insert(edit, start, ' ')
                    self.view.insert(edit, end + 1, ' ')

                # more than double
                elif(charEvenBeforeThat == '{' and charBeforeThat == ' ' and charBeforeStart == '{' and charAfterEnd == '}' and charAfterThat == ' ' and charEvenAfterThat == '}'):
                    # erase previous space
                    self.view.erase(edit, sublime.Region(start - 1, start - 2))
                    
                    # erase latter space
                    self.view.erase(edit, sublime.Region(end,  end + 1))

                    # rewrap the selection
                    self.view.insert(edit, start - 1, ' ')
                    self.view.insert(edit, end, ' ')


    def addSpaces(self, edit, pos):
        # subtract current region from selection
        self.view.sel().subtract(sublime.Region(pos, pos))

        # add 2 spaces
        self.view.insert(edit, pos, '  ')

        # move cursor to middle
        middle = pos + 1
        
        self.view.sel().add(sublime.Region(middle, middle))

