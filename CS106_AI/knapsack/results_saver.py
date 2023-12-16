import os
from os.path import join, isfile, isdir
import time

class results_saver:
    
    def __init__(self, output_dir):
        assert(isdir(output_dir))
        self.output_dir = output_dir

        self.marked_files = []

        self.mark = str(time.time())

    
    def mark_if_new_session(self, path):
        """return True if unmarked"""
        if path not in self.marked_files:
            self.marked_files.append(path)
            with open(path, 'a') as f:
                f.write("\n\n########### " + str(self.mark) + " ###########\n\n")
                
            return True
        return False
    
    def save(self, test_info ,total_value, total_weight, runtime, is_optimal, values, weights):
        # save total_value, total_weight, runtime, is_optimal to results.csv
        csv_path = join(self.output_dir, "results.csv")


        is_new = self.mark_if_new_session(csv_path)

        f = open(csv_path, "a")

        if is_new:
            for key in test_info:
                f.write(key + ", ")
        
            f.write("total_value, total_weight, runtime, is_optimal\n")
        
        for key in test_info:
            f.write(test_info[key] + ", ")
        
        f.write(str(total_value) + "," + str(total_weight) + "," + str(runtime) + "," + str(is_optimal) + "\n")

        f.close()

        # save values, weights to type.txt
        txt_path = join(self.output_dir, test_info["type"] + "_re.txt")

        is_new = self.mark_if_new_session(txt_path)

        f = open(txt_path,"a")

        f.write(test_info["path"] + "\n")
        f.write(str(len(values)) + "\n")

        for v in values:
            f.write(str(v) + " ")
        
        f.write("\n")
        
        for w in weights:
            f.write(str(w) + " ")
        
        f.write("\n")
        
        f.close()
    

