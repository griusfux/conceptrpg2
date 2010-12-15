import bgui
from .layouts import Layout

import Scripts.levels as levels
class LevelUpLayout(Layout):
	"""Layout for LevelUpState"""
	def __init__(self, sys):
		Layout.__init__(self, sys, "lvl_up_overlay", use_mouse=True)
		
		self.init = False
		self.archetype = ''
		
		self.state = {
			'str' : -1,
			'con' : -1,
			'dex' : -1,
			'int' : -1,
			'wis' : -1,
			'cha' : -1
			}
		
		main_frame = bgui.Frame(self, "lvl_main_frame", aspect=(3/2), size=[0, .8],
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED, sub_theme="HUD")
		
		#########
		# Buttons
		btn_frame = bgui.Frame(main_frame, "lvl_btn_frame", size=[1, .1], pos=[0,0], sub_theme="Level")
		self.lvl_btn = bgui.FrameButton(btn_frame, "lvl_btn", text="Accept", pt_size=25,
										size=[.15, .6], pos=[.8, .2])
		self.lvl_btn.on_click = self.accept_on_click
		
		self.lvl_cancel = bgui.FrameButton(btn_frame, "lvl_cancel", text="Cancel", pt_size=25,
										size=[.15, .6], pos=[.6, .2])
		self.lvl_cancel.on_click = self.cancel_on_click
		
		################
		# Abililty Frame
		ability_frame = bgui.Frame(main_frame, "lvl_ab_frame", size=[1, 0.45], pos=[0, 0.55])
		ability_frame.colors = [(0,0,0,0)]*4
		
		## Archetype Frame
		arch_frame = bgui.Frame(ability_frame, "lvl_arch_frame", size=[1/3, 1], pos=[0, 0], sub_theme="Level")
		arch_header = bgui.Frame(arch_frame, "lvl_arch_head", size=[1, .11], pos=[0,.89], sub_theme="Lvl_Header")
		arch_lbl = bgui.Label(arch_header, "lvl_arch_lbl", pos=[0,0], pt_size=20,text="Archetypes",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
								
								
		
		## Abillity Points Frame
		points_frame = bgui.Frame(ability_frame, "lvl_points_frame", size=[1/3, 1], pos=[1/3, 0], sub_theme="Level")
		points_header = bgui.Frame(points_frame, "lvl_points_head", size=[1, .11], pos=[0,.89], sub_theme="Lvl_Header")
		points_lbl = bgui.Label(points_header, "lvl_points_lbl", pos=[0,0], pt_size=20,text="Ability Scores",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		for i, ability in enumerate(("Charisma", "Wisdom", "Intelligence", "Dexterity", "Constitution", "Strength")):
			# Create a shorthand version of ability
			ab = ability[0:3].lower()
			# Display the ability name
			lbl = bgui.Label(points_frame, "lvl_%s_ab"%ab, text=ability, pos=[.05, i*.1+0.05], pt_size=18)
			lbl.on_click = self.ab_lbl_on_click
			
			# Display a box with the score
			score_frame = bgui.Frame(points_frame, "lvl_%s_score_frame"%ab, size=[.1, .08], pos=[1/3+0.05, i*.1+0.025], sub_theme="Box")
			score = bgui.Label(score_frame, "lvl_%s_score"%ab, pos=[0,0], pt_size=16, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			setattr(self, "%s_score"%ab, score)
			
			# Display a box with bonuses
			bonus_frame = bgui.Frame(points_frame, "lvl_%s_bonus_frame"%ab, size=[.1, .08], pos=[0.625, i*.1+0.025], sub_theme="Box")
			bonus = bgui.Label(bonus_frame, "lvl_%s_bonus"%ab, pos=[0,0], pt_size=16, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			setattr(self, "%s_bonus"%ab, bonus)
			
			# Display a box with the final score
			final_frame = bgui.Frame(points_frame, "lvl_%s_final_frame"%ab, size=[.1, .08], pos=[0.8, i*.1+0.025], sub_theme="Box")
			final = bgui.Label(final_frame, "lvl_%s_final"%ab, pos=[0,0], pt_size=16, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
			setattr(self, "%s_final"%ab, final)
			
			# Display up and down arrows next to score box
			up = bgui.Image(points_frame, "lvl_%s_up"%ab, "Textures/ui/up_arrow.png", aspect=1, size=[0, .04], pos=[1/3+0.175, i*.1+.065])
			up.on_click = self.arrow_on_click
			down = bgui.Image(points_frame, "lvl_%s_down"%ab, "Textures/ui/down_arrow.png", aspect=1, size=[0, .04], pos=[1/3+0.175, i*.1+0.025])
			down.on_click = self.arrow_on_click

		points_inst = bgui.TextBlock(points_frame, "lvl_points_inst", pos=[0, 0.75], size=[0.9, .125], 
									pt_size=14, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
		points_inst.text = "Allocate ability points until no unspent points are left"
		
		self.unspent_lbl = bgui.Label(points_frame, "lvl_unspent_lbl", pos=[1/3+0.05, 0.7], pt_size=16)
		
		base_lbl = bgui.Label(points_frame, "lvl_base_lbl", text="Base Score", pt_size=12, pos=[1/3+0.05, .625])
		bonus_lbl = bgui.Label(points_frame, "lvl_bonus_lbl", text="Bonuses", pt_size=12, pos=[.625, .625])
		final_lbl = bgui.Label(points_frame, "lvl_final_lbl", text="Final Score", pt_size=12, pos=[.8, .625])
								
								
		
		## Ability Info Frame
		ab_info_frame = bgui.Frame(ability_frame, "lvl_ab_info_frame", size=[1/3, 1], pos=[2/3, 0], sub_theme="Level")
		ab_info_header = bgui.Frame(ab_info_frame, "lvl_ab_info_head", size=[1, .11], pos=[0,.89], sub_theme="Lvl_Header")
		ab_info_lbl = bgui.Label(ab_info_header, "lvl_ab_info_lbl", pos=[0,0], pt_size=20,text="Ability Details",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		self.ab_info_name = bgui.Label(ab_info_frame, "lvl_ab_info_name", pos=[0.05, .8], pt_size=24)
		self.ab_info_name.text = "Strength"
		self.ab_info = bgui.TextBlock(ab_info_frame, "lvl_ab_info", pos=[0.05, 0.15], size=[0.9, .6], pt_size=18)
		self.ab_info.text = levels.STR_INFO
		
		
		
		#############
		# Power Frame
		power_frame = bgui.Frame(main_frame, "lvl_power_frame", size=[1, 0.45], pos=[0, 0.1])
		power_frame.colors = [(0,0,0,0)]*4
		
		## Available Powers Frame
		available_frame = bgui.Frame(power_frame, "lvl_avail_frame", size=[1/3, 1], pos=[0, 0], sub_theme="Level")
		available_header = bgui.Frame(available_frame, "lvl_available_head", size=[1, .11], pos=[0,.89], sub_theme="Lvl_Header")
		available_lbl = bgui.Label(available_header, "lvl_available_lbl", pos=[0,0], pt_size=20,text="Available Powers",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		## Known Powers Frame
		known_frame = bgui.Frame(power_frame, "lvl_known_frame", size=[1/3, 1], pos=[1/3, 0], sub_theme="Level")
		known_header = bgui.Frame(known_frame, "lvl_known_head", size=[1, .11], pos=[0,.89], sub_theme="Lvl_Header")
		known_lbl = bgui.Label(known_header, "lvl_known_lbl", pos=[0,0], pt_size=20,text="Known Powers",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		
		## Power Info Frame
		pow_info_frame = bgui.Frame(power_frame, "lvl_pow_info_frame", size=[1/3, 1], pos=[2/3, 0], sub_theme="Level")
		pow_info_header = bgui.Frame(pow_info_frame, "lvl_pow_info_head", size=[1, .11], pos=[0,.89], sub_theme="Lvl_Header")
		pow_info_lbl = bgui.Label(pow_info_header, "lvl_pow_info_lbl", pos=[0,0], pt_size=20,text="Power Details",
								options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
	def ab_lbl_on_click(self, widget):
		ab = widget.name[4:7]
		
		full = {
			'str' : 'Strength',
			'con' : 'Constitution',
			'dex' : 'Dexterity',
			'int' : 'Intelligence',
			'wis' : 'Wisdom',
			'cha' : 'Charisma'
			}
			
		self.ab_info_name.text = full[ab]
		self.ab_info.text = getattr(levels, ab.upper()+"_INFO")
		
	def arrow_on_click(self, widget):
		ab = widget.name[4:7]
		sign = widget.name[8:]
		
		
		# Check to see if there is points to spend if up is pressed
		if sign == 'up' and self.unspent_points < 1:
			return
		
		# Convert up/down to 1/-1
		sign = -1 if sign=='down' else 1
		
		# Get the score of the ability to modify
		score = int(getattr(self, ab+"_score").text)
		
		# 8 is the minimum
		if score <= 8 and sign == -1:
			return
		
		# BUY has special costs
		if self.point_mode == "BUY":
			# Values less than 10 are special
			if score in (8, 9):
				cost = 1
			# Can't buy higher than an 18
			elif score == 18 and sign == 1:
				return
			else:
				offset = 10 if sign > 0 else 11
				cost = [1, 1, 1, 2, 2, 2, 3, 4, 1][score-offset] # 1 at the end is for selling a 10 (10-11 = -1)
			# Make sure there are enough points to buy the upgrade
			if sign == 1 and cost > self.unspent_points:
				return
		else:
			cost = 1
		
		# LIMIT_TWO has special restrictions
		if self.point_mode == "LIMIT_TWO":
			if sign == self.state[ab]:
				return
			else:
				self.state[ab] = sign
			
		getattr(self, ab+"_score").text = str(score + 1*sign)
		
		# Adjust the point pool
		self.unspent_points -= cost*sign
		
	
	def cancel_on_click(self, widget):
		self.main['level_exit'] = True
		
	def accept_on_click(self, widget):
		self.main['player'].unspent_levels.pop(0)
		
		# Accept scores
		for ab in ("str", "con", "dex", "int", "wis", "cha"):
			score = int(getattr(self, ab+"_score").text)
			setattr(self.main['player'], ab+"_ab", score)
		self.main['level_exit'] = True
		
	def update(self, main):
		if not self.init:
			# Save the base color of the accept button
			self.btn_color = self.lvl_btn.base_color
			# Get the unspent level information
			self.unspent_level = main['player'].unspent_levels[0]
			# Build archetype list box
			# Load last archetype
			# Load player abilities
			for ab in ("str", "con", "dex", "int", "wis", "cha"):
				bonus = getattr(main['player'], ab+"_bonus")
				getattr(self, ab+"_bonus").text = ("+" if bonus>0 else "") + str(bonus)
				score = getattr(main['player'], ab+"_ab") - bonus
				getattr(self, ab+"_score").text =  str(score)
				
			# Determine Points and mode
			if self.unspent_level.ability_spend == "ALL":
				self.unspent_points = 0
				for ab in ("str", "con", "dex", "int", "wis", "cha"):
					score = int(getattr(self, ab+"_score").text)
					getattr(self, ab+"_score").text = str(score + self.unspent_level.ability_points)
			else:
				self.unspent_points = self.unspent_level.ability_points
				self.point_mode = self.unspent_level.ability_spend
				
			# Build available powers list box
			# Build known powers list box
			self.init = True
			
		# Update final scores
		for ab in ("str", "con", "dex", "int", "wis", "cha"):
			score = int(getattr(self, ab+"_score").text)
			bonus = getattr(main['player'], ab+"_bonus")
			getattr(self, ab+"_final").text = str(bonus+score)
		
		# Make accept button inactive if there are unspent level perks
		if self.unspent_points != 0:
			self.lvl_btn.color = [0.4, 0.4, 0.4, 1.0]
			self.lvl_btn.frozen = True
		else:
			self.lvl_btn.color = self.btn_color
			self.lvl_btn.frozen = False
				
		self.main = main
		
		self.unspent_lbl.text = "Points left to spend: " + str(self.unspent_points)