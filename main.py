"""
CMPS 2200  Assignment 2.
See Assignment 2.pdf for details.
"""
import time
import tabulate

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))

def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y

def quadratic_multiply(x, y):
  xvec = x.binary_vec
  yvec = y.binary_vec
  xvec, yvec = pad(xvec,yvec)
  
  if x.decimal_val <= 1 and y.decimal_val <= 1:
    return BinaryNumber(x.decimal_val * y.decimal_val)
  else:
    x_left,x_right = split_number(xvec)
    y_left,y_right = split_number(yvec)

    left = quadratic_multiply(x_left,y_left).decimal_val
    
    left_middle = quadratic_multiply(x_left, y_right).decimal_val
    right_middle= quadratic_multiply(x_right, y_left).decimal_val
    
    right=quadratic_multiply(x_right, y_right).decimal_val
    
    left_b = bit_shift(BinaryNumber(left), len(xvec))
    middle = left_middle + right_middle
    
    middle_b = bit_shift(BinaryNumber(middle), len(xvec)//2)
    right_b = BinaryNumber(right)
    
    answer = left_b.decimal_val + middle_b.decimal_val + right_b.decimal_val
    return BinaryNumber(answer)

    pass


def subquadratic_multiply(x, y):
  xvec = x.binary_vec
  yvec = y.binary_vec
  xvec, yvec = pad(xvec,yvec)
  
  if x.decimal_val <= 1 and y.decimal_val <= 1:
    return BinaryNumber(x.decimal_val * y.decimal_val)
  else:
    x_left,x_right = split_number(xvec)
    y_left,y_right = split_number(yvec)

    left = subquadratic_multiply(x_left,y_left).decimal_val
    x_add = BinaryNumber(x_left.decimal_val + x_right.decimal_val)
    y_add = BinaryNumber(y_left.decimal_val + y_right.decimal_val)
    left_multiply = subquadratic_multiply(x_add,y_add).decimal_val
    left_middle = subquadratic_multiply(x_left, y_left).decimal_val
    right_middle= subquadratic_multiply(x_right, y_right).decimal_val
    
    right=subquadratic_multiply(x_right, y_right).decimal_val

    left_b = bit_shift(BinaryNumber(left), len(xvec))

    middle = left_multiply - left_middle - right_middle
    
    middle_b = bit_shift(BinaryNumber(middle), len(xvec)//2)
    right_b = BinaryNumber(right)
    
    answer = left_b.decimal_val + middle_b.decimal_val + right_b.decimal_val
    return BinaryNumber(answer)

    pass


print(subquadratic_multiply(BinaryNumber(3), BinaryNumber(4)).decimal_val)


## Feel free to add your own tests here.
def test_multiply():
    assert (quadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val) == 2*2
    assert (subquadratic_multiply(BinaryNumber(4), BinaryNumber(3)).decimal_val) == 4*3
  
def print_results(results):
  print(tabulate.tabulate(results,
              headers=['size of n','quadratic time', 'subquadratic time'],
              floatfmt=".3f",
              tablefmt="github"))
def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    f(x,y)
    return (time.time() - start)*1000
def compare_multiply():
  res = []
  numbers = [10,100,1000,10000,100000,1000000,10000000,100000000,1000000000]
  for number in numbers:
    q_times = time_multiply(BinaryNumber(number),BinaryNumber(number),quadratic_multiply)
    s_times = time_multiply(BinaryNumber(number),BinaryNumber(number),subquadratic_multiply)
    res.append((number,q_times,s_times))
  print_results(res)

compare_multiply()