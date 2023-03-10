def solution(n):
    answer = []
    for i in range(1,n+1):
        if i%2 != 0:
            answer.append(i)
    return answer

arr1 = [1, 2, 3, 4, 5, 5]
arr2 = [0, 31, 24, 10, 1, 9]

print(solution(10))
print(solution(15))