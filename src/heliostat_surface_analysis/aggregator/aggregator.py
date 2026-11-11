from abc import ABC, abstractmethod

import numpy as np


class Aggregator(ABC):
    @abstractmethod
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        pass


class SumAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        return np.sum(values)


class SquaredSumAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        return np.sum(np.square(values))


class MeanAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        return np.sum(values) / len(values)


class RMSAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        square = np.square(values)
        mean_square = np.sum(square) / len(square)
        return np.sqrt(mean_square)


class ModeAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        mini = 0
        maxi = values.max()*1.001
        bins = 100

        counts, bin_edges = np.histogram(
            values,
            bins=bins,
            range=(mini, maxi)
        )

        index_of_max = counts.argmax()
        return (bin_edges[index_of_max] + bin_edges[index_of_max + 1]) / 2


class MLEAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        square = np.square(values)
        mean_square = np.sum(square) / len(square)
        return np.sqrt(mean_square/2)


class WeightedSumAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        return np.sum(values * weights)


class WeightedSquaredSumAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        return np.sum(np.square(values) * weights)


class WeightedMeanAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        weighted_values = values * weights
        return np.sum(weighted_values) / np.sum(weights)


class WeightedRMSAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        weighted_squared_values = np.square(values) * weights
        mean_square = np.sum(weighted_squared_values) / np.sum(weights)
        return np.sqrt(mean_square)


class WeightedModeAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        mini = 0
        maxi = 0.01
        increment = 1e-4
        bins = round((maxi - mini) / increment)

        counts, bin_edges = np.histogram(
            values,
            bins=bins,
            range=(mini, maxi),
            weights=weights
        )

        index_of_max = counts.argmax()
        return (bin_edges[index_of_max] + bin_edges[index_of_max + 1]) / 2


class WeightedMLEAggregator(Aggregator):
    def aggregate(self, values: np.ndarray, weights: np.ndarray) -> float:
        weighted_squared_values = np.square(values) * weights
        mean_square = np.sum(weighted_squared_values) / np.sum(weights)
        return np.sqrt(mean_square/2)
