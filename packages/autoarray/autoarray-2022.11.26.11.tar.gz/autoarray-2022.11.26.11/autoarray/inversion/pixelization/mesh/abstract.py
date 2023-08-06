import numpy as np
from typing import Dict, Optional

from autoarray.inversion.pixelization.settings import SettingsPixelization
from autoarray.inversion.pixelization.mappers.mapper_grids import MapperGrids
from autoarray.structures.grids.uniform_2d import Grid2D
from autoarray.structures.grids.sparse_2d import Grid2DSparse
from autoarray.preloads import Preloads

from autoarray.numba_util import profile_func


class AbstractMesh:
    def __init__(self):
        """
        A pixelization associates a 2D grid of (y,x) coordinates (which are expected to be aligned with a masked
        dataset) which are aligned with a masked dataset with a 2D grid of pixels.

        Both of these grids (e.g. the masked dataset's 2D grid and the grid of the pixelization's pixels) have (y,x)
        coordinates in two reference frames:

        - `data`: the original reference frame of the masked data.

        - `source`: a reference frame where grids in the `data` reference frame are transformed to a new reference
        frame (e.g. their (y,x) coordinates may be shifted, stretched or have a more complicated operation performed
        on them).

        The grid associated with the masked dataset and pixelization have the following variable names:

        - `grid_slim`: the (y,x) grid of coordinates of the original masked data (which can be in the data frame and
        given the variable name `data_grid_slim` or in the transformed source frame with the variable
        name `source_grid_slim`).

        - `mesh_grid`: the (y,x) grid of the pixelization's pixels which are associated with
        the `grid_slim` (y,x)  coordinates (association is always performed in the `source` reference frame).

        A pixelization therefore has up to four grids associated with it: `data_grid_slim`, `source_grid_slim`,
        `data_mesh_grid` and `source_mesh_grid`.

        If a transformation of coordinates is not applied, the `data` frame and `source` frames are identical.

        In the project `PyAutoLens`, one's data is a masked 2D image. Its `data_grid_slim` is a 2D grid where every
        (y,x) coordinate is aligned with the centre of every unmasked image pixel. A "lensing operation" transforms
        this grid of (y,x) coordinates from the `data` frame to a new grid of (y,x) coordinates in the `source` frame.
        The pixelization is then applied in the source frame.. In lensing terminology, the `data` frame is
        the `image-plane` and `source` frame the `source-plane`.
        """

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ and self.__class__ is other.__class__

    @profile_func
    def relocated_grid_from(
        self,
        source_grid_slim: Grid2D,
        settings: SettingsPixelization = SettingsPixelization(),
        preloads: Preloads = Preloads(),
    ) -> Grid2D:
        """
        Relocates all coordinates of the input `source_grid_slim` that are outside of a
        border (which is defined by a grid of (y,x) coordinates) to the edge of this border.

        The border is determined from the mask of the 2D data in the `data` frame before any transformations of the
        data's grid are performed. The border is all pixels in this mask that are pixels at its extreme edge. These
        pixel indexes are used to then determine a grid of (y,x) coordinates from the transformed `source_grid_grid` in
        the `source` reference frame, whereby points located outside of it are relocated to the border's edge.

        A full description of relocation is given in the method grid_2d.relocated_grid_from()`.

        This is used in the project PyAutoLens to relocate the coordinates that are ray-traced near the centre of mass
        of galaxies, which are heavily demagnified and may trace to outskirts of the source-plane well beyond the
        border.

        Parameters
        ----------
        source_grid_slim
            A 2D (y,x) grid of coordinates, whose coordinates outside the border are relocated to its edge.
        """
        if preloads.relocated_grid is None:

            if settings.use_border:
                return source_grid_slim.relocated_grid_from(grid=source_grid_slim)
            return source_grid_slim

        return preloads.relocated_grid

    @profile_func
    def relocated_mesh_grid_from(
        self,
        source_grid_slim: Grid2D,
        source_mesh_grid: Grid2DSparse,
        settings: SettingsPixelization = SettingsPixelization(),
    ):
        """
        Relocates all coordinates of the input `source_mesh_grid` that are outside of a border (which
        is defined by a grid of (y,x) coordinates) to the edge of this border.

        The border is determined from the mask of the 2D data in the `data` frame before any transformations of the
        data's grid are performed. The border is all pixels in this mask that are pixels at its extreme edge. These
        pixel indexes are used to then determine a grid of (y,x) coordinates from the transformed `source_grid_grid` in
        the `source` reference frame, whereby points located outside of it are relocated to the border's edge.

        A full description of relocation is given in the method grid_2d.relocated_grid_from()`.

        This is used in the project `PyAutoLens` to relocate the coordinates that are ray-traced near the centre of mass
        of galaxies, which are heavily demagnified and may trace to outskirts of the source-plane well beyond the
        border.

        Parameters
        ----------
        source_grid_slim
            A 2D grid of (y,x) coordinates associated with the unmasked 2D data after it has been transformed to the
            `source` reference frame.
        source_mesh_grid
            The centres of every Voronoi pixel in the `source` frame, which are initially derived by computing a sparse
            set of (y,x) coordinates computed from the unmasked data in the `data` frame and applying a transformation
            to this.
        settings
            Settings controlling the pixelization for example if a border is used to relocate its exterior coordinates.
        """
        if settings.use_border:
            return source_grid_slim.relocated_mesh_grid_from(mesh_grid=source_mesh_grid)
        return source_mesh_grid

    def mapper_grids_from(
        self,
        source_grid_slim: Grid2D,
        source_mesh_grid: Grid2DSparse = None,
        data_mesh_grid: Grid2DSparse = None,
        hyper_data: np.ndarray = None,
        settings=SettingsPixelization(),
        preloads: Preloads = Preloads(),
        profiling_dict: Optional[Dict] = None,
    ) -> MapperGrids:
        raise NotImplementedError

    def mesh_grid_from(
        self,
        source_grid_slim: Grid2D,
        source_mesh_grid: Grid2DSparse,
        sparse_index_for_slim_index: np.ndarray = None,
    ):
        raise NotImplementedError

    def weight_map_from(self, hyper_data: np.ndarray):

        raise NotImplementedError()

    @property
    def is_stochastic(self):
        return False

    def __str__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in self.__dict__.items()])

    def __repr__(self):
        return "{}\n{}".format(self.__class__.__name__, str(self))
