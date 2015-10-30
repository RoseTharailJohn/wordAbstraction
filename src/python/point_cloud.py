__author__ = 'rose'
import random as rnd
import pickle as pkl
outputfile = '/home/rose/UMass/Courses/F15/BINDS/output/point_cloud.pkl'
# creating a set of n random points cloud.
n = 186 # to correspond to brain regions.
min =0
max = 200
point_cloud = []
for x in range(n):
    point_cloud.append((rnd.uniform(min,max), rnd.uniform(min,max), rnd.uniform(min,max)))
print len(point_cloud)
with open(outputfile, 'wb') as f:
        pkl.dump(point_cloud, f)
#uncomment following to test
with open(outputfile, 'rb') as f:
        point_cloud_file = pkl.load(f)
print(point_cloud_file)