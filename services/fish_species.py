# Large curated aquarium fish lists
# Used for intelligent species selection by tank type


FRESHWATER_FISH = [

# A
"African Butterfly Fish",
"African Cichlid",
"Amano Shrimp",
"Angelfish",
"Arowana",
"Apistogramma",

# B
"Bala Shark",
"Banjo Catfish",
"Betta",
"Bichir",
"Bristlenose Pleco",
"Buenos Aires Tetra",

# C
"Corydoras",
"Cardinal Tetra",
"Cherry Barb",
"Clown Loach",
"Convict Cichlid",
"Crystal Red Shrimp",

# D
"Discus",
"Denison Barb",
"Dwarf Gourami",
"Dwarf Neon Rainbowfish",

# E
"Electric Blue Ram",
"Endler's Livebearer",
"Ember Tetra",

# F
"Firemouth Cichlid",
"Flowerhorn Cichlid",
"Flagfish",

# G
"Guppy",
"Glass Catfish",
"German Blue Ram",
"Giant Danio",
"Golden Wonder Killifish",

# H
"Hillstream Loach",
"Honey Gourami",

# J
"Jack Dempsey",

# K
"Kribensis",
"Kuhli Loach",

# L
"Leopard Danio",
"Loach",
"Lemon Tetra",

# M
"Molly",
"Marble Hatchetfish",
"Mbuna Cichlid",

# N
"Neon Tetra",

# O
"Otocinclus",
"Oscar",

# P
"Pearl Gourami",
"Platy",
"Pictus Catfish",
"Panda Corydoras",

# R
"Rainbowfish",
"Rummy Nose Tetra",
"Red Tail Shark",

# S
"South American Puffer",
"Swordtail",
"Severum",
"Silver Dollar",

# T
"Tiger Barb",
"Tetra",
"Threadfin Rainbowfish",

# W
"White Cloud Mountain Minnow",

# Z
"Zebra Danio"
]


MARINE_FISH = [

# A
"Achilles Tang",
"Angelfish (Marine)",
"Anthias",

# B
"Banggai Cardinalfish",
"Blenny",
"Blue Tang",
"Bicolor Angelfish",

# C
"Clownfish",
"Chromis",
"Copperband Butterflyfish",

# D
"Damselfish",
"Dottyback",
"Dragonet",

# E
"Emperor Angelfish",

# F
"Firefish",
"Foxface Rabbitfish",

# G
"Goby",
"Green Chromis",

# H
"Hawkfish",

# J
"Jawfish",

# L
"Lionfish",

# M
"Mandarin Dragonet",
"Moorish Idol",

# N
"Naso Tang",

# P
"Pufferfish",

# R
"Royal Gramma",

# S
"Sailfin Tang",
"Six Line Wrasse",
"Snowflake Eel",

# T
"Tang",
"Triggerfish",

# W
"Wrasse"
]


BRACKISH_FISH = [

# A
"Archerfish",

# B
"Bumblebee Goby",

# F
"Figure 8 Puffer",

# K
"Knight Goby",

# M
"Mono Fish",
"Mudskipper",

# S
"Scat",
"Spotted Scat",

# V
"Violet Goby"
]


def get_fish_list(tank_type):

    tank_type = tank_type.lower()

    if tank_type in ["marine", "reef"]:
        return MARINE_FISH

    if tank_type == "brackish":
        return BRACKISH_FISH

    return FRESHWATER_FISH
