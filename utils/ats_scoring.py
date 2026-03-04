def ats_score(matched, total):
    if total == 0:
        return 0
    return round((matched / total) * 100, 2)
