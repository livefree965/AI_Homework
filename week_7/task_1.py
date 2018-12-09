from pomegranate import *

guest = DiscreteDistribution({'A': 1 / 3, 'B': 1 / 3, 'C': 1 / 3})
prize = DiscreteDistribution({'A': 1 / 3, 'B': 1 / 3, 'C': 1 / 3})
result = []
for i in ['A', 'B', 'C']:
    for j in ['A', 'B', 'C']:
        for k in ['A', 'B', 'C']:
            if i == k:
                result.append([i, j, k, 0])
            elif j == k:
                result.append([i, j, k, 0])
            elif i != j:
                result.append([i, j, k, 1])
            else:
                result.append([i, j, k, 0.5])

monty = ConditionalProbabilityTable(result, [guest, prize])

s1 = State(guest, name="guest")
s2 = State(prize, name="prize")
s3 = State(monty, name="monty")
model = BayesianNetwork("Monty Hall Problem")
model.add_states(s1, s2, s3)
model.add_transition(s1, s3)
model.add_transition(s2, s3)
model.bake()
print("P['A','C','B']",model.probability(['A', 'C', 'B']))
print("P['A','C','A']",model.probability(['A', 'C', 'A']))