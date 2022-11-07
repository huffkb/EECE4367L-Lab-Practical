import logging
import threading
import queue
import time

# Creates an element with a name and a value
class Element:
    def __init__(self):
        self.name = ""
        self.value = 0

# Creates a buffer of a given size
class Buffer: 
    def __init__(self, size):
        # Creates the queue with the given size
        self.Q = queue.Queue(size)
        # Tracks the size and current number of elements
        self.size = size
        self.numElements = 0
        
        # Creates a condition variable for the enqueueing and dequeueing 
        self.cond = threading.Condition()
        
    # Dequeues an element from the queue when there is at least 1 
    # element in the queue
    def dequeue(self):
        # Waits for a notify on the condition variable
        with self.cond:
            # Checks to see if there is at least 1 element in the queue
            while(self.numElements == 0):
                # If not, then continue to wait
                self.cond.wait()
            
            # Otherwise, create an element to hold the dequeued values
            ele = Element()
            # Dequeue the next element in the queue
            ele = self.Q.get()
            # Decrement the current number of elements in the queue
            self.numElements -= 1
            # Notify all conditions 
            self.cond.notifyAll()
            # Return the dequeued element
            return ele
    
    # Enqueues an element into the queue with the given name and value
    # if the queue is not already full
    def enqueue(self, name, value):
        # Waits for a notify on the condition variable
        with self.cond:
            # Checks to see if the queue is full
            while(self.numElements == self.size):
                # If so, continue to wait
                self.cond.wait()
            
            # Otherwise, create an element hold the enqueued values
            ele = Element()
            # Assign the given name and value to the created element
            ele.name = name
            ele.value = value
            # Put the element into the queue
            self.Q.put(ele)
            # Increment the number of elements in the queue
            self.numElements += 1
            # Notify all conditions
            self.cond.notifyAll()
        
# Creates a producer with the given name and adds and element to the given buffer
class Producer:
    # Initializes the producer 
    def __init__(self, buffer, name):
        # Assigns the name of the producer to the given name
        self.name = name
        # Starts the producing thread which actually enqueues elements into the buffer
        self.p = threading.Thread(name=name,target=self.producing,args=(buffer, self.name)).start()
        
    # Enqueues 1000 elements into the buffer with the given producer name
    def producing(self, buffer, name):
        # Iterates 1000 times
        for i in range(1000):
            # Adds an element with the name of the producer and the
            # current iteration variable value
            buffer.enqueue(name,i)
            # Prints the output enqueued element onto the console
            logging.debug('Enqueued %s %d',name,i)

# Creates a consumer with the given name and takes an element out of the given buffer
class Consumer:
    # Initializes the consumer
    def __init__(self, buffer, name):
        # Assigns the name of consumer to the given name
        self.name = name
        # Creates a consuming thread with which actually dequeues elements from the buffer
        self.p = threading.Thread(name=name,target=self.consuming,args=(buffer, self.name)).start()
        
    # Dequeues either 1000 or 3000 elements from the buffer
    def consuming(self, buffer, name):
        # Creates an element to hold the dequeued values
        ele = Element()
        # Iterates 1000 times ************************************ UNCOMMENT THE FOR LOOP LINE OF CODE BELOW FOR LAB 4 EXPERIMENT 2 ************************************
        #for i in range(1000):
        # Iterates 3000 times ************************************ UNCOMMENT THE FOR LOOP LINE OF CODE BELOW FOR LAB 4 EXPERIMENT 3 ************************************
        for i in range(3000):
            # Removes an element from the buffer 
            ele = buffer.dequeue()
            # Prints the removed element from the buffer onto the console 
            logging.debug('Dequeued %s %d',ele.name,ele.value)

# Enables logging debug print statements and thread tracking
logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

# Creates a buffer of size 16
buffer = Buffer(16)

# ************************************** UNCOMMENT THE TWO LINES OF CODE BELOW FOR LAB 4 EXPERIMENT 2 **************************************
# Creates a single producer and a single consumer to enqueue 1000 elements into the
# buffer and dequeue 1000 elements from the buffer
#producer1 = threading.Thread(target=Producer,args=(buffer,"p1")).start()
#consumer1 = threading.Thread(target=Consumer,args=(buffer,"c1")).start()


# ************************************** UNCOMMENT THE FOUR LINES OF CODE BELOW FOR LAB 4 EXPERIMENT 3 **************************************
# Creates three producers and a single consumer to enqueue 1000 elements into the buffer
# for each producer and dequeue 3000 elements from the buffer
producer1 = threading.Thread(target=Producer,args=(buffer,"p1")).start()
producer2 = threading.Thread(target=Producer,args=(buffer,"p2")).start()
producer3 = threading.Thread(target=Producer,args=(buffer,"p3")).start()
consumer1 = threading.Thread(target=Consumer,args=(buffer,"c1")).start()

# Joins all of the threads except for the main thread to avoid
# terminating too early 
main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()