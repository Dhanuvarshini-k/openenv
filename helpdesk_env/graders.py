def normalize_score(score: float) -> float:
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def grade_easy(state: dict, expected: dict) -> float:
    score = 0.0
    if state.get("category") == expected["category"]:
        score += 0.5
    if state.get("priority") == expected["priority"]:
        score += 0.5
    return normalize_score(score)


def grade_medium(state: dict, expected: dict) -> float:
    score = 0.0
    if state.get("category") == expected["category"]:
        score += 0.3
    if state.get("team") == expected["team"]:
        score += 0.4
    if state.get("priority") == expected["priority"]:
        score += 0.3
    return normalize_score(score)


def grade_hard(state: dict, expected: dict) -> float:
    score = 0.0

    # triage correctness
    if state.get("category") == expected["category"]:
        score += 0.15
    if state.get("team") == expected["team"]:
        score += 0.15
    if state.get("priority") == expected["priority"]:
        score += 0.10

    # reply keyword match
    reply = (state.get("reply") or "").lower()
    matched = 0
    for kw in expected["reply_keywords"]:
        if kw.lower() in reply:
            matched += 1

    keyword_score = matched / max(1, len(expected["reply_keywords"]))
    score += 0.5 * keyword_score

    # must be resolved for full score
    if state.get("status") == "resolved":
        score += 0.10

    return normalize_score(score)