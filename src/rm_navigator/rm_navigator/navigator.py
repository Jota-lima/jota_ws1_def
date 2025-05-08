#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Point, Quaternion, PoseWithCovarianceStamped
import time


class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')
        self.get_logger().info('Navigator node has been initialized')
        
        # Definir a posição inicial que queremos usar
        self.initial_position = Point(x=0.0, y=0.0, z=0.0)
        self.initial_orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
        
        # Criar o publisher para a pose inicial
        self.initial_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )
        
        # Criar o action client para navegação
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        # Esperar pelo servidor de ações estar disponível
        self.get_logger().info('Waiting for navigation action server...')
        if not self.nav_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Navigation action server not available')
            return
        self.get_logger().info('Navigation action server connected!')
        
        # Primeiro publicar a pose inicial
        self.timer = self.create_timer(1.0, self.publish_initial_pose)
        self.initial_pose_published = False
        self.navigation_step = 0
        
    def publish_initial_pose(self):
        if self.initial_pose_published:
            return
            
        self.get_logger().info('Publishing initial pose...')
        
        # Criar a mensagem de pose inicial
        initial_pose = PoseWithCovarianceStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.get_clock().now().to_msg()
        
        # Definir a posição e orientação
        initial_pose.pose.pose.position = self.initial_position
        initial_pose.pose.pose.orientation = self.initial_orientation
        
        # Definir a matriz de covariância (valores típicos para inicialização)
        # Uma matriz 6x6 representada como uma lista de 36 elementos
        covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]
        
        initial_pose.pose.covariance = covariance
        
        # Publicar a pose
        self.initial_pose_pub.publish(initial_pose)
        self.get_logger().info('Initial pose published')
        
        # Marcar como publicado e configurar o timer para iniciar a navegação após 5 segundos
        self.initial_pose_published = True
        self.timer.cancel()
        self.timer = self.create_timer(5.0, self.start_navigation)
        
    def start_navigation(self):
        self.timer.cancel()  # Cancelar o timer para não chamar novamente
        
        # Primeiro, vamos ao destino
        self.get_logger().info('Starting navigation to target position')
        self.send_goal(x=2.0, y=1.0, z=0.0)  # Ajuste conforme seu mapa
        
    def send_goal(self, x, y, z):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = z
        goal_msg.pose.pose.orientation.w = 1.0
        
        self.get_logger().info(f'Navigating to: x={x}, y={y}')
        
        # Enviar o goal e registrar callbacks
        self.send_goal_future = self.nav_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback)
        
        self.send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().error('Goal was rejected')
            return
            
        self.get_logger().info('Goal accepted')
        
        # Obter o resultado da navegação quando terminar
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)
    
    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        
        if status == 4:  # 4 = SUCCESS
            self.get_logger().info('Navigation completed successfully!')
            
            # Verificar em qual etapa estamos
            if self.navigation_step == 0:
                self.navigation_step = 1
                self.get_logger().info('Returning to initial position...')
                time.sleep(2)  # Pequena pausa antes de voltar
                self.send_goal(
                    x=self.initial_position.x,
                    y=self.initial_position.y,
                    z=self.initial_position.z
                )
            else:
                self.get_logger().info('Full navigation sequence completed!')
        else:
            self.get_logger().error(f'Navigation failed with status: {status}')
    
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        # Para debug, podemos descomentar para ver a distância restante
        # self.get_logger().info(f'Current distance to goal: {feedback.distance_remaining}')

def main(args=None):
    rclpy.init(args=args)
    navigator = NavigatorNode()
    
    try:
        rclpy.spin(navigator)
    except KeyboardInterrupt:
        navigator.get_logger().info('Navigation canceled by user')
    finally:
        # Cleanup
        navigator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()