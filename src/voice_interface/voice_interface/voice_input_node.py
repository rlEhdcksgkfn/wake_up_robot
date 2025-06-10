# voice_input_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr

class VoiceInputNode(Node):
    def __init__(self):
        super().__init__('voice_input_node')
        self.publisher_ = self.create_publisher(String, 'voice_input', 10)
        self.timer = self.create_timer(5.0, self.listen)

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.get_logger().info('🎤 Listening...')
            try:
                audio = r.listen(source, timeout=5)
                result = r.recognize_google(audio, language='ko-KR')
                msg = String()
                msg.data = result
                self.publisher_.publish(msg)
                self.get_logger().info(f'📢 Heard: "{result}"')
            except Exception as e:
                self.get_logger().warn(f'❗ Error: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = VoiceInputNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
