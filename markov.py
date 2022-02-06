import numpy as np
def matrix_power(A, n):
    # This function computes A^n
    m = A.shape[0]
    X = np.identity(m, dtype = float)
    for i in range(n):
        X = np.matmul(X, A)
    return X

def markov(pricevec, n):
    markovprice = pricevec[-6:]
    updown = []
    counterup = 0
    counterdown = 0
    for i in range(len(markovprice)-1):
        if (markovprice[i]<markovprice[i+1]):
            updown.append(1)
            counterup+=1
        else:
            updown.append(2)
            counterdown+=1
    last_day_grow = markovprice[len(markovprice)-2] < markovprice[len(markovprice)-1]
    if last_day_grow:
        counterup-=1
    else:
        counterdown -= 1
    p11=0
    p12=0
    p21=0
    p22=0
    for i in range(1, len(markovprice)-1):
        prev = markovprice[i-1]
        curr = markovprice[i]
        pred = markovprice[i+1]
        if prev < curr < pred:
            p11 += 1
        elif prev >= curr >= pred:
            p22 += 1
        elif prev < curr and curr >= pred:
            p12 += 1
        else:
            p21 += 1

    m11= p11/counterup
    m12= p12/counterup
    m21= p21/counterdown
    m22= p22/counterdown

    A = np.array([[m11, m12], [m21,m22]])

    vec = None
    if last_day_grow:
        vec = np.array([1, 0])
    else:
        vec = np.array([0, 1])

    def get_nth_day(vec, A, n):
        AtoN = matrix_power(A, n)
        return vec.dot(AtoN)

    return get_nth_day(vec, A, 10)
