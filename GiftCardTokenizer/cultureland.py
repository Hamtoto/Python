import re

def tokenize_data(input, output):
    with open(input, 'r') as f:
        lines = f.readlines()

    tokens = []
    for line in lines:
        tokens.append(re.sub(r"(.{4})", r"\1-", line.strip())[:-1])

    with open(output, 'w') as f:
        for token in tokens:
            f.write(token + '\n')

def main():
    input = "GiftCardTokenizer/data.txt"
    output = "output.txt"
    tokenize_data(input, output)
    print('data.txt 파일을 읽고 output.txt 파일에 변환 완료했습니다.')

if __name__ == "__main__":
    main()
