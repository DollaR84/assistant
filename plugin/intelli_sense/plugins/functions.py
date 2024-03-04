from assistant.base_plugin import BasePlugin

from assistant.base.types import PluginCommand


class FunctionPlugin(BasePlugin):

    def process_selection(self, file, selection_text, start_pos, end_pos):
        def process_selection(self, file, selection_text, start_pos, end_pos):
        project_name = None
        for name, path in self.cfg.projects.items():
            if path in file:
                project_name = name

        if project_name:
            self.fs.write_queue(
                project_name, PluginCommand.FUNCTION.value, file,
                selection_text=selection_text, start_pos=start_pos, end_pos=end_pos,
            )


if __name__ == "__main__":
    FunctionPlugin().check_selection()
