import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('rm_localization')
    config_file = os.path.join(pkg_dir, 'config', 'amcl_params.yaml')
    map_dir = os.path.join(pkg_dir, 'map')
    map_yaml = os.path.join(map_dir, 'map.yaml')  # CHANGE TO YOUR CORRECT MAP FILE
    
    if not os.path.exists(map_yaml):
        raise FileNotFoundError(f"Map file not found: {map_yaml}")

    return LaunchDescription([
        # Start with static transform publisher that will continue even if AMCL fails
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='backup_map_to_odom',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
            parameters=[{'use_sim_time': True}]
        ),
        
        # Map Server Node
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{
                'yaml_filename': map_yaml,
                'use_sim_time': True,
                'qos_overrides./map.publisher.durability': 'transient_local',
                'qos_overrides./map.publisher.reliability': 'reliable'
            }]
        ),
        
        # AMCL with updated parameters
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            # Change from debug to info for less verbose logging
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[
                # Same parameters as before
                {'use_sim_time': True},
                {'set_initial_pose': True},
                {'initial_pose.x': 0.0},
                {'initial_pose.y': 0.0},
                {'initial_pose.z': 0.0},
                {'initial_pose.yaw': 0.0},
                {'transform_tolerance': 3.0},
                {'tf_broadcast': True},
                
                # Frame IDs
                {'global_frame_id': 'map'},
                {'odom_frame_id': 'odom'},
                {'base_frame_id': 'base_link'},
                
                # Laser parameters
                {'scan_topic': '/scan'},
                {'laser_model_type': 'likelihood_field'},
                {'laser_likelihood_max_dist': 2.0},
                
                # Particle count
                {'min_particles': 500},
                {'max_particles': 2000}
            ]
        ),

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
        ),
    ])