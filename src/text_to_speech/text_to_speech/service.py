from example_interfaces.srv import AddTwoInts
from interfaces.srv import TextToSpeech


import rclpy
from rclpy.node import Node
from text_to_speech.model import ZonosModel
import pygame



class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(TextToSpeech, 'text_to_speech', self.text_to_speech_callback)
        self.model = ZonosModel()
        
    def text_to_speech_callback(self, request, response):
        # response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request {request.text}')
        self.model.generate_audio(request.text)
        self.play_mp3("src/text_to_speech/text_to_speech/sample.wav")
                
        response.result = "yay finished"
        return response

    def play_mp3(self,file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  # wait until playback finishes
            pygame.time.Clock().tick(10)

def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()