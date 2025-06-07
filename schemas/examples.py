ID_EXAMPLES = [
    "d08191a1-3a4f-48e3-be3b-fc3bb31536af",
    "3d5dc460-5db7-4dd0-9d4e-3cd825ebaebd",
]

RESULT_EXAMPLES = [
    "Dɑːɹk hæd hæd jɚ jɚ ʃi suːt suːt ʃi hæd jɚ jɚ ʃi",
    "hæd suːt jɚ jɚ ʃi dɑːɹk ʃi hæd ʃi dɑːɹk ʃi hæd hæd hæd suːt jɚ suːt",
]

ACCURACY_EXAMPLES = [
    90.0,
    22.0,
    0.02,
    74.01,
]

MISTAKES_EXAMPLES = [
    [
        {
            "reference": {"position": 6, "value": "ɔːɹ"},
            "actual": {"position": 6, "value": "oʊ"},
            "type": "replacement",
        },
        {
            "reference": {"position": 14, "value": "n"},
            "actual": None,
            "type": "deletion",
        },
        {
            "reference": {"position": 18, "value": "z"},
            "actual": {"position": 18, "value": "s"},
            "type": "replacement",
        },
        {
            "reference": {"position": 20, "value": "w"},
            "actual": None,
            "type": "deletion",
        },
        {
            "reference": {"position": 21, "value": "ɑː"},
            "actual": {"position": 21, "value": "oʊ"},
            "type": "replacement",
        },
        {
            "reference": {"position": 28, "value": "l"},
            "actual": None,
            "type": "deletion",
        },
        {
            "reference": {"position": 30, "value": "ɪɹ"},
            "actual": {"position": 30, "value": "iː"},
            "type": "replacement",
        },
    ]
]
