

def normalize_interval_name(name):
    # replace periods with octothorps
    return name.replace(".","#")

def denormalize_interval_name(name):
    # replace octothorps with periods
    return name.replace("#",".")