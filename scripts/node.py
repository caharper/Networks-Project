class Node:
    def __init__(self, id, packetstream):
        self.id = id
        self.start_size = len(packetstream)
        self.packetstream = packetstream

    def get_num_remaining(self):
        return len(self.packetstream)

    def remove_flow(self):
        self.packetstream = self.packetstream[1:]

    def get_num_sent(self):
        return self.start_size - len(self.packetstream)

    def get_top_flow(self):
        return self.packetstream[0]

    def is_empty(self):
        if(len(self.packetstream) == 0):
            return True
        return False
