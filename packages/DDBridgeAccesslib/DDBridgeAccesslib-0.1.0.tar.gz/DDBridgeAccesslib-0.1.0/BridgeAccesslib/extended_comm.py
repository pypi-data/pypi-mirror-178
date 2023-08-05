"""
    **This submodule is the bridge between top layer manager and communication functionalities.**
"""
import numpy as np
import numpy.typing as npt
import logging
from typing import Callable
from .comm import Bridge
from BridgeAccesslib.data_convert import convert
from BridgeAccesslib.data_convert import pack_data_swap

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]
NDArrayInt16 = npt.NDArray[np.int16]


class ExtendedBridge(Bridge):

    def __init__(self, ip: str, sync_port: int, async_port: int, dll_absolute_path: str) -> None:
        """
        Initialize CustomBridge class
        :param ip: ip address
        :param sync_port: synchronous port
        :param async_port: asynchronous port
        :param dll_absolute_path: library absolute path
        """
        self._log = logging.getLogger(__name__)
        super().__init__(ip, sync_port, async_port, dll_absolute_path)

    def _full_array_write(self, write_func: Callable, read_func: Callable, register_data: NDArrayUint32,
                          chips_bitmap: int, len_out_array: int, attempts: int = 3) -> int:
        """
        Write the register chip by chip and checks if te operation has success
        :param write_func: Register write function from Bridge
        :param read_func: Register read function from Bridge
        :param register_data: In data to write
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect, 5 for chip register and 480 for pixel_register
        :param attempts: Attempts for each chip, if more than "attempts" raise error
        :return: a negative number in case of error, 0 if no error
        """
        counter_error: int = 0
        incr = len_out_array
        chips_bitmap_list, array_subset_pos = convert(chips_bitmap, incr)

        i = 0
        for chips_bitmap in chips_bitmap_list:
            counter_error = 0
            for attempt in range(attempts):
                data_in = register_data[array_subset_pos[i]:array_subset_pos[i] + incr]
                chip_error = write_func(data_in, chips_bitmap)
                if chip_error < 0:
                    self._log.error(f"Can't program register.")
                    counter_error += 1
                    break

                error, read_data = read_func(chips_bitmap, len_out_array)
                """ This line under is only for pixel register, in testing check functionalities."""
                # read_data = pack_data_swap(read_data)

                if np.all(read_data == data_in) or error > 0:
                    break
                else:
                    self._log.error("Error reading/comparing register data.")
                    counter_error += 1
            i += 1
        if counter_error >= attempts:
            return -1
        else:
            return 0

    # Custom pixel register
    def full_array_chip_register_write(self, chip_register_data: NDArrayUint32, chips_bitmap: int,
                                       len_out_array: int = 5, attempts: int = 3):
        """
        Write the chip register chip by chip and checks if te operation has success
        :param chip_register_data: In data to write
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :param attempts: Attempts for each chip, if more than "attempts" raise error
        :return: a negative number in case of error, 0 if no error
        """
        return self._full_array_write(self.chip_register_write, self.chip_register_read, chip_register_data,
                                      chips_bitmap, len_out_array, attempts)

    def full_array_pixel_register_write(self, pixel_register_data: NDArrayUint32, chips_bitmap: int,
                                        len_out_array: int = 480, attempts: int = 3):
        """
        Write the pixel register chip by chip and checks if te operation has success
        :param pixel_register_data: In data to write
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :param attempts: Attempts for each chip, if more than "attempts" raise error
        :return: a negative number in case of error, 0 if no error
        """
        return self._full_array_write(self.pixel_register_write, self.pixel_register_read, pixel_register_data,
                                      chips_bitmap, len_out_array, attempts)

    def load_normalization_factors(self, factor_value_mx: NDArrayUint32,
                                   chip_bitmap_array: NDArrayUint32) -> NDArrayInt16:
        """
        Program normalization factors one by one
        :param factor_value_mx: Array with all the factors
        :param chip_bitmap_array: Array with the corresponding bitmap
        :return: Errors array
        """
        error_array = []
        i = 0
        for chip_bitmap in chip_bitmap_array:
            factor_value_array = factor_value_mx[i]
            error = self.load_flood_norm_factors(factor_value_array, chip_bitmap)
            error_array.append(error)

        return np.int16(error_array)
