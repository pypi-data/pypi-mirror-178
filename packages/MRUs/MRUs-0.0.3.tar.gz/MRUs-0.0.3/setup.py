from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name = "MRUs",       
    version = "0.0.3",
    author = "MingjunXu",    	
    description = "Matrix Reduction Utils",		
    packages = find_packages(),   	#打包时，开始的目录
    requires=['numpy'],
    # 取消所有测试包
    exclude = ["*.log",],

)
