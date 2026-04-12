def normalize_score(score: float) -> float:
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def grade_easy(state: dict, expected: dict) -> float:
    """
    Easy: agent must correctly set category and priority.
    Score = 0.5 per correct field (max 1.0).
    """
    score = 0.0
    if state.get("category") == expected["category"]:
        score += 0.5
    if state.get("priority") == expected["priority"]:
        score += 0.5
    return normalize_score(score)


def grade_medium(state: dict, expected: dict) -> float:
    """
    Medium: agent must correctly set category, priority, and assign team.
    Score breakdown: category=0.3, priority=0.3, team=0.4.
    """
    score = 0.0
    if state.get("category") == expected["category"]:
        score += 0.3
    if state.get("priority") == expected["priority"]:
        score += 0.3
    if state.get("team") == expected["team"]:
        score += 0.4
    return normalize_score(score)


def grade_hard(state: dict, expected: dict) -> float:
    """
    Hard: full triage + keyword-rich reply + resolution.

    Score breakdown:
      category correct:     +0.15
      team correct:         +0.15
      priority correct:     +0.10
      reply keyword match:  up to +0.50  (proportional to keywords matched)
      ticket resolved:      +0.10
    Total max:               1.00
    """
    score = 0.0

    if state.get("category") == expected["category"]:
        score += 0.15
    if state.get("team") == expected["team"]:
        score += 0.15
    if state.get("priority") == expected["priority"]:
        score += 0.10

    # reply keyword match — proportional
    reply = (state.get("reply") or "").lower()
    keywords = expected.get("reply_keywords", [])
    if keywords:
        matched = sum(1 for kw in keywords if kw.lower() in reply)
        keyword_score = matched / len(keywords)
        score += 0.50 * keyword_score

    # must be resolved for full score
    if state.get("status") == "resolved":
        score += 0.10

    return normalize_score(score)
