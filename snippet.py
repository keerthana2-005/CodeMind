def find_max(lst):
    max_val = 0  # Logical Error: Should initialize with lst[0] instead of 0
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val

print(find_max([-5, -2, -8, -1]))  # Incorrect output expected
