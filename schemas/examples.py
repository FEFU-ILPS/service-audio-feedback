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
        {"position": 6, "reference": "ɔːɹ", "actual": "oʊ", "type": "Replacement"},
        {"position": 14, "reference": "n", "actual": None, "type": "Deletion"},
        {"position": 18, "reference": "z", "actual": "s", "type": "Replacement"},
        {"position": 20, "reference": "w", "actual": None, "type": "Deletion"},
        {"position": 21, "reference": "ɑː", "actual": "oʊ", "type": "Replacement"},
        {"position": 28, "reference": "l", "actual": None, "type": "Deletion"},
        {"position": 30, "reference": "ɪɹ", "actual": "iː", "type": "Replacement"},
    ]
]
