import os
import xacro

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Diretórios dos pacotes
    package_dir = get_package_share_directory('rm_navigation')
    localization_dir = get_package_share_directory('rm_localization')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    robot_description_dir = get_package_share_directory('robot_description')
    
    # Variáveis de configuração
    namespace = LaunchConfiguration('namespace', default='')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    autostart = LaunchConfiguration('autostart', default='true')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    map_subscribe_transient_local = LaunchConfiguration('map_subscribe_transient_local', default='true')
    
    # Arquivos de configuração
    params_path = os.path.join(package_dir, 'config', 'nav2_params.yaml')
    map_dir = os.path.join(localization_dir, 'map')
    map_file = os.path.join(map_dir, 'map.yaml')
    rviz_config_file = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')
    bt_xml_file = os.path.join(
        get_package_share_directory('nav2_bt_navigator'),
        'behavior_trees', 'navigate_w_replanning_and_recovery.xml')
    
    # Processar XACRO do robô
    xacro_file = os.path.join(robot_description_dir, 'urdf', 'robot_base.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    
    # Parâmetros do robot_state_publisher
    robot_state_publisher_params = {
        'robot_description': robot_description_raw,
        'use_sim_time': use_sim_time
    }
    
    # Remappings para TF - importante para Nav2
    remappings = [('/tf', 'tf'), ('/tf_static', 'tf_static')]
    
    # Definir nós do lifecycle manager - IMPORTANTE: map_server e amcl separados
    # para poder iniciar o localization independentemente da navegação
    loc_lifecycle_nodes = ['map_server', 'amcl']
    nav_lifecycle_nodes = ['controller_server', 'planner_server', 
                          'recoveries_server', 'bt_navigator', 'waypoint_follower']
    
    # Create our own temporary YAML files that include substitutions - CRÍTICO PARA O NAV2
    param_substitutions = {
        'use_sim_time': use_sim_time,
        'default_bt_xml_filename': default_bt_xml_filename,
        'autostart': autostart,
        'map_subscribe_transient_local': map_subscribe_transient_local
    }

    configured_params = RewrittenYaml(
        source_file=params_file,
        root_key=namespace,
        param_rewrites=param_substitutions,
        convert_types=True)
    
    return LaunchDescription([
        # Variáveis de ambiente
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
        
        # Argumentos de lançamento
        DeclareLaunchArgument(
            'namespace', default_value='',
            description='Top-level namespace'),
            
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation (Gazebo) clock if true'),
            
        DeclareLaunchArgument(
            'autostart', default_value='true',
            description='Automatically startup the nav2 stack'),
            
        DeclareLaunchArgument(
            'params_file',
            default_value=params_path,
            description='Full path to the ROS2 parameters file to use'),
            
        DeclareLaunchArgument(
            'default_bt_xml_filename',
            default_value=bt_xml_file,
            description='Full path to the behavior tree xml file to use'),
            
        DeclareLaunchArgument(
            'map_subscribe_transient_local', default_value='true',
            description='Whether to set the map subscriber QoS to transient local'),
            
        # 1. INICIAR O GAZEBO E O ROBÔ
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={
                'world': os.path.join(robot_description_dir, 'world', 'mundo1.world'),
                'verbose': 'true',
                'pause': 'false'
            }.items()
        ),
        
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_state_publisher_params],
            remappings=remappings
        ),
        
        # Spawn entity
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description',
                      '-entity', 'robot',
                      '-x', '0.0',
                      '-y', '0.0',
                      '-z', '0.5',
                      '-unpause'],
            output='screen'
        ),
        
        # 2. PUBLICAR TRANSFORMAÇÕES TF - CRÍTICO PARA A NAVEGAÇÃO
        # Transformação temporária entre odom e base_link (até o controlador do gazebo assumir)
        # IMPORTANTE: Isso resolve o problema de conexão entre árvores TF
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_odom_to_base_link',
            arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link'],
            parameters=[{'use_sim_time': use_sim_time}]
        ),
        
        # Transformação map para odom (será gerenciada pelo AMCL depois)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_map_to_odom',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
            parameters=[{'use_sim_time': use_sim_time}]
        ),
        
        # Transformação base_link para lidar_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_base_to_lidar',
            arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'lidar_link'],
            parameters=[{'use_sim_time': use_sim_time}]
        ),
            
        # 3. MAPA E LOCALIZAÇÃO
        # Map Server
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'yaml_filename': map_file},
                {'topic_name': 'map'},
                {'frame_id': 'map'}
            ],
            remappings=remappings
        ),
        
        # AMCL com tf_broadcast = False para não conflitar
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[
                {'use_sim_time': True},
                {'set_initial_pose': True},
                {'initial_pose.x': 0.0},
                {'initial_pose.y': 0.0},
                {'initial_pose.z': 0.0},
                {'initial_pose.yaw': 0.0},
                {'transform_tolerance': 3.0},
                {'tf_broadcast': True},  # MUDANÇA: False para não conflitar
                {'global_frame_id': 'map'},
                {'odom_frame_id': 'odom'},
                {'base_frame_id': 'base_link'},
                {'scan_topic': '/scan'},
                {'laser_model_type': 'likelihood_field'},
                {'laser_likelihood_max_dist': 2.0},
                {'min_particles': 500},
                {'max_particles': 2000}
            ],
            remappings=remappings
        ),
        
        # 4. EKF NODE - DIRETO NO LAUNCH
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                os.path.join(localization_dir, 'config', 'ekf_config.yaml')
            ]
        ),
        
        # 5. LIFECYCLE MANAGER PARA LOCALIZAÇÃO
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'autostart': True},
                {'node_names': loc_lifecycle_nodes}
            ]
        ),
        
        # 6. COMPONENTES DE NAVEGAÇÃO
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[configured_params],
            remappings=remappings
        ),
        
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[configured_params],
            remappings=remappings
        ),
        
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            output='screen',
            parameters=[configured_params],
            remappings=remappings
        ),
        
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[configured_params],
            remappings=remappings
        ),
        
        Node(
            package='nav2_waypoint_follower',
            executable='waypoint_follower',
            name='waypoint_follower',
            output='screen',
            parameters=[configured_params],
            remappings=remappings
        ),
        
        # 7. LIFECYCLE MANAGER PARA NAVEGAÇÃO
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'autostart': True},
                {'node_names': nav_lifecycle_nodes}
            ]
        ),
        
        # 8. INICIAR O RVIZ
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'
        )
    ])