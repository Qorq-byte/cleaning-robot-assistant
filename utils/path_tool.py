import os

def get_project_root() -> str:
    # 获取当前文件路径
    current_file = os.path.abspath(__file__)

    # 获取当前文件所在目录
    current_dir = os.path.dirname(current_file)

    # 获取项目根目录
    project_root = os.path.dirname(current_dir)

    return project_root


def get_abs_path(relative_path):
    """
    获取绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    project_root=get_project_root()
    return os.path.join(project_root, relative_path)

if __name__ == '__main__':
    print(get_project_root())
    print(get_abs_path("path_tool.py"))