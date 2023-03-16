#!/usr/bin/env python3

import numpy as np

# parameters
cutoff = 2.4 # cutoff in nm
filenames = ["SARS-CoV/CoV-run1", "SARS-CoV/CoV-run2", 
             "SARS-CoV-2/CoV2-run1", "SARS-CoV-2/CoV2-run2"]


# input
traj = []
for name in filenames:
    traj.append(np.load(name + ".heavy.npy"))

traj_cat = np.concatenate(traj)

# selection
condition =  np.any(traj_cat < cutoff, axis=0)
print("Selected {} features...".format(sum(condition)))
with open("featureEx.heavy.{}.tcl".format(int(cutoff*10)), "w") as f:
    f.write("# cutoff = {} nm\n".format(cutoff))
    # CoV
    f.write("# CoV interaction pairs (resids {ACE RBD})\nset cov {")
    i = 0
    for ace in range(21, 616):
        for rbd in range(323, 503):
            if condition[i]:
                f.write("{%d %d} " % (ace, rbd))
            i+=1
    f.write("}\n\n")

    # CoV2
    f.write("# CoV2 interaction pairs (resids {ACE RBD})\nset cov2 {")
    i = 0
    for ace in range(21, 616):
        for rbd in range(336, 517):
            if rbd == 483:
                continue
            if condition[i]:
                f.write("{%d %d} " % (ace, rbd))
            i+=1
    f.write("}\n")

# save
for t,name in zip(traj,filenames):
    traj_ext = t[:,np.argwhere(condition)[:,0]]
    np.save(name + "-ext.heavy." + str(int(cutoff*10)), traj_ext)

