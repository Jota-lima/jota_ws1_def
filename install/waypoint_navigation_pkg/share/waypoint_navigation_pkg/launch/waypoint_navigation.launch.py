from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Start rotation server first
        Node(
            package='robot_navigation',
            executable='rotation_server',
            name='rotation_server',
            output='screen'
        ),
        
        # Then start waypoint publisher
        Node(
            package='waypoint_navigation_pkg',
            executable='waypoint_publisher',
            name='waypoint_publisher',
            output='screen'
        ),
    ])