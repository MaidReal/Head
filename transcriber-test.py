import time

cur = time.time()
prev = cur
threshold = 2

buffer_speaking = False

while True:
    if (cur - prev) > 2 and buffer_speaking:
        print("2 seconds timer")
        prev = cur
        buffer_speaking = False
    
    if (cur - prev) > 4:
        buffer_speaking = True
        print("resetting buffer")
    
    cur = time.time()