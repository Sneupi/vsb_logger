from .graphing import LiveGraphTk

class GraphView(LiveGraphTk):
    """Graphing view"""
    # wrapper just for naming consistency
    def __init__(self, master):
        super().__init__(master, interval=1000)