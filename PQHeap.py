# Emil Ludvig Henriksen , emhen16@student.sdu.dk
# Áron Török-Czirmay, artor22@student.sdu.dk

def extractMin(A:list):
    """
    Fjern elementet med mindst prioritet fra 
    prioritetskøen A og returner det
    """
    min_element = min_heap_minimum(A)
    A[0] = A[len(A) - 1]
    A.pop()
    min_heapify(A,0)
    return min_element

def insert(A:list,key):
    '''
    Indsæt elementet key i prioritetskøen A
    '''
    A.append(key)
    i = len(A) - 1
    while i > 0 and A[parent(i)] > A[i]:
        A[parent(i)], A[i] = A[i], A[parent(i)]
        i = parent(i)


def createEmptyPQ():
    '''
    Returner en ny, tom prioritetskø (en tom liste)
    '''
    A = []
    return A

def parent(i):
    return (i-1) // 2

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2

def min_heapify(A:list,i):
    l = left(i)
    r = right(i)

    if l <= len(A)-1 and A[l] < A[i]:
        smallest = l
    else:
        smallest = i
    if r <= len(A)-1 and A[r] < A[smallest]:
        smallest = r
    if smallest != i:
        A[i], A[smallest] = A[smallest], A[i]
        min_heapify(A,smallest)

def build_min_heap(A):
    for i in range(len(A)//2, -1, -1):
        min_heapify(A, i)

def min_heap_minimum(A:list):
    return A[0]

if __name__ == "__main__":
    A = [2,4,3,7,7,5,6,8,9]

    build_min_heap(A)

    min_element = extractMin(A)

    insert(A, 1)

    print(A)