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
