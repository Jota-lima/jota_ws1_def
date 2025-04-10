import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_dir = get_package_share_directory('rm_localization')
    config_file = os.path.join(pkg_dir, 'config', 'amcl_params.yaml')
    map_file = os.path.join(pkg_dir, 'map', 'my_map.yaml')
    
    # Ensure map file exists
    if not os.path.exists(map_file):
        raise FileNotFoundError(f"Map file not found: {map_file}")
    
    return LaunchDescription([
        # Map Server Node
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'yaml_filename': map_file},
                {'use_sim_time': True}
            ]
        ),
        
        # AMCL Node
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[config_file]
        ),
        
        # Lifecycle Manager
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[
                {'use_sim_time': True},
                {'autostart': True},
                {'node_names': ['map_server', 'amcl']}
            ]
        )
    ])