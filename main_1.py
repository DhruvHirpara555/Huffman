import heapq
import time
import math
from heapq import heappop, heappush
from typing import Mapping

# Initializing our Nodes(which make up the tree). The nodes contain left child,right child and symbol and the freq of the character.
class Node:

    def __init__(self,ch,freq,left,right):
        self.sym = ch
        self.freq = freq
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        return self.freq == other.freq

    def __gt__(self, other):
        return self.freq > other.freq
    
    def __lt__(self, other):
        return self.freq < other.freq
     

# Counting the frequencies of each character.
def CountFreq(Str):
    Freq = {}
    for sym in Str:
        if sym in Freq:
            Freq[sym] += 1
        else:
            Freq[sym] = 1
    return Freq
# Humman treemaker
# We made a priority queue based on the frequencies of the given characters and making huffman using that PQ.
def Huffmantreemaker(Str,Freq):
    nodePQ = [] 
    for key,val in Freq.items():
        nodePQ.append(Node(key,val,None,None))
    heapq.heapify(nodePQ)
    while len(nodePQ) > 1:
        Lchild = heappop(nodePQ)
        Rchild = heappop(nodePQ)
        Freq = Lchild.freq + Rchild.freq
        newnode = Node(None,Freq,Lchild,Rchild)
        heappush(nodePQ,newnode)
    Root = nodePQ[0]
    return Root

# we are mapping every character here to a binary string, as we move towards the left child we add '0' and when move
# towards the right child we add '1' in the respective binary strings.
def Coding(Root,Str,Codemap):
    
    if Root is None:
        return

    if (Root.left is None) and (Root.right is None):
        Codemap[Root.sym] = Str
    
    Coding(Root.left,Str + '0',Codemap)
    Coding(Root.right,Str + '1',Codemap)

# we are forming our encoded string by replacing every character by its respective binary string. 
def encoding(Str,Codemap):
    start_time = time.time()
    encoded_Str = ''

    for i in Str:
        encoded_Str = encoded_Str + Codemap.get(i)
    end_time = time.time()
    print(f"Execution time for compressing: {(end_time - start_time)*1000} ms")
    return encoded_Str

# The helper functions helps us to find the leaf node with the given binary string that we get as we iterate through
# our encoded string
def Helper(Root,index,Encoded_Str,decoded_Str):
    if (Root is None):
        return index,decoded_Str
    if (Root.left is None) and (Root.right is None):
        decoded_Str = decoded_Str + Root.sym
        return index,decoded_Str

    index = index + 1
    if Encoded_Str[index] == '0':
        Root = Root.left
    elif Encoded_Str[index] == '1' :
        Root = Root.right
    return Helper(Root,index,Encoded_Str,decoded_Str)

    
# We are decoding our encoded string here, with the help of the codemap we created. We keep moving through the loop 
# until we hit a leaf node, once we hit the leaf node we replace the given binary string with its character that we had mapped to it
def decoding(Encoded_Str,Root,Codemap):
    start_time = time.time()
    decoded_Str = ''
    index = -1
    n = len(Encoded_str)
    while index < n-1:
        (index,decoded_Str) = Helper(Root,index,Encoded_Str,decoded_Str)

    end_time = time.time()
    print(f"Execution time for decompressing: {(end_time - start_time)*1000} ms")
    return decoded_Str


# Driver Function 
# File 
with open('file3input.txt','r') as file:
    Str = file.read()
F = CountFreq(Str)
Root = Huffmantreemaker(Str,F)
Codemap = {}
Coding(Root,'',Codemap)
print(Codemap)
print("\n\n\n")

Encoded_str = encoding(Str,Codemap)
with open("encode_file3.txt","w") as file:
    file.write(Encoded_str)
    file.close

with open("encode_file3.txt","r") as file:
    Encoded_source = file.read()
Decoded_Str = decoding(Encoded_source,Root,Codemap)

with open("decode_file3.txt","w") as file:
    file.write(Decoded_Str)
    file.close

# Comparing sizes of encoded and decoded files
with open("file3input.txt","r") as file:
    print(f"Size of the encoded file: {math.floor((len(file.read())))} bytes")

with open("encode_file3.txt","r") as file:
    print(f"Size of the decoded file: {math.floor((len(file.read())/8))} bytes")
