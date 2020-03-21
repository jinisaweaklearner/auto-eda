from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = 'It is an automatic script that generating information in the dataset.' 
  
setup( 
        name ='auto-eda', 
        version ='0.1.1', 
        author ='Jin Xiaocheng', 
        author_email ='xiaochengjin.random@gmail.com', 
        url ='https://github.com/jinisaweaklearner/auto_eda', 
        description ='It is an automatic script that generating information in the dataset.', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'auto-eda=src.auto_eda:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='python package auto eda', 
        install_requires = requirements, 
        zip_safe = False
) 