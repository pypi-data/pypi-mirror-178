import setuptools

setuptools.setup(
    name='haibot_rosgymbullet',
    version='0.7.0',
    description="DiffBot Ros-Gym-Bullet Environment ( For PYTHON 2.7 )",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="haibot_rosgymbullet*"),
    install_requires=['gym', 'pybullet', 'numpy', 'matplotlib']
)