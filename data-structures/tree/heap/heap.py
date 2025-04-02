class Heap: 
    def __init__(self):
        self.hq = []

    def add(self, num): 
        self.hq.append(num)
        self.__up()

    def pop(self): 
        num = self.hq[0]
        self.hq[0] = self.hq[-1]
        self.hq.pop()
        self.__down()
        return num

    def __up(self) -> None:
        curr = len(self.hq) - 1

        while self.__parent(curr) >= 0 and self.hq[self.__parent(curr)] > self.hq[curr]: 
            self.hq[self.__parent(curr)], self.hq[curr] = self.hq[curr], self.hq[self.__parent(curr)]
            curr = self.__parent(curr)

    def __down(self) -> None: 
        curr = 0 

        last = len(self.hq) - 1

        leftchild = self.__left_child(curr)
        rightchild = self.__right_child(curr)
        
        while leftchild <= last: 
            if rightchild <= last: 
                if self.hq[leftchild] >= self.hq[curr] and self.hq[rightchild] >= self.hq[curr]: 
                    break

                if self.hq[leftchild] < self.hq[rightchild]: 
                    self.hq[leftchild], self.hq[curr] = self.hq[curr], self.hq[leftchild]
                    curr = leftchild
                    leftchild = self.__left_child(curr)
                    rightchild = self.__right_child(curr)
                else: 
                    self.hq[rightchild], self.hq[curr] = self.hq[curr], self.hq[rightchild]
                    curr = rightchild
                    leftchild = self.__left_child(curr)
                    rightchild = self.__right_child(curr)
                continue
            else: 
                if self.hq[leftchild] >= self.hq[curr]: 
                    break
                else:
                    self.hq[leftchild], self.hq[curr] = self.hq[curr], self.hq[leftchild]
                    curr = leftchild
                    leftchild = self.__left_child(curr)
                    rightchild = self.__right_child(curr)


        
    def __parent(self, child) -> int: 
        return (child - 1) // 2
    
    def __left_child(self, parent) -> int: 
        return parent * 2 + 1
    
    def __right_child(self, parent) -> int: 
        return parent * 2 + 2
