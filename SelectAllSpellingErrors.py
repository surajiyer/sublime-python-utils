import sublime
import sublime_plugin


class HashableRegion(sublime.Region):
    def __hash__(self):
        return hash((self.a, self.b))


class SelectAllSpellingErrorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = set()
        while True:
            self.view.run_command('next_misspelling')
            region = self.view.sel()[0]
            region = HashableRegion(region.a, region.b, region.xpos)
            if region not in regions:
                regions.add(region)
            else:
                break
        self.view.sel().clear()
        self.view.sel().add_all(regions)


class DeleteAllSpellingErrorsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        while True:
            self.view.run_command('next_misspelling')
            region = self.view.sel()[0]
            if region.a == region.b:
                break
            else:
                self.view.erase(edit, region)
        self.view.sel().clear()
