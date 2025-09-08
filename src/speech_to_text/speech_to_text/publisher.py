import rclpy
from rclpy.node import Node
import time

from std_msgs.msg import String
from speech_to_text.models.vad_model import SileroModel


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.model = SileroModel()
        self.timer_object = self.create_timer(timer_period, self.timer_callback)
        self.WAV_OUTPUT_PATH = "src/speech_to_text/speech_to_text/recorded_audio.wav" 
        self.threshold = 2 # seconds
        self.cur = time.time()
        self.prev = self.cur
        self.buffer = False # ensures that it won't save every threshold seconds
        
    def timer_callback(self):
        msg = String()
        speaking = self.model.get_is_speaking()
    
        if speaking:
            data = "Speaking"
            self.buffer = True
            self.prev = self.cur
        else:
            data = "Silent"


        if ((self.cur - self.prev) > self.threshold) and self.buffer:
            self.get_logger().info(f'Saving audio file to {self.WAV_OUTPUT_PATH}')
            self.model.save_recording(self.WAV_OUTPUT_PATH)  # Save the buffered audio
            self.buffer = False
            data = f"Saved,{self.WAV_OUTPUT_PATH}"
        self.cur = time.time()
        msg.data = data
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()  