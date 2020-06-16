from platform_data_source import desktop_startup_main
from mozanalysis.metrics import Metric

agg_median = '''
(approx_quantiles({}, 2 IGNORE NULLS)[offset(1)])
'''.format
count_nonnull = 'countif({} is not null)'.format
min_ = 'min({})'.format
max_ = 'max({})'.format
sum_ = 'sum({})'.format


def metric(field, name=None, agg_func=agg_median, default=0):
    name = name or field
    if default is None:
        expr = agg_func(f"{field}")
    else:
        expr = agg_func(f"""
        coalesce({field}, {default})
        """)
    return Metric(
        name=name,
        data_source=desktop_startup_main,
        select_expr=expr
    )


startup_metrics = [
    metric('select_profile_all', agg_func=agg_median),

    # cold metrics
    metric('c_first_paint', agg_func=agg_median),
    metric('c_delayed_st_st', agg_func=agg_median),
    metric('c_select_profile', agg_func=agg_median),
    metric('c_session_restored', agg_func=agg_median),

    # Warm metrics
    metric('w_fp', agg_func=agg_median),
    metric('w_dss', agg_func=agg_median),
    metric('w_sr', agg_func=agg_median),
    metric('w_sp', agg_func=agg_median),

    # First cold metrics
    metric('f_fp', agg_func=min_, default=None),  #TODO: Should we use min for this one?
    metric('f_dss', agg_func=min_, default=None),
    metric('f_sp', agg_func=min_, default=None),
    metric('f_sr', agg_func=min_, default=None),

    metric('count_cold_dss', agg_func=count_nonnull, default="0"),
    metric('count_warm_dss', agg_func=count_nonnull, default="0"),

    metric('present', agg_func=max_, default="0"),
    metric('cold_exists', agg_func=max_, default="0"),
    metric('count_cold', agg_func=sum_, default="0"),
    metric('count_warm', agg_func=sum_, default="0"),
]
