# engine-design
The mechanical design model to approximate mass and factor-of-safety of varioys engine components

## Example run
from piston import piston
from global_reqs import _global_reqs
lawnmower_reqs = _global_reqs[‘lawnmower’]              #The code has two sets of requirements: auto engine and lawnmower.
my_piston = piston(lawnmower_reqs)
x={‘t_H’:4, ‘D’:75}                                     #inputs as Python dictionary
outside_x={}                                            #no outside inputs for piston
fos = my_piston.factor_of_safety(x, outside_x)          #fos output
m = my_piston.mass(x, outside_x)                        #mass output

