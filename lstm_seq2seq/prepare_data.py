import numpy as np

num_samples = 7300  # Number of samples to train on.

# Path to the data txt file on disk.
data_path = 'cmn-eng/cmn.txt'

# Vectorize the data. 矢量化数据
input_texts = []
target_texts = []
input_characters = set()
target_characters = set()

with open(data_path, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n') # 所有行

for line in lines[: min(num_samples, len(lines) - 1)]: #从样本中抽取最少10000行
    input_text, target_text = line.split('\t') # 分离出两种语言
    # We use "tab" as the "start sequence" character
    # for the targets, and "\n" as "end sequence" character.
    target_text = '\t' + target_text + '\n'
    input_texts.append(input_text)
    target_texts.append(target_text)

    # 遍历每个字符, 加到字典
    for char in input_text: 
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text:
        if char not in target_characters:
            target_characters.add(char)

input_characters = sorted(list(input_characters)) # 字典排序
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters) # 字典长度
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts]) # 每句话的长度 最大值
max_decoder_seq_length = max([len(txt) for txt in target_texts])

print('Number of samples:', len(input_texts))
print('Number of unique input tokens:', num_encoder_tokens)
print('Number of unique output tokens:', num_decoder_tokens)
print('Max sequence length for inputs:', max_encoder_seq_length)
print('Max sequence length for outputs:', max_decoder_seq_length)



input_token_index = dict(
    [(char, i) for i, char in enumerate(input_characters)]) # 字符索引字典 例 {a:0,b:1}
target_token_index = dict(
    [(char, i) for i, char in enumerate(target_characters)])

encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens),
    dtype='float32')
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')

# 同时遍历两个语言数组
for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    # 遍历一句话的字符
    for t, char in enumerate(input_text):
        # one-hot 编码
        encoder_input_data[i, t, input_token_index[char]] = 1.
    for t, char in enumerate(target_text):
        # decoder_target_data is ahead of decoder_input_data by one timestep
        # 解码目标数据 领先 解码输入数据 一步
        decoder_input_data[i, t, target_token_index[char]] = 1.
        if t > 0:
            # decoder_target_data will be ahead by one timestep
            # and will not include the start character.
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.
