import mozanalysis.metrics.desktop as mmd

#### Devtools ####
# Create a datasource only including when devtools is opened
devtools_engage_main = mmd.DataSource(
    name='devtools_engage_main',
    from_expr="""(
                SELECT
                    *,
                    DATE(submission_timestamp) AS submission_date,
                    environment.experiments,                    
                FROM `moz-fx-data-shared-prod`.telemetry.main
                WHERE payload.histograms.devtools_toolbox_opened_count IS NOT NULL  
            )""",
    experiments_column_type="native",
)

#### Startup ####
add_prop = '''
CAST(JSON_EXTRACT_SCALAR(additional_properties,
    '$.payload.simpleMeasurements.{}') as INT64)
'''.format
scalar = "payload.processes.parent.scalars.{}".format
earliest_row = "string(submission_timestamp) || '-' || cast({} as string)".format
only_cold = lambda x: f"if({scalar('startup_is_cold')}, {x}, null)"
only_warm = lambda x: f"if({scalar('startup_is_cold')}, null, {x})"

startup_query = f"""(
    SELECT
        *,
        {add_prop("selectProfile")} as select_profile_all,
        {only_cold(add_prop("delayedStartupStarted"))} as count_cold_dss,
        {only_warm(add_prop("delayedStartupStarted"))} as count_warm_dss,

        {only_cold(scalar("timestamps_first_paint"))} as c_first_paint,
        {only_cold(add_prop("delayedStartupStarted"))} as c_delayed_st_st,
        {only_cold(add_prop("sessionRestored"))} as c_session_restored,
        {only_cold(add_prop("selectProfile"))} as c_select_profile,

        {only_warm(scalar("timestamps_first_paint"))} as w_fp,
        {only_warm(add_prop("delayedStartupStarted"))} as w_dss,
        {only_warm(add_prop("sessionRestored"))} as w_sr,
        {only_warm(add_prop("selectProfile"))} as w_sp,

        {only_cold(earliest_row(add_prop("selectProfile")))} as f_sp,
        {only_cold(earliest_row(scalar("timestamps_first_paint")))} as f_fp,
        {only_cold(earliest_row(add_prop("delayedStartupStarted")))} as f_dss,
        {only_cold(earliest_row(add_prop("sessionRestored")))} as f_sr,
        {only_cold(earliest_row(add_prop("blank_window_shown")))} as f_bws,

        1 as present,
        if({scalar('startup_is_cold')}, 1, 0) as cold_exists,
        if({scalar('startup_is_cold')}, 0, 1) as warm_exists,

        if({scalar('startup_is_cold')}, 1, 0) as count_cold,
        if({scalar('startup_is_cold')}, 0, 1) as count_warm,

        DATE(submission_timestamp) AS submission_date,
        environment.experiments
    FROM `moz-fx-data-shared-prod`.telemetry.main
    WHERE sample_id >= 0
      and normalized_channel = 'beta'
      and application.name = 'Firefox'
      --and coalesce({scalar("timestamps_first_paint")}, 0) > 0
      --and coalesce({scalar("startup_is_cold")}, false)
)"""

desktop_startup_main = mmd.DataSource(
    name='desktop_startup_main',
    from_expr=startup_query,
    experiments_column_type="native",
)
