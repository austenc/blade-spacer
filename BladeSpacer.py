import sublime, sublime_plugin

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
            self.view.sel().subtract(sublime.Region(pos,pos))
            self.view.sel().add(sublime.Region(middle, middle))


class BladeSpacerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # insert any closing brackets like sublime normally does
        self.view.run_command('insert_snippet', {"contents": "{$0}"})

        for sel in self.view.sel():
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

            #triple {{{ }}}
            elif(lastChar == '{' and charBeforeLast == ' ' and charBeforeThat == '{'):
                # erase previous space
                self.view.erase(edit, sublime.Region(last-1, last-2))
                
                # erase latter space
                self.view.erase(edit, sublime.Region(last, last+1))

                # add two spaces and center
                self.addSpaces(edit, last-1)

    def addSpaces(self, edit, pos):
        # subtract current region from selection
        self.view.sel().subtract(sublime.Region(pos, pos))

        # add 2 spaces
        self.view.insert(edit, pos, '  ')

        # move cursor to middle
        middle = pos + 1
        
        self.view.sel().add(sublime.Region(middle, middle))

