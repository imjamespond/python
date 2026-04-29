import cv2
import numpy as np
from typing import Union, Any, IO, Sequence
from numpy.typing import NDArray

from typing import Union, IO, Any
import numpy as np
import cv2
from numpy.typing import NDArray
from pathlib import Path


def resize_to_width(
    img_input: Union[str, NDArray[Any], IO[bytes]]
) -> NDArray[Any]:
    """
    将单张图片（路径、numpy数组、字节流）解析并缩放为宽1024，高度自适应。
    返回: 处理后的 numpy BGR 数组
    """
    TARGET_WIDTH = 1024
    img = None

    # 1. 统一解析为 numpy array
    if isinstance(img_input, np.ndarray):
        img = img_input

    elif isinstance(img_input, str):
        # ✅ 支持中文路径
        path = Path(img_input)

        if not path.exists():
            raise ValueError(f"路径不存在: {img_input}")

        # img = cv2.imread(img_input)

        file_bytes = np.fromfile(str(path), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError(f"无法读取图片(可能损坏或格式不支持): {img_input}")

    elif hasattr(img_input, "read"):
        # 处理 IO[bytes]
        file_bytes = np.asarray(bytearray(img_input.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("无法解码字节流图片")

    else:
        raise TypeError(f"不支持的图片输入格式: {type(img_input)}")

    # 2. 宽度固定 1024，高度按比例自适应缩放
    h, w = img.shape[:2]

    if w > TARGET_WIDTH:
        scale = TARGET_WIDTH / w
        new_h = int(h * scale)

        img = cv2.resize(
            img,
            (TARGET_WIDTH, new_h),
            interpolation=cv2.INTER_AREA
        )

    return img


def test():
    import sys
    from pathlib import Path
    if len(sys.argv) < 2:
        sys.exit(1)
    file_path = Path(sys.argv[1])
    img = resize_to_width(str(file_path))
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test()
