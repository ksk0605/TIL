package heap;

import java.util.ArrayList;
import java.util.List;

public class Heap {
    private final List<Integer> heap = new ArrayList<>();

    public void insert(int value) {
        heap.add(value);
        if (heap.size() == 1)
            return;
        upHeap(heap.size() - 1);
    }

    public int poll() {
        if (heap.isEmpty()) {
            throw new IllegalStateException("힙이 비어있음");
        }
        var value = heap.get(0);
        if (heap.size() == 1) {
            heap.remove(0);
        } else {
            downHeap(heap.size() - 1);
        }
        return value;
    }

    public int peek() {
        if (heap.isEmpty()) {
            throw new IllegalStateException("힙이 비어있음");
        }
        return heap.get(0);
    }

    private void upHeap(int index) {
        int child = index;
        while (heap.get(child) < heap.get((child - 1) / 2)) {
            int parent = (child - 1) / 2;
            swap(child, parent);
        }
    }

    private void downHeap(int index) {
        heap.set(0, heap.get(index));
        heap.remove(index);

        int parent = 0;
        int size = heap.size();

        while (true) {
            int left = leftChild(parent);
            int right = rightChild(parent);
            int smallest = parent;

            if (left < size && heap.get(left) < heap.get(smallest)) {
                smallest = left;
            }

            if (right < size && heap.get(right) < heap.get(smallest)) {
                smallest = right;
            }

            if (smallest == parent)
                break;

            swap(parent, smallest);
            parent = smallest;
        }
    }

    private int leftChild(int index) {
        return index * 2 + 1;
    }

    private int rightChild(int index) {
        return index * 2 + 2;
    }

    private void swap(int i, int j) {
        int tmp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, tmp);
    }

    @Override
    public String toString() {
        var sb = new StringBuilder();
        int level = 0;
        int count = 0;
        int maxCount = 1;

        for (int i = 0; i < heap.size(); i++) {
            sb.append(heap.get(i)).append(" ");
            count++;

            if (count == maxCount) {
                sb.append("\n");
                level++;
                count = 0;
                maxCount = (int) Math.pow(2, level);
            }
        }

        return sb.toString();
    }
}
