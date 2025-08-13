from example_interfaces.srv import AddTwoInts
from interfaces.srv import TextToSpeech

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(TextToSpeech, 'text_to_speech', self.text_to_speech_callback)

    def text_to_speech_callback(self, request, response):
        # response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request {request.text}')
        response.result = "yay finished"
        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()