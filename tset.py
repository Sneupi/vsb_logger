from controller import TestController, TestView
view = TestView()
controller = TestController(view)
controller.start()