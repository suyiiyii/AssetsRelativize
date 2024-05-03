'''
文件资源归档工具
1. 将文件备份一份，以.bak后缀保存到同一目录下
2. 读取文档中的图片路径
3. 将图片复制到当前目录下的 assets 文件夹下
4. 更新文档中的图片路径
5. 保存文档
'''
import argparse
import logging
import re
import shutil
from  pathlib import Path
import os

Extensions = [
    ".png",
    ".jpg",
    ".jpeg",
]

DstDir = "assets"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file-path', help="file path to read data from", type=str, required=True
    )
    return parser.parse_args()



def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
    )
    parse = parse_args()
    logging.info("程序开始运行...")
    logging.info(f"file_path: {parse.file_path}")


    # 备份文件
    bak_file = f"{parse.file_path}.bak"
    shutil.copy2(parse.file_path, bak_file)
    logging.info(f"备份文件为: {bak_file}")

    data = ''
    with open(parse.file_path, 'r', encoding="utf-8") as f:
        data = f.read()
    logging.info(f"读取到的数据为: {data}")
    # 正则匹配
    '''
    匹配 Windows 路径
    1. 匹配盘符 [a-zA-Z]:
    2. 匹配路径分隔符 [\\/] (Windows 下路径分隔符为 \ 或 /)
    3. 匹配文件夹名称 (文件夹名称不能包含 \ / : * ? " < > |)
    4. 匹配文件名 (文件名不能包含 \ / : * ? " < > |)
    5. 匹配文件后缀名 (文件后缀名为 .xxx)
    '''

    regex = r'([a-zA-Z]:[\\/](?:[^\\/:*?"<>|\r\n]+[\\/])*[^\\/:*?"<>|\r\n]*'
    if len(Extensions) :
        regex += f'(?:{"|".join(Extensions)})'
    regex += ')'
    pattern = re.compile(regex)
    logging.info(f"正则表达式为: {pattern}")

    result:list[str] = pattern.findall(data)
    # 获取到的路径
    logging.info(f"共有 {len(result)} 条路径")
    logging.info(f"获取到的路径为: {"\n".join(result)}")

    pathPair = {x: getDstPath(Path(x), Path(parse.file_path).parent) for x in result}
    logging.info(f"需要复制的文件路径共有 {len(pathPair)} 条为: {'\n'.join([str(x) for x in pathPair])}")

    # 获取文档路径
    docPath = Path(parse.file_path).parent
    logging.info(f"文档路径为: {docPath}")
    
    for src,dst in pathPair.items():
        if not dst.parent.exists():
            os.makedirs(dst.parent)
        copyFile(src, dst.absolute())
        logging.info(f"复制文件 {src} 到 {dst} 成功")
    
    # 更新文档中的路径，将原路径替换为相对路径
    for src,dst in pathPair.items():
        logging.info(f"更新文档中的路径，将原路径 {src} 替换为相对路径 {DstDir}/{dst.name}")
        data = data.replace(str(src), f"{DstDir}/{dst.name}")

    # 保存文档
    with open(parse.file_path, 'w', encoding="utf-8") as f:
        f.write(data)
    







'''
获得需要保存文件的目标路径
'''
def getDstPath(src:Path,docPath:Path) -> Path:
    # 创建一个保存使用过的路径的集合
    if not hasattr(getDstPath, "usedPath"):
        getDstPath.usedPath = set()
    # 如果文件名没有重复，直接返回
    if src.name not in getDstPath.usedPath:
        getDstPath.usedPath.add(src.name)
        return docPath / DstDir / src.name
    # 如果文件名重复，加上后缀
    i = 1
    while True:
        name = f"{src.stem}_{i}{src.suffix}"
        if name not in getDstPath.usedPath:
            getDstPath.usedPath.add(name)
            return docPath / DstDir / name
        i += 1
    

'''
    # 复制文件
    for file_path in result:
        copyFile(file_path, "D:/")
        logging.info(f"复制文件 {file_path} 到 D:/ 成功")
'''
def copyFile(src:str, dst:str) -> None:
    # 检查目标文件是否存在
    if os.path.exists(dst):
        raise Exception(f"目标文件 {dst} 已存在") 
    shutil.copy2(src, dst)
    logging.info(f"复制文件 {src} 到 {dst} 成功")

if __name__ == "__main__":
    main()

