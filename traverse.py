import os
from pathlib import Path
from typing import Callable, Union

gap_max = int( os.getenv("GAP_MAX", "100") )
gap_step = int( os.getenv("GAP_STEP", "1") )
depth_max = int( os.getenv("DEPTH_MAX", "-1") )
start = int( os.getenv("START", "0") )

def traverse_files(
    path: Union[str, Path],
    callback: Callable[[Path, int, int, int], bool],
    ignore_errors: bool = True,
    depth_max: int = -1
) -> None:
    """
    递归遍历目录，按间隔计数规则对文件执行回调
    
    Args:
        path: 文件或文件夹路径
        callback: 回调函数，接收 (file_path)，返回 bool 是否已运行
        ignore_errors: 是否忽略权限等错误
    
    Returns:
        None
    """
    def _traverse(dir_path: Path, depth: int):

        if depth_max >= 0 and depth > depth_max:
            return

        i = 0
        gap = 1
        next = 0

        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    
                    try:
                        value = False if next > i else callback(item, i, gap, next)
                        if value and i >= start:
                            next = gap + i
                            gap += gap_step
                            gap = min(gap, gap_max)

                            # print(f"i {i}, gap {gap}, next {next}, item {item}")
                        
                    except Exception as e:
                        if not ignore_errors:
                            raise
                        print(f"处理文件 {item} 时出错: {e}")
                    
                    i += 1
                
                elif item.is_dir():
                    # 子目录，独立状态递归
                    _traverse(item, depth + 1)

            # for img in os.listdir(img_path):
            #     if os.path.isdir(img):
            #         continue

        except PermissionError:
            if not ignore_errors:
                raise
            print(f"无权限访问目录: {dir_path}")
        except Exception as e:
            if not ignore_errors:
                raise
            print(f"遍历目录 {dir_path} 时出错: {e}")

    root = Path(path)
    if root.is_file():
        # 如果传入的是文件，直接callback
        callback(root)
    elif root.is_dir():
        _traverse(root, 0)


if __name__ == '__main__':
    img_path = config.img_path
    print(img_path)
    traverse_files(img_path, lambda item, i, gap, next: (
       item.suffix.lower() in [".jpg", ".png"] and None == print(f"i {i}, gap {gap}, next {next}, item {item}")
    ), depth_max=depth_max)
