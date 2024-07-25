
# NOTE: Model (serial port) is dynamically loaded

from controller.main import Controller
from view.main import View

view = View()
controller = Controller(view)
controller.start()