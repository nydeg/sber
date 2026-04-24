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


def estimate(model: Model, trains: list[list[int]], targets: list[int]) -> float:
    recs = []

    for session in trains:
        last_item = session[-1]
        rec = model.forecast(last_item=last_item)
        recs.append(rec)
    
    result = hit_at_k(recs, targets)
    return result

def estimate_popular(model: Model, targets: list[int]) -> float:
    recs = []

    for i in range(len(targets)):
        recs.append(model.popular)
    
    result = hit_at_k(recs, targets)
    return result