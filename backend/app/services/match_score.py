def calculate_match_score(
    required_skills: list[str],
    matching_skills: list[str],
) -> float:
    """
    Calculate the job match score based only on
    required skills and matching skills.

    Formula:
        matching skills / required skills * 100
    """

    required = [
        skill.strip()
        for skill in required_skills
        if skill and skill.strip()
    ]

    matching = [
        skill.strip()
        for skill in matching_skills
        if skill and skill.strip()
    ]

    if not required:
        return 0.0

    score = (
        len(matching)
        / len(required)
    ) * 100

    return round(
        score,
        1,
    )