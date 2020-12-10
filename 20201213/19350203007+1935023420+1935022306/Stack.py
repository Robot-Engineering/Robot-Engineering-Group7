class Stack(object):
    def __init__(self):
        self.stack = list()

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            # print(self.stack.pop())
            return self.stack.pop()

        else:
            raise LookupError('stack is empty!')

    def is_empty(self):
        return bool(self.stack)

    def top(self):
        return self.stack[-1]


class Queue(Stack):
    def __init__(self, max_queue):
        super().__init__()
        self.max_queue = max_queue

    def push(self, value):
        if len(self.stack) < self.max_queue:
            self.stack.append(value)
        else:
            self.drop()
            self.push(value)

    def drop(self):
        self.stack.pop(0)
