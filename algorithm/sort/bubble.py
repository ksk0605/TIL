"""
실제 작동 흐름
5 3 1 4 2

3 5 1 4 2

3 1 5 4 2

3 1 4 5 2

3 1 4 2 5
"""


def bubble_sort(l : list[int]) -> None: 
    size = len(l)
    for i in range(size): 
        swapped = False
        for j in range(size-1 -i): 
            if l[j] > l[j+1]: 
                l[j], l[j+1] = l[j+1], l[j]
                swapped = True
        if not swapped: 
            break

l = [5, 3, 1, 4, 2]
bubble_sort(l)

print(l)