def solution(num):
    Mnum = M2num = -1
    count = 0
    for i in range(0,len(num)):
        if num[i] > Mnum:
            Mnum = num[i]
        elif num[i] == Mnum:
            count += 1
            max_same_2_num = num[i]
    for i in range(0,len(num)):
        if num[i] < Mnum and num[i] > M2num:
            M2num = num[i]
    ans = M2num * Mnum
    if count > 0:
        ans = max_same_2_num * Mnum     
    return ans
