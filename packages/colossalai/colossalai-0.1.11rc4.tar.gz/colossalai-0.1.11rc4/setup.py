from setuptools import find_packages, setup

message = """
===============================================================================

This distribution is downloaded from PyPI with 'pip install colossalai' and
it is only a placeholder. 

Please download from our project page at https://www.colossalai.org/download/ .

You may also visit our
1. GitHub: https://github.com/hpcaitech/ColossalAI
2. Discussion: https://github.com/hpcaitech/ColossalAI/discussions
3. Project page: https://www.colossalai.org/

===============================================================================
"""
print(message)


def fetch_requirements(path):
    with open(path, 'r') as fd:
        return [r.strip() for r in fd.readlines()]

setup(name='colossalai',
    version='0.1.11rc4',
    packages=find_packages(),
    description='An integrated large-scale model training system with efficient parallelization techniques',
    long_description_content_type='text/markdown',
    license='Apache Software License 2.0',
    url='https://www.colossalai.org',
    project_urls={
        'Forum': 'https://github.com/hpcaitech/ColossalAI/discussions',
        'Bug Tracker': 'https://github.com/hpcaitech/ColossalAI/issues',
        'Examples': 'https://github.com/hpcaitech/ColossalAI-Examples',
        'Documentation': 'http://colossalai.readthedocs.io',
        'Github': 'https://github.com/hpcaitech/ColossalAI',
    },
    install_requires=fetch_requirements('requirements.txt'),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: GPU :: NVIDIA CUDA',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: System :: Distributed Computing',
    ]
    )
