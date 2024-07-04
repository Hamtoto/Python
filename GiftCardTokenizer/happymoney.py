import re

with open('GiftCardTokenizer/data.txt', 'r') as f_in:
    with open('output.txt', 'w') as f_out:
        for line in f_in:
            line = re.sub(',|\s+', '\n', line)
            if not line.strip():
                continue
            f_out.write(line)

print('data.txt 파일을 읽고 output.txt 파일에 변환 완료했습니다.')
