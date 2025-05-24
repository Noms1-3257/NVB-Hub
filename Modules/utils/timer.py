import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            #print("Timer started.")

    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
            #print("Timer stopped.")

    def reset(self):
        if self.running:
            self.start_time = time.time()
        self.elapsed_time = 0
        #print("Timer reset.")

    def get_current_time(self):
        if self.running:
            return time.time() - self.start_time
        return self.elapsed_time

    def get_time_formatted(self):
        current_time = self.get_current_time()
        minutes, seconds = divmod(current_time, 60)
        return f"{int(minutes):02}:{int(seconds):02}"

if __name__ == "__main__":
    timer = Timer()
    while True:
        command = input("Enter command (start, stop, reset, time, quit): ").strip().lower()

        if command == "start":
            timer.start()
        elif command == "stop":
            timer.stop()
        elif command == "reset":
            timer.reset()
        elif command == "time":
            print("Current Timer:", timer.get_time_formatted())
        elif command == "quit":
            break
        else:
            print("Invalid command, please try again.")
