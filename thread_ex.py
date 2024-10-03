import threading

def detective_task(task_name):
    print(f'I am doing detective work for {task_name}')

#Creating thread
thread1 = threading.Thread(target=detective_task, args=("Lead A",))
thread2 = threading.Thread(target=detective_task, args=("Lead B",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('Case closed!')
