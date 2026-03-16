from datetime import datetime


SAFE_NITRATE = 40
CRITICAL_NITRATE = 80


def required_water_change_from_tests(tests):

    if not tests:
        return 0

    latest = tests[-1]

    if latest.nitrate is None:
        return 0

    nitrate = latest.nitrate

    if nitrate > 80:
        return 50

    if nitrate > 60:
        return 40

    if nitrate > 40:
        return 25

    return 0


def adjusted_water_change_recommendation(tests, changes):

    if not tests:
        return 0

    required = required_water_change_from_tests(tests)

    latest_test_time = tests[-1].timestamp

    completed = sum(
        c.percent for c in changes
        if c.timestamp >= latest_test_time
    )

    remaining = required - completed

    if remaining < 0:
        remaining = 0

    return round(remaining, 1)


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

    if latest.temperature and (latest.temperature > 30 or latest.temperature < 18):
        score -= 10

    if score < 0:
        score = 0

    return score


def nitrate_rate(tests):

    nitrates = [t.nitrate for t in tests if t.nitrate is not None]

    if len(nitrates) < 3:
        return None

    v1, v2, v3 = nitrates[-3], nitrates[-2], nitrates[-1]

    rate = (v3 - v1) / 2

    if rate <= 0:
        return None

    return rate


def predict_days_until_nitrate_critical(tests):

    nitrates = [t.nitrate for t in tests if t.nitrate is not None]

    if len(nitrates) < 3:
        return None

    rate = nitrate_rate(tests)

    if not rate:
        return None

    current = nitrates[-1]

    remaining = CRITICAL_NITRATE - current

    if remaining <= 0:
        return 0

    days = remaining / rate

    return round(days, 1)


def generate_ai_recommendations(tests):

    alerts = []

    if not tests:
        return alerts

    latest = tests[-1]

    if latest.ammonia and latest.ammonia > 0:
        alerts.append("🚨 Ammonia detected — immediate water change required")

    if latest.nitrite and latest.nitrite > 0.25:
        alerts.append("🚨 Nitrite dangerously high")

    if latest.temperature and latest.temperature > 30:
        alerts.append("🔥 Temperature too high")

    if latest.temperature and latest.temperature < 18:
        alerts.append("❄ Temperature too low")

    days = predict_days_until_nitrate_critical(tests)

    if days and days > 0:
        alerts.append(f"📊 Nitrate may exceed safe level in ~{days} days")

    change = required_water_change_from_tests(tests)

    if change > 0:
        alerts.append(f"💧 Recommended water change: {change}%")

    return alerts
