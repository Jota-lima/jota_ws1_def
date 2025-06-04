#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
import time


class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('initial_pose_publisher')
        
        # Publisher para o tópico de pose inicial
        self.pose_publisher = self.create_publisher(
            PoseWithCovarianceStamped, 
            '/initialpose', 
            10
        )
        
        # Timer para publicar a pose inicial após alguns segundos
        self.timer = self.create_timer(5.0, self.publish_initial_pose)
        self.pose_published = False
        
        self.get_logger().info('Initial Pose Publisher started - will publish pose in 5 seconds')
    
    def publish_initial_pose(self):
        if self.pose_published:
            return
            
        # Criar mensagem de pose inicial
        pose_msg = PoseWithCovarianceStamped()
        
        # Header
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'map'
        
        # Pose (posição 0,0 com orientação 0)
        pose_msg.pose.pose.position.x = 0.0
        pose_msg.pose.pose.position.y = 0.0
        pose_msg.pose.pose.position.z = 0.0
        
        # Orientação (quaternion para yaw = 0)
        pose_msg.pose.pose.orientation.x = 0.0
        pose_msg.pose.pose.orientation.y = 0.0
        pose_msg.pose.pose.orientation.z = 0.0
        pose_msg.pose.pose.orientation.w = 1.0
        
        # Covariância (incerteza da pose)
        pose_msg.pose.covariance = [
            0.25, 0.0, 0.0, 0.0, 0.0, 0.0,     # x
            0.0, 0.25, 0.0, 0.0, 0.0, 0.0,     # y
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,      # z
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,      # roll
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,      # pitch
            0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891909  # yaw
        ]
        
        # Publicar pose
        self.pose_publisher.publish(pose_msg)
        
        self.get_logger().info('✅ Initial pose published: (0.0, 0.0, 0.0°)')
        self.pose_published = True
        
        # Destruir timer após publicar
        self.timer.cancel()


def main(args=None):
    rclpy.init(args=args)
    node = InitialPosePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()