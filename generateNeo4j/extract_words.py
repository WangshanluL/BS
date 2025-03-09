import json

with open('origin_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# 第一层节点列表
words1 = list(data.keys())

# 第二层节点列表
words2 = []
for first_level_key in data.keys():
    words2.extend(list(data[first_level_key].keys()))

# 第三层节点列表
words3 = []
for first_level_key in data.keys():
    for second_level_key in data[first_level_key].keys():
        for i in data[first_level_key][second_level_key].keys():
            words3.append(f"{i}-{data[first_level_key][second_level_key][i]}")
        #words3.extend(list(data[first_level_key][second_level_key].keys()))

# 打印结果
print("第一层节点：", words1)
print("\n第二层节点：", words2)
print("\n第三层节点：", words3)