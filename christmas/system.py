
import itertools
import math
import random

import numpy as np
from pygame.locals import *

from .component import *
from .input_handler import InputIntent
from .item import *


class System:
    def __init__(self, game):
        self.game = game

    def run(self):
        filtered_entities = [entity for entity in self.game.entities
                             if entity is not None and
                             all(map(lambda c: entity.has_comp(c),
                                     self.COMPS))]
        self._run(filtered_entities)

    def _run(self, *_):
        raise NotImplementedError


class SnowParticleUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, SnowTargetComp]

    def _run(self, entities):
        # TODO: Perhaps if a player walks over the snow, it disappears or becomes compacted ice.
        for entity in entities:
            pos, vel, target = entity.get_comps(PositionComp, VelocityComp, SnowTargetComp)
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


class PlayerUpdateSystem(System):
    COMPS = [VelocityComp, MoveSpeedComp, InputConfigComp]

    def _run(self, entities):
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            vel, speed, inp_conf = entity.get_comps(VelocityComp, MoveSpeedComp, InputConfigComp)
            speed = speed.speed
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.UP]):
                vel.y -= speed
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.DOWN]):
                vel.y += speed
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.LEFT]):
                vel.x -= speed
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.RIGHT]):
                vel.x += speed


class AmmoUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, AmmoComp, InputConfigComp]

    def _run(self, entities):
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            pos, vel, ammo, inp_conf = entity.get_comps(PositionComp, VelocityComp, AmmoComp, InputConfigComp)
            if len(ammo.rounds) == 0:
                # They're empty.  Remove their ammo belt.
                entity.remove_comp(AmmoComp)
            elif inp_handler.is_key_pressed(inp_conf.key_map[InputIntent.FIRE]):
                projectile_cons = ammo.rounds.popleft()
                projectile = self.game.create_entity()
                projectile_cons.init(projectile, entity, pos.x, pos.y, vel.x, vel.y)


class PositionBoundBounceSystem(System):
    COMPS = [PositionComp, VelocityComp, SizeComp, PositionBoundComp, PositionBoundBounceMultiplierComp]

    def _run(self, entities):
        for entity in entities:
            pos, vel, size, bound, mult = entity.get_comps(PositionComp, VelocityComp, SizeComp, PositionBoundComp, PositionBoundBounceMultiplierComp)
            mult = mult.multiplier
            intended_pos = PositionComp(pos.x + vel.x, pos.y + vel.y)
            if intended_pos.x < bound.x:
                pos.x = bound.x
                vel.x *= -mult
            elif intended_pos.x + size.w > bound.x + bound.w:
                pos.x = bound.x + bound.w - size.w
                vel.x *= -mult
            if intended_pos.y < bound.y:
                pos.y = bound.y
                vel.y *= -mult
            elif intended_pos.y + size.h > bound.y + bound.h:
                pos.y = bound.y + bound.h - size.h
                vel.y *= -mult


class CollideSystem(System):
    COMPS = [PositionComp, VelocityComp, SizeComp, CollideFlag]

    def _run(self, entities):
        for (e1, e2) in itertools.combinations(entities, 2):
            pos1, vel1, size1 = e1.get_comps(PositionComp, VelocityComp, SizeComp)
            pos2, vel2, size2 = e2.get_comps(PositionComp, VelocityComp, SizeComp)
            intended_pos1 = PositionComp(pos1.x + vel1.x, pos1.y + vel1.y)
            intended_pos2 = PositionComp(pos2.x + vel2.x, pos2.y + vel2.y)
            if (intended_pos1.x < intended_pos2.x + size2.w and
                intended_pos1.x + size1.w > intended_pos2.x and
                intended_pos1.y < intended_pos2.y + size2.h and
                intended_pos1.y + size1.h > intended_pos2.y):
                if e1.has_comp(ProjectileFlag) and e2.has_comp(PlayerComp):
                    proj = e1
                    player = e2
                elif e2.has_comp(ProjectileFlag) and e1.has_comp(PlayerComp):
                    proj = e2
                    player = e1
                else:
                    # We're only interested in projectile <-> player collisions.
                    continue

                if proj.has_comp(OwnerComp) and proj.get_comp(OwnerComp).owner == player:
                    continue
                proj.kill()
                player.get_comp(PlayerComp).curr_health -= 1


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


class LifetimeUpdateSystem(System):
    COMPS = [LifetimeComp]

    def _run(self, entities):
        for entity in entities:
            lifetime = entity.get_comp(LifetimeComp)
            lifetime.life -= 1
            if lifetime.life <= 0:
                entity.kill()


class OutOfBoundsCleanupSystem(System):
    COMPS = [PositionComp, PositionBoundComp, OutOfBoundsKillFlag]
    # How far away the entity needs to go out of bounds before being killed
    DISTANCE_THRESHOLD = 500 # px

    def _run(self, entities):
        for entity in entities:
            pos, bound = entity.get_comps(PositionComp, PositionBoundComp)
            if (bound.x + bound.w + OutOfBoundsCleanupSystem.DISTANCE_THRESHOLD < pos.x or
                pos.x < bound.x - OutOfBoundsCleanupSystem.DISTANCE_THRESHOLD or
                bound.y + bound.h + OutOfBoundsCleanupSystem.DISTANCE_THRESHOLD < pos.y or
                pos.y < bound.y - OutOfBoundsCleanupSystem.DISTANCE_THRESHOLD):
                entity.kill()


class DeadCleanupSystem(System):
    COMPS = [DeadFlag]

    def _run(self, entities):
        for entity in entities:
            self.game.destroy_entity(entity)


class PlayerAnimateUpdateSystem(System):
    COMPS = [VelocityComp, DrawComp, AnimateComp]
    # Number of ticks to wait between animation frames
    IDLE_ANIM_DELAY = 5
    MOVING_ANIM_DELAY = 2
    IDLE_VELOCITY_THRESHOLD = 0.1

    def _run(self, entities):
        for entity in entities:
            vel, draw, anim = entity.get_comps(VelocityComp, DrawComp, \
                                               AnimateComp)
            if (abs(vel.x) < PlayerAnimateUpdateSystem.IDLE_VELOCITY_THRESHOLD
                and abs(vel.y) < \
                    PlayerAnimateUpdateSystem.IDLE_VELOCITY_THRESHOLD):
                anim.delay = PlayerAnimateUpdateSystem.IDLE_ANIM_DELAY
            else:
                anim.delay = PlayerAnimateUpdateSystem.MOVING_ANIM_DELAY


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


class ScheduleSystem(System):
    COMPS = [JobScheduleComp]
    def __init__(self, game):
        super().__init__(game)
        self.funcs = {'spawn_orn': lambda: OrnamentItem.init(
                                           self.game.create_entity(),
                                           self.get_rand_pos()),
                      'spawn_beer': lambda: BeerItem.init(
                                           self.game.create_entity(),
                                           self.get_rand_pos())
                     }
    def get_rand_pos(self):
        return np.random.randint(self.game.width), \
               np.random.randint(self.game.height)
    def _run(self, entities):
        t = pg.time.get_ticks()
        for entity in entities:
            job_sch = entity.get_comp(JobScheduleComp)
            if t >= job_sch.tick_time:
                self.funcs[job_sch.f]()
                job_sch.reset(t)


# TODO: Unfnished business below.
# class OrnamentUpdateSystem(System):
#     COMPS = [PositionComp, DrawComp, LifetimeComp, SizeComp]

#     def _run(self, entities):
#         # Spawn new ornament randomly.
#         ornament = self.game.create_entity()
#         # Check ornament acquisition.
#         # TODO: Check if one is an ornament and the other a player. Add a new comp?
#         for entity in entities:
#             pos, draw = entity.get_comps(PositionComp, DrawComp)
#             draw.rect.topleft = (pos.x, pos.y)


class AutonomousUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, PlayerComp]
    DEFAULT_SPEED = 1

    def _run(self, entities):
        for e in entities:
            player, pos, vel = e.get_comps(PlayerComp, PositionComp, \
                                           VelocityComp)
            if player.autonomous == False:
                continue # we don't like normies.
            if player.opponent_name is None:
                has_opp = AutonomousUpdateSystem.assign_opponent(e, entities)
                if not has_opp:
                    continue
            AutonomousUpdateSystem.move_player(e, entities)

    @staticmethod
    def move_player(entity, entities):
        pos, vel = entity.get_comps(PositionComp, VelocityComp)
        opp_entity = AutonomousUpdateSystem.get_opponent(entity, entities)
        if opp_entity is None:
            return
        opp_comps = opp_entity.get_comps(PlayerComp, \
                                         PositionComp, \
                                         VelocityComp)
        if not opp_comps:
            # No opponent, so return.
            return
        # Check memory for past moves.
        mem_comp = entity.get_comp(MemoryComp)
        update_rate = mem_comp.memory.get('update_rate')
        counter = mem_comp.memory.get('counter', 0)
        speed = mem_comp.memory.get('speed', \
                                        AutonomousUpdateSystem.DEFAULT_SPEED)
        update_vect = mem_comp.memory.get('update_vect', [0.0, 0.0])
        mem_comp.memory['counter'] = counter + 1
        # Stick in straight line before counter cycles.
        if counter % update_rate != 0:
            # vel.x = update_vect[0]
            # vel.y = update_vect[1]
            return
        # Move towards the opponent.
        _, opp_pos, opp_vel = opp_comps
        x_diff = opp_pos.x - pos.x
        y_diff = opp_pos.y - pos.y
        if abs(x_diff) > abs(y_diff):
            update_vect[0] = math.copysign(1, x_diff) * \
                             speed * \
                             (1 + 1 ** -(abs(x_diff)))
            update_vect[1] = 0
        else:
            update_vect[0] = 0
            update_vect[1] = math.copysign(1, y_diff) * \
                             speed * \
                             (1 + 1 ** -(abs(y_diff)))
        vel.x = update_vect[0]
        vel.y = update_vect[1]
        mem_comp.memory['update_vect'] = update_vect

    @staticmethod
    def get_opponent(entity, entities):
        player = entity.get_comp(PlayerComp)
        for e in entities:
            other_player = e.get_comp(PlayerComp)
            if player == other_player:
                continue
            if player.opponent_name == other_player.name:
                return e
        return None

    @staticmethod
    def assign_opponent(entity, entities):
        if not entity.has_comp(OwnerComp):
            return False
        player = entity.get_comp(PlayerComp)
        owner = entity.get_comp(OwnerComp).owner.get_comp(PlayerComp)
        victims = list(filter(lambda e: e.get_comp(PlayerComp).name not in \
                                        [player.name, owner.name], entities))
        player.opponent_name = random.choice(victims).get_comp(PlayerComp).name
        return True