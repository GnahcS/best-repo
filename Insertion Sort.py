def insertion_sort(nums):
    n = len(nums)

    for i in range(1, n):
        print(nums)
        j = i
        while nums[j-1] > nums[j] and j > 0:
            nums[j - 1], nums[j] = nums[j], nums[j - 1]
            j -= 1


nums = [1,3,4,6,2,13,1,6,7,8,6,11]
insertion_sort(nums)
print(nums)