from datetime import datetime


def required_water_change_from_tests(tests):

    if not tests:
        return 0

    latest = tests[-1]
    required = 0

    if latest.ammonia and latest.ammonia > 0.5:
        required = max(required, 60)

    if latest.ammonia and latest.ammonia > 0.25:
        required = max(required, 40)

    if latest.nitrite and latest.nitrite > 0.5:
        required = max(required, 40)

    if latest.nitrate and latest.nitrate > 80:
        required = max(required, 40)

    if latest.nitrate and latest.nitrate > 40:
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

    if latest.ammonia and latest.ammonia > 0.25:
        score -= 40

    if latest.nitrite and latest.nitrite > 0.25:
        score -= 30

    if latest.nitrate and latest.nitrate > 40:
        score -= 20

    if latest.temperature and (latest.temperature > 30 or latest.temperature < 18):
        score -= 10

    return max(score, 0)


def cycle_stage(tests):

    if not tests:
        return "Starting", 10

    latest = tests[-1]

    ammonia = latest.ammonia or 0
    nitrite = latest.nitrite or 0
    nitrate = latest.nitrate or 0

    if ammonia > 0.5:
        return "Ammonia Phase", 30

    if nitrite > 0.5:
        return "Nitrite Phase", 60

    if nitrate > 20 and ammonia < 0.25 and nitrite < 0.25:
        return "Nearly Cycled", 80

    if nitrate > 20 and ammonia == 0 and nitrite == 0:
        return "Cycled", 100

    return "Cycling", 50


def ai_recommendation(tests, recommendation):

    if not tests:
        return [
            "Tank has no water tests yet.",
            "Run a full water test.",
            "Monitor ammonia levels closely."
        ]

    latest = tests[-1]

    ammonia = latest.ammonia or 0
    nitrite = latest.nitrite or 0
    nitrate = latest.nitrate or 0

    advice = []

    if ammonia > 0.5:
        advice.append("Ammonia spike detected.")
        advice.append(f"Perform {recommendation}% water change immediately.")

    if nitrite > 0.5:
        advice.append("Nitrite spike detected.")
        advice.append("Reduce feeding and increase aeration.")

    if nitrate > 40:
        advice.append("High nitrate levels detected.")
        advice.append("Increase weekly water change schedule.")

    if ammonia == 0 and nitrite == 0 and nitrate < 20:
        advice.append("Water parameters are stable.")
        advice.append("Tank appears healthy.")

    if not advice:
        advice.append("Tank appears stable.")
        advice.append("Continue normal maintenance.")

    return advice
