from typing import Callable

import numpy as np


def create_sum_aggregator() -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values):
        return np.sum(values)

    return aggregator


def create_weighted_sum_aggregator(
    weights: np.ndarray,
) -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values: np.ndarray):
        weighted_values = values * weights
        return np.sum(weighted_values)

    return aggregator


def create_squared_sum_aggregator() -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values):
        return np.sum(np.square(values))

    return aggregator


def create_weighted_squared_sum_aggregator(
    weights: np.ndarray,
) -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values: np.ndarray):
        return np.sum(np.square(values) * weights)

    return aggregator


def create_mean_aggregator() -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values):
        return np.sum(values) / len(values)

    return aggregator


def create_weighted_mean_aggregator(
    weights: np.ndarray,
) -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values: np.ndarray):
        weighted_values = values * weights
        return np.sum(weighted_values) / np.sum(weights)

    return aggregator


def create_rms_aggregator() -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values):
        square = np.square(values)
        mean_square = np.sum(square) / len(square)
        return np.sqrt(mean_square)

    return aggregator


def create_weighted_rms_aggregator(
    weights: np.ndarray,
) -> Callable[[np.ndarray], np.ndarray]:
    def aggregator(values: np.ndarray):
        weighted_squared_values = np.square(values) * weights
        mean_square = np.sum(weighted_squared_values) / np.sum(weights)
        return np.sqrt(mean_square)

    return aggregator
