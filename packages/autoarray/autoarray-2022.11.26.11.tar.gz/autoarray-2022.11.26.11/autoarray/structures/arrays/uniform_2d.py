import logging
import numpy as np
from typing import List, Optional, Tuple, Union

from autoarray.mask.mask_2d import Mask2D
from autoarray.structures.abstract_structure import Structure
from autoarray.structures.header import Header
from autoarray.structures.arrays.uniform_1d import Array1D

from autoarray import exc
from autoarray import type as ty
from autoarray.geometry import geometry_util
from autoarray.structures.arrays import array_2d_util
from autoarray.structures.grids import grid_2d_util
from autoarray.layout import layout_util

logging.basicConfig()
logger = logging.getLogger(__name__)


class AbstractArray2D(Structure):
    def __new__(
        cls,
        array: Union[np.ndarray, List],
        mask: Mask2D,
        header: Header = None,
        *args,
        **kwargs
    ):
        """
        An array of values, which are paired to a uniform 2D mask of pixels and sub-pixels. Each entry
        on the array corresponds to a value at the centre of a sub-pixel in an unmasked pixel.

        An *Array2D* is ordered such that pixels begin from the top-row of the corresponding mask and go right and down.
        The positive y-axis is upwards and positive x-axis to the right.

        The array can be stored in 1D or 2D, as detailed below.

        Case 1: [sub-size=1, slim]:
        ---------------------------

        The Array2D is an ndarray of shape [total_unmasked_pixels].

        The first element of the ndarray corresponds to the pixel index, for example:

        - array[3] = the 4th unmasked pixel's value.
        - array[6] = the 7th unmasked pixel's value.

        Below is a visual illustration of a array, where a total of 10 pixels are unmasked and are included in \
        the array.

        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI     This is an example mask.Mask2D, where:
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIoIoIxIxIxIxI     x = `True` (Pixel is masked and excluded from the array)
        IxIxIxIoIoIoIoIxIxIxI     o = `False` (Pixel is not masked and included in the array)
        IxIxIxIoIoIoIoIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI

        The mask pixel index's will come out like this (and the direction of scaled values is highlighted
        around the mask.

        pixel_scales = 1.0"

        <--- -ve  x  +ve -->
                                                        y      x
        IxIxIxIxIxIxIxIxIxIxI  ^   array[0] = 0
        IxIxIxIxIxIxIxIxIxIxI  I   array[1] = 1
        IxIxIxIxIxIxIxIxIxIxI  I   array[2] = 2
        IxIxIxIxI0I1IxIxIxIxI +ve  array[3] = 3
        IxIxIxI2I3I4I5IxIxIxI  y   array[4] = 4
        IxIxIxI6I7I8I9IxIxIxI -ve  array[5] = 5
        IxIxIxIxIxIxIxIxIxIxI  I   array[6] = 6
        IxIxIxIxIxIxIxIxIxIxI  I   array[7] = 7
        IxIxIxIxIxIxIxIxIxIxI \/   array[8] = 8
        IxIxIxIxIxIxIxIxIxIxI      array[9] = 9

        Case 2: [sub-size>1, slim]:
        ------------------

        If the masks's sub size is > 1, the array is defined as a sub-array where each entry corresponds to the values
        at the centre of each sub-pixel of an unmasked pixel.

        The sub-array indexes are ordered such that pixels begin from the first (top-left) sub-pixel in the first
        unmasked pixel. Indexes then go over the sub-pixels in each unmasked pixel, for every unmasked pixel.
        Therefore, the sub-array is an ndarray of shape [total_unmasked_pixels*(sub_array_shape)**2]. For example:

        - array[9] - using a 2x2 sub-array, gives the 3rd unmasked pixel's 2nd sub-pixel value.
        - array[9] - using a 3x3 sub-array, gives the 2nd unmasked pixel's 1st sub-pixel value.
        - array[27] - using a 3x3 sub-array, gives the 4th unmasked pixel's 1st sub-pixel value.

        Below is a visual illustration of a sub array. Indexing of each sub-pixel goes from the top-left corner. In
        contrast to the array above, our illustration below restricts the mask to just 2 pixels, to keep the
        illustration brief.

        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI     This is an example mask.Mask2D, where:
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI     x = `True` (Pixel is masked and excluded from lens)
        IxIxIxIxIoIoIxIxIxIxI     o = `False` (Pixel is not masked and included in lens)
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI

        Our array with a sub-size looks like it did before:

        pixel_scales = 1.0"

        <--- -ve  x  +ve -->

        IxIxIxIxIxIxIxIxIxIxI  ^
        IxIxIxIxIxIxIxIxIxIxI  I
        IxIxIxIxIxIxIxIxIxIxI  I
        IxIxIxIxIxIxIxIxIxIxI +ve
        IxIxIxI0I1IxIxIxIxIxI  y
        IxIxIxIxIxIxIxIxIxIxI -ve
        IxIxIxIxIxIxIxIxIxIxI  I
        IxIxIxIxIxIxIxIxIxIxI  I
        IxIxIxIxIxIxIxIxIxIxI \/
        IxIxIxIxIxIxIxIxIxIxI

        However, if the sub-size is 2,each unmasked pixel has a set of sub-pixels with values. For example, for pixel 0,
        if *sub_size=2*, it has 4 values on a 2x2 sub-array:

        Pixel 0 - (2x2):

               array[0] = value of first sub-pixel in pixel 0.
        I0I1I  array[1] = value of first sub-pixel in pixel 1.
        I2I3I  array[2] = value of first sub-pixel in pixel 2.
               array[3] = value of first sub-pixel in pixel 3.

        If we used a sub_size of 3, for the first pixel we we would create a 3x3 sub-array:


                 array[0] = value of first sub-pixel in pixel 0.
                 array[1] = value of first sub-pixel in pixel 1.
                 array[2] = value of first sub-pixel in pixel 2.
        I0I1I2I  array[3] = value of first sub-pixel in pixel 3.
        I3I4I5I  array[4] = value of first sub-pixel in pixel 4.
        I6I7I8I  array[5] = value of first sub-pixel in pixel 5.
                 array[6] = value of first sub-pixel in pixel 6.
                 array[7] = value of first sub-pixel in pixel 7.
                 array[8] = value of first sub-pixel in pixel 8.

        Case 3: [sub_size=1, native]
        --------------------------------------

        The Array2D has the same properties as Case 1, but is stored as an an ndarray of shape
        [total_y_values, total_x_values].

        All masked entries on the array have values of 0.0.

        For the following example mask:

        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI     This is an example mask.Mask2D, where:
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIoIoIxIxIxIxI     x = `True` (Pixel is masked and excluded from the array)
        IxIxIxIoIoIoIoIxIxIxI     o = `False` (Pixel is not masked and included in the array)
        IxIxIxIoIoIoIoIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI
        IxIxIxIxIxIxIxIxIxIxI

        - array[0,0] = 0.0 (it is masked, thus zero)
        - array[0,0] = 0.0 (it is masked, thus zero)
        - array[3,3] = 0.0 (it is masked, thus zero)
        - array[3,3] = 0.0 (it is masked, thus zero)
        - array[3,4] = 0
        - array[3,4] = -1

        Case 4: [sub_size>, native]
        --------------------------------------

        The properties of this array can be derived by combining Case's 2 and 3 above, whereby the array is stored as
        an ndarray of shape [total_y_values*sub_size, total_x_values*sub_size].

        All sub-pixels in masked pixels have values 0.0.

        Parameters
        ----------
        array
            The values of the array.
        mask
            The 2D mask associated with the array, defining the pixels each array value is paired with and
            originates from.
        """

        array = array_2d_util.convert_array(array=array)

        obj = array.view(cls)
        obj.mask = mask
        obj.header = header

        return obj

    def __array_finalize__(self, obj):

        if hasattr(obj, "mask"):
            self.mask = obj.mask

        if hasattr(obj, "header"):
            self.header = obj.header
        else:
            self.header = None

    def apply_mask(self, mask: Mask2D) -> "Array2D":
        return Array2D.manual_mask(array=self.native, mask=mask, header=self.header)

    @property
    def slim(self) -> "Array2D":
        """
        Return an `Array2D` where the data is stored its `slim` representation, which is an ndarray of shape
        [total_unmasked_pixels * sub_size**2].

        If it is already stored in its `slim` representation it is returned as it is. If not, it is  mapped from
        `native` to `slim` and returned as a new `Array2D`.
        """

        if len(self.shape) == 1:
            return self

        sub_array_1d = array_2d_util.array_2d_slim_from(
            array_2d_native=self, mask_2d=self.mask, sub_size=self.mask.sub_size
        )

        return Array2D(array=sub_array_1d, mask=self.mask, header=self.header)

    @property
    def native(self) -> "Array2D":
        """
        Return a `Array2D` where the data is stored in its `native` representation, which is an ndarray of shape
        [sub_size*total_y_pixels, sub_size*total_x_pixels].

        If it is already stored in its `native` representation it is return as it is. If not, it is mapped from
        `slim` to `native` and returned as a new `Array2D`.
        """

        if len(self.shape) != 1:
            return self

        sub_array_2d = array_2d_util.array_2d_native_from(
            array_2d_slim=self, mask_2d=self.mask, sub_size=self.mask.sub_size
        )
        return Array2D(array=sub_array_2d, mask=self.mask, header=self.header)

    @property
    def binned(self) -> "Array2D":
        """
        Convenience method to access the binned-up array in its 1D representation, which is a Grid2D stored as an
        ndarray of shape [total_unmasked_pixels, 2].

        The binning up process converts a array from (y,x) values where each value is a coordinate on the sub-array to
        (y,x) values where each coordinate is at the centre of its mask (e.g. a array with a sub_size of 1). This is
        performed by taking the mean of all (y,x) values in each sub pixel.

        If the array is stored in 1D it is return as is. If it is stored in 2D, it must first be mapped from 2D to 1D.
        """

        array_2d_slim = self.slim

        binned_array_1d = np.multiply(
            self.mask.sub_fraction,
            array_2d_slim.reshape(-1, self.mask.sub_length).sum(axis=1),
        )

        return Array2D(
            array=binned_array_1d, mask=self.mask.mask_sub_1, header=self.header
        )

    @property
    def extent(self) -> np.ndarray:
        return self.mask.extent

    @property
    def in_counts(self) -> "Array2D":
        return self.header.array_eps_to_counts(array_eps=self)

    @property
    def in_counts_per_second(self) -> "Array2D":
        return self.header.array_counts_to_counts_per_second(
            array_counts=self.in_counts
        )

    @property
    def original_orientation(self) -> Union[np.ndarray, "Array2D"]:
        return layout_util.rotate_array_via_roe_corner_from(
            array=self, roe_corner=self.header.original_roe_corner
        )

    @property
    def readout_offsets(self) -> Tuple[int, int]:
        if self.header is not None:
            if self.header.readout_offsets is not None:
                return self.header.readout_offsets
        return (0, 0)

    @property
    def binned_across_rows(self) -> Array1D:
        binned_array = np.mean(np.ma.masked_array(self.native, self.mask), axis=0)
        return Array1D.manual_native(array=binned_array, pixel_scales=self.pixel_scale)

    @property
    def binned_across_columns(self) -> Array1D:
        binned_array = np.mean(np.ma.masked_array(self.native, self.mask), axis=1)
        return Array1D.manual_native(array=binned_array, pixel_scales=self.pixel_scale)

    def zoomed_around_mask(self, buffer: int = 1) -> "Array2D":
        """
        Extract the 2D region of an array corresponding to the rectangle encompassing all unmasked values.

        This is used to extract and visualize only the region of an image that is used in an analysis.

        Parameters
        ----------
        buffer
            The number pixels around the extracted array used as a buffer.
        """

        extracted_array_2d = array_2d_util.extracted_array_2d_from(
            array_2d=self.native,
            y0=self.mask.zoom_region[0] - buffer,
            y1=self.mask.zoom_region[1] + buffer,
            x0=self.mask.zoom_region[2] - buffer,
            x1=self.mask.zoom_region[3] + buffer,
        )

        mask = Mask2D.unmasked(
            shape_native=extracted_array_2d.shape,
            pixel_scales=self.pixel_scales,
            sub_size=self.sub_size,
            origin=self.mask.mask_centre,
        )

        array = array_2d_util.convert_array_2d(
            array_2d=extracted_array_2d, mask_2d=mask
        )

        return Array2D(array=array, mask=mask, header=self.header)

    def extent_of_zoomed_array(self, buffer: int = 1) -> np.ndarray:
        """
        For an extracted zoomed array computed from the method *zoomed_around_mask* compute its extent in scaled
        coordinates.

        The extent of the grid in scaled units returned as an ndarray of the form [x_min, x_max, y_min, y_max].

        This is used visualize zoomed and extracted arrays via the imshow() method.

        Parameters
        ----------
        buffer
            The number pixels around the extracted array used as a buffer.
        """
        extracted_array_2d = array_2d_util.extracted_array_2d_from(
            array_2d=self.native,
            y0=self.mask.zoom_region[0] - buffer,
            y1=self.mask.zoom_region[1] + buffer,
            x0=self.mask.zoom_region[2] - buffer,
            x1=self.mask.zoom_region[3] + buffer,
        )

        mask = Mask2D.unmasked(
            shape_native=extracted_array_2d.shape,
            pixel_scales=self.pixel_scales,
            sub_size=self.sub_size,
            origin=self.mask.mask_centre,
        )

        return mask.extent

    def resized_from(
        self, new_shape: Tuple[int, int], mask_pad_value: int = 0.0
    ) -> "Array2D":
        """
        Resize the array around its centre to a new input shape.

        If a new_shape dimension is smaller than the current dimension, the data at the edges is trimmed and removed.
        If it is larger, the data is padded with zeros.

        If the array has even sized dimensions, the central pixel around which data is trimmed / padded is chosen as
        the top-left pixel of the central quadrant of pixels.

        Parameters
        -----------
        new_shape
            The new 2D shape of the array.
        """

        resized_array_2d = array_2d_util.resized_array_2d_from(
            array_2d=self.native, resized_shape=new_shape
        )

        resized_mask = self.mask.resized_mask_from(
            new_shape=new_shape, pad_value=mask_pad_value
        )

        array = array_2d_util.convert_array_2d(
            array_2d=resized_array_2d, mask_2d=resized_mask
        )

        return Array2D(array=array, mask=resized_mask, header=self.header)

    def padded_before_convolution_from(
        self, kernel_shape: Tuple[int, int], mask_pad_value: int = 0.0
    ) -> "Array2D":
        """
        When the edge pixels of a mask are unmasked and a convolution is to occur, the signal of edge pixels will be
        'missing' if the grid is used to evaluate the signal via an analytic function.

        To ensure this signal is included the array can be padded, where it is 'buffed' such that it includes all
        pixels whose signal will be convolved into the unmasked pixels given the 2D kernel shape. The values of
        these pixels are zeros.

        Parameters
        ----------
        kernel_shape
            The 2D shape of the kernel which convolves signal from masked pixels to unmasked pixels.
        """
        new_shape = (
            self.shape_native[0] + (kernel_shape[0] - 1),
            self.shape_native[1] + (kernel_shape[1] - 1),
        )
        return self.resized_from(new_shape=new_shape, mask_pad_value=mask_pad_value)

    def trimmed_after_convolution_from(
        self, kernel_shape: Tuple[int, int]
    ) -> "Array2D":
        """
        When the edge pixels of a mask are unmasked and a convolution is to occur, the signal of edge pixels will be
        'missing' if the grid is used to evaluate the signal via an analytic function.

        To ensure this signal is included the array can be padded, a padded array can be computed via the method
        *padded_before_convolution_from*. This function trims the array back to its original shape, after the padded array
        has been used for computational.

        Parameters
        ----------
        kernel_shape
            The 2D shape of the kernel which convolves signal from masked pixels to unmasked pixels.
        """
        psf_cut_y = int(np.ceil(kernel_shape[0] / 2)) - 1
        psf_cut_x = int(np.ceil(kernel_shape[1] / 2)) - 1
        array_y = int(self.mask.shape[0])
        array_x = int(self.mask.shape[1])
        trimmed_array_2d = self.native[
            psf_cut_y : array_y - psf_cut_y, psf_cut_x : array_x - psf_cut_x
        ]

        resized_mask = self.mask.resized_mask_from(new_shape=trimmed_array_2d.shape)

        array = array_2d_util.convert_array_2d(
            array_2d=trimmed_array_2d, mask_2d=resized_mask
        )

        return Array2D(array=array, mask=resized_mask, header=self.header)

    def output_to_fits(self, file_path: str, overwrite: bool = False):
        """
        Output the array to a .fits file.

        Parameters
        ----------
        file_path
            The output path of the file, including the filename and the `.fits` extension e.g. '/path/to/filename.fits'
        overwrite
            If a file already exists at the path, if overwrite=True it is overwritten else an error is raised.
        """
        array_2d_util.numpy_array_2d_to_fits(
            array_2d=self.native, file_path=file_path, overwrite=overwrite
        )


class Array2D(AbstractArray2D):
    @classmethod
    def manual_slim(
        cls,
        array: Union[np.ndarray, List],
        shape_native: Tuple[int, int],
        pixel_scales: ty.PixelScales,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
        header: Optional[Header] = None,
    ) -> "Array2D":
        """
        Create an Array2D (see `AbstractArray2D.__new__`) by inputting the array values in 1D, for example:

        array=np.array([1.0, 2.0, 3.0, 4.0])

        array=[1.0, 2.0, 3.0, 4.0]

        From 1D input the method cannot determine the 2D shape of the array and its mask, thus the shape_native must be
        input into this method. The mask is setup as a unmasked `Mask2D` of shape_native.

        Parameters
        ----------
        array or list
            The values of the array input as an ndarray of shape [total_unmasked_pixels*(sub_size**2)] or a list of
            lists.
        shape_native
            The 2D shape of the mask the array is paired with.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the mask's coordinate system.
        """

        pixel_scales = geometry_util.convert_pixel_scales_2d(pixel_scales=pixel_scales)

        if shape_native and len(shape_native) != 2:
            raise exc.ArrayException(
                "The input shape_native parameter is not a tuple of type (int, int)"
            )

        mask = Mask2D.unmasked(
            shape_native=shape_native,
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
        )

        array = array_2d_util.convert_array_2d(array_2d=array, mask_2d=mask)

        return Array2D(array=array, mask=mask, header=header)

    @classmethod
    def manual_native(
        cls,
        array: Union[np.ndarray, List],
        pixel_scales: ty.PixelScales,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
        header: Optional[Header] = None,
    ) -> "Array2D":
        """
        Create an Array2D (see `AbstractArray2D.__new__`) by inputting the array values in 2D, for example:

        array=np.ndarray([[1.0, 2.0],
                         [3.0, 4.0]])

        array=[[1.0, 2.0],
              [3.0, 4.0]]

        The 2D shape of the array and its mask are determined from the input array and the mask is setup as an
        unmasked `Mask2D` of shape_native.

        Parameters
        ----------
        array or list
            The values of the array input as an ndarray of shape [total_y_pixels*sub_size, total_x_pixel*sub_size] or a
             list of lists.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the mask's coordinate system.
        """

        pixel_scales = geometry_util.convert_pixel_scales_2d(pixel_scales=pixel_scales)

        array = array_2d_util.convert_array(array=array)

        shape_native = (int(array.shape[0] / sub_size), int(array.shape[1] / sub_size))

        mask = Mask2D.unmasked(
            shape_native=shape_native,
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
        )

        array = array_2d_util.convert_array_2d(array_2d=array, mask_2d=mask)

        return Array2D(array=array, mask=mask, header=header)

    @classmethod
    def manual(
        cls,
        array: Union[np.ndarray, List],
        pixel_scales: ty.PixelScales,
        shape_native: Tuple[int, int] = None,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
        header: Optional[Header] = None,
    ) -> "Array2D":
        """
        Create an Array2D (see `AbstractArray2D.__new__`) by inputting the array values in 1D or 2D, automatically
        determining whether to use the 'manual_slim' or 'manual_native' methods.

        See the manual_slim and manual_native methods for examples.

        Parameters
        ----------
        array or list
            The values of the array input as an ndarray of shape [total_unmasked_pixels*(sub_size**2)] or a list of
            lists.
        shape_native
            The 2D shape of the mask the array is paired with.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the mask's coordinate system.
        """
        array = array_2d_util.convert_array(array=array)

        if len(array.shape) == 1:
            return cls.manual_slim(
                array=array,
                pixel_scales=pixel_scales,
                shape_native=shape_native,
                sub_size=sub_size,
                origin=origin,
            )
        return cls.manual_native(
            array=array,
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
            header=header,
        )

    @classmethod
    def manual_mask(
        cls, array: Union[np.ndarray, List], mask: Mask2D, header: Header = None
    ) -> "Array2D":
        """
        Create an `Array2D` (see `AbstractArray2D.__new__`) by inputting the array values in 1D or 2D with its mask,
        for example:

        mask = Mask2D([[True, False, False, False])
        array=np.array([1.0, 2.0, 3.0])

        Parameters
        ----------
        array
            The values of the array input as an ndarray of shape [total_unmasked_pixels*(sub_size**2)] or a list of
            lists.
        mask
            The mask whose masked pixels are used to setup the sub-pixel grid.
        """
        array = array_2d_util.convert_array_2d(array_2d=array, mask_2d=mask)
        return Array2D(array=array, mask=mask, header=header)

    @classmethod
    def full(
        cls,
        fill_value: float,
        shape_native: Tuple[int, int],
        pixel_scales: ty.PixelScales,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
        header: Optional[Header] = None,
    ) -> "Array2D":
        """
        Create an `Array2D` (see `AbstractArray2D.__new__`) where all values are filled with an input fill value,
        analogous to the method np.full().

        From 1D input the method cannot determine the 2D shape of the array and its mask, thus the shape_native must be
        input into this method. The mask is setup as a unmasked `Mask2D` of shape_native.

        Parameters
        ----------
        fill_value
            The value all array elements are filled with.
        shape_native
            The 2D shape of the mask the array is paired with.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the mask's coordinate system.
        """
        if sub_size is not None:
            shape_native = (shape_native[0] * sub_size, shape_native[1] * sub_size)

        return cls.manual_native(
            array=np.full(fill_value=fill_value, shape=shape_native),
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
            header=header,
        )

    @classmethod
    def ones(
        cls,
        shape_native: Tuple[int, int],
        pixel_scales: ty.PixelScales,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
        header: Header = None,
    ) -> "Array2D":
        """
        Create an Array2D (see `AbstractArray2D.__new__`) where all values are filled with ones, analogous to the
        method np.ones().

        From 1D input the method cannot determine the 2D shape of the array and its mask, thus the shape_native must be
        input into this method. The mask is setup as a unmasked `Mask2D` of shape_native.

        Parameters
        ----------
        shape_native
            The 2D shape of the mask the array is paired with.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the mask's coordinate system.
        """
        return cls.full(
            fill_value=1.0,
            shape_native=shape_native,
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
            header=header,
        )

    @classmethod
    def zeros(
        cls,
        shape_native: Tuple[int, int],
        pixel_scales: ty.PixelScales,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
        header: Header = None,
    ) -> "Array2D":
        """
        Create an Array2D (see `AbstractArray2D.__new__`) where all values are filled with zeros, analogous to the
        method np.ones().

        From 1D input the method cannot determine the 2D shape of the array and its mask, thus the shape_native must be
        input into this method. The mask is setup as a unmasked `Mask2D` of shape_native.

        Parameters
        ----------
        shape_native
            The 2D shape of the mask the array is paired with.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the mask's coordinate system.
        """
        return cls.full(
            fill_value=0.0,
            shape_native=shape_native,
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
            header=header,
        )

    @classmethod
    def from_fits(
        cls,
        file_path: str,
        pixel_scales: ty.PixelScales,
        hdu: int = 0,
        sub_size: int = 1,
        origin: Tuple[float, float] = (0.0, 0.0),
    ) -> "Array2D":
        """
        Create an Array2D (see `AbstractArray2D.__new__`) by loading the array values from a .fits file.

        Parameters
        ----------
        file_path
            The path the file is loaded from, including the filename and the `.fits` extension,
            e.g. '/path/to/filename.fits'
        hdu
            The Header-Data Unit of the .fits file the array data is loaded from.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-array.
        origin
            The (y,x) scaled units origin of the coordinate system.
        """
        array_2d = array_2d_util.numpy_array_2d_via_fits_from(
            file_path=file_path, hdu=hdu
        )

        header_sci_obj = array_2d_util.header_obj_from(file_path=file_path, hdu=0)
        header_hdu_obj = array_2d_util.header_obj_from(file_path=file_path, hdu=hdu)

        return cls.manual_native(
            array=array_2d,
            pixel_scales=pixel_scales,
            sub_size=sub_size,
            origin=origin,
            header=Header(header_sci_obj=header_sci_obj, header_hdu_obj=header_hdu_obj),
        )

    @classmethod
    def manual_yx_and_values(
        cls,
        y: Union[np.ndarray, List],
        x: Union[np.ndarray, List],
        values: Union[np.ndarray, List],
        shape_native: Tuple[int, int],
        pixel_scales: ty.PixelScales,
        sub_size: int = 1,
        header: Header = None,
    ) -> "Array2D":
        """
        Create an `Array2D` (see `AbstractArray2D.__new__`) by inputting the y and x pixel values where the array is filled
        and the values to fill the array, for example:

        y = np.array([0, 0, 0, 1])
        x = np.array([0, 1, 2, 0])
        value = [1.0, 2.0, 3.0, 4.0]

        From 1D input the method cannot determine the 2D shape of the grid and its mask, thus the shape_native must be
        input into this method. The mask is setup as a unmasked `Mask2D` of shape_native.

        Parameters
        ----------
        y or list
            The y pixel indexes where value sare input, as an ndarray of shape [total_y_pixels*sub_size] or a list.
        x or list
            The x pixel indexes where value sare input, as an ndarray of shape [total_y_pixels*sub_size] or a list.
        values or list
            The values which are used too fill in the array.
        shape_native
            The 2D shape of the mask the grid is paired with.
        pixel_scales
            The (y,x) scaled units to pixel units conversion factors of every pixel. If this is input as a `float`,
            it is converted to a (float, float) structure.
        sub_size
            The size (sub_size x sub_size) of each unmasked pixels sub-grid.
        origin
            The origin of the grid's mask.
        """
        pixel_scales = geometry_util.convert_pixel_scales_2d(pixel_scales=pixel_scales)

        from autoarray.structures.grids.uniform_2d import Grid2D

        grid = Grid2D.manual_yx_1d(
            y=y, x=x, shape_native=shape_native, pixel_scales=pixel_scales, sub_size=1
        )

        grid_pixels = grid_2d_util.grid_pixel_indexes_2d_slim_from(
            grid_scaled_2d_slim=grid.slim,
            shape_native=shape_native,
            pixel_scales=pixel_scales,
        )

        array_1d = np.zeros(shape=shape_native[0] * shape_native[1])

        for i in range(grid_pixels.shape[0]):
            array_1d[i] = values[int(grid_pixels[i])]

        return cls.manual_slim(
            array=array_1d,
            pixel_scales=pixel_scales,
            shape_native=shape_native,
            sub_size=sub_size,
            header=header,
        )
