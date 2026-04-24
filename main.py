from src.getdata import train_test_split, get_sessions
from src.model import Model
from src.test import estimate, estimate_popular

n = 10
filepath = "data/sessions.jsonl"

sessions = get_sessions(filepath=filepath)
trains, targets = train_test_split(sessions=sessions)

model = Model(n)
model.create_graph(trains)

print(estimate(model=model, trains=trains, targets=targets))
print(estimate_popular(model=model, targets=targets))

