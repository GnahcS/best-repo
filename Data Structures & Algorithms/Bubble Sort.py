def bubbleSort(nums):
    n = len(nums)
    
    # Bool that checks for swaps. If no swaps were made during an iteration the list is sorted
    swappped = False

    # Iterates through the whole list comarping value pairs. Swaps them if they are unordered  
    for i in range(n):
        print(nums)
        for j in range(1, n):
            if nums[j-1] <= nums[j]:
                swapped = False
            else:
                temp = nums[j-1]
                nums[j-1] = nums[j]
                nums[j] = temp
                swapped = True

        if swapped == True:
            return




nums = [1,3,4,6,2,13,1,6,7,8,6,11]
bubbleSort(nums)
print(nums)