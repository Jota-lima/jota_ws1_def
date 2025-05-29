import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, PoseStamped
from std_srvs.srv import Trigger
from custom_interfaces.action import Rotate
import math
import time


# Copy of euler_from_quaternion function to avoid dependency issues
def euler_from_quaternion(quaternion):
    """
    Convert quaternion to Euler angles (roll, pitch, yaw).
    quaternion = [x, y, z, w]
    """
    x, y, z, w = quaternion
    
    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    
    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)
    
    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    
    return roll, pitch, yaw

class WaypointPublisher(Node):
    def __init__(self):
        super().__init__('waypoint_publisher')
        
        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Action client for rotation
        self.rotation_client = ActionClient(self, Rotate, 'rotate_robot')
        
        # Create the service to start the waypoint sequence
        self.start_service = self.create_service(
            Trigger, 'start_waypoint_navigation', self.start_navigation_callback)
        
        # Navigation state variables
        self.step = 0
        self.navigation_active = False
        self.rotating = False
        self.forward_speed = 0.2  # m/s
        self.distance_threshold = 0.5  # m - distance to wall threshold
        self.min_front_distance = float('inf')
        self.step_start_time = None
        
        # Robot state from odometry
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_heading = 0.0  # degrees
        
        # Create timer for navigation control
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.get_logger().info('Step-based waypoint navigation node initialized')
        self.get_logger().info('Waiting for start_waypoint_navigation service to be called...')
    
    def odom_callback(self, msg):
        """Process odometry data to track robot position and orientation"""
        # Get position
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        # Get orientation as Euler angles
        orientation_q = msg.pose.pose.orientation
        roll, pitch, yaw = euler_from_quaternion(
            [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w])
        
        # Convert to degrees
        self.current_heading = math.degrees(yaw)
    
    def scan_callback(self, msg):
        """Process LaserScan data to detect obstacles in front"""
        center_idx = len(msg.ranges) // 2
        front_arc = msg.ranges[center_idx - 10:center_idx + 10]
        valid_ranges = [r for r in front_arc if not math.isnan(r) and not math.isinf(r)]
        self.min_front_distance = min(valid_ranges) if valid_ranges else float('inf')
    
    def start_navigation_callback(self, request, response):
        """Service callback to start navigation sequence"""
        self.get_logger().info('Starting step-based navigation sequence')
        self.navigation_active = True
        self.step = 1
        return response
    
    def timer_callback(self):
        if not self.navigation_active:
            return
            
        if self.step == 1:  
            if self.min_front_distance < self.distance_threshold:
                self.stop_robot()
                self.get_logger().info('=== Step 1: Wall detected ===')
                self.step += 1
            else:
                self.move_forward()
        
        elif self.step == 2:  
            if not self.rotating:
                self.get_logger().info('=== Step 2: Starting 180-degree rotation ===')
                self.rotate_robot(185.0)
                
        elif self.step == 3:  
            if self.min_front_distance < self.distance_threshold and not self.rotating:
                self.stop_robot()
                self.get_logger().info('=== Step 3: Wall detected ===')
                self.step += 1
            else:
                self.move_forward()

        elif self.step == 4: 
            if not self.rotating:
                self.get_logger().info('=== Step 4: Starting 180-degree rotation ===')
                self.rotate_robot(185.0)

        elif self.step == 5:  
            if self.step_start_time is None:
                self.step_start_time = time.time()  
                
            elapsed_time = time.time() - self.step_start_time
            
            if elapsed_time < 17.0:  
                self.move_forward()
            else:
                self.stop_robot()
                self.get_logger().info('=== Step 5: Time limit reached (17s) ===')
                self.step_start_time = None  
                self.step += 1

        elif self.step == 6: 
            if not self.rotating:
                self.get_logger().info('=== Step 6: Starting 90-degree rotation ===')
                self.rotate_robot(95.0)
                
        elif self.step == 7:  
            if self.step_start_time is None:
                self.step_start_time = time.time()  
                
            elapsed_time = time.time() - self.step_start_time
            
            if elapsed_time < 15: 
                self.move_forward()
            else:
                self.stop_robot()
                self.get_logger().info('=== Step 7: Time limit reached (15s) ===')
                self.step_start_time = None  
                self.step += 1
        
        elif self.step == 8:  
            if not self.rotating:
                self.get_logger().info('=== Step 8: Starting 90-degree rotation ===')
                self.rotate_robot(-95.0)

        elif self.step == 9:  
            if self.step_start_time is None:
                self.step_start_time = time.time()  
                
            elapsed_time = time.time() - self.step_start_time
            
            if elapsed_time < 13:  
                self.move_forward()
            else:
                self.stop_robot()
                self.get_logger().info('=== Step 9: Time limit reached (13s) ===')
                self.step_start_time = None  
                self.step += 1

        elif self.step == 10:  
            if not self.rotating:
                self.get_logger().info('=== Step 10: Starting 90-degree rotation ===')
                self.rotate_robot(95.0)

        elif self.step == 11: 
            if self.min_front_distance < self.distance_threshold and not self.rotating:
                self.stop_robot()
                self.get_logger().info('=== Step 11: Wall detected ===')
                self.step += 1
            else:
                self.move_forward()
        
        elif self.step == 12: 
            if not self.rotating:
                self.get_logger().info('=== Step 12: Starting 180-degree rotation ===')
                self.rotate_robot(-185.0)

        elif self.step == 13: 
            if self.min_front_distance < self.distance_threshold and not self.rotating:
                self.stop_robot()
                self.get_logger().info('=== Step 13: Wall detected ===')
                self.step += 1
            else:
                self.move_forward()

        elif self.step == 14: 
            if not self.rotating:
                self.get_logger().info('=== Step 14: Starting 90-degree rotation ===')
                self.rotate_robot(-95.0) 
            
        elif self.step == 15:  
            if self.step_start_time is None:
                self.step_start_time = time.time()  
                
            elapsed_time = time.time() - self.step_start_time
            
            if elapsed_time < 25:  
                self.move_forward()
            else:
                self.stop_robot()
                self.get_logger().info('=== Step 15: Time limit reached (25s) ===')
                self.step_start_time = None  
                self.step += 1

        elif self.step == 16:  
            if not self.rotating:
                self.get_logger().info('=== Step 16: Starting 90-degree rotation ===')
                self.rotate_robot(-95.0)

        elif self.step == 17: 
            if self.min_front_distance < self.distance_threshold and not self.rotating:
                self.stop_robot()
                self.get_logger().info('=== Step 17: Wall detected ===')
                self.step += 1
            else:
                self.move_forward()

        elif self.step == 18:  
            self.get_logger().info('=== Navigation sequence completed ===')
            self.navigation_active = False
    
    def rotate_robot(self, degrees):
        """Use the rotation action server to rotate the robot"""
        if self.rotating:
            return
            
        self.rotating = True
        self.stop_robot()
        time.sleep(0.5)
        
        goal_msg = Rotate.Goal()
        goal_msg.angle_degrees = float(degrees)
        
        self.get_logger().info(f'Sending rotation goal: {degrees:.1f} degrees')
        
        # Wait for the action server
        try:
            self.rotation_client.wait_for_server(timeout_sec=2.0)
            self.send_goal_future = self.rotation_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback
            )
            self.send_goal_future.add_done_callback(self.goal_response_callback)
        except Exception as e:
            self.get_logger().error(f'Failed to send rotation goal: {str(e)}')
            self.rotating = False
    
    def move_forward(self):
        """Move robot forward at constant speed"""
        cmd = Twist()
        cmd.linear.x = self.forward_speed
        self.cmd_vel_pub.publish(cmd)
    
    def stop_robot(self):
        """Stop robot movement"""
        cmd = Twist()
        self.cmd_vel_pub.publish(cmd)
    
    def feedback_callback(self, feedback_msg):
        """Handle rotation feedback"""
        if feedback_msg.feedback.remaining_degrees % 90 < 1:
            self.get_logger().info(f'=== Rotation remaining: {feedback_msg.feedback.remaining_degrees:.0f} degrees ===')

    def goal_response_callback(self, future):
        """Handle rotation goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Rotation goal was rejected!')
            self.rotating = False
            return
        self.get_logger().info('=== Rotation goal accepted ===')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle rotation result"""
        try:
            result = future.result().result
            if result.success:
                self.get_logger().info('=== Rotation completed successfully ===')
                time.sleep(1.0)
                self.step += 1
            else:
                self.get_logger().warn('=== Rotation failed ===')
        except Exception as e:
            self.get_logger().error(f'Error getting rotation result: {str(e)}')
        self.rotating = False


def main(args=None):
    rclpy.init(args=args)
    node = WaypointPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.stop_robot()
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()