import pygame as pg

from .component import DrawComp


class Entity:
    def __init__(self, ident):
        self.ident = ident
        self.comps = {}

    def add_comp(self, comp):
        comp_type = type(comp)
        assert(not self.has_comp(comp_type))
        self.comps[comp_type] = comp

    def set_comp(self, comp):
        comp_type = type(comp)
        if self.has_comp(comp_type):
            old_comp = self.comps[comp_type]
            if isinstance(old_comp, DrawComp):
                # Need to manually kill dead sprites, or else they will
                # continue to be drawn.
                old_comp.kill()
        self.comps[comp_type] = comp

    def remove_comp(self, comp_type):
        assert(self.has_comp(comp_type))
        del self.comps[comp_type]

    def has_comp(self, comp_type):
        return comp_type in self.comps

    def get_comp(self, comp_type):
        return self.comps[comp_type]

    def get_comps(self, *comps):
        return tuple(self.comps[comp] for comp in comps)
