sum = 0
def calc(arr):
    global sum
    if(len(arr) <= 0):
      return
    if int(arr[0]) > 0:
      sum += int(arr[0]) ** 4
    calc(arr[1:])

n = int(input())
string = input()
nums = string.split(' ')

calc(nums)
print(sum)