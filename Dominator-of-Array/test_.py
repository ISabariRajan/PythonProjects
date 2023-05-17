import sys
import random
import main

# Randomly generate numbers between -9 to 9 for testing purpose
# Calls "find_dominator_of_array" then returns the array and output
def do_testing():
    array_obj = []
    value = 1
    # loops untils value is anything but 0
    while(value != 0):
        value = random.randint(-9, 9)
        array_obj.append(value)
        while(random.randint(0,1)):
            array_obj.append(value)

    # Find Dominator of Array
    index = main.find_dominator_of_array(array_obj, len(array_obj))
    print()
    print("The Test Array: " + str(array_obj))
    print("Dominator index: " + str(index))

n = int(sys.argv[1])
for i in range(0, n):
    do_testing()