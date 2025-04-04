# 정렬 알고리즘

## 버블 정렬 (Bubble Sort)
### 🔍 개념 설명
* 인접한 두 원소를 비교해서, 크기 순서에 맞지 않으면 서로 교환한다.
* 한 사이클 돌면 가장 큰 값이 맨 뒤로 간다.
* 최선의 경우 O(n), 최악의 경우 O(n^2), 평균 O(n^2)
* 거의 안씀, 더 좋은 알고리즘이 많음 
* [구현코드](https://github.com/ksk0605/TIL/blob/main/algorithm/sort/bubble.py)

## 선택 정렬 (Selection Sort)
### 🔍 개념 설명
* 매번 가장 작은 요소(또는 가장 큰 요소)를 선택해서 맨 앞자리와 교환하는 방식.
* 전체 리스트 중에서 가장 작은 값을 찾음
* 그것을 맨 앞 값과 교환
* 그 다음부터는 두 번째 자리부터 반복
* 결국 정렬 완료될 때까지 n-1번 반복
* [구현코드](https://github.com/ksk0605/TIL/blob/main/algorithm/sort/selection.py)

| 항목         | 선택 정렬 (Selection Sort) |
|--------------|-----------------------------|
| 시간복잡도    | O(n²) 항상 일정             |
| 공간복잡도    | O(1) (별도의 추가 자료구조 없이 주어진 배열 내에서 해결) |
| 정렬 안정성   | ❌ 불안정 정렬(원소들의 상대적 순서가 항상 보장 안됨)  |
| 특징          | 가장 작은 값을 선택해 교환  |
| 장점          | 구현이 쉽고 교환 횟수 적음  |
| 단점          | 느림, 실무에 거의 안 쓰임   |

## 삽입 정렬 (Insertion Sort)
### 🔍 개념 설명
* 앞쪽은 정렬된 구간, 뒤쪽은 정렬되지 않은 구간
* 하나씩 꺼내어 적절한 위치에 삽입하며 정렬을 확장하는 방식
* 왼쪽부터 하나씩 "꺼내서" 자신보다 큰 값들을 오른쪽으로 밀고 빈자리에 자신을 삽입
* [구현코드](https://github.com/ksk0605/TIL/blob/main/algorithm/sort/insertion.py)

| 항목         | 선택 정렬 (Selection Sort) |
|--------------|-----------------------------|
| 시간복잡도    | 최악 O(n²), 최선 O(n) 이미 정렬된 경우, 평균 O(n²)            |
| 공간복잡도    | O(1) |
| 정렬 안정성   | 안정 정렬  |
| 특징          | 거의 정렬된 배열에서 매우 빠름 |
| 실무          | 일부 정렬 알고리즘의 하위 로직으로 자주 쓰임 (예: Timsort -> Python의 sorted(), Java의 Arrays.sort() (객체 타입) 에서 실제로 사용) |


## 병합 정렬 (Merge Sort)

## 퀵 정렬 (Quick Sort)

## 힙 정렬 (Heap Sort)

## 계수 정렬 (Counting Sort)

## 기수 정렬 (Radix Sort)

## 셸 정렬 (Shell Sort, 선택)