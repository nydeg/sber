from src.getdata import train_test_split, get_sessions
from src.model import Model
from src.test import estimate, estimate_popular

n = 10
filepath = "data/sessions.jsonl"

sessions = get_sessions(filepath=filepath)
trains, targets = train_test_split(sessions=sessions)

model = Model(n)
model.create_graph(trains)

results = estimate(model=model, trains=trains, targets=targets) # results[0] это общий результат который нас интересует, на следующих индексах
                                                                # находятся оценка hit@10 для подгрупп, которые можно посмотреть на images/hist

print(f'Hit@10 для модели: {results[0]}')
print(f'Hit@10 для подгрупп: {results[1:]}')
print(f'Hit@10 для popular baseline: {estimate_popular(model=model, targets=targets)}')


# import matplotlib.pyplot as plt
# from collections import Counter

# графы, всё что ниже можно расскоментить чтобы посмотреть на графы
# гистограмма показывающая соотношение
# lengths = [len(session) for session in sessions]

# plt.hist(lengths, bins=15)
# plt.xlabel("Длина сессии")
# plt.ylabel("Количество сессий")
# plt.title("Session length distribution")
# plt.show()

# частоты
# counter = Counter()
# for session in sessions:
#     counter.update(session)

# freqs = [cnt for _, cnt in counter.most_common()]

# plt.figure()
# plt.plot(freqs)
# plt.xlabel("Ранг товара")
# plt.ylabel("Частота")
# plt.title("Item frequency distribution")
# plt.show()

# переходы
# degrees = [len(neighbors) for neighbors in model.probabilities.values()]

# plt.figure()
# plt.hist(degrees, bins=25)
# plt.xlabel("Количество переходов")
# plt.ylabel("Количество товаров")
# plt.title("Transition count per item")
# plt.show()

# таргет pos
# positions = []

# for session, target in zip(trains, targets):
#     recs = model.forecast(session)

#     if target in recs:
#         positions.append(recs.index(target) + 1)

# plt.figure()
# plt.hist(positions, bins=10)
# plt.xlabel("Позиция в топе")
# plt.ylabel("Количество")
# plt.title("Target position distribution")
# plt.show()