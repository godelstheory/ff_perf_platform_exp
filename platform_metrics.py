import mozanalysis.metrics.desktop as mmd
import mozanalysis.metrics as met
from platform_data_source import devtools_engage_main

from utils import extract_keyed_sum

# Memory
memory_total = met.Metric(
    name='memory_total',
    data_source=mmd.main,
    select_expr=met.agg_histogram_mean('payload.histograms.memory_total')
)

# GC
gc_max_pause_ms_2 = met.Metric(
    name='gc_max_pause_ms_2',
    data_source=mmd.main,
    select_expr=met.agg_histogram_mean('payload.histograms.gc_max_pause_ms_2')
)

