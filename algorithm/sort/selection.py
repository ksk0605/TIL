""" 
초기:       [5, 3, 1, 4, 2]

1단계: 최소값 1 → 첫 번째 값과 교환  
          ↓
          [1, 3, 5, 4, 2]

2단계: 최소값 2 → 두 번째 값과 교환  
          ↓
          [1, 2, 5, 4, 3]

3단계: 최소값 3 → 세 번째 값과 교환  
          ↓
          [1, 2, 3, 4, 5]

4단계: 이미 정렬됨
"""

def selection(l : list[int]) -> None: 
    L = len(l)
    for i in range(L): 
        for j in range(i+1, L):
            if l[i] > l[j]: 
                l[i], l[j] = l[j], l[i] 
        print(l)

l = [5, 3, 1, 4, 2]

selection(l)