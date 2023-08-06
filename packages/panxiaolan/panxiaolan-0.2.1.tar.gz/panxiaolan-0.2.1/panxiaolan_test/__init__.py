from . import *

# 自定义参数
__version__='0.1'

# __init__.py文件中的__all__参数的功劳，它可以指定用户导入所有模块时，可以导入那些模块，不可以导入那些模块。
__all__=["Hello","Name"] # Hello 代表同文件夹中的Hello.py文件

# 函数
def __version__():
    return "0.2"