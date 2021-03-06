import random

import Scripts.effects as Effect

def power(self, controller, user):
    targets = controller.get_targets(self, user)
    if targets == []:
        return
    target = targets[0]
    
    controller.animate_spell(user)

    def f_collision(effect):
        strength = 4 + random.randrange(0, 3)
        controller.deal_damage(user, target, self, strength, "ARCANE")

    pos = user.object.position
    effect = Effect.ProjectileEffect("pelt", pos, target)
    effect.f_collision = f_collision
    controller.add_effect(effect)