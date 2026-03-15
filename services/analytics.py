from datetime import datetime


# -----------------------------
# Utility
# -----------------------------

def apply_dilution(value, water_changes):

    if value is None:
        return None

    result = value

    for change in water_changes:
        dilution = change.percent / 100
        result = result * (1 - dilution)

    return round(result, 2)


# -----------------------------
# Cycle Detection
# -----------------------------

def detect_cycle_stage(tests):

    if not tests:
        return "No Data"

    ammonia_present = any(t.ammonia and t.ammonia > 0.1 for t in tests)
    nitrite_present = any(t.nitrite and t.nitrite > 0.1 for t in tests)
    nitrate_present = any(t.nitrate and t.nitrate > 5 for t in tests)

    if ammonia_present and not nitrite_present:
        return "Early Cycle"

    if nitrite_present and not nitrate_present:
        return "Nitrite Phase"

    if nitrate_present and ammonia_present:
        return "Late Cycle"

    if nitrate_present and not ammonia_present and not nitrite_present:
        return "Cycle Complete"

    return "Unknown"


# -----------------------------
# Cycle Progress
# -----------------------------

def cycle_progress(tests):

    if not tests:
        return 0

    stage = detect_cycle_stage(tests)

    progress_map = {
        "Early Cycle": 25,
        "Nitrite Phase": 50,
        "Late Cycle": 75,
        "Cycle Complete": 100
    }

    return progress_map.get(stage, 10)


# -----------------------------
# Nitrate Spike
# -----------------------------

def nitrate_spike(values):

    if not values:
        return False

    if values[-1] > 40:
        return True

    return False


# -----------------------------
# Ammonia Alert
# -----------------------------

def ammonia_warning(tests):

    if not tests:
        return False

    latest = tests[-1]

    if latest.ammonia and latest.ammonia > 0.5:
        return True

    return False


# -----------------------------
# Temperature Alert
# -----------------------------

def temperature_alert(tests):

    if not tests:
        return None

    latest = tests[-1]

    if latest.temperature is None:
        return None

    if latest.temperature > 28:
        return "High"

    if latest.temperature < 20:
        return "Low"

    return None


# -----------------------------
# Tank Health Score
# -----------------------------

def tank_health_score(tests):

    if not tests:
        return 50

    latest = tests[-1]

    score = 100

    # Ammonia
    if latest.ammonia is not None:
        if latest.ammonia > 1:
            score -= 50
        elif latest.ammonia > 0.25:
            score -= 30

    # Nitrite
    if latest.nitrite is not None:
        if latest.nitrite > 1:
            score -= 30
        elif latest.nitrite > 0.25:
            score -= 20

    # Nitrate
    if latest.nitrate is not None:
        if latest.nitrate > 80:
            score -= 30
        elif latest.nitrate > 40:
            score -= 15

    # Temperature
    if latest.temperature is not None:
        if latest.temperature > 30 or latest.temperature < 18:
            score -= 20
        elif latest.temperature > 28 or latest.temperature < 20:
            score -= 10

    # pH
    if latest.ph is not None:
        if latest.ph < 6 or latest.ph > 8.5:
            score -= 10

    if score < 0:
        score = 0

    return score


# -----------------------------
# Water Change Recommendation
# -----------------------------

def adjusted_water_change_recommendation(tests, water_changes):

    if not tests:
        return 0

    latest = tests[-1]

    ammonia = apply_dilution(latest.ammonia, water_changes)
    nitrite = apply_dilution(latest.nitrite, water_changes)
    nitrate = apply_dilution(latest.nitrate, water_changes)

    recommendation = 0

    if ammonia and ammonia > 0.25:
        recommendation += 40

    if nitrite and nitrite > 0.25:
        recommendation += 30

    if nitrate and nitrate > 40:
        recommendation += 30

    if recommendation > 90:
        recommendation = 90

    return recommendation
