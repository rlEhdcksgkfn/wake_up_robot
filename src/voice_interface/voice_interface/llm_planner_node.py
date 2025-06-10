import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from builtin_interfaces.msg import Time
from datetime import datetime, timedelta
import re


class LLMPlannerNode(Node):
    def __init__(self):
        super().__init__('llm_planner_node')
        self.subscription = self.create_subscription(
            String,
            'voice_input',
            self.voice_callback,
            10)
        self.wake_pub = self.create_publisher(Time, 'wake_time', 10)
        self.intent_pub = self.create_publisher(String, 'parsed_intent', 10)
        self.get_logger().info('🧠 LLM Planner Node started')

    def voice_callback(self, msg):
        text = msg.data
        self.get_logger().info(f'🗣 Received voice input: {text}')

    # 시간과 분 모두 파싱
        hour_match = re.search(r'(\d+)\s*시간', text)
        minute_match = re.search(r'(\d+)\s*분', text)

        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0

        if hours > 0 or minutes > 0:
            now = datetime.now()
            wake_time = now + timedelta(hours=hours, minutes=minutes)
            wake_msg = Time()
            wake_msg.sec = int(wake_time.timestamp())
            wake_msg.nanosec = int((wake_time.timestamp() % 1) * 1e9)
            self.wake_pub.publish(wake_msg)

            intent_msg = String()
            intent_msg.data = f'Wake me up in {hours} hours and {minutes} minutes'
            self.intent_pub.publish(intent_msg)

            self.get_logger().info(f'⏰ Wake time set for {wake_time.strftime("%H:%M:%S")}')
        else:
            self.get_logger().warn('⚠️ Could not parse wake time from input.')


def main(args=None):
    rclpy.init(args=args)
    node = LLMPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
