# https://adventofcode.com/2021/day/16

from functools import reduce

FILE = 'input.txt'
# FILE = 'input-small.txt'


class Packet:
    def __init__(self, version: int, type: int, literal_value: int = None, subpackets=None):
        if subpackets is None:
            subpackets = []

        self.version = version
        self.type = type
        self.literal_value = literal_value
        self.subpackets = subpackets

    def __str__(self):
        return "<<{}, {}, {}, {}>>".format(self.version, self.type, self.literal_value, self.subpackets)

    def __repr__(self):
        return self.__str__()

    def version_sum(self):
        return self.version + sum([p.version_sum() for p in self.subpackets])

    def _subpacket_values(self) -> list:
        return [p.value() for p in self.subpackets]

    def value(self):
        if self.type == 0:
            return sum(self._subpacket_values())
        elif self.type == 1:
            return reduce(lambda x, y: x * y, self._subpacket_values())
        elif self.type == 2:
            return min(self._subpacket_values())
        elif self.type == 3:
            return max(self._subpacket_values())
        elif self.type == 4:
            return self.literal_value
        elif self.type == 5:
            values = self._subpacket_values()
            return int(values[0] > values[1])
        elif self.type == 6:
            values = self._subpacket_values()
            return int(values[0] < values[1])
        elif self.type == 7:
            values = self._subpacket_values()
            return int(values[0] == values[1])

        # Should not happen
        assert False

    @staticmethod
    def parse(binary: str) -> ('Packet', str):
        if len(binary) < 6:
            # No header, no packet
            return None, binary

        version = int(binary[0:3], 2)
        type = int(binary[3:6], 2)

        if type == 4:
            # literal value
            binary_value = ''
            i = 6
            has_next = True
            while has_next:
                if binary[i] == '0':
                    has_next = False
                binary_value += binary[i + 1:i + 5]
                i += 5
            return Packet(version, type, literal_value=int(binary_value, 2)), binary[i:]
        else:
            # operator
            if binary[6] == '0':
                # operator with known length of subpackets bits
                length = int(binary[7: 7+15], 2)
                subpackets = []
                subpackets_binary = binary[22:22 + length]
                while True:
                    subpacket, subpackets_binary = Packet.parse(subpackets_binary)
                    if subpacket is None:
                        break
                    subpackets.append(subpacket)

                return Packet(version, type, subpackets=subpackets), binary[22 + length:]
            else:
                # operator with known number of subpackets
                number_of_subpackets = int(binary[7: 18], 2)
                subpackets = []
                subpackets_binary = binary[18:]
                for _ in range(number_of_subpackets):
                    subpacket, subpackets_binary = Packet.parse(subpackets_binary)
                    subpackets.append(subpacket)

                return Packet(version, type, subpackets=subpackets), subpackets_binary


with open(FILE) as f:
    for line in f.readlines():  # Allow multiple inputs for easier debugging
        line = line.strip()
        binary = (bin(int(line, 16))[2:]).zfill(len(line) * 4)  # Convert to binary and don't loose leading 0
        # print(line)
        # print(binary)

        main_packet, _ = Packet.parse(binary)
        # print(main_packet)
        print(main_packet.version_sum())  # 1. part
        print(main_packet.value())        # 2. part

