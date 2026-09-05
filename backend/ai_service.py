def generate_world(genre: str, tone: str, concept: str):

    return {
        "genre": genre,
        "tone": tone,
        "concept": concept,

        "regions": [
            {
                "type": "REGION",
                "name": "Hastinapura",
                "description": "The ancient capital of the Kuru dynasty and the center of political power."
            },
            {
                "type": "REGION",
                "name": "Indraprastha",
                "description": "A prosperous kingdom established by the Pandavas."
            }
        ],

        "factions": [
            {
                "type": "FACTION",
                "name": "Kaurava Court",
                "description": "The ruling faction centered around Duryodhana and the Kuru royal court."
            },
            {
                "type": "FACTION",
                "name": "Pandava Alliance",
                "description": "The faction led by the five Pandava brothers seeking their rightful kingdom."
            }
        ],

        "characters": [
            {
                "type": "CHARACTER",
                "name": "Yudhishthira",
                "description": "The eldest Pandava, known for his commitment to duty and justice."
            },
            {
                "type": "CHARACTER",
                "name": "Duryodhana",
                "description": "The eldest Kaurava prince whose ambition drives the succession conflict."
            }
        ],

        "events": [
            {
                "type": "EVENT",
                "name": "Rise of the Kuru Dynasty",
                "description": "The Kuru dynasty grows into a powerful political force."
            },
            {
                "type": "EVENT",
                "name": "Pandavas and Kauravas",
                "description": "Growing rivalry between the two branches of the Kuru family leads to political tension."
            },
            {
                "type": "EVENT",
                "name": "Rise of Indraprastha",
                "description": "The Pandavas establish Indraprastha and build a prosperous kingdom."
            }
        ]
    }