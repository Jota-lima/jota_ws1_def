import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
from robot_navigation.utils.tf_transformations import euler_from_quaternion
from custom_interfaces.action import Rotate

class RotationActionServer(Node):
    def __init__(self):
        super().__init__('rotation_action_server')
        self._action_server = ActionServer(
            self,
            Rotate,
            'rotate_robot',
            self.execute_callback)
        
        # Publisher para controlar movimento do robô
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 100)
        
        # Subscriber para receber posição atual do robô
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        
        self.current_heading = 0.0
        self.initial_heading = None
        self.target_angle = None
        self.get_logger().info('Rotation Action Server has been started')

    def odom_callback(self, msg):
        # Extrai orientação da odometria
        orientation = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w])
        
        # Converte para graus
        self.current_heading = math.degrees(yaw)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executando rotação...')
        
        # Obtém ângulo solicitado
        requested_angle = goal_handle.request.angle_degrees
        self.get_logger().info(f'Ângulo de rotação solicitado: {requested_angle} graus')
        
        # Armazena heading inicial como referência
        self.initial_heading = self.current_heading
        
        # Calcula ângulo alvo
        self.target_angle = (self.initial_heading + requested_angle) % 360
        
        # Cria mensagens de feedback e resultado
        feedback_msg = Rotate.Feedback()
        result = Rotate.Result()
        
        # Cria mensagem twist para rotação
        twist_msg = Twist()
        
        # Determina direção da rotação
        rotation_speed = 5  # radianos por segundo
        if requested_angle > 0:
            twist_msg.angular.z = rotation_speed
        else:
            twist_msg.angular.z = -rotation_speed
        
        # Inicia rotação
        rotation_complete = False
        
        while not rotation_complete:
            # Verifica se goal foi cancelado
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal cancelado')
                
                # Para rotação
                twist_msg.angular.z = 0.0
                self.publisher_.publish(twist_msg)
                return Rotate.Result()
            
            # Calcula ângulo restante
            remaining_angle = abs(self.target_angle - self.current_heading)
            if remaining_angle > 180:
                remaining_angle = 360 - remaining_angle
                
            # Atualiza feedback
            feedback_msg.remaining_degrees = remaining_angle
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: {remaining_angle} graus restantes')
            
            # Verifica se rotação está completa (com threshold para precisão)
            if remaining_angle < 5.0:
                rotation_complete = True
            
            # Publica comando de rotação
            self.publisher_.publish(twist_msg)
            
            # Sleep para controlar taxa do loop
            rclpy.spin_once(self, timeout_sec=0.1)
        
        # Para rotação
        twist_msg.angular.z = 0.0
        self.publisher_.publish(twist_msg)
        
        # Define resultado
        result.success = True
        result.final_angle = self.current_heading
        goal_handle.succeed()
        
        self.get_logger().info('Rotação completada com sucesso')
        return result

def main(args=None):
    rclpy.init(args=args)
    rotation_server = RotationActionServer()
    rclpy.spin(rotation_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()