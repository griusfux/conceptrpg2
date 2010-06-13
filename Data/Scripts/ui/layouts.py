import bgui

class DunGenLayout(bgui.Widget):
	
	def __init__(self, sys):
		
		bgui.Widget.__init__(self, sys, "dun_gen_layout", [1, 1])
		
		self.screen = bgui.Image(self, 'dun_gen_img', 'Textures/generatingw.png', size=[1, 1])
		
	# def _draw(self):
		# print("Me draws now?")