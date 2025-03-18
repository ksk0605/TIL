# 왜 리스트 슬라이싱은 for 반복문 보다 빠를까?

[백준 2531번 문제 회전 초밥](https://www.acmicpc.net/problem/2531)을 풀다가 문득 궁금증이 생겼다. 아래는 내가 작성한 풀이다. 

```python
import sys
n, d, k, coupon = map(int, sys.stdin.readline().split())

belt = [0] * n
for i in range(n): 
    belt[i] = int(sys.stdin.readline())

start = 0
maxd = 0
while start < n: 

    ## 리스트 슬라이싱(성공)
    if (start + k) <= n:
        cnt_belt = set(belt[start:start+k])
    else:
        cnt_belt = set(belt[start:])
        cnt_belt.update(belt[:(start+k)%n])
    cnt_belt.add(coupon)

    ## 반복문 방식 (시간초과)
    # print(cnt_belt)
    # for i in range(k):
    #     cnt_belt.add(belt[(start+i)%n])
    # print(cnt_belt)
    maxd = max(maxd, len(cnt_belt))
    start  = start + 1

print(maxd)
```

처음에는 주석처리한 반복문 방식으로 현재 내가 계산하고자 하는 윈도우(해당 문제는 슬라이드 윈도우 or 투 포인터 라고 부르는 유형의 문제)를 찾는 방식으로 풀었다. 그러나 이 방식은 시간초과가 났다. 그후 위 처럼 슬라이싱 윈도우를 적용했더니 무사히 통과한 걸 볼 수 있었다. 

왜 리스트 슬라이싱은 시간을 통과하고 
반복문은 통과하지 못했을까

## 리스트 슬라이싱 vs 반복문

Python의 리스트는 단순한 연결 리스트(Linked List)나 기본적인 배열(Array)이 아니라 **동적 배열 (Dynamic Array)**로 구현되어 있다.

**Python 리스트는 내부적으로 C 배열을 사용하여 요소를 저장**한다. 이는 C 배열의 특성 그대로, 연속된 메모리 블록을 할당하여 저장 (즉, 물리적으로 메모리상에서 연속됨) 한다는 것. 이때 **리스트 크기가 커질 경우 더 큰 메모리 블록을 할당한 뒤 복사(Resizing)** 하는 작업을 알아서 해주기 때문에 동적 배열이라고 부른다. 

파이썬에서 list[start:end]을 실행하면 내부적으로 새로운 리스트를 생성하면서 기존 리스트의 요소를 복사한다. 이 과정에서 Python이 C 언어의 저수준 메모리 복사 연산을 사용하여 매우 빠르게 수행된다.

### 파이썬 내부 구현 
실제 소스 코드를 보자. 

```c
static PyObject *
list_slice(PyListObject *a, Py_ssize_t ilow, Py_ssize_t ihigh)
{
    // 새로운 리스트 객체 생성
    PyListObject *np;
    Py_ssize_t i;
    
    // 새로운 리스트 크기 설정
    Py_ssize_t len = ihigh - ilow;
    if (len <= 0)
        return PyList_New(0);  // 빈 리스트 반환

    // 새로운 리스트를 메모리에 할당
    np = (PyListObject *) PyList_New(len);
    if (!np)
        return NULL;  // 메모리 할당 실패

    // 기존 리스트의 데이터를 새로운 리스트로 복사
    for (i = 0; i < len; i++) {
        PyObject *item = a->ob_item[i + ilow];  // 원본 리스트의 i번째 요소 가져오기
        Py_INCREF(item);  // 참조 카운트 증가
        np->ob_item[i] = item;  // 새로운 리스트에 복사
    }

    return (PyObject *)np;  // 새로운 리스트 반환
}
```
소스 코드에서 포인터를 활용한 매우 저수준 즉, 직접 메모리를 참조한 복사를 진행하는 것을 볼 수 있다. 그리고 매번 PyObject를 생성하는 list.append() 방식과 다르게 한번이 PyObject 를 생성하는 효율적인 연산이 가능하다는 것도 유추할 수 있다. 

### 반면 반복문은? 

Python에서 리스트를 복사하는 가장 기본적인 방법은 위 처럼 for 루프를 돌면서 요소를 하나씩 추가하는 것이다.

```python
old_list = [1, 2, 3, 4, 5]
new_list = []
for item in old_list:
    new_list.append(item)
```
python 슬라이싱의 내부 구현을 보았으니 위 코드가 왜 느릴 수 밖에 없는지 추측해볼 수 있다. 
1. for 문을 돌면서 Python 인터프리터가 각 요소를 하나씩 처리해야 한다.
2. append()를 호출할 때마다 **리스트의 크기가 증가하면서 메모리 재할당(reallocation)**이 발생할 수도 있다.
3. Python의 동적 타입 시스템(각 요소가 PyObject로 래핑됨) 때문에 오버헤드가 발생한다(슬라이싱은 1회만 래핑).

## 속도 테스트 해보기 
실제로 소스코드로 테스트 해보면 이렇다. 

```python 
import time

# 큰 리스트 생성
N = 10**7
lst = list(range(N))

# for 문을 이용한 복사 (느림)
start = time.time()
copy1 = []
for x in lst:
    copy1.append(x)
end = time.time()
print(f"for loop 복사 시간: {end - start:.5f} 초")

# 리스트 슬라이싱을 이용한 복사 (빠름)
start = time.time()
copy2 = lst[:]
end = time.time()
print(f"리스트 슬라이싱 복사 시간: {end - start:.5f} 초")
```
### 결과 
![테스트 결과](../../images/Screenshot%202025-03-18%20at%206.02.25 PM.png)
약 20배 정도 슬라이싱이 더 빠른 것을 확인할 수 있다. 이는 앞서 설명한 것처럼 슬라이싱이 C 레벨에서 최적화된 메모리 복사를 수행하기 때문이다.

## 결론

파이썬의 리스트 슬라이싱이 for 반복문보다 훨씬 빠른 이유는 다음과 같이 정리할 수 있다:

1. 슬라이싱은 C 레벨에서 구현된 최적화된 메모리 복사를 사용한다
2. 한 번의 메모리 할당으로 필요한 크기의 리스트를 생성한다
3. PyObject 래핑 작업이 한 번만 발생한다

반면 for 반복문은:
1. 파이썬 인터프리터가 각 요소를 개별적으로 처리해야 한다
2. append() 호출마다 메모리 재할당이 필요할 수 있다
3. 각 요소마다 PyObject 래핑이 발생한다

따라서 대량의 데이터를 다룰 때는 가능한 한 슬라이싱을 사용하는 것이 좋다. 이는 파이썬의 내부 구현을 이해하고 활용하는 좋은 예시가 된다.

# 레퍼런스 
* [파이썬 공식 레포](https://github.com/python/cpython/blob/c353764fd564e401cf47a5d9efab18c72c60014e/Objects/listobject.c#L440)
* [스택오버플로우](https://stackoverflow.com/questions/13203601/big-o-of-list-slicing/13203625)