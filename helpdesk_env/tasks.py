TASKS = {
    "easy": {
        "description": "Identify the issue category and set ticket priority",
        "max_steps": 6,
        "required_fields": ["category", "priority"],
    },
    "medium": {
        "description": "Classify issue, set priority, and assign to the correct team",
        "max_steps": 8,
        "required_fields": ["category", "priority", "team"],
    },
    "hard": {
        "description": "Full triage: classify, prioritise, assign team, send keyword-rich reply, resolve ticket",
        "max_steps": 10,
        "required_fields": ["category", "priority", "team", "reply", "status"],
    },
}
