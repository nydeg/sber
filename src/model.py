from collections import defaultdict, Counter

class Model:
    def __init__(self, n: int):
        self.probabilities = defaultdict(lambda: defaultdict(int)) # граф вида словари (номер товара: вероятность) в словаре 
                                # (номер товара: словарь с соседями)
        self.popular = [] # на случай если топ 10 не набирается просто добавим самые популярные
        self.n = n # hit@n 

    def create_graph(self, sessions: list[list[int]]): # на вход трейны, в классе создается граф 
        counter = Counter()

        for session in sessions:
            counter.update(session)
            for i in range(len(session) - 1):
                self.probabilities[session[i]][session[i + 1]] += 1
        
        # выше посчитаны частоты, ниже поменяно на вероятности
        for key in self.probabilities.keys():
           summ = sum(self.probabilities[key].values())
           for new_key in self.probabilities[key].keys():
               self.probabilities[key][new_key] /= summ

        # чтобы не возиться с словарями в словарях + сортировка
        for key in self.probabilities.keys():
            new_list = sorted(self.probabilities[key].items(), key=lambda x: -x[1]) # сортируем только по вероятности
            self.probabilities[key] = new_list

        self.popular = [items[0] for items in counter.most_common(self.n)] # baseline, самые популярные 
        
    def forecast(self, last_item: int) -> list[int]: # принимает трейны, возвращает топ 10 (self.n)
        if last_item not in self.probabilities:
            return self.popular[:self.n]
        
        if len(self.probabilities[last_item]) < self.n:
            # добиваем количество до 10 с помощью популярных
            top = []
            for items in self.probabilities[last_item]:
                if items[0] not in top:
                    top.append(items[0])

            for item in self.popular:
                if item not in top:
                    top.append(item)

            return top[:self.n]
        return [items[0] for items in self.probabilities[last_item][:self.n]]