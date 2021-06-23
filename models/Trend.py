class Trend:
    def __init__(self):
        self.wave_cycles = set()
        self.waves = set()

    def add_wave(self, wave):
        self.waves.add(wave)

    def add_wavecycle(self, wave_cycle):
        self.wave_cycles.add(wave_cycle)

    def get_wave_by_degree(self, degree: int):
        pass

    def plot(self):
        pass

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass


