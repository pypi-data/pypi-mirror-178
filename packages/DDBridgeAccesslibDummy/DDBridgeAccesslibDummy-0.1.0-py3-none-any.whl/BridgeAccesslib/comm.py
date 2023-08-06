import ctypes
import numpy as np
import numpy.typing as npt
import logging

# Typing
NDArrayUint32 = npt.NDArray[np.uint32]


class AcqInfo(ctypes.Structure):
    _fields_ = [("pulses_width", ctypes.c_uint32),
                ("pulses", ctypes.c_uint32),
                ("timer_reg", ctypes.c_uint16),
                ("belt_dir", ctypes.c_bool),
                ("test_pulses", ctypes.c_bool),
                ("tdi", ctypes.c_bool)]


def bitmap_deserializer(chip_bitmap: int) -> NDArrayUint32:
    first_bb = chip_bitmap & 0xFFFFFFFF  # first 30 chips
    second_bb = (chip_bitmap & (0xFFFFFFFF << 32)) >> 32
    return np.array([first_bb, second_bb], dtype=np.uint32)


class Bridge:
    """
    The function of this class is to interact with the client running on the FPGA through a dynamic libray
    """

    def __init__(self, ip: str, sync_port: int, async_port: int, dll_absolute_path: str) -> None:
        """
        Initialize bridge class
        :param ip: ip address
        :param sync_port: synchronous port
        :param async_port: asynchronous port
        :param dll_absolute_path: library absolute path
        """
        self._bridge_log = logging.getLogger(__name__)
        try:
            self.my_dll = ctypes.CDLL(dll_absolute_path)
        except OSError:
            self._bridge_log.error(f"Impossible to find dynamic library with the following path: {dll_absolute_path}")
            raise OSError

        error = self.my_dll.InitCommunication(ctypes.c_char_p(f"{ip}".encode("utf-8")), sync_port, async_port, True)
        if error < 0:
            self._bridge_log.error("Impossible to communicate with server.")
            raise ConnectionError

    def close_communication(self) -> None:
        """
        Close communication with dynamic library
        """
        self.my_dll.CloseCommunication()

    # Resets
    def camera_reset(self) -> int:
        """
        Reset all ERICA chips
        :return: a negative number in case of error, 0 if no error
        """
        return self.my_dll.CameraReset()

    def controller_reset(self) -> None:
        """
        Reset FPGA controller
        :return: a negative number in case of error, 0 if no error
        """
        return self.my_dll.ControllerReset()

    # Chip_register
    def chip_register_write(self, chip_register_data: NDArrayUint32, chips_bitmap: int) -> int:
        """
        Write to chip register. (If we are writing more than one chip only it is possible to write the same data)
        :param chip_register_data: in data to write
        :param chips_bitmap: bitmap of the selected chip
        :return: a negative number in case of error, 0 if no error
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_p_out = chip_register_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        return self.my_dll.ChipRegisterWrite(c_p_out, map_pointer)

    def chip_register_read(self, chips_bitmap: int, len_out_array: int = 5) -> (int, NDArrayUint32):
        """
        It reads chip register from selected chip
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :return: a negative number in case of error, 0 if no error / Chip register data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        out_data = np.zeros((len_out_array,), dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.ChipRegisterRead(out_data_p, map_pointer)
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)

        return dll_info, out

    def full_array_chip_register_read(self, chips_bitmap: int, len_out_array: int = 150) -> (int, NDArrayUint32):
        """
        It reads chip register from all the chips
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :return: a negative number in case of error, 0 if no error / Chip register data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        out_data = np.zeros((len_out_array,), dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.FullArrayChipRegisterRead(out_data_p, map_pointer)
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)

        return dll_info, out

    # Pixel_register
    def pixel_register_write(self, pixel_register_data: NDArrayUint32, chips_bitmap: int) -> int:
        """
        Write to pixel register. (If we are writing more than one chip only it is possible to write the same data)
        :param pixel_register_data: in data to write
        :param chips_bitmap: bitmap of the selected chip
        :return: a negative number in case of error, 0 if no error
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_p_out = pixel_register_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        return self.my_dll.PixelRegisterWrite(c_p_out, map_pointer)

    def pixel_register_read(self, chips_bitmap: int, len_out_array: int = 480) -> (int, NDArrayUint32):
        """
        It reads pixel register from selected chip
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :return: a negative number in case of error, 0 if no error / Pixel register data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        out_data = np.zeros((len_out_array,), dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.PixelRegisterRead(out_data_p, map_pointer)
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)

        return dll_info, out

    def full_array_pixel_register_read(self, chips_bitmap: int, len_out_array: int = 14400) -> (int, NDArrayUint32):
        """
        It reads pixel register from all the chips
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :return: a negative number in case of error, 0 if no error / Pixel register data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        out_data = np.zeros((len_out_array,), dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.FullArrayPixelRegisterRead(out_data_p, map_pointer)
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)

        return dll_info, out

    # Chip identification
    def read_id(self, chips_bitmap: int) -> (int, np.uint32):
        """
        Read ID of selected chip
        :param chips_bitmap: bitmap of enabled chips
        :return: a negative number in case of error, 0 if no error / Identification data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        pointer = ctypes.POINTER(ctypes.c_uint32)
        num = ctypes.c_uint32(0)
        addr = ctypes.addressof(num)
        ptr = ctypes.cast(addr, pointer)
        dll_info = self.my_dll.ReadEricaID(ptr, map_pointer)

        return dll_info, ptr[0]

    def full_array_read_erica_id(self, chips_bitmap: int, len_out_array: int = 30) -> (int, NDArrayUint32):
        """
        Read ID of all chips
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :return: a negative number in case of error, 0 if no error / Pixel register data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        out_data = np.zeros((len_out_array,), dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.FullArrayReadEricaID(out_data_p, map_pointer)
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)

        return dll_info, out

    # Temperature
    def read_temperature(self, chips_bitmap: int) -> (int, np.uint32):
        """
        Read temperature of the selected chip
        :param chips_bitmap: bitmap of enabled chips
        :return: a negative number in case of error, 0 if no error / Temperature data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        pointer = ctypes.POINTER(ctypes.c_uint32)
        num = ctypes.c_uint32(0)
        addr = ctypes.addressof(num)
        ptr = ctypes.cast(addr, pointer)
        dll_info = self.my_dll.ReadTemperature(ptr, map_pointer)

        return dll_info, np.uint32(ptr[0])

    def full_array_read_temperature(self, chips_bitmap: int, len_out_array: int = 30) -> (int, NDArrayUint32):
        """
        Read temperature of all chips
        :param chips_bitmap: bitmap of the selected chip
        :param len_out_array: size of the data we expect
        :return: a negative number in case of error, 0 if no error / Temperature data
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        out_data = np.zeros((len_out_array,), dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.FullArrayReadReadTemperature(out_data_p, map_pointer)
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)

        return dll_info, out

    # Acquisition
    def acq(self, chips_bitmap: int, pulses_width: int, pulses: int, timer_reg: int,
            belt_dir: bool, test_pulses: bool, tdi: bool, frames: int) -> int:
        """
        Acquire the requested number of frames and stored in fpga buffer
        :param chips_bitmap: bitmap of the selected chip
        :param pulses_width:
        :param pulses:
        :param timer_reg:
        :param belt_dir:
        :param test_pulses:
        :param tdi:
        :param frames: number of frames to acquire
        :return: a negative number in case of error, 0 if no error
        """
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32 * 30 = 14400
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        acq_info_struct = AcqInfo(pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)
        return self.my_dll.ACQuisition(acq_info_struct, ctypes.c_uint32(frames), map_pointer)

    def acq_cont(self, chips_bitmap: int, pulses_width: int, pulses: int, timer_reg: int,
                 belt_dir: bool, test_pulses: bool, tdi: bool) -> int:
        """
        Acquire frames continuously, in this mode an ACQuisitionStop must be used to finish acquisition, and stored in
        fpga buffer
        :param chips_bitmap: bitmap of the selected chip
        :param pulses_width:
        :param pulses:
        :param timer_reg:
        :param belt_dir:
        :param test_pulses:
        :param tdi:
        :return: a negative number in case of error, 0 if no error
        """
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        acq_info_struct = AcqInfo(pulses_width, pulses, timer_reg, belt_dir, test_pulses, tdi)
        return self.my_dll.ACQuisitionCont(acq_info_struct, map_pointer)

    def stop_acq(self) -> int:
        """
        Stop current acquisition.
        :return: a negative number in case of error, 0 if no error
        """
        return self.my_dll.ACQuisitionStop()

    def pop_frame(self, time_out: int = 600, len_out_array: int = 14400) -> (int, NDArrayUint32):
        """
        Copies last frame of internal buffer to provided pointer or, if buffer is empty, wait for new data for
        up to timeout_ms
        :param time_out: how many ms to wait
        :param len_out_array: expected output len
        :return: 0 in case of success, -1 if a cancel has been requested / Acquisition data
        """
        # 1920 bytes --> 15360 bit / packs 32 --> 480 packs uint32 * 30 = 14400
        out_data = np.full((len_out_array,), 0xff, dtype=np.uint32)
        out_data_p = out_data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        dll_info = self.my_dll.PopDataWithTimeout(out_data_p, ctypes.c_uint32(time_out))
        out = np.ctypeslib.as_array(out_data_p, out_data.shape)
        return dll_info, out

    def cancel_pop_frame(self) -> None:
        """
        If a pop frame is waiting for data, force it to exit returning an error
        """
        self.my_dll.CancelPopFrame()

    # Heart beat
    def update_hb(self) -> int:
        """
        Sends a heart beat to the server. It must be sent with a period of 2.5 seconds.

        Server can automatically detect when a client is offline and remove it.
        To avoid this the heartbeat must be updated periodically.
        By default, the server will remove a client after 5s without receiving a heartbeat
        :return: a negative number in case of error, 0 if no error
        """
        return self.my_dll.UpdateHB()

    # Internal DLL functions
    def get_element_counter(self) -> np.uint32:
        """
        Returns the number of elements in the buffer.
        Data is temporarily stored in a circular buffer.
        This functions returns the current number of elements in it.
        Note: This function doesn't interact with the server
        :return: number of elements in buffer
        """
        return np.uint32(self.my_dll.GetElemCounter())

    def reset_buffer(self) -> None:
        """
        Removes data from buffer.
        Remove all current data in buffer, resets counters to 0.
        Note: his function doesn't interact with the server
        """
        self.my_dll.ResetBuffer()

    def get_timeout_counter(self) -> np.uint32:
        """
        Get number of timeouts.
        There is a counter to know how many times we tried to read data  but received an error instead
        (ie: a timeout most probably).
        This functions returns that counter.
        Note: This function doesn't interact with the server
        :return: counter of timeout errors
        """
        return np.uint32(self.my_dll.GetTimeoutsCounter())

    def reset_timeout_counter(self) -> None:
        """
        Reset timeout counter to 0.
        Remove all current data in buffer, resets counters to 0.
        Note: his function doesn't interact with the server
        """
        self.my_dll.ResetTimeoutsCounter()

    def get_write_idx(self) -> np.uint32:
        """
        Data is stored in a circular buffer. This function returns the "write pointer" of that buffer.
        Note: This function doesn't interact with the server
        :return: write pointer of circular buffer
        """
        return np.uint32(self.my_dll.GetWriteIdx())

    def get_read_idx(self) -> np.uint32:
        """
        Data is stored in a circular buffer. This function returns the "write pointer" of that buffer.
        Note: This function doesn't interact with the server
        :return: write pointer of circular buffer
        """
        return np.uint32(self.my_dll.GetReadIdx())

    # Factors and high voltage
    def load_flood_norm_factors(self, factor_value_mx: NDArrayUint32, chips_bitmap: int) -> int:
        """
        Load normalization factors
        :param factor_value_mx: Matrix with all the factors values
        :param chips_bitmap: bitmap of enabled chips
        :return: a negative number in case of error, 0 if no error
        """
        bitmap = bitmap_deserializer(chips_bitmap)
        map_pointer = bitmap.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_p_out = factor_value_mx.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        return self.my_dll.LoadFloodNormFactors(c_p_out, map_pointer)

    def set_hv(self, counts: float) -> int:
        """
        Set voltage
        :param counts: counts number of counts to write
        :return: a negative number in case of error, 0 if no error
        """
        counts = int((counts / 2.5) * 65535)
        return self.my_dll.SetHV(ctypes.c_uint32(counts))

    def set_tpdac(self, counts: float) -> int:
        """
        Set TPDAC
        :param counts: counts number of counts to write
        :return: a negative number in case of error, 0 if no error
        """
        counts = int((counts / 2.5) * 65535)
        return self.my_dll.SetTPDAC(ctypes.c_uint32(counts))

    # Debugging functions
    def print_all_regs(self) -> None:
        """
        Reads all registers of the FPGA and print them to stdout
        """
        self.my_dll.PrintAllRegs()


def to_fixed(f_mx, e=12):
    out = []
    for f in f_mx:
        a = f * (2 ** e)
        b = int(round(a))
        if a < 0:
            # next three lines turns b into it's 2's complement.
            b = abs(b)
            b = ~b
            b += 1
            out.append(b)
        else:
            out.append(b)
    return out
