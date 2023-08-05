"""
    This submodule inheritance DataPacker, DataUnpacker and specialize for DeepDetection
"""
import numpy as np
import numpy.typing as npt
from BitConvertAccesslib.data_manager import DataPacker, DataUnpacker

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]


class DeepDataPacker(DataPacker):
    """
    This object is a specialization of DataPacker designed to work with DeepDetection.
    """

    def pixel_reg_to_pack(self, pixel_reg_data: NDArrayUint32, bit_len_config: list, bit_len_packs: int) -> list:
        """
        Use DataPacker.array_to_pack and DataPacker.split_pack to convert the pixel_register matrix to dll format
        :param pixel_reg_data: Pixel register matrix, usual shape = (30, 8, 20, 44)
        :param bit_len_config: Pixel register bit len configuration, usual shape = (44,)
        :param bit_len_packs: The pack bits value, usual 32 bits.
        :return: Data packed used in dll.
        """
        mx_pack_data_out = []

        for chip_pos in range(len(pixel_reg_data)):
            for rows_pos in range(len(pixel_reg_data[0])):
                for column_pos in range(len(pixel_reg_data[0][0])):
                    decimal_pack_data_out, bit_len_data_out = self.array_to_pack(pixel_reg_data[chip_pos][rows_pos]
                                                                                 [column_pos], bit_len_config)
                    mx_pack_data_out.append(self.split_pack(decimal_pack_data_out, bit_len_data_out, bit_len_packs))

        return mx_pack_data_out

    def chip_reg_to_pack(self, chip_reg_data: NDArrayUint32, bit_len_config: list, bit_len_packs: int) -> list:
        """
        Use DataPacker.array_to_pack and DataPacker.split_pack to convert the chip_register matrix to dll format
        :param chip_reg_data: Chip register matrix, usual shape = (19,)
        :param bit_len_config: Chip register bit len configuration, usual shape = (19,)
        :param bit_len_packs: The pack bits value, usual 32 bits.
        :return: Data packed used in dll.
        """
        mx_pack_data_out = []
        for chip_pos in range(len(chip_reg_data)):
            decimal_pack_data_out, bit_len_data_out = self.array_to_pack(chip_reg_data[chip_pos], bit_len_config)
            mx_pack_data_out.append(np.flip(self.split_pack(decimal_pack_data_out, bit_len_data_out, bit_len_packs)))

        return mx_pack_data_out


class DeepDataUnpacker(DataUnpacker):
    """
    This object is a specialization of DataUnpacker designed to work with DeepDetection.
    """

    def pack_to_pixel_reg(self, dll_packed_data: list, expected_output_shape: tuple, bit_len_packs: int,
                          bit_len_config: list) -> NDArrayUint32:
        """
        Use DataUnpacker.merge_pack_arr and DataUnpacker.pack_to_arr to convert the dll format to pixel_register matrix
        :param dll_packed_data: Data packed data read from dll
        :param expected_output_shape: Expected output shape, usually it is (N_CHIPS, 8, 20, 44)
        :param bit_len_packs: The pack bits value, usual 32 bits
        :param bit_len_config: Pixel register bit len configuration, usual shape = (44,)
        :return: Data read in the correspond format.
        """
        mx_data_container = np.zeros(expected_output_shape, dtype=np.uint32)

        packs_len = int(np.ceil(np.sum(bit_len_config) / bit_len_packs))
        packs_pos = packs_len
        pos = 0
        for chip_pos in range(len(mx_data_container)):
            for rows_pos in range(len(mx_data_container[0])):
                for column_pos in range(len(mx_data_container[0][0])):
                    decimal_data, bit_len_sum = self.merge_pack_arr(dll_packed_data[pos:packs_pos], bit_len_packs)
                    pos += packs_len
                    packs_pos += packs_len
                    mx_data_container[chip_pos][rows_pos][column_pos] = self.pack_to_arr(decimal_data, bit_len_config)

        return mx_data_container

    def pack_to_chip_reg(self, dll_packed_data: list, expected_output_shape: tuple, bit_len_packs: int,
                         bit_len_config: list) -> NDArrayUint32:
        """
        Use DataUnpacker.merge_pack_arr and DataUnpacker.pack_to_arr to convert the dll format to pixel_register matrix
        :param dll_packed_data: Data packed data read from dll
        :param expected_output_shape: Expected output shape, usually it is (N_CHIPS, 19)
        :param bit_len_packs: The pack bits value, usual 32 bits
        :param bit_len_config: Pixel register bit len configuration, usual shape = (19,)
        :return: Data read in the correspond format.
        """
        mx_data_container = np.zeros(expected_output_shape, dtype=np.uint32)

        packs_len = int(np.ceil(np.sum(bit_len_config) / bit_len_packs))
        packs_pos = packs_len
        pos = 0
        for chip_pos in range(len(mx_data_container)):
            decimal_data, bit_len_sum = self.merge_pack_arr(np.flip(dll_packed_data[pos:packs_pos]),
                                                            bit_len_packs)
            pos += packs_len
            packs_pos += packs_len
            mx_data_container[chip_pos] = self.pack_to_arr(decimal_data, bit_len_config)

        return mx_data_container
