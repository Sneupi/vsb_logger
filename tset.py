import tkinter as tk

# import view.widgets.demos as wd
# wd.demo_all()

# import view.live_graph.demos as lgd
# lgd.demo_livegraph(10)

# import view.demos as vd
# vd.demo_all()

# from view.view import View
# v = View()
# v.start()

from controller.controller import TestController, TestView
tv = TestView()
tc = TestController(tv)
tc.start()