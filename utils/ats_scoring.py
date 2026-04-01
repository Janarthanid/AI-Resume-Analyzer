def calculate_score(matches):
    matched = len(matches["matched"])
    missing = len(matches["missing"])

    total = matched + missing

    if total == 0:
        return 0

    score = (matched / total) * 100
    return int(score)