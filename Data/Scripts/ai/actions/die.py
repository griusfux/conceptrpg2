def die(game_state, character):
	game_state.monster_list.remove(character)
	character.object.end()