import pandas as pd
from ..utils.global_variables import BASE_OSCILLATION_NAMES, ANOMALY_TYPE_NAMES


class Compatibility:
    combinations = pd.DataFrame(
        [
            [1, 1, 1, 1, 0, 0, 0],  # amplitude
            [1, 1, 1, 1, 1, 0, 1],  # extremum
            [1, 0, 0, 1, 0, 0, 0],  # frequency
            [1, 1, 1, 1, 1, 0, 1],  # mean
            [1, 0, 1, 1, 0, 0, 0],  # pattern
            [1, 0, 0, 1, 0, 0, 0],  # pattern_shift
            [1, 1, 1, 1, 1, 0, 1],  # platform
            [1, 1, 1, 1, 1, 0, 1],  # trend
            [1, 1, 1, 1, 1, 0, 1],  # variance
            [0, 0, 0, 0, 0, 1, 0],  # mode_correlation
        ],
        columns=[BASE_OSCILLATION_NAMES.SINE, BASE_OSCILLATION_NAMES.RANDOM_WALK, BASE_OSCILLATION_NAMES.CYLINDER_BELL_FUNNEL,
                 BASE_OSCILLATION_NAMES.ECG, BASE_OSCILLATION_NAMES.POLYNOMIAL, BASE_OSCILLATION_NAMES.RANDOM_MODE_JUMP,
                 BASE_OSCILLATION_NAMES.FORMULA],
        index=[ANOMALY_TYPE_NAMES.AMPLITUDE, ANOMALY_TYPE_NAMES.EXTREMUM, ANOMALY_TYPE_NAMES.FREQUENCY, ANOMALY_TYPE_NAMES.MEAN,
               ANOMALY_TYPE_NAMES.PATTERN, ANOMALY_TYPE_NAMES.PATTERN_SHIFT, ANOMALY_TYPE_NAMES.PLATFORM, ANOMALY_TYPE_NAMES.TREND,
               ANOMALY_TYPE_NAMES.VARIANCE, ANOMALY_TYPE_NAMES.MODE_CORRELATION],
        dtype=bool
    )

    @staticmethod
    def check(anomaly: str, base_oscillation: str) -> bool:
        return Compatibility.combinations.loc[anomaly, base_oscillation]
