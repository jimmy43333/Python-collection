import socket
import threading
import concurrent.futures

def handle_client(self, client_socket, idle_break=False):
        client_socket.settimeout(self.socket_idle_timeout)
        temp = ""
        count = 0
        while self.socket_running:
            try:
                request = client_socket.recv(self.socket_len).decode()
                count = 0
                if request == "exit":
                    client_socket.close()
                    break
                if request:
                    if len(request) >= self.socket_len:
                        if not self.socket_len_alert:
                            # socket package length
                            alert_msg = f"(Publish alert ONCE) " \
                                        f"socket package len {self.socket_len}: " \
                                        f"{request[:200]}..."
                            # Publish alert flag
                            self.publisher.pub_ats_alert(alert_msg, "O")
                            self.socket_len_alert = True
                    request = temp + request
                    temp = ""
                    request = request.split("\n")
                    for ele in request:
                        if ele:
                            parsed_dictionary = ele
                            if parsed_dictionary == "Fragment":
                                temp = ele
                                continue
                            if parsed_dictionary:
                                sid = parsed_dictionary["SID"]
                                self.handle_data_function[sid](parsed_dictionary)
                else:
                    break
                client_socket.send("ACK!".encode())
            except socket.timeout:
                if idle_break:
                    count += 1
                    if count >= self.socket_idle_timeout_retry:
                        duration = self.socket_idle_timeout * count
                        who = client_socket.getpeername()
                        msg = f"[x] Client Idle (> {duration} secs), Disconnect: {who} !"
                        self.log_debug_data(msg)
                        client_socket.close()
                        break
                else:
                    continue
            except socket.error:
                break
            except Exception as e:
                self.log(f"handle_client: {str(e)}")

    def run_socket_server(self, ip, port):
        bind_ip = ip
        bind_port = int(port)
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socket_server.bind((bind_ip, bind_port))
            socket_server.listen(168)
            self.socket_server.append(socket_server)
        except Exception as e:
            self.publisher.pub_ats_alert(e)
            raise Exception(e)
        self.log_debug_data("[*] Listening on %s:%d" % (bind_ip, bind_port))
        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as client_executor:
            while self.socket_running:
                try:
                    client, addr = socket_server.accept()
                    t = threading.active_count()
                    # 目前已建立的池中 threads 數量
                    pt = len(client_executor._threads)
                    # judge item in the list
                    if self.socket_idle_break_list and addr[0] in self.socket_idle_break_list:
                        msg = f"[*] Accepted from: {addr[0]}:{addr[1]}" \
                              f", Enable Break (T:{t}, PT:{pt})"
                        flag = True
                    else:
                        msg = f"[*] Accepted from: {addr[0]}:{addr[1]} (T:{t}, PT:{pt})"
                        flag = False
                    self.log_debug_data(msg)
                    client_executor.submit(self.handle_client, client, flag)
                    # client_handler = threading.Thread(target=self.handle_client,
                    #                                 args=(client,))
                    # client_handler.start()
                except KeyboardInterrupt:
                    break