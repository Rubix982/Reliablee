import collections


class LFUCache:
    def _init_(self, capacity):
        self.remain = capacity
        self.least_freq = 1
        self.node_for_freq = collections.defaultdict(collections.OrderedDict)
        self.node_for_key = dict()

    def _update(self, key, value):
        _, freq = self.node_for_key[key]
        self.node_for_freq[freq].pop(key)
        if len(self.node_for_freq[self.least_freq]) == 0:
            self.least_freq += 1
        self.node_for_freq[freq+1][key] = (value, freq+1)
        self.node_for_key[key] = (value, freq+1)

    def get(self, key):
        if key not in self.node_for_key:
            return -1
        value = self.node_for_key[key][0]
        self._update(key, value)
        return value

    def put(self, key, value):
        if key in self.node_for_key:
            self._update(key, value)
        else:
            self.node_for_key[key] = (value, 1)
            self.node_for_freq[1][key] = (value, 1)
            if self.remain == 0:
                removed = self.node_for_freq[self.least_freq].popitem(
                    last=False)
                self.node_for_key.pop(removed[0])
            else:
                self.remain -= 1
                self.least_freq = 1
