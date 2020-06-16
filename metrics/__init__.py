import mozanalysis.metrics.desktop as mmd
import mozanalysis.metrics as met

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

