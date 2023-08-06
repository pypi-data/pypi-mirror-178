from setuptools import setup,find_packages
setup(
    name = "MRUs",       
    version = "0.0.1",
    author = "MingjunXu",    	
    description = "Matrix Reduction Utils",		
    packages = find_packages("MRUs"),   	#打包时，开始的目录
    package_dir = {"":"MRUs"},		# 告诉 setuptools 包都在 qiye 下
    package_data = {
    ## 包含 data 文件夹下所有的 *.dat 文件
        "":[".py"],
    },
    # 取消所有测试包
    exclude = ["*.log",]

)
