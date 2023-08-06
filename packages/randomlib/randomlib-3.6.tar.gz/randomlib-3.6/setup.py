from setuptools import setup

setup(
    name='randomlib',
    version='3.6',
    # author='L3Cube',
    # author_email='l3cube.pune@gmail.com',
    # description='An NLP Library for Marathi Language',
    # url='https://github.com/l3cube-pune/MarathiNLP.git',
    packages=['randomlib','randomlib.autocomplete', 'randomlib.datasets', 'randomlib.hate', 'randomlib.maskFill', 'randomlib.modelRepo', 'randomlib.preprocess', 'randomlib.sentiment', 'randomlib.tagger', 'randomlib.tokenizer'],# can also use setuptools.find_packages()
    include_package_data=True,
    install_requires=['importlib_resources','pandas','transformers','numpy','torch','IPython','huggingface_hub'], 
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
