# 移除扩展的attr语法中的指定图像的属性移

import os
import re

import fire


def preprocess(file: str):
    with open(file, "r") as f:
        lines = f.readlines()

    buffer = []
    # 移除掉 image attr
    for line in lines:
        if line.startswith("![]"):
            # ![](...){: .img-center-75 }
            stripped = re.sub(r"\{.+\}", "", line)
            # print(stripped)
            buffer.append(stripped)
        # 移除掉pygments增加的code block的属性
        elif line.startswith("```"):
            try:
                lang, *attrs = line.split(" ")
                buffer.append(lang)
                for attr in attrs:
                    k, v = attr.split("=")
                    if k == "title":
                        buffer.append(f"\n#{v}")
            except Exception:
                print(f"不能解析{line}")
        elif line.startswith("!!!"):
            try:
                _, cat, *_ = line.split(" ")
                if cat.upper() in "INFO,TIP,TIPS,CITE,WARNING,NOTE,READMORE,QUOTE,ATTENTION":
                    buffer.append(f"!!! {cat}\n\n")
            except Exception:
                print(f"不能解析{line}")
        else:
            buffer.append(line)

    filename = os.path.basename(file)
    with open(f"/tmp/{filename}", "w") as f:
        f.writelines(buffer)


fire.Fire({
    "preprocess": preprocess
})

