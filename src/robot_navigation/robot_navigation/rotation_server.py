import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import threading
from robot_navigation.utils.tf_transformations import euler_from_quaternion
from custom_interfaces.action import Rotate

class RotationActionServer(Node):
    def __init__(self):
        super().__init__('rotation_action_server')
        
        # Create separate callback groups
        self.action_callback_group = ReentrantCallbackGroup()
        self.odom_callback_group = MutuallyExclusiveCallbackGroup()
        
        self._action_server = ActionServer(
            self,
            Rotate,
            'rotate_robot',
            self.execute_callback,
            callback_group=self.action_callback_group)
        
        # Publisher para controlar movimento do robô
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Subscriber para receber posição atual do robô
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10,
            callback_group=self.odom_callback_group)
        
        self.current_heading = 0.0
        self.initial_heading = None
        self.target_angle = None
        self.heading_lock = threading.Lock()
        self.rotation_speed = 0.2  
        self.angle_threshold = 5.0  
        self.get_logger().info('Rotation Action Server has been started')

    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w])

        with self.heading_lock:
            self.current_heading = math.degrees(yaw)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing rotation...')
        
        requested_angle = goal_handle.request.angle_degrees
        self.get_logger().info(f'Requested rotation angle: {requested_angle} degrees')
        
        with self.heading_lock:
            self.initial_heading = self.current_heading
            self.target_angle = (self.initial_heading + requested_angle) % 360
        
        feedback_msg = Rotate.Feedback()
        result = Rotate.Result()
        twist_msg = Twist()
        
        
        if requested_angle > 0:
            twist_msg.angular.z = self.rotation_speed
        else:
            twist_msg.angular.z = -self.rotation_speed
        
        rotation_complete = False
        rate = self.create_rate(20)  
        
        while not rotation_complete:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_rotation()
                return Rotate.Result()
            
            with self.heading_lock:
                current_heading = self.current_heading
                target_angle = self.target_angle
            
            remaining_angle = abs(target_angle - current_heading)
            if remaining_angle > 180:
                remaining_angle = 360 - remaining_angle
            
            feedback_msg.remaining_degrees = remaining_angle
            goal_handle.publish_feedback(feedback_msg)
            
            if remaining_angle < self.angle_threshold:
                rotation_complete = True
                break
            
            self.publisher_.publish(twist_msg)
            rate.sleep()
        
        self.stop_rotation()
        
        result.success = True
        with self.heading_lock:
            result.final_angle = self.current_heading
        goal_handle.succeed()
        
        self.get_logger().info('Rotation completed successfully')
        return result

    def stop_rotation(self):
        twist_msg = Twist()
        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    rotation_server = RotationActionServer()
    
    # Use a MultiThreadedExecutor to handle callbacks from multiple threads
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(rotation_server)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        rotation_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()