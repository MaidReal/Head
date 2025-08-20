import rclpy
from rclpy.node import Node

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
        self.current = self.get_clock().now()
        self.last_spoken = self.get_clock().now()

        
    def timer_callback(self):
        msg = String()
        speaking = self.model.get_is_speaking()
        now = self.get_clock().now()
        
        if speaking:
            data = "Speaking"
            self.last_spoken = now
        else:
            data = "Silent"

        sec_now, nsec_now = now.seconds_nanoseconds()
        sec_last, nsec_last = self.last_spoken.seconds_nanoseconds()

        time_difference = sec_now - sec_last + (nsec_now - nsec_last) / 1e9

        if time_difference > self.threshold:
            self.get_logger().info(f'Saving audio file to {self.WAV_OUTPUT_PATH}')
            self.model.save_recording()  # Save the buffered audio
            self.last_spoken = now  # reset the timer after saving
            
        self.current = self.get_clock().now()
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