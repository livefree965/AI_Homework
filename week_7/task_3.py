from pomegranate import *

PatientAge_set = ['0-30', '31-65', '65+']
CTScanResult_set = ['Ischemic Stroke', 'Hemmorraghic Stroke']
MRIScanResult_set = ['Ischemic Stroke', 'Hemmorraghic Stroke']
StrokeType_set = ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic']
Anticoagulants_set = ['Used', 'Not used']
Mortality_set = ['True', 'False']
Disability_set = ['Negligible', 'Moderate', 'Severe']

PatientAge = DiscreteDistribution({'0-30': 0.10, '31-65': 0.30, '65+': 0.60})

CTScanResult = DiscreteDistribution({'Ischemic Stroke': 0.7, 'Hemmorraghic Stroke': 0.3})

MRIScanResult = DiscreteDistribution({'Ischemic Stroke': 0.7, 'Hemmorraghic Stroke': 0.3})

StrokeType = ConditionalProbabilityTable(
    [['Ischemic Stroke', 'Ischemic Stroke', 'Ischemic Stroke', 0.8],
     ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Ischemic Stroke', 0.5],
     ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Ischemic Stroke', 0.5],
     ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Ischemic Stroke', 0],
     ['Ischemic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', 0],
     ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Hemmorraghic Stroke', 0.4],
     ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', 0.4],
     ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Hemmorraghic Stroke', 0.9],
     ['Ischemic Stroke', 'Ischemic Stroke', 'Stroke Mimic', 0.2],
     ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 0.1],
     ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Stroke Mimic', 0.1],
     ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 0.1]], [CTScanResult, MRIScanResult])

Anticoagulants = DiscreteDistribution({'Used': 0.5, 'Not used': 0.5})

Mortality = ConditionalProbabilityTable(
    [['Ischemic Stroke', 'Used', 'False', 0.28],
     ['Hemmorraghic Stroke', 'Used', 'False', 0.99],
     ['Stroke Mimic', 'Used', 'False', 0.1],
     ['Ischemic Stroke', 'Not used', 'False', 0.56],
     ['Hemmorraghic Stroke', 'Not used', 'False', 0.58],
     ['Stroke Mimic', 'Not used', 'False', 0.05],
     ['Ischemic Stroke', 'Used', 'True', 0.72],
     ['Hemmorraghic Stroke', 'Used', 'True', 0.01],
     ['Stroke Mimic', 'Used', 'True', 0.9],
     ['Ischemic Stroke', 'Not used', 'True', 0.44],
     ['Hemmorraghic Stroke', 'Not used', 'True', 0.42],
     ['Stroke Mimic', 'Not used', 'True', 0.95]], [StrokeType, Anticoagulants])

Disability = ConditionalProbabilityTable(
    [['Ischemic Stroke', '0-30', 'Negligible', 0.80],
     ['Hemmorraghic Stroke', '0-30', 'Negligible', 0.70],
     ['Stroke Mimic', '0-30', 'Negligible', 0.9],
     ['Ischemic Stroke', '31-65', 'Negligible', 0.60],
     ['Hemmorraghic Stroke', '31-65', 'Negligible', 0.50],
     ['Stroke Mimic', '31-65', 'Negligible', 0.4],
     ['Ischemic Stroke', '65+', 'Negligible', 0.30],
     ['Hemmorraghic Stroke', '65+', 'Negligible', 0.20],
     ['Stroke Mimic', '65+', 'Negligible', 0.1],
     ['Ischemic Stroke', '0-30', 'Moderate', 0.1],
     ['Hemmorraghic Stroke', '0-30', 'Moderate', 0.2],
     ['Stroke Mimic', '0-30', 'Moderate', 0.05],
     ['Ischemic Stroke', '31-65', 'Moderate', 0.3],
     ['Hemmorraghic Stroke', '31-65', 'Moderate', 0.4],
     ['Stroke Mimic', '31-65', 'Moderate', 0.3],
     ['Ischemic Stroke', '65+', 'Moderate', 0.4],
     ['Hemmorraghic Stroke', '65+', 'Moderate', 0.2],
     ['Stroke Mimic', '65+', 'Moderate', 0.1],
     ['Ischemic Stroke', '0-30', 'Severe', 0.1],
     ['Hemmorraghic Stroke', '0-30', 'Severe', 0.1],
     ['Stroke Mimic', '0-30', 'Severe', 0.05],
     ['Ischemic Stroke', '31-65', 'Severe', 0.1],
     ['Hemmorraghic Stroke', '31-65', 'Severe', 0.1],
     ['Stroke Mimic', '31-65', 'Severe', 0.3],
     ['Ischemic Stroke', '65+', 'Severe', 0.3],
     ['Hemmorraghic Stroke', '65+', 'Severe', 0.6],
     ['Stroke Mimic', '65+', 'Severe', 0.8]], [StrokeType, PatientAge])

S1 = State(PatientAge, name='patient_age')
S2 = State(CTScanResult, name='ct_scan_result')
S3 = State(MRIScanResult, name='mri_scan_result')
S4 = State(StrokeType, name='stroke_type')
S5 = State(Anticoagulants, name='anticoagulants')
S6 = State(Mortality, name='mortality')
S7 = State(Disability, name='disability')

model = BayesianNetwork("Diagnosing Problem")

model.add_states(S1, S2, S3, S4, S5, S6, S7)

# Add transitions (edges)
model.add_transition(S2, S4)
model.add_transition(S3, S4)
model.add_transition(S4, S6)
model.add_transition(S5, S6)
model.add_transition(S4, S7)
model.add_transition(S1, S7)
model.bake()
# model.plot()

all = 0
special = 0
for i in MRIScanResult_set:
    for j in StrokeType_set:
        for k in Anticoagulants_set:
            for l in Disability_set:
                tmp = model.probability(['0-30', 'Ischemic Stroke', i, j, k, 'True', l])
                special += tmp
                all += tmp + model.probability(['0-30', 'Ischemic Stroke', i, j, k, 'False', l])
print(special / all)
all = 0
special = 0
for i in CTScanResult_set:
    for j in StrokeType_set:
        for k in Anticoagulants_set:
            for l in Mortality_set:
                tmp = model.probability(['65+', i, 'Ischemic Stroke', j, k, l, 'Severe'])
                special += tmp
                all += tmp + model.probability(
                    ['65+', i, 'Ischemic Stroke', j, k, l, 'Negligible']) + model.probability(
                    ['65+', i, 'Ischemic Stroke', j, k, l, 'Moderate'])
print(special / all)
all = 0
special = 0
for i in Anticoagulants_set:
    for j in Mortality_set:
        for k in Disability_set:
            tmp = model.probability(['65+', 'Hemmorraghic Stroke', 'Ischemic Stroke', 'Stroke Mimic', i, j, k])
            special += tmp
            all += tmp + model.probability(
                ['65+', 'Hemmorraghic Stroke', 'Ischemic Stroke', 'Ischemic Stroke', i, j, k]) + model.probability(
                ['65+', 'Hemmorraghic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', i, j, k])
print(special / all)
all = 0
special = 0
for i in CTScanResult_set:
    for j in MRIScanResult_set:
        for k in Disability_set:
            tmp = model.probability(['0-30', i, j, 'Stroke Mimic', 'Used', 'False', k])
            special += tmp
            all += tmp + model.probability(['0-30', i, j, 'Stroke Mimic', 'Used', 'True', k])
print(special / all)
all = 0
special = 0
print(model.probability(['0-30', 'Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 'Used', 'False', 'Severe']))
