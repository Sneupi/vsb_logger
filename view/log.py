
from .widgets.file_action import FileAction

class LogView(FileAction):
    """View for Log file menu"""
    # wrapper for naming consistency
    def __init__(self, master):
        super().__init__(master, text="Log CPI")
    