# 성능과 안정성을 염두하며 개발 공부 하기

## 배운 것을 성능과 안정성 관점에서 잘 써먹으려고 해보자 

### CASE 1 
> Transaction Atomicity : 하나의 트랜잭션 내에 있는 모든 쿼리는 모두 성공하거나 실패해야 한다. 

이런 내용을 공부했다고 하자. **이걸 달달 외우고 넘어가면 안된다.** 

#### 계좌 이체 예제
> UPDATE accounts SET balance = balance - 100000 WHERE account_id = 100;   
> 여기까지만 실행되었는데 중간에 문제가 생겼다면?  
> UPDATE accounts SET balance = balance + 100000 WHERE account_id = 200;   

트랜잭션이라는 개념을 몰랐다면 위의 경우에 안정성/데이터 불일치 문제를 만날 수 있다는 사실을 이해하자. 이걸 나중에 개발할 때 Transcation을 잘 염두해야겠다는 생각을 해야함. 

#### 구매 후기 작성 시 쿠폰 발급 
> 구매 후기 테이블에 insert  
> 쿠폰 발급 테이블에 insert

어플리케이션 기능을 구현할 때 두 쿼리가 atomic 하게 작동하지 않으면, 구매 후기를 작성했는데 쿠폰이 발급되지 않는다든지 하는 이슈가 발생할 수 이쓴ㄴ 것.

### CASE 2 
> race condition: 두 개 이상의 스레드들이 공유 데이터에 접근할 때 예상과 다른 동작이 발생하는 현상 

해결책으로 syncronized, lock, Atomic Type, thread-safe 클래스 등등을 배웠다고 하자. 

```java 
@Service 
public class IdtoName { 

    private final Map<String, String> idToName = new HashMap<>();

    public void update(String id, String name) { idToName.put(id, name); }

    public String getBy(String id) { return idToName.get(id); }
}
```

멀티스레드 환경에서, 위 코드에서 발생할 수 있는 문제를 예상해보자.  
1. @Service 에 의해 스프링 빈으로 관리된다. 
2. 따라서 IdToName 은 Singleton 으로 관리된다. 
3. 멀티스레드 환경에서 하나의 IdToName 객체에 접근하게 된다면 내부의 hashMap idToName 변수는 공통접근이 가능한 변수가 된다. 
4. 따라서 update 함수의 동작에 의해 간헐적으로 race condition 이 발생할 수 있다. 

```java 
@Service 
public class IdtoName { 

    private final Map<String, String> idToName = new ConcurrentHashMap<>();

    public void update(String id, String name) { idToName.put(id, name); }

    public String getBy(String id) { return idToName.get(id); }
}
```

해결책 중 하나로 ConcurrentHashMap을 활용하는 것이 있다. Thread-safe 개념을 활용한 예제. 

## 비슷한 종류는 성능이나 안정성 관점에서 비교해서 정리해보자

### CASE 1 
자바는 멀티스레딩 환경인데 Thread-safe 한 StringBuffer를 써야지! 
```java 
@Service 
class MultiThreadSafe { 
    public String makeGreetingMsg(String userId){ 
        User user = repository.findBy(userId); 
        StringBuffer buffer = new StringBuffer(); 
        buffer.append("Hello, ").append(user.name); 
        // ... 
        return buffer.toString();
    }
}
```
과연 잘 해결한 것이 맞을까? 사실 위 예제에서는 꼭 StringBuffer를 사용할 필요가 없다. 왜냐하면 함수 내 지역변수이기 때문에 애초에 크리티컬 섹션이 아니기 때문. 그럼 위에서 StringBuilder 를 사용하는 건 안되는 걸까? 

```java 
@Service 
class MultiThreadSafe { 
    public String makeGreetingMsg(String userId){ 
        User user = repository.findBy(userId); 
        StringBuilder buffer = new StringBuilder(); 
        buffer.append("Hello, ").append(user.name); 
        // ... 
        return buffer.toString();
    }
}
```

StringBuffer 는 스레드 안전한 대신 내부적으로 더 많은 작업으로 인해 StringBuilder에 비해 성능이 느리다. 그래서 StringBuilder로 교체하더라도 사실 문제가 없고 오히려 성능적으로 더 좋다. 

#### 예시들 
1. StringBuffer vs StringBuilder 
2. HashMap vs ConcurrentHashMap
3. List vs Set
    * JAVA의 경우 많이 쓰는 ArrayList / HashSet 자료형이 있음. 둘다 동일하게 동작은 한다. 둘다 contains 를 제공하기 때문에 특정 요소가 들어있는지는 쉽게 알 수 있지만 성능면에서는 O(1) 인 HashSet 이 O(n)인 ArrayList 보다 더 빠르다. 
4. SortedSet vs HashSet 
5. TreeMap vs HashMap 
6. ArrayList vs LinkedList 
    * ex. 단지 처음부터 끝까지 순회(traverse)할 것이라면, ArrayList를 쓰나 LinkedList를 쓰나 상관이 없을까요?
    * 둘다 O(n) 이니까 똑같지 않을까? 
    * 아니지 둘이 메모리에 저장하는 방식이 다르니까. 
    * ArrayList 는 내부적으로 배열로 작동, 메모리에 연속적으로 들어있기 때문에 빠르다. 
    * LinkedList 는 모든 노드가 연속적으로 존재한다는 보장이 없다. 그래서 참조값을 넘나드는 과정에서 성능이 느려질 수 있음. 
    * 캐시도 영향을 준다. [Cache Locality](https://velog.io/@lob3767/%EC%BA%90%EC%8B%9C%EC%9D%98-%EC%A7%80%EC%97%AD%EC%84%B1Cache-Locality)에 의해 확률적으로 더 Cache Hit 가 더 높은 것.
    * 꼬리질문 으로 캐시는 한번에 몇 바이트나 읽어올까...

## 병목 지점은 성능에 안좋은 영향을 줄 가능성이 있다

### CASE 1 
락을 통해 [mutual exclusion(상호배제)](https://ko.wikipedia.org/wiki/%EC%83%81%ED%98%B8_%EB%B0%B0%EC%A0%9C)을 보장해야 하는 상황. 즉 한번에 하나의 스레드만 접근해야하는 상황. 

```java 
@Service 
class ExclusiveService { 
    private ReentrantLock lock = new ReentrantLock(); 

    public void callExclusively() { 
        lock.lock(); 
        try { 
            // Critical Section
            targetClient.updateResult(...); // HTTP 호출
        } finally { 
            lock.unlock();
        }
    }
}
```

**정말 Critical Section 에 들어가야 하는가?** HTTP 호출은 상대적으로 오래걸리는 작업이다. 락은 결국 줄을 세우는 일인데 HTTP 호출을 락을 건 상태에서 작업하게 된다면 결과적으로 성능이 느려지는 병목지점이 된다.  

예를들어 큐를 사용하더라도 모든 스레드가 하나의 큐에 접근하게 된다면 이것 또한 병목지점이 될 가능성이 있다. 그럼 여러개의 큐를 두어서 작동하게 하면 안될까? 라는 아이디어를 적용한 것이 topic별 다수의 병렬작업이 가능한 Kafka가 있다. 

### CASE 2
DBCP의 max 와 min 값을 다르게 준 상황(min:2, max:6) 이때 트래픽이 값자기 몰리면 서버들이 한번에 DB와 커넥션을 맺는 시도를 하게 된다. 모든 서버가 DB와 커넥션을 급격하게 늘리려는 시도를 하는 동안에 커넥션은 3 way handshake 와 같은 긴 작업들로 인해 데이터베이스 커넥션 풀이 병목이 된다. 계속해서 요청은 들어오고 스레드 풀이 커넥션 풀을 받기까지도 기다리게 된다면 스레드풀 소모가 점점 늘어나고 결과적으로, Tomcat 스레드 풀까지 모두 소진하게 되면 서버가 죽는 상황이 발생할 수도 있는 것.

## 성능의 어느 부분이 좋아지는건가? 
Netty가 Tomcat 보다 좋다고 하는데 성능이 어떤 면에서 좋은건가? 

|  | Tomcat | Netty |   
| ----- | ---- | --- |   
| 동작 방식  | Thread per request (요청 당 스레드 할당) | EventLoop (적은 스레드로도 많은 요청을 처리) |   
| 스레드 수(default) | 10 to 200 | core 수 x 2배 | 

throughput(처리량)이 눈에 띄게 좋아지는 것 (response time 이 아니라)
성능이 어느관점에서 좋아지는 건지 잘 이해해야한다. API 응답 속도가 빨라지는 것이 아니다. Netty가 성능을 좋아지니까 써야지~ 라는 생각은 매우 얕다. 트래픽이 많이 몰릴때도 안정적으로 작동할 수 있을 뿐. 

즉, 잘 이해하고 쓰자!

#### 그외 예시 
* 동작 원리를 바탕으로 성능까지 연결시켜 생각하기   
    -> clustered index 의 동작원리를 이해하면 primary key는 랜덤 값으로 잡는 것을 조심하게 된다. 
    -> JVM의 GC를 알면 stop the world의 존재를 인지하게 된다. 
* SPOF(single point of failure)를 경계할 것 
* 리소스의 한계를 고려할 것  
    -> kafka 파티션 개수는 몇 개 까지가 적절할까? 
    -> 스레드 개수는 몇 개 까지가 적절할까? 