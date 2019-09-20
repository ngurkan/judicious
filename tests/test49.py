from copy import deepcopy
from random import shuffle, sample, random

import judicious

# judicious.seed("f1f06ce6-f6a7-894f-e9e6-bf337e421ace")


def trial_sequences(n_stimuli, n_ratings,
                    n_trials, n_retests, shuffle_sequences=False):

    # crucial tests
    assert n_stimuli % n_trials == 0
    assert n_retests <= n_trials

    # unique stimulus IDs
    stimuli = list(range(1, n_stimuli+1))

    # create lists of lists of trials
    sequences = []
    for _ in range(n_ratings):

        # for each rating batch, shuffle stimuli
        shuffle(stimuli)
        stimuli_perm = deepcopy(stimuli)

        # partition the stimuli into n_trial chunks
        for i in range(0, n_stimuli, n_trials):
            sequence = stimuli_perm[i:i + n_trials]
            retests = sample(sequence, n_retests)
            shuffle(retests)
            sequences += [sequence + retests]

    if shuffle_sequences:
        shuffle(sequences)

    return sequences


def judge_faces(faces, attribute):
    """Run through an experiment on judging faces."""
    person = judicious.Person()
    # r_consent = person.consent()
    r_attrition = person.attrition()
    r_instruct = person.instruct_judge_faces()
    results = []
    for face in faces:
        r = person.judge_face(face, attribute)
        results.append(r)
    r_debrief = person.debrief()
    return results


attributes = ['trustworthy', 'attractive']
facttributes = []
for attribute in attributes:
    sequences = trial_sequences(
        n_stimuli=1 ,
        n_ratings=1,
        n_trials=1,
        n_retests=1,
        shuffle_sequences=False
    )
    facttributes.extend([(sequence, attribute) for sequence in sequences])

print(facttributes)
print(len(facttributes))
results = judicious.map3(judge_faces, facttributes, timeout=300)
print(results)
