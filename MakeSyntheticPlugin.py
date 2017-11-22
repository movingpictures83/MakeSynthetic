# TMC created this script on 7/2/15
# Purpose: Generate synthetic networks
# Intention is to produce examples that demonstrate the advantages
# of our approach (ATria) over others.
# Thus, you can specify the number of social clubs you want,
# minimum and maximum size, number of rival clubs you want,
# number of common enemies you want, and the amount of noise.
# At the moment noise just produces green edges, red edges are thus
# assumed to be predefined.

# Also specify the name.  The file created will appear in 
# (name)/(name).gml.  We use GML so that it can be easily analyzed by Cytoscape.

# Correlation Values for:
# Nodes within a social club: [0.75 - 1)
# Edges with a common enemy: (-1 - 0.75]
# Nodes between rival clubs: [-0.5 - 0]
# Noise: [0 - 0.5]

# hubs and noise are percentages.
# The amount of hub nodes will be equal to that percentage times the size of the largest club
# The amount of noise will be equal to that percentage times the number of nodes (i.e. if the graph
# has 100 nodes, there will be 50 edges that are random, with lower correlations [0 - 0.5]
import numpy
import math
import random
import sys
##############################
# Parameters

class MakeSyntheticPlugin:
   def input(self, filename):
      myfile = open(filename, 'r')

      self.numclouds = int(myfile.readline())
      self.minsize = int(myfile.readline())
      self.maxsize = int(myfile.readline())
#print "Enter number of clouds (value minus 2 should be a multiple of 3):" 
#self.numclouds = int(raw_input())
#print "Enter output file (end in .gml):"
#outfile = raw_input()
#print "Enter minimum cloud size: "
#self.minsize = int(raw_input())
#print "Enter maximum cloud size: "
#self.maxsize = int(raw_input())

#self.numclouds = 11
#self.maxsize = 20
#self.minsize = 16
   def run(self):
####################################################
# Determine the size of each club first.
      cloudsizes = numpy.zeros([self.numclouds])
      for i in range(self.numclouds):
         cloudsizes[i] = random.randint(self.minsize, self.maxsize)
####################################################

####################################################
# Now compute n, the total number of nodes
#
# First, number of hubs
      self.n = int(int(sum(cloudsizes)))
####################################################

####################################################
# Obtain the correct number of nodes
# Partition them into clubs, hubs and common enemies
# We can just do this linearly
#
      nodes = range(0, self.n)
      clouds = []
      node = 0
      for i in range(self.numclouds):
         clouds.append([])
         for j in range(int(cloudsizes[i])):
            clouds[i].append(node)
            node += 1
####################################################


####################################################
# Build adjacency matrix
#
      self.ADJ = numpy.zeros([self.n, self.n])
# Clouds, green edges
   # For each cloud, place a random edges 0.75-1 between every pair
   # Give each other node in the club, relatively high magnitude edge
   # All tertiary edges should be less than the others with the driver
      for j in range(0, self.numclouds):
        cloud = clouds[j]
        for node1 in cloud:
           for node2 in cloud:
              if (node1 != node2):
                 self.ADJ[node1][node2] = random.random()*0.15 + 0.85
                 self.ADJ[node2][node1] = self.ADJ[node1][node2]


# Set up connections between clouds.
# These will be a random positive weight from 0.75 to 1.
      numsets = (self.numclouds - 2) / 3
# Don't use the same random node twice for the middle clouds.
      randomcloudtwos = []

# Left most cloud is cloud zero
# The random node will connect with a random node in cloud two.
      randomcloudzero = clouds[0][random.randint(0, len(clouds[0])-1)]
      randomcloudtwo = clouds[2][random.randint(0, len(clouds[2])-1)]
      self.ADJ[randomcloudzero][randomcloudtwo] = random.random()*0.25 + 0.75
      self.ADJ[randomcloudtwo][randomcloudzero] = random.random()*0.25 + 0.75
      randomcloudtwos.append(randomcloudtwo)

# Rightmost cloud is cloud (self.numclouds-1)
# The random node will connect with a random node in cloud (self.numclouds-3)
      randomcloudlast = clouds[self.numclouds-1][random.randint(0, len(clouds[self.numclouds-1])-1)]
      randomcloudthirdlast = clouds[self.numclouds-3][random.randint(0, len(clouds[self.numclouds-3])-1)]
      self.ADJ[randomcloudlast][randomcloudthirdlast] = random.random()*0.25 + 0.75
      self.ADJ[randomcloudthirdlast][randomcloudlast] = random.random()*0.25 + 0.75
      randomcloudtwos.append(randomcloudthirdlast)

# Now start at cloud 1, go in groups of three
      for cloudnum in range(1, self.numclouds-3, 3):
         cloud1 = clouds[cloudnum]
         cloud2 = clouds[cloudnum+1]
         cloud3 = clouds[cloudnum+2]
         print "Cloud 1: ", cloudnum, " Cloud2: " , cloudnum+1, " Cloud3: ", cloudnum+2
         randomcloud1 = cloud1[random.randint(0, len(cloud1)-1)]
         randomcloud21 = cloud2[random.randint(0, len(cloud2)-1)]
         while (randomcloud21 in randomcloudtwos):
            randomcloud21 = cloud2[random.randint(0, len(cloud2)-1)]
         randomcloudtwos.append(randomcloud21)
         randomcloud22 = cloud2[random.randint(0, len(cloud2)-1)]
         while (randomcloud22 in randomcloudtwos):
            randomcloud22 = cloud2[random.randint(0, len(cloud2)-1)]
         randomcloudtwos.append(randomcloud22)
         randomcloud3 = cloud3[random.randint(0, len(cloud3)-1)]
         self.ADJ[randomcloud1][randomcloud21] = random.random()*0.25 + 0.75
         self.ADJ[randomcloud21][randomcloud1] = random.random()*0.25 + 0.75
         self.ADJ[randomcloud22][randomcloud3] = random.random()*0.25 + 0.75
         self.ADJ[randomcloud3][randomcloud22] = random.random()*0.25 + 0.75

# Join the middle clouds.
      for cloudnum in range(0, numsets, 3):
         cloud1 = clouds[cloudnum*3+2]
         cloud2 = clouds[(cloudnum+1)*3+2]
         cloud3 = clouds[(cloudnum+2)*3+2]
         randomcloud1 = cloud1[random.randint(0, len(cloud1)-1)]
         while (randomcloud1 in randomcloudtwos):
            randomcloud1 = cloud1[random.randint(0, len(cloud1)-1)]
         randomcloudtwos.append(randomcloud1)
         randomcloud21 = cloud2[random.randint(0, len(cloud2)-1)]
         while (randomcloud21 in randomcloudtwos):
            randomcloud21 = cloud2[random.randint(0, len(cloud2)-1)]
         randomcloudtwos.append(randomcloud21)
         randomcloud22 = cloud2[random.randint(0, len(cloud2)-1)]
         while (randomcloud22 in randomcloudtwos):
            randomcloud22 = cloud2[random.randint(0, len(cloud2)-1)]
         randomcloudtwos.append(randomcloud22)
         randomcloud3 = cloud3[random.randint(0, len(cloud3)-1)]
         while (randomcloud3 in randomcloudtwos):
            randomcloud3 = cloud1[random.randint(0, len(cloud1)-1)]
         randomcloudtwos.append(randomcloud3)
         self.ADJ[randomcloud1][randomcloud21] = random.random()*0.25 + 0.75
         self.ADJ[randomcloud21][randomcloud1] = random.random()*0.25 + 0.75
         self.ADJ[randomcloud22][randomcloud3] = random.random()*0.25 + 0.75
         self.ADJ[randomcloud3][randomcloud22] = random.random()*0.25 + 0.75
   

   def output(self, filename):
      gmlfile = open(filename, 'w')


      gmlfile.write("graph [\n")
      for i in range(self.n):
         gmlfile.write("node [\n")
         gmlfile.write("id "+str(i)+"\n")
         gmlfile.write("label \"A"+str(i)+"\"\n")
         gmlfile.write("]\n")
      for i in range(self.n):
         for j in range(i+1, self.n):
          if (self.ADJ[i][j] != 0):
            gmlfile.write("edge [\n")
            gmlfile.write("source "+str(i)+"\n")
            gmlfile.write("target "+str(j)+"\n")
            gmlfile.write("weight "+str(self.ADJ[i][j])+"\n")
            gmlfile.write("]\n")
      gmlfile.write("]\n")






      



