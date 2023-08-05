"""
    This submodule  contain the DataPacke and DataUnpacker class and bits_to_max_decimal function used in both class.
"""
import numpy as np
import numpy.typing as npt
from struct import unpack
import logging

data_packer_log = logging.getLogger(__name__)

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]


def bits_to_max_decimal(bits_in: int) -> int:
    """
    This function convert bits length integer to the correspond max decimal number
    :param bits_in: bits length
    :return: Returns the maximum decimal number
    """
    str_array_out = []
    for i in range(bits_in):
        str_array_out.append("1")

    join_str_out = "".join(str_array_out)
    max_decimal = int(join_str_out, 2)
    return max_decimal


class DataPacker:
    """
    The function of this object is to pass python data to C format data.
    """

    def array_to_pack(self, data_array: list, bit_len: list) -> (int, int):
        """
        This method converts a 1D data array to a representative packed decimal number
        :param data_array: n length 1d array of data
        :param bit_len: same length array as 'data_array', represent the bit len distribution for each position
        :return: Decimal packed data
        """
        data_out = 0
        sum_bit_len = 0
        if len(data_array) == len(bit_len):
            for pos in range(len(data_array)):
                if pos == 0:
                    data_out = (int(data_array[pos] & bits_to_max_decimal(bit_len[pos])) << 0)

                else:
                    sum_bit_len += bit_len[pos - 1]
                    data_out |= int(data_array[pos] & bits_to_max_decimal(bit_len[pos])) << sum_bit_len

            sum_bit_len += bit_len[-1]
            return data_out, sum_bit_len

        else:
            data_packer_log.error("Data array and bit len array must have the same length")
            raise AssertionError

    def split_pack(self, decimal_packed_data: int, bit_len_data: int, split_len: int) -> list:
        """
        Split packed data to separate bit len packed data
        :param decimal_packed_data: Decimal packed data
        :param bit_len_data: How many bits does 'decimal_packed_data' occupy
        :param split_len: Bit size of packets
        return: Packed split.
        """
        sum_bit_len = 0
        pack_array_out = []
        packs = int(np.ceil(bit_len_data / split_len))  # Round up float value
        max_decimal = bits_to_max_decimal(split_len)

        for pack in range(packs):
            pack_array_out.append((decimal_packed_data >> sum_bit_len) & max_decimal)
            sum_bit_len += split_len

        return pack_array_out


class DataUnpacker:
    """
    The function of this object is to convert C  data format to python format.
    """

    def pack_to_arr(self, decimal_pack: int, bit_len_array: list) -> list:
        """
        This method converts packed decimal number to a data array
        :param decimal_pack: Decimal packed data in
        :param bit_len_array: Bits length distribution for the array out
        :return: Data array out.
        """
        array_data_out = []
        sum_bit_len = 0

        for bit_length in bit_len_array:
            array_data_out.append((decimal_pack >> sum_bit_len) & bits_to_max_decimal(bit_length))
            sum_bit_len += bit_length

        return array_data_out

    def merge_pack_arr(self, pack_array: list, bits_data_packs: int) -> (int, int):
        """
        Merge separate bit len packed data to single packed data.
        :param pack_array: Packed data array in.
        :param bits_data_packs: Bit size to unpack.
        :return: Single decimal data value out
        """
        data_out = 0
        sum_bit_len = 0
        for pos in range(len(pack_array)):
            if pos == 0:
                data_out = (int(pack_array[pos] & bits_to_max_decimal(bits_data_packs)) << 0)

            else:
                sum_bit_len += bits_data_packs
                data_out |= int(pack_array[pos] & bits_to_max_decimal(bits_data_packs)) << sum_bit_len

        sum_bit_len += bits_data_packs

        return data_out, sum_bit_len


def acq_unpack(data: list, reshape_format: tuple) -> NDArrayUint32:
    unpack_data = unpack("H" * ((len(data)) * 2), data)
    try:
        data_reshape = np.uint32(np.reshape(unpack_data, reshape_format))
        return data_reshape
    except ValueError as e:
        data_packer_log.error(f"Can't reshape the correspond data: {e}")
        raise ValueError
