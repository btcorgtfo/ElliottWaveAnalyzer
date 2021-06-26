from models.WaveRules import WaveRule
from models.MonoWave import MonoWaveUp, MonoWaveDown


class WavePattern:
    """
    Class to build a wave pattern from consecutive MonoWaves, e.g. 5 for an impulse and 3 for a correction
    """
    def __init__(self, waves: list, wave_options: list = None, verbose: bool = False):
        self.__waves = waves
        self.__verobse = verbose
        self.degree = waves[0].degree
        self.type = str  # impulse, correction, zigzag etc
        self.wave_options = wave_options

        __waves_dict = dict()
        for i, wave in enumerate(self.__waves):
            #TODO if len waves = 3 -> map 1 - a etc

            key = f'wave{i+1}'
            __waves_dict.setdefault(key, wave)

        self.waves = __waves_dict

    def check_rule(self, waverule: WaveRule) -> bool:
        """
        Checks if WaveRule is valid for the WavePattern

        :param waverule:
        :return: True if all WaveRules are fullfilled, False otherwise

        """
        for rule, conditions in waverule.conditions.items():

            no_of_waves = len(conditions.get('waves'))
            function = conditions.get('function')
            message = conditions.get('message')

            if no_of_waves == 2:
                wave1 = self.waves.get(conditions.get('waves')[0])
                wave2 = self.waves.get(conditions.get('waves')[1])
                if not function(wave1, wave2):
                    if self.__verobse:
                        print(f'Rule Violation of {waverule.name} for condition {rule}: {message}')
                    return False

            elif no_of_waves == 3:
                wave1 = self.waves.get(conditions.get('waves')[0])
                wave2 = self.waves.get(conditions.get('waves')[1])
                wave3 = self.waves.get(conditions.get('waves')[2])

                if not function(wave1, wave2, wave3):
                    if self.__verobse:
                        print(f'Rule Violation of {waverule.name} for condition {rule}: {message}')
                    return False

            elif no_of_waves == 4:
                wave1 = self.waves.get(conditions.get('waves')[0])
                wave2 = self.waves.get(conditions.get('waves')[1])
                wave3 = self.waves.get(conditions.get('waves')[2])
                wave4 = self.waves.get(conditions.get('waves')[3])

                if not function(wave1, wave2, wave3, wave4):
                    if self.__verobse:
                        print(f'Rule Violation of {waverule.name} for condition {rule}: {message}')
                    return False

            else:
                raise NotImplementedError('other than 2 or 3 waves as argument not implemented')

        return True

    @property
    def low(self) -> float:
        return self.__waves[0].low

    @property
    def high(self) -> float:
        return self.__waves[-1].high

    @property
    def idx_start(self) -> int:
        return self.waves.get('wave1').idx_start

    @property
    def idx_end(self) -> int:
        if 'wave5' in self.waves.keys():
            return self.waves.get('wave5').idx_end
        else:
            return self.waves.get('wave3').idx_end

    @property
    def dates(self):
        dates = list()
        for wave_no, wave in self.waves.items():
            dates.extend(wave.dates)

        return dates

    @property
    def values(self):
        values = list()
        for wave_no, wave in self.waves.items():
            if isinstance(wave, MonoWaveUp):
                values.extend([wave.low, wave.high])
            elif isinstance(wave, MonoWaveDown):
                values.extend([wave.high, wave.low])
            else:
                raise NotImplementedError()

        return values

    @property
    def labels(self) -> list:
        """
        Labels 12345 for impulse and ABC for correction to be placed at the end of the waves in the plots.

        :return:
        """
        labels = list()
        reference_length = next(iter(self.waves.items()))[1].length

        for wave_no, wave in self.waves.items():
            if wave.label in ['B', '2', '3']:
                labels.extend([" ", f'{wave.label} ({round(wave.length/reference_length, 3)})'])
            else:
                labels.extend([" ", f'{wave.label}'])
        return labels

    def __eq__(self, other):
        if all([self.waves[key].low == other.waves[key].low and self.waves[key].high == other.waves[key].high for key, value in self.waves.items()]):
            return True
        else:
            return False

    def __hash__(self):
        hash_str = f'{self.low}{self.high}'
        return hash(hash_str)
