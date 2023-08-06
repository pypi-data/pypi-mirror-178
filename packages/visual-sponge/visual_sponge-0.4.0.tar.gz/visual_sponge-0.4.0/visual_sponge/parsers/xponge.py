from . import Parser
from .. import Model, Xponge


class PDBParser(Parser, formats="xponge_residue"):
    @staticmethod
    def Model_Parse(m, **kwargs):
      atoms = []
      model = None
      return atoms, model
