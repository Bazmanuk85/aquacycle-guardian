from datetime import datetime


def required_water_change_from_tests(tests):

    if not tests:
        return 0

    latest = tests[-1]
    required = 0

    if latest.ammonia is not None and latest.ammonia > 0.5:
        required = max(required, 60)

    if latest.ammonia is not None and latest.ammonia > 0.25:
        required = max(required, 40)

    if latest.nitrite is not None and latest.nitrite > 0.5:
        required = max(required, 40)

    if latest.nitrate is not None and latest.nitrate > 80:
        required = max(required, 40)

    if latest.nitrate is not None and latest.nitrate > 40:
        required = max(required, 25)

    return required


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

    return max(round(remaining, 1), 0)


def tank_health_score(tests):

    if not tests:
        return 50

    latest = tests[-1]
    score = 100

    if latest.ammonia is not None and latest.ammonia > 0.25:
        score -= 40

    if latest.nitrite is not None and latest.nitrite > 0.25:
        score -= 30

    if latest.nitrate is not None and latest.nitrate > 40:
        score -= 20

    if latest.temperature is not None and (latest.temperature > 30 or latest.temperature < 18):
        score -= 10

    return max(score, 0)


def detect_trend(values):

    if len(values) < 3:
        return "stable"

    if values[-1] > values[-2] > values[-3]:
        return "rising"

    if values[-1] < values[-2] < values[-3]:
        return "falling"

    return "stable"


def estimate_days_to_threshold(values, threshold):

    if len(values) < 3:
        return None

    v1, v2, v3 = values[-3], values[-2], values[-1]

    rate = (v3 - v1) / 2

    if rate <= 0:
        return None

    remaining = threshold - v3

    if remaining <= 0:
        return 0

    days = remaining / rate

    return round(days, 1)


def generate_ai_recommendations(tests):

    alerts = []

    if not tests:
        return alerts

    latest = tests[-1]

    nitrate_values = [t.nitrate for t in tests if t.nitrate is not None]
    nitrite_values = [t.nitrite for t in tests if t.nitrite is not None]
    temp_values = [t.temperature for t in tests if t.temperature is not None]

    nitrate_trend = detect_trend(nitrate_values)
    nitrite_trend = detect_trend(nitrite_values)
    temp_trend = detect_trend(temp_values)

    # Immediate issues

    if latest.ammonia is not None and latest.ammonia > 0:
        alerts.append("🚨 Ammonia detected — perform immediate water change")

    if latest.nitrite is not None and latest.nitrite > 0.25:
        alerts.append("🚨 Nitrite dangerously high — toxic to fish")

    if latest.nitrate is not None and latest.nitrate > 50:
        alerts.append("⚠ Nitrate high — schedule water change")

    if latest.temperature is not None and latest.temperature > 30:
        alerts.append("🔥 Temperature too high — risk of oxygen depletion")

    if latest.temperature is not None and latest.temperature < 18:
        alerts.append("❄ Temperature too low for most tropical fish")

    # Trend alerts

    if nitrate_trend == "rising":
        alerts.append("📈 Nitrate trending upward — water quality declining")

    if nitrite_trend == "rising":
        alerts.append("📈 Nitrite increasing trend detected")

    if temp_trend == "rising":
        alerts.append("📈 Temperature rising trend detected")

    # Predictive alerts

    nitrate_days = estimate_days_to_threshold(nitrate_values, 80)

    if nitrate_days and nitrate_days > 0:
        alerts.append(
            f"📊 Nitrate may exceed safe level in ~{nitrate_days} days"
        )

    temp_days = estimate_days_to_threshold(temp_values, 30)

    if temp_days and temp_days > 0:
        alerts.append(
            f"🌡 Temperature may exceed safe range in ~{temp_days} days"
        )

    return alerts
