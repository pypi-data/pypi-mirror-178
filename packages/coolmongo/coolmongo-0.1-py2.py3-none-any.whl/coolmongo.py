from collections import deque


class coolmongo():
    def __init__(self, mkconn):
        self.mkconn = mkconn
        self.pool = deque([])

    def append(self, obj):
        self.pool.append(obj)
    
    def get(self):
        try:
            return self.pool.popleft()
        except:
            return self.mkconn()
