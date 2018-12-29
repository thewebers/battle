from pygame.locals import *

from .component import *
from .santa import CoalProjectile


class System:
    def __init__(self, game):
        self.game = game

    def run(self):
        filtered_entities = [entity for entity in self.game.entities
                             if entity is not None and
                             all(map(lambda c: entity.has_comp(c), self.COMPS))]
        self._run(filtered_entities)

    def _run(self, *_):
        raise NotImplementedError


class ParticleUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, ParticleComp]

    def _run(self, entities):
        # TODO: Perhaps if a player walks over the snow, it disappears or becomes compacted ice.
        for entity in entities:
            pos, vel, target = entity.get_comps(PositionComp, VelocityComp, ParticleComp)
            if pos.y == target.y: 
                vel.x = 0
                vel.y = 0
            pos.x += vel.x 
            pos.y += vel.y 


class TopPlayerUpdateSystem(System):
    COMPS = [VelocityComp, TopPlayerFlag]
    MOVE_SPEED = 5.0

    def _run(self, entities):
        assert(len(entities) == 1)
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            vel = entity.get_comp(VelocityComp)
            if inp_handler.is_key_pressed(K_w):
                vel.y -= TopPlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_pressed(K_s):
                vel.y += TopPlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_pressed(K_a):
                vel.x -= TopPlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_pressed(K_d):
                vel.x += TopPlayerUpdateSystem.MOVE_SPEED


class BottomPlayerUpdateSystem(System):
    COMPS = [VelocityComp, BottomPlayerFlag]
    MOVE_SPEED = 5.0

    def _run(self, entities):
        assert(len(entities) == 1)
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            pos, vel = entity.get_comps(PositionComp, VelocityComp)
            if inp_handler.is_key_pressed(K_UP):
                vel.y -= BottomPlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_pressed(K_DOWN):
                vel.y += BottomPlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_pressed(K_LEFT):
                vel.x -= BottomPlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_pressed(K_RIGHT):
                vel.x += BottomPlayerUpdateSystem.MOVE_SPEED


class AmmoUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, AmmoComp]

    def _run(self, entities):
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            pos, vel, ammo = entity.get_comps(PositionComp, VelocityComp, AmmoComp)
            if len(ammo.rounds) == 0:
                # They're empty.  Remove their ammo belt.
                entity.remove_comp(AmmoComp)
            elif inp_handler.is_key_pressed(K_SPACE):
                projectile_cons = ammo.rounds.popleft()
                projectile = self.game.create_entity()
                projectile_cons.init(projectile, pos.x, pos.y, vel.x, vel.y)


class PositionBoundSystem(System):
    COMPS = [PositionComp, VelocityComp, SizeComp, PositionBoundComp]

    def _run(self, entities):
        for entity in entities:
            pos, vel, size, bound = entity.get_comps(PositionComp, VelocityComp, SizeComp, PositionBoundComp)
            intended_pos = PositionComp(pos.x + vel.x, pos.y + vel.y)
            if intended_pos.x < bound.x:
                pos.x = bound.x
                vel.x *= -10
            elif intended_pos.x + size.w > bound.x + bound.w:
                pos.x = bound.x + bound.w - size.w
                vel.x *= -10
            if intended_pos.y < bound.y:
                pos.y = bound.y
                vel.y *= -10
            elif intended_pos.y + size.h > bound.y + bound.h:
                pos.y = bound.y + bound.h - size.h
                vel.y *= -10


class PositionUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp]

    def _run(self, entities):
        for entity in entities:
            pos, vel = entity.get_comps(PositionComp, VelocityComp)
            pos.x += vel.x
            pos.y += vel.y


class VelocityAttenuateSystem(System):
    COMPS = [VelocityComp, VelocityAttenuateFlag]

    def _run(self, entities):
        VELOCITY_ATTENUATION = 0.5

        for entity in entities:
            vel = entity.get_comp(VelocityComp)
            vel.x *= VELOCITY_ATTENUATION
            vel.y *= VELOCITY_ATTENUATION


class PlayerAnimateUpdateSystem(System):
    COMPS = [VelocityComp, DrawComp, AnimateComp]
    # Number of ticks to wait between animation frames
    IDLE_ANIM_DELAY = 5
    MOVING_ANIM_DELAY = 2
    IDLE_VELOCITY_THRESHOLD = 0.1

    def _run(self, entities):
        for entity in entities:
            vel, draw, anim = entity.get_comps(VelocityComp, DrawComp, AnimateComp)
            if (abs(vel.x) < PlayerAnimateUpdateSystem.IDLE_VELOCITY_THRESHOLD
                and abs(vel.y) < PlayerAnimateUpdateSystem.IDLE_VELOCITY_THRESHOLD):
                anim.delay = PlayerAnimateUpdateSystem.IDLE_ANIM_DELAY
            else:
                anim.delay = PlayerAnimateUpdateSystem.MOVING_ANIM_DELAY


class LifetimeUpdateSystem(System):
    COMPS = [LifetimeComp]

    def _run(self, entities):
        for entity in entities:
            lifetime = entity.get_comp(LifetimeComp)
            lifetime.life -= 1
            if lifetime.life <= 0:
                entity.kill()


class DeadCleanupSystem(System):
    COMPS = [DeadFlag]

    def _run(self, entities):
        for entity in entities:
            self.game.destroy_entity(entity)


class OutOfBoundsCleanupSystem(System):
    COMPS = [PositionComp, SizeComp, VelocityComp, OutOfBoundsComp]
    TRESPASS_THRESHOLD = 500 # px

    def _run(self, entities):
        for entity in entities:
            pos, vel, size, bound = entity.get_comps(PositionComp, VelocityComp, SizeComp, OutOfBoundsComp)
            intended_pos = PositionComp(pos.x + vel.x, pos.y + vel.y)

            delete = False
            if intended_pos.x < bound.x:
                delete = True
            elif intended_pos.x + size.w > bound.x + bound.w:
                delete = True
            if intended_pos.y < bound.y:
                delete = True
            elif intended_pos.y + size.h > bound.y + bound.h:
                delete = True
            
            if delete:
                print('Delete time :)')
                self.game.destroy_entity(entity)


class AnimateUpdateSystem(System):
    COMPS = [DrawComp, AnimateComp]

    def _run(self, entities):
        for entity in entities:
            draw, anim = entity.get_comps(DrawComp, AnimateComp)
            if anim.clock >= anim.delay:
                draw.img_idx = (draw.img_idx + 1) % len(draw.images)
                draw.image = draw.images[draw.img_idx]
                anim.clock = 0
            anim.clock += 1


class DrawUpdateSystem(System):
    COMPS = [PositionComp, DrawComp]

    def _run(self, entities):
        for entity in entities:
            pos, draw = entity.get_comps(PositionComp, DrawComp)
            draw.rect.topleft = (pos.x, pos.y)
