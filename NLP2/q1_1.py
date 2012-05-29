import matplotlib.pyplot as plt
import math
import numpy as np

def generateDataset(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    def ti(xi): return f(xi) + np.random.normal(0.0, sigma, 1) 
    vti = np.vectorize(ti)
    t = vti(x)
    return (x,t)

def makePlot(N, f, x, t):
    vf = np.vectorize(f)
    y = vf(x)
    sizes = [40,50,70]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,t, s=sizes,marker = '.', facecolor='red' )
    plt.plot(x,y)
    plt.show()
 
 
def main():
    N = 50
    f = math.sin
    (x,t) = generateDataset(N, f, 0.03);
    makePlot(N, f, x, t)
    
if __name__ == '__main__':
    main() 