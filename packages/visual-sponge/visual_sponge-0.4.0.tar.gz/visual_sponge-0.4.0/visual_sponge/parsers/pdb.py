from pathlib import Path

import numpy as np

from . import Parser
from .. import Model, mda, ChainReader


class PDBParser(Parser, formats="pdb"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, topology_format="PDB", **kwargs)
        if hasattr(u.atoms, "elements"):
            atoms = [{"elem": atom.element, "atom": atom.name, "resi": int(atom.resid), "resn": atom.resname, "x": float(atom.position[0]), "y": float(atom.position[1]), "z": float(atom.position[2]), "bonds":[]} for atom in u.atoms]
        else:
            atoms = [{"elem": atom.name[0], "atom": atom.name, "resi": int(atom.resid), "resn": atom.resname, "x": float(atom.position[0]), "y": float(atom.position[1]), "z": float(atom.position[2]), "bonds":[]} for atom in u.atoms]
        distances = u.atoms.positions.reshape(1, -1, 3) - u.atoms.positions.reshape(-1, 1, 3)
        distances = np.einsum("ijx,ijx->ij", distances, distances)
        mask = distances < 2.56
        for i, atomi in enumerate(atoms):
            for j in range(i + 1, len(atoms)):
                if mask[i][j]:
                    atomi["bonds"].append(j)
        model = Model(name=Path(m).stem, u=u)
        model.traj_files.append((m, "PDB"))
        return atoms, model

    @staticmethod
    def Traj_Parse(traj, model, append, **kwargs):
        if not append:
            model.traj_files = [(traj, "PDB")]
        else:
            model.traj_files.append((traj, "PDB"))
        model.u.trajectory = ChainReader(model.traj_files, **kwargs)

