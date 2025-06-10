import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pygame
import threading
import os
import time


class ASMRPlayerNode(Node):
    def __init__(self):
        super().__init__('asmr_player_node')
        self.subscription = self.create_subscription(
            String,
            'parsed_intent',
            self.intent_callback,
            10)
        self.get_logger().info('🎧 ASMR Player Node started')

        # 재생할 ASMR 파일 경로
        self.asmr_path = '/home/garuda/ros2_ws/src/voice_interface/sound/fire.mp3'

        self.get_logger().info(f'📂 ASMR path: {self.asmr_path}')
        self.play_asmr()

# 파일 존재 여부 확인
    # if not os.path.exists(self.asmr_path):
    #     self.get_logger().error('❌ ASMR sound file not found at the specified path!')
    # else:
    #     self.get_logger().info('✅ ASMR file exists and is ready to play.')

    def intent_callback(self, msg):
        intent = msg.data.lower()
        self.get_logger().info(f'🧠 Intent received: {intent}')

        if 'asmr' in intent:
            self.get_logger().info('🎵 Playing ASMR...')
            threading.Thread(target=self.play_asmr).start()
        else:
            self.get_logger().info('🛑 Not an ASMR intent. Ignoring.')

    def play_asmr(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.asmr_path)
            pygame.mixer.music.play()
            time.sleep(10)
            pygame.mixer.music.stop()
            # 음악이 끝날 때까지 대기
            while pygame.mixer.music.get_busy():
                pass
        except Exception as e:
            self.get_logger().error(f'❌ Failed to play ASMR with pygame: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = ASMRPlayerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
