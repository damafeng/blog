from app import create_app
import sys
from os.path import abspath, dirname

# 设置当前目录为工作目录
sys.path.insert(0, abspath(dirname(__file__)))


app = create_app()
application = app
