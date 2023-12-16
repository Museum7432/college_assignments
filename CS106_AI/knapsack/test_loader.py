from collections import deque
import os
from os.path import join, isfile
import re

def list_directories(path):
    return [f for f in os.listdir(path) if not isfile(f)]

class test_loader:
    def __init__(self, root_path):
        self.root_path = root_path
    
    def load_types(self):
        """load first"""
        dirs = list_directories(self.root_path)
        matched = [d for d in dirs if re.search(r"[0-9][0-9][A-Za-z]+$", str(d))]
        self.types = sorted(matched)
        return self.types

    def set_types(self, test_type):
        assert(test_type in self.types)

        self.type = test_type
    
    def get_type(self):
        return self.type
    
    def load_sizes(self):
        """load second, after type"""
        assert(self.type)
        dirs = list_directories(join(self.root_path,self.type))
        matched = [d for d in dirs if re.search(r"n[0-9]+$", str(d))]
        self.sizes = sorted(matched)
        return self.sizes
    
    def set_size(self, test_size):
        assert(test_size in self.sizes)
        self.size = test_size
    
    def get_size(self):
        return self.size
    
    def load_ranges(self):
        """load third, after size"""
        assert(self.size)

        dirs = list_directories(join(self.root_path,self.type,self.size))
        matched = [d for d in dirs if re.search(r"R[0-9]+$", str(d))]
        self.ranges = sorted(matched)
        return self.ranges
    
    def set_range(self, test_range):
        """load fourth, after range"""
        assert(test_range in self.ranges)

        self.range = test_range
    
    def get_range(self):
        return self.range
    
    def load_tests(self):
        assert(self.range)

        dirs = list_directories(join(self.root_path,self.type,self.size, self.range))
        matched = [d for d in dirs if re.search(r"s[0-9]+\.kp$", str(d))]
        self.tests = sorted(matched)
        return self.tests

    def set_test(self,test_name):
        assert(test_name in self.tests)
        self.test = test_name
    
    def get_test_name(self):
        return self.test
    
    def get_test_path(self):
        return join(self.root_path,self.type,self.size, self.range, self.test)
    
    def get_info(self):
        info = dict()
        
        info["type"] = self.type

        info["size"] = self.size

        info["range"] = self.range

        info["name"] = self.test

        info["path"] = self.get_test_path()

        return info

    def _read_raw(self):
        path = self.get_test_path()

        raw = deque([])
        with open(path, 'r') as f:
            for line in f:
                for s in line.split():
                    raw.append(int(s))
        return raw
    
    def parse_test(self):
        raw = self._read_raw()

        no_items = raw.popleft()
        capacities = [raw.popleft()]

        values = []

        weights = []

        for i in range(no_items):
            values.append(raw.popleft())
            weights.append(raw.popleft())
    
        return no_items, capacities, values, [weights]

 




# def test(path):
#     loader = test_loader(path)
#     test_types = loader.load_types()
#     loader.set_types(1)

#     test_sizes = loader.load_sizes()
#     loader.set_sizes(1)

#     test_ranges = loader.load_ranges()
#     loader.set_range(1)

#     tests = loader.load_tests()
#     loader.set_test(11)

#     print(loader.parse_test())
