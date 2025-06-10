# ~/ros2_ws/src/voice_interface/setup.py

from setuptools import setup

package_name = 'voice_interface'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your name',
    maintainer_email='your@email.com',
    description='Voice interface for wakebot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'voice_input_node = voice_interface.voice_input_node:main',
            'llm_planner_node = voice_interface.llm_planner_node:main',
            'wake_scheduler_node = voice_interface.wake_scheduler_node:main',
            'asmr_player_node = voice_interface.asmr_player_node:main',
        ],
    },
)

