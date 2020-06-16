def extract_keyed_sum(field, key):
    return f"""`moz-fx-data-shared-prod.udf.json_extract_histogram`(`moz-fx-data-shared-prod.udf.get_key`({field}, '{key}')).sum"""