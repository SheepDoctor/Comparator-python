import numpy as np
import sys

def generate(n):
    print(n)
    arr = np.random.randint(-5, 5, n)
    for i in range(arr.shape[0]):
        print(arr[i], end=' ')
    
    
def main(size):
    generate(n=size[0])
    
if __name__ == '__main__':
    size = [int(x) for x in sys.argv[1:]]
    main(size)