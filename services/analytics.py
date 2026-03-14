def detect_cycle_stage(tests):

    if not tests:
        return "No Data", 0

    ammonia = tests[-1].ammonia
    nitrite = tests[-1].nitrite
    nitrate = tests[-1].nitrate

    if ammonia > 0.5 and nitrite == 0:
        return "Ammonia Phase", 25

    if nitrite > 0.5:
        return "Nitrite Phase", 50

    if nitrate > 10 and ammonia == 0 and nitrite == 0:
        return "Nitrate Phase", 75

    if ammonia == 0 and nitrite == 0 and nitrate > 5:
        return "Cycle Complete", 100

    return "Cycling", 40


def analyze_water_quality(tests):

    alerts = []
    recommendations = []

    if not tests:
        return alerts, recommendations, 100

    latest = tests[-1]

    ammonia = latest.ammonia
    nitrite = latest.nitrite
    nitrate = latest.nitrate
    ph = latest.ph
    temp = latest.temperature

    health_score = 100

    if ammonia > 0.25:
        alerts.append("Ammonia detected — dangerous for fish")
        recommendations.append("Immediate water change recommended")
        health_score -= 30

    if nitrite > 0.5:
        alerts.append("Nitrite spike detected")
        recommendations.append("Perform a 50% water change")
        health_score -= 20

    if nitrate > 40:
        alerts.append("High nitrate levels")
        recommendations.append("Recommended water change: 40–60%")
        health_score -= 15

    if temp > 28:
        alerts.append("Water temperature too high")
        recommendations.append("Check heater or room temperature")
        health_score -= 10

    if ph < 6 or ph > 8.5:
        alerts.append("pH outside safe range")
        recommendations.append("Check buffering and water chemistry")
        health_score -= 10

    if health_score < 0:
        health_score = 0

    return alerts, recommendations, health_score
