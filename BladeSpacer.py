import sublime, sublime_plugin

class BladeSpacerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for sel in self.view.sel():

			# the previously typed letter position
			last = sel.end()

			# insert any closing brackets like sublime normally does
			self.view.run_command('insert_snippet', {"contents": "{$0}"})

			print(self.view.substr(last-1)+'| 1')
			print(self.view.substr(last-2)+'| 2')

			# was the last typed character a curly brace?
			if(self.view.substr(last-1) == '{'):
				self.addSpaces(edit, last)

			# probably a triple curly brace
			elif(self.view.substr(last-1) == ' ' and self.view.substr(last-2) == '{'):
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
