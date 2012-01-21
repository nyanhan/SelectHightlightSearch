# coding=utf-8
import sublime
import sublime_plugin
import re

Active = False
Select = ""

class SelectHightlightSearch(sublime_plugin.TextCommand):

	def run(self, edit):
		sel = self.view.sel()[0]
		sel = self.view.word(min(sel.a, sel.b))
		word = self.view.substr(sel)
		word = self.filter(word)

		if word is None:
			return

		try:
			others = self.view.find_all(word, sublime.LITERAL)
			global Select
			Select = word
		except:
			print "find_all error !"
			return
		
		self.hightlight(others)
		self.view.window().run_command("slurp_find_string")

	def filter(self, word):
		word = word.strip()

		if re.search('[a-zA-Z0-9$_]', word) is None:
			return None
		else:
			return word

	def hightlight(self, arr):
		global Active, Force
		self.view.add_regions("select_hightlight_search", arr, "invalid.deprecated", sublime.DRAW_EMPTY_AS_OVERWRITE)
		Active = True
		Force = True
	

class SelectHightlightSearchEvent(sublime_plugin.EventListener):

	def on_selection_modified(self, view):
		global Active, Force
		if Active:
			# if sel.a == sel.b:
			# 	Force = False
			# 	return
			
			if Force:
				Force = False
				return
			sel = view.sel()[0]
			sel = view.word(min(sel.a, sel.b))
			word = view.substr(sel)
			word = word.strip()
			if word.find(Select) >= 0:
				return
			
			view.erase_regions("select_hightlight_search")
			Active = False

	def on_activated(self, view):
		view.erase_regions("select_hightlight_search")
