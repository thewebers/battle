import pygame as pg

from .component import DrawComp, DeadFlag


class Entity:
    def __init__(self, ident):
        self.ident = ident
        self.comps = {}

    def kill(self):
        self.add_comp(DeadFlag())

    def add_comp(self, comp):
        comp_type = type(comp)
        assert(not self.has_comp(comp_type))
        self.comps[comp_type] = comp

    def set_comp(self, comp):
        comp_type = type(comp)
        if self.has_comp(comp_type):
            self.remove_comp(comp_type)
        self.comps[comp_type] = comp

    def remove_comp(self, comp_type):
        assert(self.has_comp(comp_type))
        comp = self.comps[comp_type]
        if isinstance(comp, DrawComp):
            # Need to manually kill dead sprites, or else they will
            # continue to be drawn.
            comp.kill()
        del self.comps[comp_type]

    def has_comp(self, comp_type):
        return comp_type in self.comps

    def get_comp(self, comp_type):
        return self.comps[comp_type]

    def get_comps(self, *comps):
        return tuple(self.comps[comp] for comp in comps)
