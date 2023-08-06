import random
class RandAlph:
    def __init__(self, num):
        self.num = num
    def rand(self):
        x = [chr(random.randint(65,91)) for x in range(self.num)]
        x = "".join(x)
        return x