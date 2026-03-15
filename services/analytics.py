from datetime import datetime


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


def cycle_progress(tests):

    stage = detect_cycle_stage(tests)

    mapping = {
        "Early Cycle": 25,
        "Nitrite Phase": 50,
        "Late Cycle": 75,
        "Cycle Complete": 100
    }

    return mapping.get(stage, 10)


def ammonia_warning(tests):

    if not tests:
        return False

    latest = tests[-1]

    return latest.ammonia is not None and latest.ammonia > 0.5


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

    return max(score, 0)


def adjusted_water_change_recommendation(tests, water_changes):

    if not tests:
        return 0

    latest_test = tests[-1]

    required = 40

    completed = sum(
        wc.percent for wc in water_changes
        if wc.timestamp >= latest_test.timestamp
    )

    remaining = required - completed

    return max(remaining, 0)


def maintenance_reminder(water_changes, tests):

    if not tests:
        return None

    if not water_changes:
        return {"days": 7}

    latest_change = water_changes[-1]

    days_since = (datetime.utcnow() - latest_change.timestamp).days

    remaining = 7 - days_since

    return {"days": max(remaining, 0)}
