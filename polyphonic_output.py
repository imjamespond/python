import json

def replace_with_json():
    with open('output.json', 'r', encoding='utf-8') as f:
        list = json.load(f)

        with open("input.txt", "r", encoding="utf-8") as f:
            text = f.read()

            with open('output.txt', 'w', encoding='utf-8') as f:
                seen = {}
                # 步骤：
                # 1. for item in data:
                # 2. if item[0] not in seen:
                # 3. setdefault() 方法同时完成了检查和添加两个操作
                list = [seen.setdefault(item[0], item) for item in list if item[0] not in seen]
                print('result:\n', seen, '\n', list)
                for original, replacement in list:
                    text = text.replace(original, replacement)
                f.write(text)


# ---------- 示例 ----------
if __name__ == "__main__":

  replace_with_json()
