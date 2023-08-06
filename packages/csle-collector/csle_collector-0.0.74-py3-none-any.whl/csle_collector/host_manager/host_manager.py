import logging
import socket
import time
import grpc
import threading
from concurrent import futures
from confluent_kafka import Producer
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
from csle_collector.host_manager.host_manager_util import HostManagerUtil
import csle_collector.constants.constants as constants


class HostMonitorThread(threading.Thread):
    """
    Thread that collects the Host statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str,
                 time_step_len_seconds: int):
        """
        Intializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from
        :param hostname: hostname of the server we are pushing from
        :param time_step_len_seconds: the length of a timestep
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.latest_ts = time.time()
        self.failed_auth_last_ts = HostManagerUtil.read_latest_ts_auth()
        self.login_last_ts = HostManagerUtil.read_latest_ts_login()
        self.time_step_len_seconds = time_step_len_seconds
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info("HostMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses log files and metrics on the host and pushes it to Kafka periodically

        :return: None
        """
        while self.running:
            time.sleep(self.time_step_len_seconds)
            host_metrics = HostManagerUtil.read_host_metrics(failed_auth_last_ts=self.failed_auth_last_ts,
                                                             login_last_ts=self.login_last_ts)
            record = host_metrics.to_kafka_record(ip=self.ip)
            self.producer.produce(constants.KAFKA_CONFIG.HOST_METRICS_TOPIC_NAME, record)
            self.producer.poll(0)
            self.failed_auth_last_ts = HostManagerUtil.read_latest_ts_auth()
            self.login_last_ts = HostManagerUtil.read_latest_ts_login()


class HostManagerServicer(csle_collector.host_manager.host_manager_pb2_grpc.HostManagerServicer):
    """
    gRPC server for collecting Host statistics.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.HOST_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.HOST_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.host_monitor_thread = None
        logging.info(f"Starting the HostManager hostname: {self.hostname} ip: {self.ip}")

    def getIdsAlerts(self, request: csle_collector.host_manager.host_manager_pb2.GetHostMetricsMsg,
                     context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
        """
        Gets the host metrics from given timestamps

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with IDS statistics
        """
        host_metrics = HostManagerUtil.read_host_metrics(failed_auth_last_ts=request.failed_auth_last_ts,
                                                         login_last_ts=request.login_last_ts)
        host_metrics_dto = host_metrics.to_dto(ip=self.ip)
        return host_metrics_dto

    def startHostMonitor(self, request: csle_collector.host_manager.host_manager_pb2.StartHostMonitorMsg,
                         context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        Starts the Host monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor thread
        """
        logging.info(f"Starting the HostMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.host_monitor_thread is not None:
            self.host_monitor_thread.running = False
        self.host_monitor_thread = HostMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                     ip=self.ip, hostname=self.hostname,
                                                     time_step_len_seconds=request.time_step_len_seconds)
        self.host_monitor_thread.start()
        logging.info("Started the HostMonitor thread")
        return csle_collector.host_manager.host_manager_pb2.HostMonitorDTO(running=True)

    def stopHostMonitor(self, request: csle_collector.host_manager.host_manager_pb2.StopHostMonitorMsg,
                        context: grpc.ServicerContext) -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        Stops the Host monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor thread
        """
        if self.host_monitor_thread is not None:
            self.host_monitor_thread.running = False
        return csle_collector.host_manager.host_manager_pb2.HostMonitorDTO(running=False)

    def getHostMonitorStatus(self, request: csle_collector.host_manager.host_manager_pb2.GetHostMonitorStatusMsg,
                             context: grpc.ServicerContext) \
            -> csle_collector.host_manager.host_manager_pb2.HostMonitorDTO:
        """
        Gets the status of the Host Monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Host monitor
        """
        running = False
        if self.host_monitor_thread is not None:
            running = self.host_monitor_thread.running
        return csle_collector.host_manager.host_manager_pb2.HostMonitorDTO(running=running)


def serve(port: int = 50049, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "host_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.HOST_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.HOST_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.host_manager.host_manager_pb2_grpc.add_HostManagerServicer_to_server(
        HostManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"HostManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
