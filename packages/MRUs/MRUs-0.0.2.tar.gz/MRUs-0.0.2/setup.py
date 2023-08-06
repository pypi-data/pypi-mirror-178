from setuptools import setup,find_packages
setup(
    name = "MRUs",       
    version = "0.0.2",
    author = "MingjunXu",    	
    description = "Matrix Reduction Utils",		
    packages = find_packages(),   	#打包时，开始的目录
    requires=['numpy'],
    # 取消所有测试包
    exclude = ["*.log",],

)
