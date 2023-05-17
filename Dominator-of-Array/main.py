def find_dominator_of_array(array_obj, array_length):
    array_counter = {}

    max = 1
    index = -1
    i = 0
    # loop through each element and adds to counter map
    for key in array_obj:
        if (key in array_counter):
            array_counter[key] += 1
        else:
            array_counter[key] = 1
        
        # Also checks if the count of an element is the highest count and store its index
        # value = array_counter[key]
        # if(value > max):
        #     max = value
        #     index = i
        # If maximum count is grater than half array length, then return index of the element
        if(array_counter[key] > (array_length//2)):
            return i
        i += 1

    # If no element count is greater than half array length then return -1
    return -1


if __name__ == "__main__":
    array_obj = [2, -3, -3, 5, 3, 3, -4, -4, -4, -4, -4, -4, -4, -4, -4, 0]
    index = find_dominator_of_array(array_obj, len(array_obj))
    print(index)