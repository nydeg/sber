from src.getdata import train_test_split, get_sessions
from src.model import Model

filepath = "data/sessions.jsonl"
sessions = get_sessions(filepath=filepath)

# print(len(sessions))

trains, targets = train_test_split(sessions=sessions)

model = Model()
model.create_graph(trains)
