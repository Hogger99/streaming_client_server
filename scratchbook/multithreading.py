import threading
import time

def calculate_square(number):
    square = number * number
    print(f"The square of {number} is {square}")
    time.sleep(1)


def multithread_1():
    start_ts = time.time()
    numbers = list(range(10))

    threads = []
    for number in numbers:
        thread = threading.Thread(target=calculate_square, args=(number,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"{time.time() - start_ts} secs")
    print("All threads have finished.")


def synchronous_task():

    start_ts = time.time()
    numbers = list(range(10))
    for n in numbers:
        square = n * n
        print(f"The square of {n} is {square}")
        time.sleep(1)
    print(f"{time.time() - start_ts} secs")

if __name__ == "__main__":

    print('syncrhonous')
    synchronous_task()

    print("multi")
    multithread_1()
    