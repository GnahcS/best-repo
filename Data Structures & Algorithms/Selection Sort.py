def selection_sort(nums):
    for i in range(0, len(nums) - 1):
        print(nums)
        currentMinIndex = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[currentMinIndex]:
                currentMinIndex = j
        
        nums[i], nums[currentMinIndex] = nums[currentMinIndex], nums[i] #swap
    

nums = [1,3,4,6,2,13,-3,6,7,8,34,11]
selection_sort(nums)
print(nums)


    # while n >= 0:
    #     for i in range(0, n + 1):
    #         if largestValue < nums[i]:
    #             largestValue = nums[i]
    #             largestValueIndex = i

    #     if largestValue == nums[-1]:
    #         continue
    #     else:
    #         temp = nums[n]    
    #         nums[n], nums[largestValueIndex] = largestValue, temp

    #       n -= 1




    