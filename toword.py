# 移除扩展的attr语法中的指定图像的属性移

import fire
import re
import os

def remove_image_attr(file: str):
    with open(file, "r") as f:
        lines = f.readlines()

    buffer = []
    for line in lines:
        if line.startswith("![]"):
            # ![](...){: .img-center-75 }
            stripped = re.sub(r"\{.+\}", "", line)
            # print(stripped)
            buffer.append(stripped)
        else:
            buffer.append(line)

    filename = os.path.basename(file)
    with open(f"/tmp/{filename}", "w") as f:
        f.writelines(buffer)


fire.Fire({
    "remove_image_attr": remove_image_attr
})

