from datetime import datetime


# -------------------------
# Nitrate Spike Detection
# -------------------------

def nitrate_spike(values):

    if not values:
        return False

    latest = values[-1]

    if latest is None:
        return False

    return latest > 40


# -------------------------
# Cycle Stage Detection
# -------------------------

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


# -------------------------
# Cycle Progress %
# -------------------------

def cycle_progress(tests):

    stage = detect_cycle_stage(tests)

    progress = {
        "Early Cycle": 25,
        "Nitrite Phase": 50,
        "Late Cycle": 75,
        "Cycle Complete": 100
    }

    return progress.get(stage, 10)


# -------------------------
# Ammonia Alert
# -------------------------

def ammonia_warning(tests):

    if not tests:
        return False

    latest = tests[-1]

    if latest.ammonia is None:
        return False

    return latest.ammonia > 0.5


# -------------------------
# Temperature Alerts
# -------------------------

def temperature_alert(tests):

    if not tests:
        return None

    latest = tests[-1]

    if latest.temperature is None:
        return None

    temp = latest.temperature

    if temp >= 30:
        return "Danger"

    if temp >= 28:
        return "Warning"

    if temp <= 18:
        return "Low"

    return None


# -------------------------
# Tank Health Score
# -------------------------

def tank_health_score(tests):

    if not tests:
        return 50

    latest = tests[-1]

    score = 100

    if latest.ammonia and latest.ammonia > 0.25:
        score -= 40

    if latest.nitrite and latest.nitrite > 0.25:
        score -= 30

    if latest.nitrate and latest.nitrate > 40:
        score -= 20

    if latest.temperature:

        if latest.temperature >= 30 or latest.temperature <= 18:
            score -= 15

        elif latest.temperature >= 28:
            score -= 8

    if latest.ph and (latest.ph < 6 or latest.ph > 8.5):
        score -= 10

    return max(score, 0)


# -------------------------
# Water Change Needed From Tests
# -------------------------

def required_water_change_from_tests(tests):

    if not tests:
        return 0

    latest = tests[-1]

    required = 0

    if latest.ammonia:

        if latest.ammonia > 0.5:
            required = max(required, 60)

        elif latest.ammonia > 0.25:
            required = max(required, 40)

    if latest.nitrite:

        if latest.nitrite > 0.5:
            required = max(required, 40)

    if latest.nitrate:

        if latest.nitrate > 80:
            required = max(required, 40)

        elif latest.nitrate > 40:
            required = max(required, 25)

    return required


# -------------------------
# Adjust Water Change After Changes
# -------------------------

def adjusted_water_change_recommendation(tests, water_changes):

    if not tests:
        return 0

    latest_test = tests[-1]

    required = required_water_change_from_tests(tests)

    completed = 0

    for wc in water_changes:

        if wc.timestamp >= latest_test.timestamp:
            completed += wc.percent

    remaining = required - completed

    if remaining < 0:
        remaining = 0

    return round(remaining, 1)


# -------------------------
# Weekly Maintenance Reminder
# -------------------------

def maintenance_reminder(water_changes):

    if not water_changes:
        return 7

    latest_change = water_changes[-1]

    days_since = (datetime.utcnow() - latest_change.timestamp).days

    remaining = 7 - days_since

    if remaining < 0:
        remaining = 0

    return remaining
