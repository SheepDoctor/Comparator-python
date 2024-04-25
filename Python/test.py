n = int(input())
numbers = input()
number_list = list(map(int, numbers.split()))
print(' '.join(map(str, number_list)))
