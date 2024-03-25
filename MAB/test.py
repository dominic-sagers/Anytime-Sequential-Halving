import time

if __name__ == "__main__":
    current_time = time.time()
    print(current_time)
    while(time.time() - current_time < 5):
        print("I am running")
        time.sleep(1)
        
    print(time.time())