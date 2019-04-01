# MakeSynthetic
# Language: Python
# Input: TXT (contains number of highly connected components, the min size of each, and the max size of each)
# Output: GML (network with these properties, random weights) 
# Tested with: PluMA 1.0, Python 3.6

PluMA plugin to make a synthetic network.  These can be useful for testing algorithm functionality
when real data is unavailable.  This plugin takes as input a text file with three integers on separate lines.
The first line should contain the number of "clouds" or tightly connected components, the second the minimum
size of each cloud, and the third the maximum size of each cloud.

The plugin will then create a network with the specified number of clouds, each with a number of nodes equal
to a random value between the specified minimum and maximum sizes.  It then connects nodes in the same cloud
with edges weighted with random values between 0.85 and 1.  It will also choose random nodes in different
clouds and connect them by edges with random values between 0.75 and 1.  This number of edges will be equal
to the number of clouds minus 2.

The plugin will output the network in the Graph Modeling Language (GML).
