import sublime, sublime_plugin

class BladeSpacerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for sel in self.view.sel():

			# the previously typed letter position
			first = sel.end()

			# insert any closing brackets like sublime normally does
			self.view.run_command('insert_snippet', {"contents": "{$0}"})

			if(self.view.substr(first-1) == '{'):
				# add 2 spaces
				self.view.insert(edit, first+1, '  ')

				# move cursor to middle
				middle = first+2
				self.view.sel().clear()
				self.view.sel().add(sublime.Region(middle, middle))