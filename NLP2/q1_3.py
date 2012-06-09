import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import math

# returns 3 pairs of vectors of size N each,
# (x-test, t-test), (x-validate, t-validate) and (x-train, t-train).
# The target values are generated with Gaussian noise N(0, sigma).
def  generateDataset3(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=3*N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    pairs = [(xi, f(xi) + np.random.normal(0.0, sigma, 1)[0]) for xi in x]
    np.random.shuffle(pairs) 
    test = pairs[:N]
    train = pairs[N:N*2]
    dev =pairs[N*2:]
    xts , tts = zip(*test)
    xtr , ttr = zip(*train)
    xdv , tdv = zip(*dev)
    return ((xts,tts),(xtr,ttr),(xdv,tdv))

# y(x) = w0 + w1x + w2x^2 + ... + wMx^M
def Y(w,x):
    return sum([wk*(math.pow(x,k)) for k,wk in enumerate(w)])

# The normalized error of the model-
# NEw = ....
def normalized_error(w,x,t):
    return (1.0/len(t))*math.pow(sum([math.pow(ti - sum([wm*math.pow(xi, m) for m,wm in enumerate(w)]) , 2) for xi,ti in zip(x,t)]), 0.5)

# returns the optimal polynomial of degree M that approximates the dataset 
# according the least squares objective
def optimizePLS(x, t, M, lamda):
    design_matrix = np.array([[math.pow(xi,m) for m in np.arange(M+1)] for xi in x])  # This is A
    prod = np.dot(design_matrix.T, design_matrix)      # prod is (AT*A)
    lamdaI = lamda*np.eye(M+1)                         # id is lamda*I
    s = prod + lamdaI                                  # s is ((AT*A) + lamda*I)
    i = np.linalg.inv(s)                               # i is (s^-1)
    m = np.dot(i, design_matrix.T)                     # m is (i*AT)
    W_LS = np.dot(m, t)                                # w is (m*t)
    return W_LS

# selects the best value lambda given a dataset for
# training (xt, tt) and a validation test (xv, tv)
def optimize_PLS(xtr, ttr, xv, tv, M):
    bestNE = 100;
    for i in np.arange(-20,6):
        lamda = math.pow(math.e, i)
        w = optimizePLS(xtr, ttr, M, lamda)
        e = normalized_error(w,xv,tv)
        if(e < bestNE):
            bestNE = e
            WPLS = w 
    return WPLS

def normalized_errorPlot(sets, M ):
    (xts,tts) = sets[0] # test 
    (xtr,ttr) = sets[1] # train
    (xv,tv) = sets[2] # dev
    x = [] 
    val = []
    train = []
    test = []
    for i in np.arange(-20,6):
        x.append(i)       
        lamda = math.pow(math.e, i)
        w1 = optimizePLS(xtr, ttr, M, lamda)
        e = normalized_error(w1,xv,tv)
        train.append(e)    
        e = normalized_error(w1,xts,tts)
        test.append(e)
    plt.title('N = %d' % len(tv))
    plt.plot(x,train,lw=1,color= 'blue')
    plt.plot(x,test,lw=1,color= 'red')
    plt.legend(( 'Train', 'Test'),'upper center', shadow=True)
    plt.xlabel('ln(lambda)')
    plt.ylabel('NE')
    plt.show()
    
def makeSinPlot(sets,f,M):
    (xts,tts) = sets[0] # test 
    (xtr,ttr) = sets[1] # train
    (xv,tv) = sets[2] # dev
    xy =np.linspace(0.0, 1.0, num=100)
    vf = np.vectorize(f)
    y = vf(xy)
    fig = plt.figure()
    wls = optimize_PLS(xtr, ttr, xv, tv, M)
    w = [Y(wls,xi) for xi in xy]
    ax = fig.add_subplot(111)
    ats = ax.scatter(xts,tts, s=50,marker = 'o', edgecolors ='red' , facecolor='none' )
    atr = ax.scatter(xtr,ttr, s=50,marker = 'o', edgecolors ='blue' , facecolor='none' )
    av = ax.scatter(xv,tv, s=50,marker = 'o', edgecolors ='green' , facecolor='none' )
    plt.plot(xy,w,'r-')
    plt.plot(xy,y,'g-')
    plt.legend([ats,atr,av],['Test' , 'Train' , 'Development'],'upper right', shadow=True)
    plt.show()

    
def main():
    N = 10
    def f(x): return math.sin(2*math.pi*x)
    sets = generateDataset3(N, f, 0.03)
    normalized_errorPlot(sets, 9)
    makeSinPlot(sets,f,9)
    N = 100
    sets = generateDataset3(N, f, 0.03)
    normalized_errorPlot(sets, 9)
    makeSinPlot(sets,f,9)
    
if __name__ == '__main__':
    main() 