import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import serial

class BMP280Publisher(Node):
    def __init__(self):
        super().__init__('bmp280_publisher')
        
        # Serijski port
        self.serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        # Publisher
        self.publisher_ = self.create_publisher(Float32, 'bmp280/pressure', 10)

        # Timer koji poziva callback svakih 0.1 sekundu
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        try:
            if self.serial_port.in_waiting > 0:
                line = self.serial_port.readline().decode('utf-8').strip()
                pressure = float(line)
                msg = Float32()
                msg.data = pressure
                self.publisher_.publish(msg)
                self.get_logger().info(f'Published pressure: {pressure:.2f}')
        except Exception as e:
            self.get_logger().warn(f'Failed to parse serial data: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = BMP280Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
