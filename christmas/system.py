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


class SnowUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, SnowFlagComp]

    def _run(self, entities):
        # TODO: Perhaps if a player walks over the snow, it disappears or becomes compacted ice.
        for entity in entities:
            pos, vel, target = entity.get_comps(PositionComp, VelocityComp, SnowFlagComp)
            if pos.y == target.y: 
                continue 
            pos.x += vel.x 
            pos.y += vel.y 


class WeberUpdateSystem(System):
    COMPS = [VelocityComp, WeberFlagComp]
    MOVE_SPEED = 5.0

    def _run(self, entities):
        assert(len(entities) == 1)
        for entity in entities:
            vel = entity.get_comp(VelocityComp)
            if self.game.is_key_pressed(K_w):
                vel.y -= WeberUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_s):
                vel.y += WeberUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_a):
                vel.x -= WeberUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_d):
                vel.x += WeberUpdateSystem.MOVE_SPEED


class SantaUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, SantaFlagComp]
    MOVE_SPEED = 5.0

    def _run(self, entities):
        assert(len(entities) == 1)
        for entity in entities:
            pos, vel = entity.get_comps(PositionComp, VelocityComp)
            if self.game.is_key_pressed(K_UP):
                vel.y -= SantaUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_DOWN):
                vel.y += SantaUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_LEFT):
                vel.x -= SantaUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_RIGHT):
                vel.x += SantaUpdateSystem.MOVE_SPEED
            if self.game.is_key_pressed(K_SPACE):
                coal = self.game.create_entity()
                CoalProjectile.init(coal, pos.x, pos.y, vel.x, vel.y)


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
    COMPS = [VelocityComp, VelocityAttenuateFlagComp]

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
    COMPS = [DeadFlagComp]

    def _run(self, entities):
        for entity in entities:
            self.game.destroy_entity(entity)


class TrespassCleanupSystem(System):
    COMPS = [PositionComp, PositionBoundComp]
    TRESPASS_THRESHOLD = 500 # px

    def _run(self, entities):
        for entity in entities:
            pos, bound = entity.get_comps(PositionComp, PositionBoundComp)
            delete = False
            if bound.x + bound.w + TrespassCleanupSystem.TRESPASS_THRESHOLD < pos.x:
                delete = True
            elif pos.x < bound.x - TrespassCleanupSystem.TRESPASS_THRESHOLD:
                delete = True
            elif bound.y + bound.h + TrespassCleanupSystem.TRESPASS_THRESHOLD < pos.y:
                delete = True
            elif pos.y < bound.y - TrespassCleanupSystem.TRESPASS_THRESHOLD:
                delete = True
            
            if delete:
                self.game.destroy_entity(entity)
                print('Deleted trespassing entitiy.')


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
