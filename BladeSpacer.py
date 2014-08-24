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
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(middle, middle))


class BladeSpacerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for sel in self.view.sel():

            last           = sel.end()
            lastChar       = self.view.substr(last-1)
            charBeforeLast = self.view.substr(last-2)


            # insert any closing brackets like sublime normally does
            self.view.run_command('insert_snippet', {"contents": "{$0}"})

            # was the last typed character a curly brace?
            if(lastChar == '{'):
                self.addSpaces(edit, last)

            # triple {{{ }}}
            elif(lastChar == ' ' and charBeforeLast == '{'):
                # erase previous space
                self.view.erase(edit, sublime.Region(last, last-1))
                
                # erase latter space
                self.view.erase(edit, sublime.Region(last+1, last+2))

                # add two spaces and center! write function 
                self.addSpaces(edit, last-1)

    def addSpaces(self, edit, pos):
        # add 2 spaces
        self.view.insert(edit, pos+1, '  ')

        # move cursor to middle
        middle = pos+2
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(middle, middle))
