from models.WavePattern import WavePattern

class WaveCycle:
    """
    One Cycle of 12345 -> ABC
    """
    def __init__(self, wavepattern_up: WavePattern, wavepattern_down: WavePattern):
        self.wp_up = wavepattern_up
        self.wp_down = wavepattern_down
        self.degree = self.wp_up.degree
        self.waves = list()
        self.extract_waves()

    @property
    def end_idx(self):
        return self.wp_down.end_idx

    @property
    def start_idx(self):
        return self.wp_up.start_idx

    def extract_waves(self):
        for key, wave in self.wp_up.waves.items():
            self.waves.append(wave)

        for key, wave in self.wp_down.waves.items():
            self.waves.append(wave)

    @property
    def dates(self):
        dates = self.wp_up.dates
        dates.extend(self.wp_down.dates)
        return dates

    @property
    def values(self):
        values = self.wp_up.values
        values.extend(self.wp_down.values)
        return values

    @property
    def labels(self):
        labels = self.wp_up.labels
        labels.extend(self.wp_down.labels)
        return labels

    # @classmethod
    # def from_wave_options(cls, df: pd.DataFrame, waveoptions_up: WaveOptions, waveoptions_down: WaveOptions):
    #     idx_start = np.argmin(np.array(list(df['Low'])))
    #
    #     wa = WaveAnalyzer(df=df, verbose=True)
    #
    #     waves_up = wa.find_impulsive_wave(idx_start=idx_start, wave_config=waveoptions_up.values)
    #     wave_pattern_up = WavePattern(waves_up)
    #     waves_down = wa.find_corrective_wave(idx_start=waves_up[4].idx_end, wave_config=waveoptions_down.values)
    #     wave_pattern_down = WavePattern(waves_down)
    #
    #     return cls(wave_pattern_up, wave_pattern_down)

    def __eq__(self, other):
        if self.wp_down.values == other.wp_down.values and self.wp_up.values == other.wp_up.values:
            return True
        else:
            return False

    def __hash__(self):
        str_to_hash = f'{self.wp_up.values}_{self.wp_down.values}'
        return hash(str_to_hash)
