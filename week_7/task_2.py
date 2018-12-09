from pomegranate import *

Burglary = DiscreteDistribution({'T': 0.001, 'F': 0.999})
Earthquake = DiscreteDistribution({'T': 0.002, 'F': 0.998})
Alarm_cond = [['T', 'T', 'T', 0.95], ['T', 'T', 'F', 0.05], ['T', 'F', 'T', 0.94], ['T', 'F', 'F', 0.06],
              ['F', 'T', 'T', 0.29], ['F', 'T', 'F', 0.71], ['F', 'F', 'T', 0.001], ['F', 'F', 'F', 0.999]]

Alarm = ConditionalProbabilityTable(Alarm_cond, [Burglary, Earthquake])

JohnCalls = ConditionalProbabilityTable([['T', 'T', 0.90], ['T', 'F', 0.1], ['F', 'T', 0.05], ['F', 'F', 0.95]],
                                        [Alarm])
MaryCalls = ConditionalProbabilityTable([['T', 'T', 0.70], ['T', 'F', 0.3], ['F', 'T', 0.01], ['F', 'F', 0.99]],
                                        [Alarm])
s1 = State(Burglary, name="Burglary")
s2 = State(Earthquake, name="Earthquake")
s3 = State(Alarm, name="Alarm")
s4 = State(JohnCalls, name="JohnCalls")
s5 = State(MaryCalls, name="MaryCalls")
model = BayesianNetwork("Task_2")
model.add_states(s1, s2, s3, s4, s5)
model.add_transition(s1, s3)
model.add_transition(s2, s3)
model.add_transition(s3, s4)
model.add_transition(s3, s5)
model.bake()
res = 0
for i in ['T', 'F']:
    for j in ['T', 'F']:
        for k in ['T', 'F']:
            res += model.probability([i, j, k, 'T', 'T'])
print("P['J','M']", res)
print("P['B','E','A','J','M']", model.probability(['T', 'T', 'T', 'T', 'T']))
res = 0
all_res = 0
for i in ['T', 'F']:
    for j in ['T', 'F']:
        tmp = model.probability([i, j, 'T', 'T', 'F'])
        res += tmp
        all_res += tmp + model.probability([i, j, 'F', 'T', 'F'])
print("P['A'|'J','M']", res / all_res)
res = 0
all_res = 0
for i in ['T', 'F']:
    for j in ['T', 'F']:
        tmp = model.probability(['F', i, j, 'T', 'F'])
        res += tmp
        all_res += tmp + model.probability(['F', i, j, 'T', 'T']) + model.probability(
            ['F', i, j, 'F', 'T']) + model.probability(['F', i, j, 'F', 'F'])
print("P['J','-M'|'-B']", res / all_res)
