
from .widgets.file_action import FileAction

class LogView(FileAction):
    """View for Log file menu"""
    # wrapper for naming consistency
    def __init__(self, master, toggle_func=None):
        super().__init__(master, action_name="Log CPI", toggle_func=toggle_func)
    