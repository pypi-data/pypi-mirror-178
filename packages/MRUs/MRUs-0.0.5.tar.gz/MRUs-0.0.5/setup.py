from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name = "MRUs",       
    version = "0.0.5",
    author = "MingjunXu",    	
    description = "Matrix Reduction Utils",		
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(), 
    requires=['numpy'],
    exclude = ["*.log",],

)
