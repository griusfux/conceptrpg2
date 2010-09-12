def seek(game_state, character):
	if character.target:
		linear = character.target.object.position - character.object.position
		
		linear.normalize()
		linear *= character.speed
		
		angular = (0, 0, 0)
		
		game_state.move(character, linear, angular)