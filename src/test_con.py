import socket
import time
import logging

class SocketTaskServer:
    def __init__(self, host="192.168.131.39", program_port=30000, motion_port=30001, mixingport = 30002):
        self.HOST = host
        self.PROGRAMMPORT = program_port
        self.MOTIONPORT = motion_port
        self.MIXINGPORT = mixingport
        logging.basicConfig(level=logging.DEBUG)

    def connection(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            logging.debug(f"Host: {host}, Port: {port}")
            s.listen(5)
            logging.debug(f"Listening on {host}:{port}")
            c, addr = s.accept()
            logging.debug(f"Connection established with {addr}")
            return c, s
        except socket.error as e:
            logging.error(f"Socket error: {e}")
            return None, None

    def trigger_start_program(self, x, y):
        c, s = self.connection(self.HOST, self.PROGRAMMPORT)
        if c is None or s is None:
            logging.error("Failed to establish connection for start program")
            return

        try:
            msg = c.recv(1024).decode()
            logging.debug(f"Received message: {msg}")
            time.sleep(1)
            if msg == "send":
                cmd = f'({x},{y})\n'
                c.sendall(cmd.encode())
                logging.debug(f"Data sent successfully: {cmd}")
            else:
                logging.error("Unexpected message received")
        except Exception as e:
            logging.error(f"Socket connection failed: {e}")
        finally:
            c.close()
            s.close()

    def trigger_motion_started(self):
        c, s = self.connection(self.HOST, self.MOTIONPORT)
        
        if c is None or s is None:
            logging.error("Failed to establish connection for motion started")
            return

        try:
            while True:
                msg = c.recv(1024).decode()
                logging.debug(f"Received message: {msg}")
                if msg == "motion_started":
                    logging.debug("Motion started")
                    c.sendall(b"recordings_started\n")
                    logging.debug("Sent recordings_started")
                    break
                time.sleep(1)
        except Exception as e:
            logging.error(f"Socket connection failed: {e}")
        finally:
            c.close()
            s.close()
        

        
        
    def stop_mixing(self):
        print("Stop Mixing")
        c, s = self.connection(self.HOST, self.MIXINGPORT)
        if c is None or s is None:
            logging.error("Failed to establish connection for start program")
            return

        try:
            msg = c.recv(1024).decode()
            logging.debug(f"Received message: {msg}")
            time.sleep(1)

            cmd = f'(1)\n'
            c.sendall(cmd.encode())
            logging.debug(f"Data sent successfully: {cmd}")
        except Exception as e:
            logging.error(f"Socket connection failed: {e}")
        finally:
            c.close()
            s.close()



server = SocketTaskServer()
server.trigger_start_program(2, 2)

