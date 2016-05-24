


#import mock
import unittest
import thread
from persica import connection

import time
timeout = 1

class TestWebsocket(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
        import thread
        connections = []

        class SimpleEcho(WebSocket):
            def inject_mock(self, mock):
                self.mock = mock

            def handleMessage(self):
                # echo message back to client
                self.sendMessage(self.data)
                if self.mock:
                    self.mock.message(message)
                

            def handleConnected(self):
                connections.append(self)
                self.mock = None


            def handleClose(self):

                if self.mock:
                    self.mock.message(message)  
                connections.remove(self)

        server = SimpleWebSocketServer('', 8100, SimpleEcho)
        self.connections = connections


        thread.start_new_thread(server.serveforever, () )


    def test_opens_connection_on_start(self):
        connection.start()
        self.assertEqual(len(self.connections), 1, "No connection established on start.")

    def test_reconnects_on_close(self):
        connection.start()
        self.connections[0].close()
        # Wait for connection to close
        while (len(self.connections) == 1): 
            time.sleep(0.001)
        start = time.time()
        while (time.time() - start < timeout):
            if len(self.connections) == 1:
                return
        self.assertEqual(len(self.connections), 1, "Connection not reeastablished after closing.")
        





    def tearDown(self):
        for c in self.connections:
            c.close()




