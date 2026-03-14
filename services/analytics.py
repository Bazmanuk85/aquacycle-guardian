def calculate_toxicity(tests):

    if not tests:
        return 0

    latest = tests[-1]

    toxicity = 0

    if latest.ammonia is not None:
        toxicity += latest.ammonia * 80

    if latest.nitrite is not None:
        toxicity += latest.nitrite * 60

    if latest.nitrate is not None:
        toxicity += latest.nitrate * 0.5

    if latest.temperature is not None:
        if latest.temperature > 28:
            toxicity += 10
        if latest.temperature < 22:
            toxicity += 10

    return toxicity


def recommended_water_change_from_toxicity(toxicity):

    if toxicity < 10:
        return 0

    if toxicity < 25:
        return 10

    if toxicity < 50:
        return 25

    if toxicity < 80:
        return 50

    return 70


def adjusted_water_change_recommendation(tests, water_changes):

    toxicity = calculate_toxicity(tests)

    base = recommended_water_change_from_toxicity(toxicity)

    total_change = sum(w.percent for w in water_changes)

    remaining = base - total_change

    if remaining < 0:
        remaining = 0

    return round(remaining, 1)
