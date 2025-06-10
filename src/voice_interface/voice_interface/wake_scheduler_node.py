import os
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Time
from std_msgs.msg import Empty
from datetime import datetime
import time
import threading

class WakeSchedulerNode(Node):
    def __init__(self):
        super().__init__('wake_scheduler_node')
        self.subscription = self.create_subscription(
            Time,
            'wake_time',
            self.wake_time_callback,
            10)
        self.publisher_ = self.create_publisher(Empty, 'wake_trigger', 10)
        self.get_logger().info('⏳ Wake Scheduler Node started')

    def wake_time_callback(self, msg):
        target_time = datetime.fromtimestamp(msg.sec + msg.nanosec * 1e-9)
        now = datetime.now()
        wait_seconds = (target_time - now).total_seconds()

        if wait_seconds <= 0:
            self.get_logger().warn('⚠️ Target time is in the past! Triggering immediately.')
            self._trigger()
        else:
            self.get_logger().info(f'🕒 Waiting for {wait_seconds:.1f} seconds until {target_time.strftime("%H:%M:%S")}')
            thread = threading.Thread(target=self._sleep_and_trigger, args=(wait_seconds,))
            thread.start()

    def _sleep_and_trigger(self, seconds):
        time.sleep(seconds)
        self._trigger()

    def _trigger(self):
        self.get_logger().info('⏰ Wake time reached! Publishing /wake_trigger')
        self.publisher_.publish(Empty())
        os.system('beep')  # beep 명령어 실행 (리눅스용 기본 벨 소리)

def main(args=None):
    rclpy.init(args=args)
    node = WakeSchedulerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
