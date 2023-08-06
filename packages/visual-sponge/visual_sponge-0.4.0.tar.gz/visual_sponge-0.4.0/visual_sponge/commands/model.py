from pathlib import Path

from .. import MACROS, Model, Xponge
from ..parsers import Parser

def MODEL(m, format_=None, **kwargs):
    """MODEL(m, format_=None, **kwargs)
  Get a new Model instance

  :return: a new Model instance
  :param m: the model
  :param format_: the model format. If not given, the format will be guessed.
  :param **kwargs: options specified to the format.
    """
    if format_ is None:
        if isinstance(m, str):
            path = Path(m)
            suffix = path.suffix
            if suffix != "txt":
                format_ = suffix[1:]
            else:
                raise NotImplementedError
        elif isinstance(m, (Xponge.ResidueType, Xponge.Residue)):
            format_ = "xponge_residue"
        else:
            raise TypeError
    parser = Parser(format_)
    atoms, model = parser.Model_Parse(m, **kwargs)
    Model.WORKING = model
    MACROS.CMD = [{"cmd":"MODEL", "atoms": atoms, "name": model.name},
                  {"cmd":"DEFAULT", "mid":Model.WORKING.id}]
    return model
