import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="aibotweb",  # 模块名称
    version="1.0",  # 当前版本
    author="chenyuegui",  # 作者
    author_email="lnj0@foxmail.com",  # 作者邮箱
    description="用tcp命令驱动ai-bot，控制浏览器",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    # 依赖模块
    install_requires=[],
    python_requires='>=3',
)
