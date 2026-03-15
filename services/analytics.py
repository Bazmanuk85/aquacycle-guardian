from datetime import datetime


# -----------------------------
# Cycle Detection
# -----------------------------

def detect_cycle_stage(tests):

    if not tests:
        return "No Data"

    ammonia_seen = any(t.ammonia and t.ammonia > 0 for t in tests)
    nitrite_seen = any(t.nitrite and t.nitrite > 0 for t in tests)
    nitrate_seen = any(t.nitrate and t.nitrate > 0 for t in tests)

    if ammonia_seen and not nitrite_seen:
        return "Early Cycle"

    if nitrite_seen and not nitrate_seen:
        return "Mid Cycle"

    if nitrate_seen:
        return "Cycle Complete"

    return "Unknown"


# -----------------------------
# Cycle Progress %
# -----------------------------

def cycle_progress(tests):

    if not tests:
        return 0

    stage = detect_cycle_stage(tests)

    if stage == "Early Cycle":
        return 30

    if stage == "Mid Cycle":
        return 60

    if stage == "Cycle Complete":
        return 100

    return 10


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
# Ammonia Danger
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
        return False

    latest = tests[-1]

    if latest.temperature:

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

    if latest.ammonia and latest.ammonia > 0.25:
        score -= 30

    if latest.nitrite and latest.nitrite > 0.5:
        score -= 20

    if latest.nitrate and latest.nitrate > 40:
        score -= 20

    if latest.temperature:

        if latest.temperature > 28 or latest.temperature < 20:
            score -= 10

    if score < 0:
        score = 0

    return score


# -----------------------------
# Water Change Recommendation
# -----------------------------

def adjusted_water_change_recommendation(tests, changes):

    if not tests:
        return 0

    latest = tests[-1]

    required = 0

    if latest.ammonia and latest.ammonia > 0.25:
        required += 30

    if latest.nitrite and latest.nitrite > 0.5:
        required += 30

    if latest.nitrate and latest.nitrate > 40:
        required += 40

    performed = sum(c.percent for c in changes)

    remaining = required - performed

    if remaining < 0:
        remaining = 0

    return round(remaining, 1)
