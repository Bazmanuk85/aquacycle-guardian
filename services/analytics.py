from datetime import datetime


SAFE_NITRATE = 40
CRITICAL_NITRATE = 80


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


def recommended_water_change_for_nitrate(tests):

    if not tests:
        return 0

    latest = tests[-1]

    nitrate = latest.nitrate

    if nitrate is None:
        return 0

    if nitrate > 80:
        return 50

    if nitrate > 60:
        return 40

    if nitrate > 40:
        return 25

    return 0


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

        alerts.append(
            f"📊 Nitrate may exceed safe level in ~{days} days"
        )

        change = recommended_water_change_for_nitrate(tests)

        if change:
            alerts.append(
                f"💧 Recommended water change: {change}%"
            )

    return alerts
