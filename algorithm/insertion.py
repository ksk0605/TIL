"""
[더 일반적인 경우]
뒤에서부터 더 클때 밀어주기만 하면 됨.

def insertion_sort(l: list[int]) -> None:
    for i in range(1, len(l)):
        target = l[i]
        j = i - 1
        while j >= 0 and l[j] > target:
            l[j + 1] = l[j]  # 값 밀기
            j -= 1
        l[j + 1] = target  # 삽입

"""

def insertion_sort(l : list[int])->None: 
    L = len(l)
    for i in range(L): 
        print(str(i+1) + "번째")
        for j in range(0, i): 
            target = l[i]
            if l[j] > l[i]:
                for k in reversed(range(j+1, i+1)):
                    l[k] = l[k-1] 
                l[j] = target
                break

        print(l)

l = [5, 3, 1, 4, 2]
insertion_sort(l)