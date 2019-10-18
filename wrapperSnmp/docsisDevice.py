# -*- coding: utf-8 -*-


class DocsisDevice:
    """Represents the avalaible  Docsis Devices ids
    """
    __idCmts = "Cmts"
    __idCm = "Cm"
    __idCm31 = "Cm31"
    __idCmInCmts = "CmInCmts"

    @staticmethod
    def cmts(): return DocsisDevice.__idCmts

    @staticmethod
    def cm(): return DocsisDevice.__idCm

    @staticmethod
    def cm31(): return DocsisDevice.__idCm31

    @staticmethod
    def cm_in_cmts(): return DocsisDevice.__idCmInCmts
