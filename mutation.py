import random
from itertools import repeat

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence

def mutation(individual, low, up, indpb):
    """modified from the original mutUniformInt in deap.tools to have attributes with step=5 for thickness insolation
    Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.

    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    :param low: The lower bound or a :term:`python:sequence` of
                of lower bounds of the range from which to draw the new
                integer.
    :param up: The upper bound or a :term:`python:sequence` of
               of upper bounds of the range from which to draw the new
               integer.
    :param indpb: Independent probability for each attribute to be mutated.
    :returns: A tuple of one individual.
    """
    size = len(individual)
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))
    for i, xl, xu in zip(range(size-1), low, up):
        if random.random() < indpb:
            individual[i] = random.randrange(xl, xu, 5)
    if random.random() < indpb:
        individual[size-1]=random.randint(low[size-1],up[size-1])
    return individual
if __name__ == "__main__":
    indiv=[20,40,30,2]
    low=[10,10,10,0]
    up=[50,50,50,3]
    indp=1/4
    mutant=mutation(indiv,low,up,indp)
    print(mutant)