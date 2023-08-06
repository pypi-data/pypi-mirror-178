from dataclasses import dataclass
from typing import Type

from . import BaseAnomaly, AnomalyProtocol
from ...utils.base_oscillation_kind import BaseOscillationKind


@dataclass
class AnomalyFrequencyParameters:
    frequency_factor: float = 1.0


class AnomalyFrequency(BaseAnomaly):
    def __init__(self, parameters: AnomalyFrequencyParameters):
        super().__init__()
        self.frequency_factor = parameters.frequency_factor

    def generate(self, anomaly_protocol: AnomalyProtocol) -> AnomalyProtocol:
        if anomaly_protocol.base_oscillation_kind == BaseOscillationKind.Sine:
            sine = anomaly_protocol.base_oscillation
            length = anomaly_protocol.end - anomaly_protocol.start
            subsequence = sine.generate_only_base(anomaly_protocol.ctx.to_bo(), length, sine.frequency * self.frequency_factor, freq_mod=sine.freq_mod)
            anomaly_protocol.subsequences.append(subsequence)
        elif anomaly_protocol.base_oscillation_kind == BaseOscillationKind.ECG:
            ecg = anomaly_protocol.base_oscillation
            subsequence = ecg.generate_only_base(anomaly_protocol.ctx.to_bo(), frequency=ecg.frequency * self.frequency_factor)[anomaly_protocol.start:anomaly_protocol.end]
            anomaly_protocol.subsequences.append(subsequence)
        else:
            self.logger.warn_false_combination(self.__class__.__name__, anomaly_protocol.base_oscillation_kind.name)
        return anomaly_protocol

    @property
    def requires_period_start_position(self) -> bool:
        return True

    @staticmethod
    def get_parameter_class() -> Type[AnomalyFrequencyParameters]:
        return AnomalyFrequencyParameters
