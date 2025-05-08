import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Diretórios dos pacotes
    package_dir = get_package_share_directory('rm_navigation')
    turtlebot3_dir = get_package_share_directory('turtlebot3_gazebo')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    
    # Variáveis de configuração
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Arquivos de configuração
    params_path = os.path.join(package_dir, 'config', 'nav2_params.yaml')
    map_dir = os.path.join(get_package_share_directory('rm_localization'), 'map')
    map_file = os.path.join(map_dir, 'map.yaml')
    rviz_config_file = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')
    
    return LaunchDescription([
        # Variáveis de ambiente
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
        
        # Argumentos de lançamento
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation clock if true'),
            
        # 1. LANÇAR O GAZEBO COM O TURTLEBOT3
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(turtlebot3_dir, 'launch', 'turtlebot3_world.launch.py')
            )
        ),
        
        # 2. COMPONENTES DE NAVEGAÇÃO
        
        # Map Server
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'yaml_filename': map_file}
            ]
        ),
        
        # AMCL
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[params_path]
        ),
        
        # Nav2 Controller
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[params_path]
        ),
        
        # Nav2 Planner
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[params_path]
        ),
        
        # Nav2 Recoveries
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            output='screen',
            parameters=[params_path]
        ),
        
        # Nav2 BT Navigator
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[params_path]
        ),
        
        # Nav2 Waypoint Follower
        Node(
            package='nav2_waypoint_follower',
            executable='waypoint_follower',
            name='waypoint_follower',
            output='screen',
            parameters=[params_path]
        ),
        
        # Lifecycle Manager
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'autostart': True},
                {'node_names': ['map_server', 
                               'amcl',
                               'controller_server',
                               'planner_server', 
                               'recoveries_server',
                               'bt_navigator',
                               'waypoint_follower']}
            ]
        ),
        
        # 3. INICIAR O RVIZ COM CONFIGURAÇÃO DO NAV2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        )
    ])