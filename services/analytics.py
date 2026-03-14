SAFE_TEMP_LOW = 22
SAFE_TEMP_HIGH = 28


def detect_cycle_stage(tests):

    if not tests:
        return "No data"

    ammonia_vals = [t.ammonia for t in tests if t.ammonia is not None]
    nitrite_vals = [t.nitrite for t in tests if t.nitrite is not None]
    nitrate_vals = [t.nitrate for t in tests if t.nitrate is not None]

    if ammonia_vals and max(ammonia_vals) > 0 and not nitrite_vals:
        return "Ammonia phase"

    if nitrite_vals and max(nitrite_vals) > 0:
        return "Nitrite phase"

    if nitrate_vals and max(nitrate_vals) > 0:
        return "Cycle complete"

    return "Cycle starting"


def cycle_progress(tests):

    if not tests:
        return 0

    stage = detect_cycle_stage(tests)

    if stage == "Cycle starting":
        return 10

    if stage == "Ammonia phase":
        return 40

    if stage == "Nitrite phase":
        return 70

    if stage == "Cycle complete":
        return 100

    return 0


def nitrate_spike(tests):

    nitrates = [t.nitrate for t in tests if t.nitrate is not None]

    if len(nitrates) < 2:
        return None

    if nitrates[-1] > nitrates[-2] + 10:
        return "Nitrate spike detected"

    if nitrates[-1] > 40:
        return "Nitrate dangerously high"

    return None


def ammonia_warning(tests):

    ammonia = [t.ammonia for t in tests if t.ammonia is not None]

    if not ammonia:
        return None

    latest = ammonia[-1]

    if latest > 0.5:
        return "Ammonia dangerous"

    if latest > 0.25:
        return "Ammonia rising"

    return None


def temperature_alert(tests):

    temps = [t.temperature for t in tests if t.temperature is not None]

    if not temps:
        return None

    t = temps[-1]

    if t > SAFE_TEMP_HIGH:
        return "Temperature too high"

    if t < SAFE_TEMP_LOW:
        return "Temperature too low"

    return None


def apply_water_change_dilution(tests, water_changes):

    if not tests:
        return tests

    nitrate = None

    for t in tests:
        if t.nitrate is not None:
            nitrate = t.nitrate

    for wc in water_changes:
        if nitrate is not None:
            nitrate = nitrate * (1 - wc.percent / 100)

    return nitrate


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
