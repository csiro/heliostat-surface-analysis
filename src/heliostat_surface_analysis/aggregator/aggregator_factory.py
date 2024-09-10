from heliostat_surface_analysis.config.aggregator_option import AggregatorOption
from heliostat_surface_analysis.config.aggregator_option import AggregatorOptionName
from heliostat_surface_analysis.aggregator import aggregator

class AggregatorFactory:
    @classmethod
    def get_aggregator(cls, option: AggregatorOption):
        if option.name == AggregatorOptionName.sum:
            return aggregator.SumAggregator()
        elif option.name == AggregatorOptionName.squared_sum:
            return aggregator.SquaredSumAggregator()
        elif option.name == AggregatorOptionName.mean:
            return aggregator.MeanAggregator()
        elif option.name == AggregatorOptionName.rms:
            return aggregator.RMSAggregator()
        elif option.name == AggregatorOptionName.mode:
            return aggregator.ModeAggregator()
        elif option.name == AggregatorOptionName.mle:
            return aggregator.MLEAggregator()
        elif option.name == AggregatorOptionName.weighted_sum:
            return aggregator.WeightedSumAggregator()
        elif option.name == AggregatorOptionName.weighted_squared_sum:
            return aggregator.WeightedSquaredSumAggregator()
        elif option.name == AggregatorOptionName.weighted_mean:
            return aggregator.WeightedMeanAggregator()
        elif option.name == AggregatorOptionName.weighted_rms:
            return aggregator.WeightedRMSAggregator()
        elif option.name == AggregatorOptionName.weighted_mode:
            return aggregator.WeightedModeAggregator()
        elif option.name == AggregatorOptionName.weighted_mle:
            return aggregator.WeightedMLEAggregator()
        else:
            raise RuntimeError("aggregator not recognised")
