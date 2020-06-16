from mozanalysis.metrics import Metric, agg_sum
from platform_data_source import devtools_engage_main
from utils import extract_keyed_sum

# Devtools
devtools_keys = ('inspector', 'webconsole', 'jsdebugger', 'styleeditor', 'performance',
                 'memory', 'netmonitor', 'storage', 'dom')
devtools_probes = ('devtools_cold_toolbox_open_delay_ms', 'devtools_warm_toolbox_open_delay_ms',
                   'devtools_toolbox_page_reload_delay_ms')

devtools_perf_metrics = {'{}_{}'.format(probe, x): Metric(
      name='{}_{}'.format(probe, x),
      # data_source=mmd.main,
      data_source=devtools_engage_main,
      select_expr=agg_sum(extract_keyed_sum('payload.keyed_histograms.{}'.format(probe), x))
      ) for x in devtools_keys for probe in devtools_probes}

