from collections import defaultdict

class Model:
    def __init__(self):
        self.probabilities = defaultdict(lambda: defaultdict(int)) # граф вида словари (номер товара: вероятность) в словаре 
                                # (номер товара: словарь с соседями)
        self.popular = [] # на случай если топ 10 не набирается просто добавим самые популярные

    def create_graph(self, sessions: list[list[int]]): # на вход трейны, в классе создается граф 
        for session in sessions:
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

        
