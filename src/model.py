from collections import defaultdict, Counter

class Model:
    def __init__(self, n: int):
        self.probabilities = defaultdict(lambda: defaultdict(int))  # граф вида словари (номер товара: вероятность) в словаре 
                                                                    # (номер товара: словарь с соседями)
        self.popular = []   # на случай если топ 10 не набирается просто добавим самые популярные
        self.n = n # hit@n 

    # убираю шум (редкие, случайные переходы)
    def _delete_noise(self, count: int):
        for key in self.probabilities.keys():
            for new_key in list(self.probabilities[key].keys()):
                if self.probabilities[key][new_key] < count:
                    del self.probabilities[key][new_key]


    def create_graph(self, sessions: list[list[int]]): # на вход трейны, в классе создается граф 
        counter = Counter() # чтобы посчитать популярные (baseline)

        for session in sessions:
            counter.update(session)
            for i in range(len(session) - 1):
                if session[i] == session[i + 1]: # вообще ничего не поменяло на практике
                    continue
                self.probabilities[session[i]][session[i + 1]] += 1

        self._delete_noise(2) # для наглядности можно закомментить, прирост 1.4 процента
        
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
        
    def forecast(self, train: list[int]) -> list[int]: # принимает трейны, возвращает топ 10 (self.n)
        last_item = train[-1]

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
    
    def experiment_forecast(self, train: list[int]) -> list[int]:   # с prev для коротких сессий, так как я выяснил 
                                                                    # что для коротких сессий ниже hit score, предположительно из-за популярных
                                                                    # => надо уменьшить их количество
        last_item = train[-1]
        prev_item = train[-2] if len(train) > 1 else None

        seen = set() # чтобы постоянно не доставать элементы из top для проверки

        if last_item not in self.probabilities:
            return self.popular[:self.n]
        
        if len(self.probabilities[last_item]) < self.n:
            # добиваем количество до 10 с помощью популярных
            top = []
            for items in self.probabilities[last_item]:
                if items[0] not in seen:
                    top.append([items[0], items[1]])
                    seen.add(items[0])

            # если длина сессии маленькая, то используем prev
            if len(train) <= 12 and len(train) > 4 and prev_item in self.probabilities:
                for items in self.probabilities[prev_item]:
                    if items[0] not in seen:
                        top.append([items[0], items[1]])
                        seen.add(items[0])
                    elif items[0] in seen:
                        for i in range(len(top)):
                            if top[i][0] == items[0]:
                                top[i][1] += 0.1
            
            if len(top) < self.n: # если все еще меньше то опять добиваем популярными
                for item in self.popular:
                    if item not in seen:
                        top.append([item, 0.01])

            return [items[0] for items in sorted(top, key=lambda x: -x[1])[:self.n]]
        return [items[0] for items in self.probabilities[last_item][:self.n]]