import heap.Heap;

public class App {
    public static void main(String[] args) throws Exception {
        var heap = new Heap();
        heap.insert(6);
        heap.insert(2);
        heap.insert(1);
        heap.insert(5);
        heap.insert(4);
        heap.insert(2);
        System.out.println(heap);
        System.out.println("-----------------");
        heap.poll();
        System.out.println(heap);
        System.out.println("-----------------");
        heap.poll();
        System.out.println(heap);
    }
}
