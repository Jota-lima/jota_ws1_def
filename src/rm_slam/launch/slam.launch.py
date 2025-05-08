from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('rm_slam'),
        'config',
        'slam_config.yaml'
    )

    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                config_file,
                {'use_sim_time': True}
            ],
            remappings=[
                ('/scan', '/scan'),
                ('/map', '/map'),
                ('/map_metadata', '/map_metadata'),
            ]
        )
    ])