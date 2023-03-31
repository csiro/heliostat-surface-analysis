from abc import ABC, abstractmethod

import numpy as np


class Aggregator(ABC):
    @abstractmethod
    def aggregate(self, values: np.ndarray) -> float:
        pass


class WeightedAggregator(Aggregator):
    def __init__(self, weights: np.ndarray):
        self.weights = weights


class SumAggregator(Aggregator):
    def aggregate(self, values: np.ndarray) -> float:
        return np.sum(values)


class SquaredSumAggregator(Aggregator):
    def aggregate(self, values: np.ndarray) -> float:
        return np.sum(np.square(values))


class MeanAggregator(Aggregator):
    def aggregate(self, values: np.ndarray) -> float:
        return np.sum(values) / len(values)


class RMSAggregator(Aggregator):
    def aggregate(self, values: np.ndarray) -> float:
        square = np.square(values)
        mean_square = np.sum(square) / len(square)
        return np.sqrt(mean_square)


class ModeAggregator(Aggregator):
    def aggregate(self, values: np.ndarray) -> float:
        mini = 0
        maxi = 0.01
        increment = 2e-4
        bins = round((maxi - mini) / increment)

        counts, bin_edges = np.histogram(
            values,
            bins=bins,
            range=(mini, maxi)    
        )

        index_of_max = counts.argmax()
        return (bin_edges[index_of_max] + bin_edges[index_of_max + 1]) / 2


class WeightedSumAggregator(WeightedAggregator):
    def aggregate(self, values: np.ndarray) -> float:
        return np.sum(values * self.weights)


class WeightedSquaredSumAggregator(WeightedAggregator):
    def aggregate(self, values: np.ndarray) -> float:
        return np.sum(np.square(values) * self.weights)


class WeightedMeanAggregator(WeightedAggregator):
    def aggregate(self, values: np.ndarray) -> float:
        weighted_values = values * self.weights
        return np.sum(weighted_values) / np.sum(self.weights)


class WeightedRMSAggregator(WeightedAggregator):
    def aggregate(self, values: np.ndarray) -> float:
        weighted_squared_values = np.square(values) * self.weights
        mean_square = np.sum(weighted_squared_values) / np.sum(self.weights)
        return np.sqrt(mean_square)


class WeightedModeAggregator(WeightedAggregator):
    def aggregate(self, values: np.ndarray) -> float:
        mini = 0
        maxi = 0.01
        increment = 1e-4
        bins = round((maxi - mini) / increment)

        counts, bin_edges = np.histogram(
            values,
            bins=bins,
            range=(mini, maxi),
            weights=self.weights
        )

        index_of_max = counts.argmax()
        return (bin_edges[index_of_max] + bin_edges[index_of_max + 1]) / 2
