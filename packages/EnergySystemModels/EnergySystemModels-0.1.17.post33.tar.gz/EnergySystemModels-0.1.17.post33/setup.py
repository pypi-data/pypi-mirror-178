from setuptools import setup, find_packages, find_namespace_packages

with open("README.md","r") as fh:
    long_description=fh.read()

setup(
    name='EnergySystemModels',


    version='0.1.17-33',

    description='Energy systems models are the mathematical models that are developed in order to represent as reliably as possible various energy-related problems.',

    
    classifiers =[   'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10', "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    package_dir = {"":"src"},
    packages=find_packages(where="src"),
    package_data={"": ["*.ini"], },
    #py_modules=['AHU.Coil.HeatingCoil'],
    #packages=['ahu', 'ahu.Coil'],
    python_requires=">=3.7",
    

    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["pandas","CoolProp~=6.4.1","pylab-sdk~=1.3.2","matplotlib","tkintertable~=1.3.3","numpy","pyqtgraph","thermochem","sip", "PyQt-builder","PyQt5","scikit-learn",],
    extra_require={"dev":["pytest>=3.7",],},
    url="https://github.com/ZoheirHADID/EnergySystemModels",
    author="Zoheir HADID",
    author_email="zoheir.hadid@gmail.com"
    )