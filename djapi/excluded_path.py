def custom_preprocessing_hook(endpoints):
    # your modifications to the list of operations that are exposed in the schema
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        # Remove all but DRF API endpoints
        if "schema" not in path:
            filtered.append((path, path_regex, method, callback))
    return filtered
