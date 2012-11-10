# MakeModel.py <H_dir> <data_dir> <data_file> <model_file>
# EG. python MakeModel.py data lorenz.4 m12s.4y

import sys, os.path, pickle, random, numpy

from itertools import dropwhile

def skip_header(lines):
    isheader = lambda line: line.startswith("#")
    return dropwhile(isheader, lines)
    
def read_data(data_dir, data_file):
    # Read in <data_file>
    f = open(os.path.join(data_dir, data_file), 'r')
    lines = skip_header(f)
    y = [int(line)-1 for line in lines]
    f.close()
    return y, max(y)+1

def randomP(A):
    """ Fill allocated array A with random normalized probability
    """
    sum = 0
    for i in range(len(A)):
        x = random.random()
        sum += x
        A[i] = x
    A /= sum
    return A

# control and model parameters
niterations = 20        # maximum number of iterations
nstates = 12             # about the data

_, data_dir, data_file, model_file = sys.argv
#import Scalar_sparse as Scalar
import Scalar

Y, cardy = read_data(data_dir, data_file)
Y = numpy.array(Y,numpy.int32)

random.seed(3)
P_S0 = randomP(numpy.zeros(nstates))
P_S0_ergodic = randomP(numpy.zeros(nstates))
P_ScS = numpy.zeros((nstates,nstates))
P_YcS = numpy.zeros((nstates,cardy))
for AA in (P_ScS,P_YcS):
    for A in AA:
        randomP(A)

# Train the model
mod = Scalar.HMM(P_S0,P_S0_ergodic,P_ScS,P_YcS)
mod.train(Y,N_iter=niterations)

# Save model in <model_file>
f = open(os.path.join(data_dir, model_file), 'wb')
pickle.dump(mod, f)
f.close()

#Local Variables:
#mode:python
#End: