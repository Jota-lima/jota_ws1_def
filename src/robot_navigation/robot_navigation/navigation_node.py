import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from custom_interfaces.action import Rotate
import math
import time
from enum import Enum, auto

class NavigationState(Enum):
    FORWARD_UNTIL_WALL = auto()
    ROTATE_180 = auto()
    ROTATE_90_CCW = auto()
    ROTATE_90_CW = auto()
    FORWARD_MIDDLE = auto()
    FORWARD_SHORT = auto()
    FORWARD_LONG = auto()
    FINISHED = auto()

class NavigationNode(Node):
    def __init__(self):
        super().__init__('navigation_node')
        
        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        
        # Action client for rotation
        self.action_client = ActionClient(self, Rotate, 'rotate_robot')
        
       
        self.srv = self.create_service(Empty, 'start_navigation', self.start_navigation_callback)
        
        
        self.step = 0
        self.navigation_active = False
        self.rotating = False
        self.distance_threshold = 0.5
        self.min_front_distance = float('inf')
        
        
        self.forward_speed = 0.2


        self.step_start_time = None
        
        
        self.timer = self.create_timer(0.1, self.timer_callback)

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
                self.get_logger().info('=== Step 5: Time limit reached (11s) ===')
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
            
            if elapsed_time < 16:  
                self.move_forward()
            else:
                self.stop_robot()
                self.get_logger().info('=== Step 9: Time limit reached (10s) ===')
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
        

            
        
        
        
        

    def start_navigation_callback(self, request, response):
        self.get_logger().info('Starting navigation sequence')
        self.navigation_active = True
        self.step = 1
        return response

    def scan_callback(self, msg):
        center_idx = len(msg.ranges) // 2
        front_arc = msg.ranges[center_idx - 10:center_idx + 10]
        valid_ranges = [r for r in front_arc if not math.isnan(r) and not math.isinf(r)]
        self.min_front_distance = min(valid_ranges) if valid_ranges else float('inf')

    def rotate_robot(self, degrees):
        if self.rotating:
            return
        self.rotating = True
        self.stop_robot()
        time.sleep(0.5)
        
        goal_msg = Rotate.Goal()
        goal_msg.angle_degrees = degrees
        
        try:
            self.action_client.wait_for_server(timeout_sec=2.0)
            self.send_goal_future = self.action_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback
            )
            self.send_goal_future.add_done_callback(self.goal_response_callback)
        except Exception as e:
            self.get_logger().error(f'Failed to send rotation goal: {str(e)}')
            self.rotating = False

    def move_forward(self):
        cmd = Twist()
        cmd.linear.x = self.forward_speed
        self.cmd_vel_pub.publish(cmd)

    def stop_robot(self):
        cmd = Twist()
        self.cmd_vel_pub.publish(cmd)

    def feedback_callback(self, feedback_msg):
        if feedback_msg.feedback.remaining_degrees % 90 < 1:
            self.get_logger().info(f'=== Rotation remaining: {feedback_msg.feedback.remaining_degrees:.0f} degrees ===')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Rotation goal was rejected!')
            self.rotating = False
            return
        self.get_logger().info('=== Rotation goal accepted ===')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
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
    node = NavigationNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()