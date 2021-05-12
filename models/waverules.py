from __future__ import annotations
from abc import ABC, abstractmethod


class WaveRule(ABC):
    def __init__(self, name: str):
        self.name = name
        self.conditions = self.set_conditions()

    @abstractmethod
    def set_conditions(self):
        pass

    def __repr__(self):
        return str(self.conditions)


class Impulse(WaveRule):
    """
    Das Ende der zweiten Welle kommt nie über den Anfang der ersten Welle;
    Die dritte Welle erstreckt sich immer jenseits der Spitze der ersten Welle;
    Das Ende der vierten Welle kommt nie über nie die Spitze der ersten Welle;
    Die dritte Welle ist niemals die kürzeste aller agierenden Wellen;

    Die dritte Welle ist immer ein Impuls;
    Die erste Welle ist entweder ein Impuls oder eine führende Diagonale;
    Die fünfte Welle kann entweder ein Impuls oder eine Diagonale sein;
    Die zweite Welle könnte die Form jeder Korrekturwelle annehmen, jedoch nie zu einem Dreieck werden;
    Die vierte Welle könnte die Form jeder Korrekturwelle annehmen.

    """
    def set_conditions(self):
        # conditon returns TRUE -> no exit
        conditions = {# WAVE 2
                      'w2_1': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: wave2.low > wave1.low,
                             'message': 'End of Wave2 is lower than Start of Wave1.'},

                      'w2_2': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: wave2.length >= 0.2 * wave1.length,
                             'message': 'Wave2 is shorten than 20% of Wave1.'},

                      'w2_3': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: 9 * wave2.duration > wave1.duration,
                             'message': 'Wave2 is longer than 9x Wave1'},

                      # WAVE 3
                      'w3_1': {'waves': ['wave1', 'wave3', 'wave5'],
                             'function': lambda wave1, wave3, wave5: not (
                                       wave3.length < wave5.length and wave3.length < wave1.length),
                             'message': 'Wave3 is the shortest Wave.'},

                      'w3_2': {'waves': ['wave1', 'wave3'],
                             'function': lambda wave1, wave3: wave3.high > wave1.high,
                             'message': 'End of Wave3 is lower than End of Wave1'},

                      'w3_3': {'waves': ['wave1', 'wave3'],
                             'function': lambda wave1, wave3: wave3.length >= wave1.length / 3.,
                             'message': 'Wave3 is shorter than 1/3 of Wave1'},

                      'w3_4': {'waves': ['wave2', 'wave3'],
                             'function': lambda wave2, wave3: wave3.length > wave2.length,
                             'message': 'Wave3 shorter than Wave2'},

                      'w3_5': {'waves': ['wave1', 'wave3'],
                            'function': lambda wave1, wave3: 7 * wave3.duration > wave1.duration,
                            'message': 'Wave3 more than 7 times longer than Wave1.'},

                      # WAVE 4
                      'w4_1': {'waves': ['wave1', 'wave4'],
                             'function': lambda wave1, wave4: wave4.low > wave1.high,
                             'message': 'End of Wave4 is lower than End of Wave1'},

                      # WAVE 5
                      'w5_1': {'waves': ['wave3', 'wave5'],
                               'function': lambda wave3, wave5: wave3.high < wave5.high,
                               'message': 'End of Wave5 is lower than End of Wave3'},
                      }

        return conditions


class TDWave(WaveRule):
    def set_conditions(self):
        # conditon returns TRUE -> no exit
        conditions = {# WAVE 2
                      'w2_1': {'waves': ['wave1', 'wave2'],
                             'function': lambda wave1, wave2: wave2.length > wave1.length * 0.59,
                             'message': 'End of Wave2 corrected less  50% of Wave1.'},

                        'w2_2': {'waves': ['wave1', 'wave2'],
                         'function': lambda wave1, wave2: wave2.length < wave1.length * 0.64,
                         'message': 'End of Wave2 corrected more than 65% of Wave1.'},

                        'w2_3': {'waves': ['wave1', 'wave2'],
                         'function': lambda wave1, wave2: 9 * wave2.duration > wave1.duration,
                         'message': 'Wave2 is longer than 9x Wave1'},
        }

        return conditions