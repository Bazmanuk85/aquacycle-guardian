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
