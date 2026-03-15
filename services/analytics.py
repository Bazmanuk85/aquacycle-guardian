from datetime import datetime


# -----------------------------
# Nitrate Spike Detection
# -----------------------------

def nitrate_spike(values):

    if not values:
        return False

    latest = values[-1]

    return latest is not None and latest > 40


# -----------------------------
# Cycle Detection
# -----------------------------

def detect_cycle_stage(tests):

    if not tests:
        return "No Data"

    ammonia_seen = any(t.ammonia and t.ammonia > 0.1 for t in tests)
    nitrite_seen = any(t.nitrite and t.nitrite > 0.1 for t in tests)
    nitrate_seen = any(t.nitrate and t.nitrate > 5 for t in tests)

    if ammonia_seen and not nitrite_seen:
        return "Early Cycle"

    if nitrite_seen and not nitrate_seen:
        return "Nitrite Phase"

    if nitrate_seen and ammonia_seen:
        return "Late Cycle"

    if nitrate_seen and not ammonia_seen and not nitrite_seen:
        return "Cycle Complete"

    return "Unknown"


# -----------------------------
# Cycle Progress
# -----------------------------

def cycle_progress(tests):

    stage = detect_cycle_stage(tests)

    progress_map = {
        "Early Cycle": 25,
        "Nitrite Phase": 50,
        "Late Cycle": 75,
        "Cycle Complete": 100
    }

    return progress_map.get(stage, 10)


# -----------------------------
# Ammonia Warning
# -----------------------------

def ammonia_warning(tests):

    if not tests:
        return False

    latest = tests[-1]

    return latest.ammonia is not None and latest.ammonia > 0.5


# -----------------------------
# Temperature Alerts
# -----------------------------

def temperature_alert(tests):

    if not tests:
        return None

    lates
