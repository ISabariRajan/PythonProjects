from os.path import abspath, dirname, join as joinpath
import core


script_dir = dirname(abspath(__file__))
input_file = joinpath(script_dir, "input.txt")
input_lines = []
pattern_indexes = []
with open(input_file, "r") as f:
    input_lines = f.readlines()

pattern_file = joinpath(script_dir, "patterns.txt")
patterns = []
with open(pattern_file, "r") as f:
    patterns = f.readlines()
# print(input_lines, patterns)
core_obj = core.Core()

def test():
    output = {}
    for pattern in patterns:
        output[pattern] = []
        pattern = pattern.replace("\n", "")
        count = 0
        # indexes = []
        for line in input_lines:
            core_obj.set_text(line)
            # print(line)
            pattern_indexes = core_obj.find_patterns_in_text(pattern)
            # indexes = pattern_indexes
            output[pattern] = pattern_indexes
        # for line in input_lines:
        #     if pattern in line:

        #         print("Found " + pattern + " In " + str(line.index(pattern)))
        #         print(line)

            # output.append((pattern, pattern_indexes, count))
    return output