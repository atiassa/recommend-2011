import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import math

def generateDataset(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    t = [f(xi) + np.random.normal(0.0, sigma, 1)[0] for xi in x]
    return (x,t)

def phi(x,M):
    fi = np.array([math.pow(x, i) for i in np.arange(0,M+1)])
    return fi.T 

def bayesianEstimator(X, t, M, alpha, sigma2):
    I = np.eye(M+1)          
    B = (1.0/sigma2)
    def m(x):
        S = np.linalg.inv(alpha*I + B*sum([np.dot(phi(xn,M),phi(xn,M).T) for xn in X]))
        phix = phi(x,M)
        BxTs = B * np.dot(phix.T, S)
        v = sum([np.dot(phi(xn,M), tn) for xn,tn in zip(X,t)])
        return v*BxTs
    
    def var(x):
        S = np.linalg.inv(alpha*I + B*sum([np.dot(phi(xn,M),phi(xn,M).T) for xn in X]))
        phix = phi(x,M)
        phiTS = np.dot(phix.T, S)
        return sigma2 + np.dot(phiTS, phix) 
       
    return (m, var)

def drawPlot(x, t, f, m, var):
    vf = np.vectorize(f)
    vm = np.vectorize(m)
    vvar = np.vectorize(var)
    y = vf(x)
#    ym = vm(x)   ##########################3
#    yvar = vvar(x)
#    yvarup = ym + math.pow(yvar(x),0.5)
#    yvardown = ym - math.pow(yvar(x),0.5)
    fig = plt.figure()
    sizes = 100
    ax = fig.add_subplot(111)
    ax.scatter(x,t, s=sizes,marker= 'o',edgecolors ='blue', facecolor='none' )
    plt.plot(x,y,lw=2,color= 'green')
    plt.plot(x,y+.03,lw=2,color= 'red')
    plt.plot(x,y-.03,lw=2,color= 'red')
#    plt.plot(x,yvarup,lw=2,color= 'red' ,alpha=0.2)
#    plt.plot(x,yvardown,lw=2,color= 'red',alpha=0.2)
    #plt.plot(x,y,lw=100,color= 'red', alpha=0.2)
    plt.show()

def main():
    N = 100
    f = math.sin
    (x,t) = generateDataset(N, f, 0.03);
    alpha = 0.005
    sigma2 = 1/11.1
    M = 9 
    (m,var) = bayesianEstimator(x, t, M, alpha, sigma2)
    drawPlot(x, t, f, m, var)
    
if __name__ == '__main__':
    main() 