from abc import ABC, abstractmethod

class WaveOptions:
    """
    WaveOptions are a list of integers denoting the number of intermediate min / maxima should be skipped while
    finding a MonoWave.

    E.g. [1,0,0,0,0] will skip the first found maxima for the first MonoWaveUp.

    """
    def __init__(self, i: int, j: int = None, k: int = None, l: int = None, m: int = None):
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.m = m

    def __repr__(self):
        return f'[{self.i}, {self.j}, {self.k}, {self.l}, {self.m}]'

    @property
    def values(self):
        if self.k is not None:
            return [self.i, self.j, self.k, self.l, self.m]
        else:
            return [self.i, self.j]

    def __hash__(self):
        if self.k is not None:
            hash_str = f'{self.i}_{self.j}_{self.k}_{self.l}_{self.m}'
        else:
            hash_str = f'{self.i}_{self.j}'
        return hash(hash_str)

    def __eq__(self, other):
        if self.k is not None:
            if self.i == other.i and self.j == other.j and self.k == other.k and self.l == other.l and self.m == other.m:
                return True
            else:
                return False
        else:
            if self.i == other.i and self.j == other.j:
                return True
            else:
                return False

    def __lt__(self, other):
        """
        implementation of a ranking of WaveOptions. [1,0,0,0,0] should be larger than [0,0,0,0,0] and [1,2,0,0,0] should
        be larger than [1,1,0,0,0] etc.

        As the sets in the Generators are not sorted, the implementation helps to sort the WaveOptions and go from
        smallest / shortest waves, e.g. [0,0,0,0,0] to larger ones

        :param other:
        :return:
        """
        # WaveOption has [i, j, k, l, m]

        if self.i < other.i:
            return True

        elif self.i == other.i:

            if self.j < other.j:
                return True

            elif self.j == other.j:

                if self.k == other.k:
                    if self.l < other.l:
                        return True
                    elif self.l == other.l:
                        if self.m < other.m:
                            return True
                        else:
                            return False
                    else:
                        return False

                elif self.k < other.k:
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False


class WaveOptionsGenerator(ABC):
    def __init__(self, up_to: int):
        self.__up_to = up_to
        self.options = self.populate()

    @property
    def up_to(self):
        return self.__up_to

    @property
    def number(self):
        return len(self.options)

    @abstractmethod
    def populate(self) -> set:
        pass

    @property
    def options_sorted(self):
        """
        Will sort from small to large values [0,0,0,0,0] -> [n, n, n, n, n]
        :return:
        """
        all_options = list(self.options)
        return sorted(all_options)


class WaveOptionsGenerator5(WaveOptionsGenerator):
    """
    WaveOptionsGenerator for impulsive 12345 movements

    """
    def populate(self) -> set:
        checked = set()

        for i in range(0, self.up_to):
            for j in range(0, self.up_to):
                for k in range(0, self.up_to):
                    for l in range(0, self.up_to):
                        for m in range(0, self.up_to):

                            if i == 0:
                                j = k = l = m = 0
                            if j == 0:
                                k = l = m = 0
                            if k == 0:
                                l = m = 0
                            if l == 0:
                                m = 0
                            wave_options = WaveOptions(i, j, k, l, m)
                            checked.add(wave_options)
        return checked


class WaveOptionsGenerator2(WaveOptionsGenerator):
    """
    WaveOptions for 12 Waves
    """
    def populate(self) -> set:
        checked = list

        for i in range(0, self.up_to):
            for j in range(0, self.up_to):
                if i == 0:
                    j = 0

                wave_options = WaveOptions(i, j, None, None, None)
                checked.append(wave_options)
        return checked


class WaveOptionsGenerator3(WaveOptionsGenerator):
    """
    WaveOptions for corrective (ABC) like movements
    """
    def populate(self) -> set:
        checked = set()

        for i in range(0, self.up_to):
            for j in range(0, self.up_to):
                for k in range(0, self.up_to):
                    if i == 0:
                        j = k = 0
                    if j == 0:
                        k = 0

                    wave_options = WaveOptions(i, j, k, None, None)
                    checked.add(wave_options)
        return checked
