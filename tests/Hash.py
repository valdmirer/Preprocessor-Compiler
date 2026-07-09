class HASHash:

    def __init__(self, value=None):
        self.seed = 1
        self.value = self.SELECT(value.strip()) if value else value
        self.a = 1664_525
        self.c = 1013_904_223
        self.m = 2**32

    def SELECT(self, value):
        if value.strip():
            value = value.strip().replace(" ", '')
            mid = len(value) // 2
            quarter = len(value) // 4
            shuffled = value[mid:] + value[:mid] + value[quarter:] + value[:quarter]
            with_entropy = "".join(f"{i}{ch}" for i, ch in enumerate(shuffled))
            return ("".join(chr(ord(c) ^ (i % 7)) for i, c in enumerate(value))+
                    f"{len(value)}|{value}|{len(value)*7}"+
                    f"{len(value)}|{with_entropy}|{len(value)*7}"+
                    "".join(chr(ord(c) ^ (i % 7)) for i, c in enumerate(value))+
                    f"{len(value)}|{value}|{len(value)*7}")
        else:
            return ''

    def hash(self, value=None):
        if value:
            self.value = self.SELECT(value.strip())
            
        hashvalue = self.seed
        if isinstance(self.value, str):
            numeric = sum(ord(c) for c in self.value)
        else:
            numeric = int(self.value)
        hashvalue  = (self.a * hashvalue + self.c + numeric) % self.m
        return hashvalue % 10000

    def testCollisions(self, hashes):
        """Last minute resorting to a tortoise & hare algorithm for detecting any collions
        not worked on that much just a small test.
        """
        
        tortoise = hashes[0]
        hare = hashes[0]

        # Move tortoise by one step and hare by two steps until they meet
        while True:
            try:
                tortoise = hashes[tortoise]
            except Exception as E:
                print(E)
                return -1, hare == tortoise, hare, tortoise
            try:
                hare = hashes[hashes[hare]]
            except Exception as E:
                print(E)
                return -1, hare == tortoise, hare, tortoise
            if tortoise == hare:
                break

        # Phase 2: Finding the entrance to the cycle (the duplicate number).
        tortoise = hashes[0]
        while tortoise != hare:
            tortoise = hashes[tortoise]
            hare = hashes[hare]

        return hare

if __name__ == '__main__':
    import time
    from decimal import Decimal
    start_time = time.perf_counter()
    print(HASHash('ray ray').hash())
    end_time = time.perf_counter()
    execution_time = Decimal(end_time - start_time)
    print(execution_time)
    raise Exception(f"Execution time: {execution_time} seconds")
