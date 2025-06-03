import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import Trigger
from tf2_ros import TransformListener, Buffer
import math
import time


class WaypointPublisher(Node):
    def __init__(self):
        super().__init__('waypoint_publisher')
        
        # Action client for Nav2 navigation
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        # TF2 listener para verificar posição atual
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Service to start waypoint navigation
        self.start_service = self.create_service(
            Trigger, 'start_waypoint_navigation', self.start_navigation_callback)
        
        # Waypoints baseados nos pontos que funcionaram no terminal
        self.waypoints = [
            # Sala 1 - baseado no primeiro waypoint que funcionou
            {"x": 3.89, "y": 1.53, "yaw": 0.0, "name": "Sala Principal"},
            
            # Cozinha - baseado no segundo waypoint
            {"x": -1.90, "y": 4.68, "yaw": 1.57, "name": "Cozinha"},
            
            # Quarto - explorando área adjacente
            {"x": 2.0, "y": 4.0, "yaw": 3.14, "name": "Quarto"},
            
            # Área de entrada - volta para próximo do ponto inicial
            {"x": 0.0, "y": 0.0, "yaw": 0.0, "name": "Área de Entrada"}
        ]
        
        # Navigation state
        self.current_waypoint_index = 0
        self.navigation_active = False
        self.goal_handle = None
        
        # Tolerância para considerar que chegou ao waypoint (metros)
        self.waypoint_tolerance = 0.5  # 50cm de tolerância
        
        # Timer para verificar posição periodicamente
        self.position_check_timer = self.create_timer(1.0, self.check_position_callback)
        
        self.get_logger().info('Nav2 Waypoint Publisher initialized')
        self.get_logger().info(f'Loaded {len(self.waypoints)} waypoints:')
        for i, wp in enumerate(self.waypoints):
            self.get_logger().info(f'  {i+1}. {wp["name"]}: ({wp["x"]:.2f}, {wp["y"]:.2f})')
        self.get_logger().info(f'Waypoint tolerance: {self.waypoint_tolerance}m')
        self.get_logger().info('Call service: ros2 service call /start_waypoint_navigation std_srvs/srv/Trigger')
    
    def get_robot_position(self):
        """Obter posição atual do robô usando TF2"""
        try:
            # Transformação de base_link para map
            transform = self.tf_buffer.lookup_transform(
                'map', 'base_link', rclpy.time.Time(), timeout=rclpy.duration.Duration(seconds=1.0))
            
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            
            return x, y
        except Exception as e:
            self.get_logger().warn(f'Failed to get robot position: {str(e)}')
            return None, None
    
    def calculate_distance(self, x1, y1, x2, y2):
        """Calcular distância euclidiana entre dois pontos"""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def check_position_callback(self):
        """Timer callback para verificar se chegou ao waypoint"""
        if not self.navigation_active:
            return
        
        # Obter posição atual
        robot_x, robot_y = self.get_robot_position()
        if robot_x is None or robot_y is None:
            return
        
        # Verificar distância até o waypoint atual
        current_wp = self.waypoints[self.current_waypoint_index]
        distance = self.calculate_distance(robot_x, robot_y, current_wp["x"], current_wp["y"])
        
        # Log da posição atual ocasionalmente
        if hasattr(self, '_position_log_counter'):
            self._position_log_counter += 1
        else:
            self._position_log_counter = 1
        
        if self._position_log_counter % 5 == 0:  # A cada 5 segundos
            self.get_logger().info(
                f'Current position: ({robot_x:.2f}, {robot_y:.2f}) | '
                f'Target: ({current_wp["x"]:.2f}, {current_wp["y"]:.2f}) | '
                f'Distance: {distance:.2f}m')
    
    def start_navigation_callback(self, request, response):
        """Service callback to start waypoint navigation sequence"""
        if self.navigation_active:
            response.success = False
            response.message = "Navigation already in progress"
            return response
        
        self.get_logger().info('=== Starting Nav2 waypoint navigation sequence ===')
        self.current_waypoint_index = 0
        self.navigation_active = True
        
        # Wait for Nav2 action server
        if not self.nav_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Nav2 action server not available!')
            response.success = False
            response.message = "Nav2 action server not available"
            self.navigation_active = False
            return response
        
        # Start with first waypoint
        self.send_next_waypoint()
        
        response.success = True
        response.message = f"Started navigation sequence with {len(self.waypoints)} waypoints"
        return response
    
    def send_next_waypoint(self):
        """Send next waypoint in sequence to Nav2"""
        if self.current_waypoint_index >= len(self.waypoints):
            self.get_logger().info('=== All waypoints completed! Navigation sequence finished ===')
            self.navigation_active = False
            return
        
        # Get current waypoint
        waypoint = self.waypoints[self.current_waypoint_index]
        
        # Create Nav2 goal
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = self.create_pose_stamped(
            waypoint["x"], waypoint["y"], waypoint["yaw"])
        
        self.get_logger().info(
            f'=== Waypoint {self.current_waypoint_index + 1}/{len(self.waypoints)}: '
            f'{waypoint["name"]} ===')
        self.get_logger().info(
            f'Navigating to: ({waypoint["x"]:.2f}, {waypoint["y"]:.2f}, '
            f'{math.degrees(waypoint["yaw"]):.0f}°)')
        
        # Send goal to Nav2
        self.send_goal_future = self.nav_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self.send_goal_future.add_done_callback(self.goal_response_callback)
    
    def create_pose_stamped(self, x, y, yaw):
        """Create a PoseStamped message for Nav2"""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        
        # Position
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = 0.0
        
        # Orientation (convert yaw to quaternion)
        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        
        return pose
    
    def goal_response_callback(self, future):
        """Handle Nav2 goal response"""
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().error('=== Waypoint goal rejected by Nav2! ===')
            self.navigation_active = False
            return
        
        self.get_logger().info('=== Waypoint goal accepted by Nav2 ===')
        self.goal_handle = goal_handle
        
        # Wait for result
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.result_callback)
    
    def feedback_callback(self, feedback_msg):
        """Handle Nav2 navigation feedback"""
        # Log progress occasionally (every 50 feedback messages to avoid spam)
        if hasattr(self, '_feedback_counter'):
            self._feedback_counter += 1
        else:
            self._feedback_counter = 1
        
        if self._feedback_counter % 50 == 0:
            current_wp = self.waypoints[self.current_waypoint_index]
            self.get_logger().info(f'Navigating to {current_wp["name"]}... (progress update)')
    
    def result_callback(self, future):
        """Handle Nav2 navigation result"""
        try:
            result = future.result().result
            current_wp = self.waypoints[self.current_waypoint_index]
            
            # VERIFICAÇÃO ADICIONAL: Confirmar se realmente chegou ao waypoint
            robot_x, robot_y = self.get_robot_position()
            
            if robot_x is not None and robot_y is not None:
                distance = self.calculate_distance(
                    robot_x, robot_y, current_wp["x"], current_wp["y"])
                
                self.get_logger().info(
                    f'Nav2 result received. Distance to target: {distance:.2f}m '
                    f'(tolerance: {self.waypoint_tolerance}m)')
                
                # Verificar se realmente chegou ao destino
                if distance <= self.waypoint_tolerance:
                    self.get_logger().info(
                        f'=== ✅ Reached {current_wp["name"]} successfully! '
                        f'(Distance: {distance:.2f}m) ===')
                    
                    # Brief pause at waypoint
                    time.sleep(2.0)
                    
                    # Move to next waypoint
                    self.current_waypoint_index += 1
                    self.send_next_waypoint()
                    
                else:
                    self.get_logger().warn(
                        f'=== ⚠️  Nav2 says reached {current_wp["name"]}, but robot is '
                        f'{distance:.2f}m away (tolerance: {self.waypoint_tolerance}m) ===')
                    
                    # Tentar novamente o mesmo waypoint
                    self.get_logger().info(f'=== 🔄 Retrying waypoint {current_wp["name"]} ===')
                    time.sleep(1.0)
                    self.send_next_waypoint()  # Reenvia o mesmo waypoint
                    return
                    
            else:
                self.get_logger().error(f'=== Failed to get robot position for verification ===')
                # Se não conseguir verificar posição, assume que chegou
                self.get_logger().info(f'=== Reached {current_wp["name"]} (no position verification) ===')
                self.current_waypoint_index += 1
                time.sleep(2.0)
                self.send_next_waypoint()
                
        except Exception as e:
            self.get_logger().error(f'Error processing navigation result: {str(e)}')
            self.navigation_active = False
    
    def cancel_navigation(self):
        """Cancel current navigation if active"""
        if self.navigation_active and self.goal_handle:
            self.get_logger().info('=== Canceling current navigation ===')
            cancel_future = self.goal_handle.cancel_goal_async()
            self.navigation_active = False


def main(args=None):
    rclpy.init(args=args)
    node = WaypointPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('=== Shutting down waypoint navigation ===')
        node.cancel_navigation()
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()