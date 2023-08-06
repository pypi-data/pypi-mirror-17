from setuptools import setup

setup(
    name='vrep-api-python',
    packages=['vrep-api-python'],
    version='0.1.1',
    description='Simple python binding for V-REP robotics simulator',
    url='https://github.com/Troxid/vrep-api-python',
    author='troxid',
    author_email='troxid@yandex.ru',
    license='MIT',
    keywords='vrep robotics simulator binding api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    data_files=[('scenes', ['scenes/Pioneer.ttt', 'scenes/sceneLabWork.ttt', 'testAllComponents.ttt'])]
)
