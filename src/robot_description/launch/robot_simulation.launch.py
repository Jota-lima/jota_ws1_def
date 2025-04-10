import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Declare the launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    # Get paths and process XACRO
    xacro_file = "robot_base.xacro"
    description_package_name = "robot_description"
    description_package_path = get_package_share_directory(description_package_name)
    xacro_file_path = os.path.join(description_package_path, 'urdf', xacro_file)

    # Process XACRO file
    xacro_file = os.path.join(description_package_path, 'urdf', 'robot_base.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Parameters
    robot_state_publisher_params = {
        'robot_description': robot_description_raw,
        'use_sim_time': use_sim_time
    }

    # Include Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': os.path.join(description_package_path, 'world', 'mundo1.world'),
            'verbose': 'true',
            'pause': 'true'
        }.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_state_publisher_params]
    )

    # RViz
    rviz_config_dir = os.path.join(description_package_path, 'rviz', 'robot_vis.rviz')
    
    # Verificar se o arquivo de configuração existe
    if not os.path.exists(rviz_config_dir):
        # Se não existir, usar configuração padrão
        rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
        )
    else:
        # Se existir, usar o arquivo de configuração
        rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-d', rviz_config_dir]
        )

    # Spawn entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                  '-entity', 'robot',
                  '-x', '0.0',
                  '-y', '0.0',
                  '-z', '0.5',
                  '-unpause'],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        rviz_node,
    ])
