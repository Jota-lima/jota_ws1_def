import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Obter caminhos
    desc_package_path = get_package_share_directory('robot_description')
    
    # Incluir o launch file da simulação do robô
    simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(desc_package_path, 'launch', 'robot_simulation.launch.py')
        )
    )
    
    # Node de servidor de ação para rotação
    rotation_server = Node(
        package='robot_navigation',
        executable='rotation_server',
        name='rotation_action_server',
        output='screen',
    )
    
    # Node de navegação principal
    navigation_node = Node(
        package='robot_navigation',
        executable='navigation_node',
        name='navigation_node',
        output='screen',
    )
    
    return LaunchDescription([
        simulation_launch,
        rotation_server,
        navigation_node
    ])
