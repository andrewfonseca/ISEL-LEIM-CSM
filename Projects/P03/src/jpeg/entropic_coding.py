from numpy import abs, int
from numpy import binary_repr
from numpy import zeros

from .ac import AC
from .dc import DC


class Stream:

    def __init__(self, pretty=False):
        self.__regular_text = ""
        self.__pretty_text = ""
        self.__enable_pretty = pretty

    @property
    def regular(self):
        return self.__regular_text

    @property
    def pretty(self):
        return self.__pretty_text

    def join(self, stream):
        self.__regular_text = "{}{}".format(
            self.__regular_text,
            stream.regular
        )

        if not self.__enable_pretty:
            return self

        self.__pretty_text = "{this}{space}{new}".format(
            this=self.__pretty_text,
            space=" " if self.__pretty_text != "" else "",
            new=stream.pretty
        )

        return self

    def add(self, size_bits: str, signal_bits: str, amplitude_bits: str):
        if amplitude_bits == "0":
            self.__regular_text = "{stream}{size}".format(
                stream=self.__regular_text,
                size=size_bits
            )
        else:
            self.__regular_text = "{stream}{size}{signal}{amplitude}".format(
                stream=self.__regular_text,
                size=size_bits,
                signal=signal_bits,
                amplitude=amplitude_bits
            )

        if not self.__enable_pretty:
            return

        if amplitude_bits == "0":
            self.__pretty_text = "{stream}{space}{size}".format(
                stream=self.__pretty_text,
                space=" " if self.__pretty_text != "" else "",
                size=size_bits
            )
        else:
            self.__pretty_text = "{stream}{space}{size} {signal} {amplitude}".format(
                stream=self.__pretty_text,
                space=" " if self.__pretty_text != "" else "",
                size=size_bits,
                signal=signal_bits,
                amplitude=amplitude_bits
            )

    def add_prefix(self, prefix):
        self.__regular_text = "{prefix}{stream}".format(
            prefix=prefix,
            stream=self.__regular_text
        )

        if not self.__enable_pretty:
            return

        self.__pretty_text = "{prefix}{space}{stream}".format(
            prefix=prefix,
            space=" " if self.__pretty_text != "" else "",
            stream=self.__pretty_text
        )

    def add_suffix(self, suffix: str):
        self.__regular_text = "{stream}{suffix}".format(
            stream=self.__regular_text,
            suffix=suffix
        )

        if not self.__enable_pretty:
            return

        self.__pretty_text = "{stream} {suffix}".format(
            stream=self.__pretty_text,
            suffix=suffix
        )

    def remove(self, size: int):
        self.__regular_text = self.__regular_text[size:]

        if not self.__enable_pretty:
            return

        if self.__pretty_text is None:
            return

        total_spaces = 0

        for c in range(len(self.__pretty_text[0: size + 3])):
            if self.__pretty_text[c] == " ":
                total_spaces += 1

        self.__pretty_text = self.__pretty_text[size + total_spaces:]

    def __str__(self):
        if self.__pretty_text != "":
            return self.__pretty_text

        return self.__regular_text

    def __len__(self):
        return len(self.__regular_text)

    def __getitem__(self, item):
        return self.__regular_text[item]

eob = "1010"

k3 = {
    0: "00",
    1: "010",
    2: "011",
    3: "100",
    4: "101",
    5: "110",
    6: "1110",
    7: "11110",
    8: "111110",
    9: "1111110",
    10: "11111110",
    11: "111111110",
}

k5 = {
    # (0, 0): "1010",
    (0, 1): "00",
    (0, 2): "01",
    (0, 3): "100",
    (0, 4): "1011",
    (0, 5): "11010",
    (0, 6): "1111000",
    (0, 7): "11111000",
    (0, 8): "1111110110",
    (0, 9): "1111111110000010",
    (0, 10): "1111111110000011",
    (1, 1): "1100",
    (1, 2): "11011",
    (1, 3): "1111001",
    (1, 4): "111110110",
    (1, 5): "11111110110",
    (1, 6): "1111111110000100",
    (1, 7): "1111111110000101",
    (1, 8): "1111111110000110",
    (1, 9): "1111111110000111",
    (1, 10): "1111111110001000",
    (2, 1): "11100",
    (2, 2): "11111001",
    (2, 3): "1111110111",
    (2, 4): "111111110100",
    (2, 5): "1111111110001001",
    (2, 6): "1111111110001010",
    (2, 7): "1111111110001011",
    (2, 8): "1111111110001100",
    (2, 9): "1111111110001101",
    (2, 10): "1111111110001110",
    (3, 1): "111010",
    (3, 2): "111110111",
    (3, 3): "111111110101",
    (3, 4): "1111111110001111",
    (3, 5): "1111111110010000",
    (3, 6): "1111111110010001",
    (3, 7): "1111111110010010",
    (3, 8): "1111111110010011",
    (3, 9): "1111111110010100",
    (3, 10): "1111111110010101",
    (4, 1): "111011",
    (4, 2): "1111111000",
    (4, 3): "1111111110010110",
    (4, 4): "1111111110010111",
    (4, 5): "1111111110011000",
    (4, 6): "1111111110011001",
    (4, 7): "1111111110011010",
    (4, 8): "1111111110011011",
    (4, 9): "1111111110011100",
    (4, 10): "1111111110011101",
    (5, 1): "1111010",
    (5, 2): "11111110111",
    (5, 3): "1111111110011110",
    (5, 4): "1111111110011111",
    (5, 5): "1111111110100000",
    (5, 6): "1111111110100001",
    (5, 7): "1111111110100010",
    (5, 8): "1111111110100011",
    (5, 9): "1111111110100100",
    (5, 10): "1111111110100101",
    (6, 1): "1111011",
    (6, 2): "111111110110",
    (6, 3): "1111111110100110",
    (6, 4): "1111111110100111",
    (6, 5): "1111111110101000",
    (6, 6): "1111111110101001",
    (6, 7): "1111111110101010",
    (6, 8): "1111111110101011",
    (6, 9): "1111111110101100",
    (6, 10): "1111111110101101",
    (7, 1): "11111010",
    (7, 2): "111111110111",
    (7, 3): "1111111110101110",
    (7, 4): "1111111110101111",
    (7, 5): "1111111110110000",
    (7, 6): "1111111110110001",
    (7, 7): "1111111110110010",
    (7, 8): "1111111110110011",
    (7, 9): "1111111110110100",
    (7, 10): "1111111110110101",
    (8, 1): "111111000",
    (8, 2): "111111111000000",
    (8, 3): "1111111110110110",
    (8, 4): "1111111110110111",
    (8, 5): "1111111110111000",
    (8, 6): "1111111110111001",
    (8, 7): "1111111110111010",
    (8, 8): "1111111110111011",
    (8, 9): "1111111110111100",
    (8, 10): "1111111110111101",
    (9, 1): "111111001",
    (9, 2): "1111111110111110",
    (9, 3): "1111111110111111",
    (9, 4): "1111111111000000",
    (9, 5): "1111111111000001",
    (9, 6): "1111111111000010",
    (9, 7): "1111111111000011",
    (9, 8): "1111111111000100",
    (9, 9): "1111111111000101",
    (9, 10): "1111111111000110",
    (10, 1): "111111010",
    (10, 2): "1111111111000111",
    (10, 3): "1111111111001000",
    (10, 4): "1111111111001001",
    (10, 5): "1111111111001010",
    (10, 6): "1111111111001011",
    (10, 7): "1111111111001100",
    (10, 8): "1111111111001101",
    (10, 9): "1111111111001110",
    (10, 10): "1111111111001111",
    (11, 1): "1111111001",
    (11, 2): "1111111111010000",
    (11, 3): "1111111111010001",
    (11, 4): "1111111111010010",
    (11, 5): "1111111111010011",
    (11, 6): "1111111111010100",
    (11, 7): "1111111111010101",
    (11, 8): "1111111111010110",
    (11, 9): "1111111111010111",
    (11, 10): "1111111111011000",
    (12, 1): "1111111010",
    (12, 2): "1111111111011001",
    (12, 3): "1111111111011010",
    (12, 4): "1111111111011011",
    (12, 5): "1111111111011100",
    (12, 6): "1111111111011101",
    (12, 7): "1111111111011110",
    (12, 8): "1111111111011111",
    (12, 9): "1111111111100000",
    (12, 10): "1111111111100001",
    (13, 1): "11111111000",
    (13, 2): "1111111111100010",
    (13, 3): "1111111111100011",
    (13, 4): "1111111111100100",
    (13, 5): "1111111111100101",
    (13, 6): "1111111111100110",
    (13, 7): "1111111111100111",
    (13, 8): "1111111111101000",
    (13, 9): "1111111111101001",
    (13, 10): "1111111111101010",
    (14, 1): "1111111111101011",
    (14, 2): "1111111111101100",
    (14, 3): "1111111111101101",
    (14, 4): "1111111111101110",
    (14, 5): "1111111111101111",
    (14, 6): "1111111111110000",
    (14, 7): "1111111111110001",
    (14, 8): "1111111111110010",
    (14, 9): "1111111111110011",
    (14, 10): "1111111111110100",
    (15, 0): "11111111001",
    (15, 1): "1111111111110101",
    (15, 2): "1111111111110110",
    (15, 3): "1111111111110111",
    (15, 4): "1111111111111000",
    (15, 5): "1111111111111001",
    (15, 6): "1111111111111010",
    (15, 7): "1111111111111011",
    (15, 8): "1111111111111100",
    (15, 9): "1111111111111101",
    (15, 10): "1111111111111110",
    # Extra keys
    (16, 1): "b0000000000000001",
    (17, 1): "b0000000000000010",
    (18, 1): "b0000000000000011",
    (19, 1): "b0000000000000100",
    (20, 1): "b0000000000000101",
    (21, 1): "b0000000000000110",
    (22, 1): "b0000000000000111",
    (23, 1): "b0000000000001000",
    (24, 1): "b0000000000001001",

}


def generate_signal_bits(amplitude: int) -> str:
    return "1" if amplitude < 0 else "0"


def generate_signal(bit: str) -> int:
    return 1 if bit == "0" else -1


def generate_amplitude_bits(amplitude: int) -> str:
    return binary_repr(abs(amplitude))


def encode(dc: DC, ac: AC) -> Stream:
    stream = Stream()

    # DC stream
    size_bits = k3.get(dc.size)
    signal_bits = generate_signal_bits(dc.amplitude)
    amplitude_bits = generate_amplitude_bits(dc.amplitude)

    stream.add(size_bits, signal_bits, amplitude_bits)

    # AC stream
    amplitudes = ac.amplitudes
    zrls = ac.zero_run_lengths
    sizes = ac.sizes

    for i in range(len(amplitudes)):

        if zrls[i] > 15:
            n_zeros = zrls[i]
            while n_zeros > 0:
                if n_zeros > 15:
                    size_bits = k5.get((15, 0))
                    signal_bits = generate_signal_bits(0)
                    amplitude_bits = generate_amplitude_bits(0)
                else:
                    size_bits = k5.get((n_zeros, sizes[i]))
                    signal_bits = generate_signal_bits(amplitudes[i])
                    amplitude_bits = generate_amplitude_bits(amplitudes[i])

                stream.add(size_bits, signal_bits, amplitude_bits)
                n_zeros -= 15
        else:
            size_bits = k5.get((zrls[i], sizes[i]))
            if size_bits is None:
                size_bits = k5.get((0, 1))
            signal_bits = generate_signal_bits(amplitudes[i])
            amplitude_bits = generate_amplitude_bits(amplitudes[i])

            stream.add(size_bits, signal_bits, amplitude_bits)

    # EOB stream
    stream.add_suffix(eob)

    return stream


def decode(stream: Stream, total_elements: int) -> (DC, AC, Stream):
    dc = None
    ac = None

    i = 0

    # DC stream
    while i < len(stream) and dc is None:
        i += 1

        for k in k3:
            if stream[0: i] != k3.get(k):
                continue

            size = k
            amplitude = 0

            if size > 0:
                signal = generate_signal(stream[i: i + 1])
                i += 1
                amplitude = int(stream[i: i + size], 2) * signal

            dc = DC(amplitude, size)
            stream.remove(i + size)
            break

    # AC stream
    zrls = zeros(total_elements, dtype=int)
    amplitudes = zeros(total_elements, dtype=int)
    i = 0
    j = 0

    while stream[0: i] != eob:
        i += 1

        for k in k5:
            if stream[0: i] != k5.get(k):
                continue

            zrls[j], size = k[0], k[1]

            if size > 0:
                signal = generate_signal(stream[i: i + 1])
                i += 1
                amplitudes[j] = int(stream[i: i + size], 2) * signal

            stream.remove(i + size)
            j += 1
            i = 0
            break

    idx = amplitudes != 0
    amplitudes = amplitudes[idx]
    zrls = zrls[idx]

    ac = AC(zrls, amplitudes)

    # EOB stream
    stream.remove(len(eob))

    return dc, ac, stream

