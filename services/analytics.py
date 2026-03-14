def detect_cycle_stage(tests):

    if not tests:
        return "No Data", 0

    ammonia_values = []
    nitrite_values = []
    nitrate_values = []

    for t in tests:
        try:
            ammonia_values.append(float(t.ammonia))
        except:
            ammonia_values.append(0)

        try:
            nitrite_values.append(float(t.nitrite))
        except:
            nitrite_values.append(0)

        try:
            nitrate_values.append(float(t.nitrate))
        except:
            nitrate_values.append(0)

    latest_ammonia = ammonia_values[-1]
    latest_nitrite = nitrite_values[-1]
    latest_nitrate = nitrate_values[-1]

    if latest_ammonia > 0.5 and latest_nitrite == 0:
        return "Ammonia Phase", 25

    if latest_nitrite > 0.5:
        return "Nitrite Phase", 50

    if latest_nitrate > 10 and latest_ammonia == 0 and latest_nitrite == 0:
        return "Nitrate Phase", 75

    if latest_ammonia == 0 and latest_nitrite == 0 and latest_nitrate > 5:
        return "Cycle Complete", 100

    return "Cycling", 40
