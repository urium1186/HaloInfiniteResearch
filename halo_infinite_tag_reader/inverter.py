#!/usr/bin/python2.7

from z3 import *
import sys

"""
  See https://raw.githubusercontent.com/yonik/java_util/master/src/util/hash/MurmurHash3.java
  for implementation of the code modelled below
  
  The one downside is that the logic is so complex in some of the switch statements below
  that I had to concretize the length of the input data array, this is ok as usually you can 
  iteratively tune this until you get meaningful plaintext inputs, or it follows a fixed schema, etc.  
"""
def dk(i):
  return "k"+str(i)

def dh(i):
  return "h"+str(i)

def solve():
  s = SolverFor("BV")
  s.set("local_ctx",True)
  
  # Concrete
  roundedEnd = length & 0xfffffffc
  c1 = 0xcc9e2d51
  c2 = 0x1b873593
  seed = 0xefef # this is fixed in the impl I'm looking into
  
  # Based on array theory, maps an Int32 to a Byte
  data = Array('data', BitVecSort(32), BitVecSort(8))
  
  kvecs = {}  
  hvecs = {}

  # ha and ka are allocation counters for each map
  ka = 0
  ha = 0

  # init hvecs to seed
  hvecs[dh(ha)] = BitVec(dh(ha),32)
  s.add(hvecs[dh(ha)] == seed)
  ha += 1 
  
  i=0
  while i < roundedEnd:
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((SignExt(24,data[i]) & 0xff) | ((SignExt(24,data[i+1]) & 0xff) << 8) | ((SignExt(24,data[i+2]) & 0xff) << 16) | (SignExt(24, data[i+3]) << 24)))
    ka += 1

    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == kvecs[dk(ka-1)] * c1)
    ka +=1

    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((kvecs[dk(ka-1)] << 15) | LShR(kvecs[dk(ka-1)],17)))
    ka += 1
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == kvecs[dk(ka-1)] * c2)
    ka +=1

    hvecs[dh(ha)] = BitVec(dh(ha),32)
    s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] ^ kvecs[dk(ka-1)]))
    ha += 1    
 
    hvecs[dh(ha)] = BitVec(dh(ha),32) 
    s.add(hvecs[dh(ha)] == ((hvecs[dh(ha-1)] << 13) | LShR(hvecs[dh(ha-1)],19)))
    ha += 1
    
    hvecs[dh(ha)] = BitVec(dh(ha),32) 
    s.add(hvecs[dh(ha)] == ((hvecs[dh(ha-1)] * 5) + 0xe6546b64))
    ha += 1
    i += 4
 
  # had to concretize this as the logic (ROT32) in the `switch == 1`
  # statement below cannot be inlined to the z3.If statement
  # SSA means lots of duplication here, sorry..
  switch = length & 3
  
  if switch == 3:
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((SignExt(24,data[roundedEnd + 2]) & 0xff) << 16))
    ka += 1    

    # fallthrough 1 
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] | ((SignExt(24,data[roundedEnd + 1]) & 0xff) << 8)))
    ka +=1

    # fallthrough 2
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] | (SignExt(24,data[roundedEnd]) & 0xff)))
    ka +=1  
  
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] * c1))
    ka +=1  
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((kvecs[dk(ka-1)] << 15) | LShR(kvecs[dk(ka-1)],17)))
    ka +=1  
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] * c2))
    ka +=1  
    
    hvecs[dh(ha)] = BitVec(dh(ha),32) 
    s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] ^ kvecs[dk(ka-1)]))
    ha += 1 
 
  if switch == 2:
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((SignExt(24,data[roundedEnd + 1]) & 0xff) << 8))
    ka +=1

    # fallthrough 2
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] | (SignExt(24,data[roundedEnd]) & 0xff)))
    ka +=1  
  
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] * c1))
    ka +=1  
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((kvecs[dk(ka-1)] << 15) | LShR(kvecs[dk(ka-1)],17)))
    ka +=1  
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] * c2))
    ka +=1  

    hvecs[dh(ha)] = BitVec(dh(ha),32) 
    s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] ^ kvecs[dk(ka-1)]))
    ha += 1 
  
  if switch == 1:
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (SignExt(24,data[roundedEnd]) & 0xff))
    ka +=1  
  
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] * c1))
    ka +=1  
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == ((kvecs[dk(ka-1)] << 15) | LShR(kvecs[dk(ka-1)],17)))
    ka +=1  
    
    kvecs[dk(ka)] = BitVec(dk(ka),32) 
    s.add(kvecs[dk(ka)] == (kvecs[dk(ka-1)] * c2))
    ka +=1  

    hvecs[dh(ha)] = BitVec(dh(ha),32) 
    s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] ^ kvecs[dk(ka-1)]))
    ha += 1 
  
  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] ^ length))
  ha += 1 
  
  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == LShR(hvecs[dh(ha-1)],16))
  ha += 1 
  
  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == hvecs[dh(ha-2)] ^ hvecs[dh(ha-1)]) 
  ha += 1 

  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] * 0x85ebca6b))
  ha += 1 

  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == LShR(hvecs[dh(ha-1)],13))
  ha += 1 

  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == hvecs[dh(ha-2)] ^ hvecs[dh(ha-1)]) 
  ha += 1 
  
  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == (hvecs[dh(ha-1)] * 0xc2b2ae35))
  ha += 1 

  hvecs[dh(ha)] = BitVec(dh(ha),32) 
  s.add(hvecs[dh(ha)] == LShR(hvecs[dh(ha-1)],16))
  ha += 1 

  s.add(hash_result == hvecs[dh(ha-2)] ^ hvecs[dh(ha-1)]) 

  ch = s.check()
  print(ch)
  if ch.r == 1:
    model = s.model()
    print("\ninverting 0x%x returns:" % hash_result)
    data = model[data]
    for i in range(0 ,length):
      print( solve(data))
      print( data.num_args())
      print( data.arg(2))
      #print( data.entry(i))
      #print( model.eval(i))
      #print( data[i].eval(i))
  else:
    print(s.unsat_core())

"""
# should really use proper argparse here, but lazy
if not sys.stdin.isatty():
  # piped from build output
  hash_result = int(sys.stdin.read(),0) 
  length = int(sys.argv[1])

elif len(sys.argv) != 3:
  print( "Sorry, calling format has to be like ./inverter.py 0x(<murmurhash>) original_data_length")
  sys.exit(1)

else:
  # just called directly
  hash_result = int(sys.argv[1],0)
  length = int(sys.argv[2]) 
 """
hash_result = 1138711306
length = 10
solve() 