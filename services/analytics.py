from statistics import mean

SAFE_RANGES = {
    "ammonia": 0.0,
    "nitrite": 0.0,
    "nitrate_warning": 40,
    "temperature_low": 22,
    "temperature_high": 28
}


def detect_cycle_stage(tests):

    if not tests:
        return "No Data"

    ammonia_vals = [t.ammonia for t in tests if t.ammonia is not None]
    nitrite_vals = [t.nitrite for t in tests if t.nitrite is not None]
    nitrate_vals = [t.nitrate for t in tests if t.nitrate is not None]

    if ammonia_vals and max(ammonia_vals) > 0 and not nitrite_vals:
        return "Cycle Stage: Ammonia Rising"

    if nitrite_vals and max(nitrite_vals) > 0:
        return "Cycle Stage: Nitrite Phase"

    if nitrate_vals and max(nitrate_vals) > 0 and max(ammonia_vals) == 0 and max(nitrite_vals) == 0:
        return "Cycle Complete"

    return "Cycle Unknown"


def nitrate_spike(tests):

    nitrates = [t.nitrate for t in tests if t.nitrate is not None]

    if len(nitrates) < 2:
        return None

    if nitrates[-1] - nitrates[-2] > 10:
        return "Nitrate spike detected"

    if nitrates[-1] > SAFE_RANGES["nitrate_warning"]:
        return "Nitrate dangerously high"

    return None


def ammonia_warning(tests):

    ammonia = [t.ammonia for t in tests if t.ammonia is not None]

    if not ammonia:
        return None

    if ammonia[-1] > 0.5:
        return "Ammonia dangerous"

    if ammonia[-1] > 0.25:
        return "Ammonia rising"

    return None


def temperature_alert(tests):

    temps = [t.temperature for t in tests if t.temperature is not None]

    if not temps:
        return None

    temp = temps[-1]

    if temp > SAFE_RANGES["temperature_high"]:
        return "Temperature too high"

    if temp < SAFE_RANGES["temperature_low"]:
        return "Temperature too low"

    return None


def recommend_water_change(tests):

    nitrates = [t.nitrate for t in tests if t.nitrate is not None]

    if not nitrates:
        return None

    nitrate = nitrates[-1]

    if nitrate <= 20:
        return 0

    if nitrate <= 40:
        return 25

    if nitrate <= 80:
        return 50

    return 70


def tank_health_score(tests):

    score = 100

    ammonia = [t.ammonia for t in tests if t.ammonia is not None]
    nitrite = [t.nitrite for t in tests if t.nitrite is not None]
    nitrate = [t.nitrate for t in tests if t.nitrate is not None]

    if ammonia and ammonia[-1] > 0:
        score -= 30

    if nitrite and nitrite[-1] > 0:
        score -= 30

    if nitrate and nitrate[-1] > 40:
        score -= 20

    return max(score, 0)


def apply_water_change_dilution(tests, water_changes):

    if not water_changes:
        return tests

    adjusted = []

    nitrate = None

    for t in tests:

        if t.nitrate is not None:
            nitrate = t.nitrate

        adjusted.append(t)

    for wc in water_changes:

        if nitrate is not None:

            dilution = wc.percent / 100

            nitrate = nitrate * (1 - dilution)

    return adjusted
