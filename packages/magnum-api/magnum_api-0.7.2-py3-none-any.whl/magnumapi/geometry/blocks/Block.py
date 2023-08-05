from __future__ import annotations

import json
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Optional

import pandas as pd
import matplotlib.pyplot as plt

from roxieapi.cadata.CableDefinition import CableDefinition
from roxieapi.cadata.ConductorDefinition import ConductorDefinition
from roxieapi.cadata.InsulationDefinition import InsulationDefinition
from roxieapi.cadata.StrandDefinition import StrandDefinition

from magnumapi.geometry.definitions.BlockDefinition import BlockDefinition
from magnumapi.geometry.primitives.Area import Area


class Block(ABC):
    """ An Block class implementing a container with block definitions from cadata input.
    In addition, the class stores initialized coordinates of all conductors per block.
    This is a base class extended by implementations of different types (cos-theta, rectangular, etc.).
    """

    def __init__(self,
                 cable_def: CableDefinition,
                 insul_def: InsulationDefinition,
                 strand_def: StrandDefinition,
                 conductor_def: ConductorDefinition) -> None:
        """ Method constructing an instance of a Block class

        :param cable_def: a cable definition from cadata
        :param insul_def: an insulation definition from cadata
        :param strand_def: a strand definition from cadata
        :param conductor_def: a conductor definition from cadata
        """
        self.cable_def = cable_def
        self.insul_def = insul_def
        self.strand_def = strand_def
        self.conductor_def = conductor_def
        self.block_def: Optional[BlockDefinition] = None
        self.areas: List[Area] = []
        self._invariant_cache = None

    def compute_surface(self):
        """ Method computing surface of a block as S = nco * ns * S_strand,
        where S_strand = pi * d_strand^2 / 4

        :return: a surface of a block in mm^2
        """
        return self.block_def.nco * self.cable_def.n_s * self.strand_def.compute_surface()

    def compute_surface_cu(self):
        """ Method computing copper surface of a block as S = nco * ns * S_strand_cu,
        where S_strand_cu = f_cu * pi * d_strand^2 / 4

        :return: a copper surface of a block in mm^2
        """
        return self.block_def.nco * self.cable_def.n_s * self.strand_def.compute_surface_cu()

    def compute_surface_nocu(self):
        """ Method computing copper surface of a block as S = nco * ns * S_strand_nocu,
        where S_strand_nocu = f_nocu * pi * d_strand^2 / 4

        :return: a non-copper surface of a block in mm^2
        """
        return self.block_def.nco * self.cable_def.n_s * self.strand_def.compute_surface_nocu()

    def get_min_max_xy(self) -> tuple:
        """
        Method returning a tuple with min/max x and y coordinates of cable corners for an initialized block

        :return: (min_x, max_x, min_y, max_y)
        """
        all_lines = [line for area in self.areas for line in area.lines]
        all_points = [line.p1 for line in all_lines] + [line.p2 for line in all_lines]
        x = [point.x for point in all_points]
        y = [point.y for point in all_points]

        return min(x), max(x), min(y), max(y)

    @abstractmethod
    def plot_block(self, ax: plt.Axes) -> None:
        """ Abstract method for plotting an insulated block

        :param ax: a matplotlib axis on which a block will be plotted
        """
        raise NotImplementedError('This method is not implemented for this class')

    @abstractmethod
    def plot_bare_block(self, ax: plt.Axes) -> None:
        """ Abstract method for plotting a bare block

        :param ax: a matplotlib axis on which a bare block will be plotted
        """
        raise NotImplementedError('This method is not implemented for this class')

    @property
    def hash_as_str(self) -> str:
        def get_object_dict(object):
            object_dict: dict = deepcopy(object.__dict__)
            if "_invariant_cache" in object_dict.keys():
                object_dict.pop("_invariant_cache")
            return object_dict

        return json.dumps(self, default=get_object_dict)

    def empty_areas(self) -> None:
        """ Method setting areas to an empty array

        """
        self.areas = []

    def get_bare_areas(self) -> List[Area]:
        """ Method returning bare areas, i.e., areas without insulation

        :return: a list of areas without insulation of a given block
        """
        return [self.get_bare_area(area) for area in self.areas]

    def get_bare_area(self, area_ins: Area) -> Area:
        """ Abstract method for returning a bare area

        :param area_ins: an insulated area
        :return: a bare area
        """
        raise NotImplementedError('This method is not implemented for this class')

    @abstractmethod
    def build_areas(self) -> None:
        """ Abstract method for building a block

        """
        raise NotImplementedError('This method is not implemented for this class')

    @abstractmethod
    def to_block_df(self) -> pd.DataFrame:
        """ Abstract method for converting a block definition into a ROXIE-compatible dataframe

        """
        raise NotImplementedError('This method is not implemented for this class')

    @abstractmethod
    def to_abs_dict(self):
        """ Abstract method for returning the absolute dictionary for block definition

        """
        raise NotImplementedError('This method is not implemented for this class')

    @abstractmethod
    def to_rel_dict(self, alpha_ref: float, phi_ref: float):
        """ Abstract method for returning the absolute dictionary for block definition

        """
        raise NotImplementedError('This method is not implemented for this class')

    @abstractmethod
    def homogenize(self):
        """ Abstract method for homogenizing a block

        """
        raise NotImplementedError('This method is not implemented for this class')

    def to_df(self) -> pd.DataFrame:
        """ Method concatenating rows representing coordinates of each area into a dataframe

        :return: a dataframe with coordinate information of each area of a block instance
        """
        return pd.concat([area.to_df() for area in self.areas], axis=0)

    def is_outside_of_first_quadrant(self, eps=1e-30) -> True:
        """ Method checking whether at least one area of a given block are outside of the first quadrant

        :param eps: a machine precision for comparison of 0 value
        :return: True if at least one area of a given block is outside of the first quadrant,
        False otherwise, i.e., if all areas are within the first quadrant.
        """
        if not self.areas:
            return False

        is_inside_first_quadrant = False
        for area in self.areas:
            is_inside_first_quadrant |= Area.is_outside_of_first_quadrant(area, eps=eps)

        return is_inside_first_quadrant

    def rotate(self, angle: float) -> Block:
        """
        Method rotating block by a given angle in degrees w.r.t. origin of the coordinate system (0, 0).
        The rotation is applied to each area

        :param angle: rotation angle in degrees
        :return: new instance of the rotated block
        """
        block_copy = deepcopy(self)
        block_copy.areas = [area.rotate(angle) for area in block_copy.areas]

        return block_copy

    def mirror_x(self) -> Block:
        """
        Method mirroring the block w.r.t. x-axis.
        The mirroring is applied to each area

        :return: new instance of the mirrored block
        """
        block_copy = deepcopy(self)
        block_copy.areas = [area.mirror_x() for area in block_copy.areas]

        return block_copy

    def mirror_y(self) -> Block:
        """
        Method mirroring the block w.r.t. y-axis.
        The mirroring is applied to each area

        :return: new instance of the mirrored block
        """
        block_copy = deepcopy(self)
        block_copy.areas = [area.mirror_y() for area in block_copy.areas]

        return block_copy

    def negate_current(self) -> Block:
        block_copy = deepcopy(self)
        block_copy.block_def.current *= -1

        return block_copy