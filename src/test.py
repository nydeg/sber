from src.model import Model

def hit_at_k(
    recommendations: list[list[int]],
    true_items: list[int],
    k: int = 10,
) -> float:
    """
    Вычисление Hit@K для списка предсказаний.

    Parameters
    ----------
    recommendations : list of lists of ints
        recommendations[i] — ранжированный список
        рекомендаций для i-го примера.
    true_items : list of ints
        true_items[i] — истинный следующий товар
        для i-го примера.
    k : int
        Отсечка top-K (по умолчанию 10).

    Returns
    -------
    float
        Hit@K, значение от 0 до 1.
    """
    assert len(recommendations) == len(true_items), \
        "recommendations и true_items должны совпадать по длине"

    hits = 0
    for recs, true_item in zip(recommendations, true_items):
        if true_item in recs[:k]:
            hits += 1

    return hits / len(true_items)


def estimate(model: Model, trains: list[list[int]], targets: list[int]) -> list[float]:
    recs = []

    short = []
    short_targets = []
    mediuml = []
    mediuml_targets = []
    mediumr = []
    mediumr_targets = []
    long = []
    long_targets = []

    for i, session in enumerate(trains):
        rec = model.experiment_forecast(session)
        recs.append(rec)

        # числа ниже опираются на граф
        if len(session) <= 4:
            short.append(rec)
            short_targets.append(targets[i])
        if len(session) > 4 and len(session) < 12:
            mediuml.append(rec)
            mediuml_targets.append(targets[i])
        if len(session) >= 12 and len(session) < 18:
            mediumr.append(rec)
            mediumr_targets.append(targets[i])
        if len(session) >= 18:
            long.append(rec)
            long_targets.append(targets[i])
        
    
    result = hit_at_k(recs, targets)
    result_short = hit_at_k(short, short_targets)
    result_mediuml = hit_at_k(mediuml, mediuml_targets)
    result_mediumr = hit_at_k(mediumr, mediumr_targets)
    result_long = hit_at_k(long, long_targets)

    return [result, result_short, result_mediuml, result_mediumr, result_long]


def estimate_popular(model: Model, targets: list[int]) -> float:
    recs = []

    for i in range(len(targets)):
        recs.append(model.popular)
    
    result = hit_at_k(recs, targets)
    return result