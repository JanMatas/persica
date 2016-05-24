

from socketIO_client import SocketIO, BaseNamespace
import time
import threading 
import subprocess

class Namespace(BaseNamespace):



    def register_cmd_callbacks(self, fn):
        self.cmdCallbacks.append(fn)


    def on_connect(self):
        self.cmdCallbacks = []
        print ("connected")
        
    
    def on_disconnect(self):
        print('disconnected')

    def on_cmd(self, args):
        print (args)
        for cb in self.cmdCallbacks:
            cb(args)







class WsThread(threading.Thread):


    def __init__(self):
        super(WsThread, self).__init__()
        self.ready = False
        self.condition = threading.Condition()

    def _set_ready(self):
        self.condition.acquire()
        self.ready = True
        self.condition.notify_all()
        self.condition.release()

    def run(self):
        self.socketIO = SocketIO('192.168.1.10', 3000, params={'did': 10563})
        self.device_namespace = self.socketIO.define(Namespace, '/device')
        self._set_ready() 
        self.socketIO.wait()


    def register_cmd_callbacks(self, fn):
        self.condition.acquire()
        while not self.ready:
            self.condition.wait()
        self.device_namespace.register_cmd_callbacks(fn)
        self.condition.release()

    def stop(self):
        self.condition.acquire()
        self.ready = False
        self.socketIO.disconnect()
        self.condition.release()



    def send(self,message):
        self.condition.acquire()
        while not self.ready:
            self.condition.wait()
        self.device_namespace.emit(message)
        self.condition.release()

    def __del__(self):
        self.stop()

class Connection(object):

    def __init__(self):
        self.thread = WsThread()
        self.thread.start()

    def send(self,message):
        self.thread.send(message)

    def close(self):
        self.thread.stop()

    def register_cmd_callbacks(self, fn):
        self.thread.register_cmd_callbacks(fn)

if __name__ == "__main__":
    connection = Connection()
    connection.send("hello")
    time.sleep(10)
    connection.close()
