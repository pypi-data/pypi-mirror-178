def bubble_sort(input_list):
    """
        Input:
            input_list is the list provided as input.
        Output:
            Returns and changes the original input_list to a sorted list.
    """
    input_list_length = len(input_list)

    for pointer1 in range(input_list_length):

        for pointer2 in range(input_list_length-pointer1-1):

            if input_list[pointer2] > input_list[pointer2 + 1] :

                temp = input_list[pointer2]
                input_list[pointer2] = input_list[pointer2+1]
                input_list[pointer2+1] = temp
    
    return input_list     


def selectionSort(input_list):
    input_list_length = len(input_list)

    for currrent in range(input_list_length):
        min_index = currrent

        for i in range(currrent + 1, input_list_length):

            # to sort in descending order, change > to < in this line
            # select the minimum element in each loop
            if input_list[i] < input_list[min_index]:
                min_index = i

        # put min at the correct position
        (input_list[currrent], input_list[min_index]) = (input_list[min_index], input_list[currrent])
    return input_list

