import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from speech_to_text.models.transcriber_model import WhisperModel


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.model = WhisperModel()
        
        

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        
        if "Saved" in msg.data:
            self.get_logger().info("Starting transcriber")
            msg_list = msg.data.split(",") # [Saved, Path]
            transcribed_message = self.model.transcribe(msg_list[1])
            self.get_logger().info(f"Transcribed message: {transcribed_message['text']}")
        


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()