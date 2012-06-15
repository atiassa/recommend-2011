import matplotlib.pyplot as plt
import math
import numpy as np

# return a tuple with the 2 vectors x and t
# where the xi values are equi-distant on the [0,1] segment (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
# and t is ti = y(xi) + Normal(mu, sigma)
def generateDataset(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    t = [f(xi) + np.random.normal(0.0, sigma, 1)[0] for xi in x]
    return (x,t)

def makePlot(N, f, x, t, sigma):
    vf = np.vectorize(f)
    xx = np.linspace(0.0, 1.0, num=100)
    y = vf(xx)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,t, s=50,marker= 'o',edgecolors ='blue', facecolor='none' )
    plt.plot(xx,y,lw=1,color= 'g')
    plt.title('sigma = %.2f' % sigma)
    plt.show()
 
def main():
    N = 50
    sigma = 00.3
    def f(x):
        return math.sin(2*math.pi*x)
    (x,t) = generateDataset(N, f,sigma);
    makePlot(N, f, x, t , sigma)
    
if __name__ == '__main__':
    main() 