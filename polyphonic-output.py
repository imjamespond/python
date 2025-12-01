import json

def replace_with_json():
    with open('output.json', 'r', encoding='utf-8') as f:
        list = json.load(f)

        with open("input.txt", "r", encoding="utf-8") as f:
            text = f.read()

            with open('output.txt', 'w', encoding='utf-8') as f:
                for original, replacement in list:
                    text = text.replace(original, replacement)
                f.write(text)


# ---------- 示例 ----------
if __name__ == "__main__":

  replace_with_json()
