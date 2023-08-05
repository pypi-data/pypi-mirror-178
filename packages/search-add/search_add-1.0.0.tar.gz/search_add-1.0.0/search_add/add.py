
def add (x,y):
    array = []
    for N in range(x, y + 1):
        if N > 1:
            for i in range(2, N):
                if (N % i) == 0:
                    break
            else:
                # print(N)
                array.append(N)
    return array
