import setuptools
 
setuptools.setup(
    # 项目的名称
    name="xuefei",
    #项目的版本
    version="0.0.2",
    # 项目的作者
    author="xuefei",
    # 作者的邮箱
    author_email="494199078@qq.com",
    # 项目描述
    description="别觉得自己厉害",
    # 项目的长描述
    long_description="别觉得自己厉害",
    # 以哪种文本格式显示长描述
    long_description_content_type="text/markdown",  # 所需要的依赖 
    install_requires=[],  # 比如["flask>=0.10"]
    # 项目主页
    url="https://www.baidu.com",
    # 项目中包含的子包，find_packages() 是自动发现根目录中的所有的子包。
    packages=setuptools.find_packages(),
    # 其他信息，这里写了使用 Python3，MIT License许可证，不依赖操作系统。
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)