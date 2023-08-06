# from tests.tools.build_env import *
from big_thing_py.tests.tools.mqtt_monitor_client import *
from big_thing_py.tests.tools.element_controller import *
from big_thing_py.tests.tools.test_tools_common import *
from big_thing_py.tests.tools.test_tools_utils import *


class SoPElement():

    def __init__(self, mqtt_monitor_client: SoPMQTTMonitor = None, debug: bool = None, data: SimulationData = None) -> None:
        # basic info
        self._name = data.name
        self._host = data.host
        self._port = data.port
        self._level = data.level

        # additional info
        self._is_local = data.is_local
        self._remote_user = data.remote_user
        self._remote_host = data.remote_host
        self._remote_port = data.remote_port
        self._remote_password = data.remote_password

        self._element_controller = None
        self._mqtt_monitor_client = None

        self._status: ScenarioStateType = None

        if self._is_local:
            if not self._remote_host:
                self._remote_host = '127.0.0.1'
            if not self._remote_port:
                self._remote_port = 22
            if not self._remote_user:
                self._remote_user = os.path.expanduser('~')

        self._element_controller = SoPElementController(
            user=self._remote_user, host=self._remote_host, port=self._remote_port, password=self._remote_password)

        if not mqtt_monitor_client:
            self._mqtt_monitor_client = SoPMQTTMonitor(
                name=self._name, host=self._host, port=self._port, debug=debug, level=self._level)
        else:
            self._mqtt_monitor_client = mqtt_monitor_client

    def set_mqtt_monitor_client(self, mqtt_monitor_client: SoPMQTTMonitor):
        self._mqtt_monitor_client = mqtt_monitor_client
        self._host = mqtt_monitor_client._host
        self._port = mqtt_monitor_client._port
        self._level = mqtt_monitor_client._level

    def get_mqtt_monitor_client(self):
        return self._mqtt_monitor_client


class SoPDelayElement(SoPElement):

    def __init__(self, mqtt_monitor_client: SoPMQTTMonitor = None, debug: bool = None, data: SimulationData = None) -> None:
        super().__init__(mqtt_monitor_client, debug, data)
        self._duration = data.duration

    def run(self):
        time.sleep(self._duration)

        return self


class SoPMiddlewareElement(SoPElement):

    def __init__(self, mqtt_monitor_client: SoPMQTTMonitor = None, parent_mqtt_monitor_client: SoPMQTTMonitor = None, debug: bool = None, data: SimulationData = None,
                 clean_start: bool = None, with_parent: bool = None) -> None:
        super().__init__(mqtt_monitor_client, debug, data)

        # thing & scenario in middleware
        self._thing_list: List[SoPThingElement] = []
        self._scenario_list: List[SoPScenarioElement] = []

        # additional middleware element's info
        self._local_server_port = data.local_server_port
        self._parent_host = data.parent_host
        self._parent_port = data.parent_port
        self._web_socket_port = data.web_socket_port
        self._ssl_web_socket_port = data.ssl_web_socket_port
        self._ssl_port = data.ssl_port

        self._parent_mqtt_monitor_client: SoPMQTTMonitor = parent_mqtt_monitor_client

        self._element_controller.connect()
        self._connected = True

        # replace '~' in path to absolute home directory
        if self._is_local:
            self._root_path = home_dir_append(data.middleware_path).rstrip('/')
            self._middleware_out_path = home_dir_append(
                data.middleware_out_path).rstrip('/')
        else:
            self._root_path = home_dir_append(
                data.middleware_path, self._remote_user).rstrip('/')
            self._middleware_out_path = home_dir_append(
                data.middleware_out_path, self._remote_user).rstrip('/')

        self._middleware_cfg_file_path = None
        self._mosquitto_config_file_path = None
        self._init_script_file_path = None
        self._run_script_file_path = None

        self._with_parent = with_parent
        self._clean_start = clean_start
        self._event_log: List[EventHolder] = []

        self._energy_score = 0
        self._qos_score = 0

        self._middleware_cfg = f'''{"" if self._with_parent else "//"}parent_broker_uri = "tcp://{self._parent_host}:{self._parent_port}"
broker_uri = "tcp://{self._host}:{self._port}"

middleware_identifier = "{self._name}"
socket_listening_port = {self._local_server_port}
alive_checking_period = 60

main_db_file_path = "{self._middleware_out_path}/{self._name}_Main.db"
value_log_db_file_path = "{self._middleware_out_path}/{self._name}_ValueLog.db"

log_level = 5
log_file_path = "{self._middleware_out_path}/{self._name}_middleware.log"
log_max_size = 300
log_backup_num = 100'''

        self._mosquitto_conf = f'''persistence true
persistence_location /var/lib/mosquitto/

include_dir /etc/mosquitto/conf.d

listener {self._port} 0.0.0.0
protocol mqtt
allow_anonymous true

listener {self._web_socket_port} 0.0.0.0
protocol websockets
allow_anonymous true

listener {self._ssl_port} 0.0.0.0
protocol mqtt
allow_anonymous true
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/host.crt
keyfile /etc/mosquitto/certs/host.key
require_certificate true

listener {self._ssl_web_socket_port} 0.0.0.0
protocol websockets
allow_anonymous true
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/host.crt
keyfile /etc/mosquitto/certs/host.key
require_certificate true'''

        self._init_sh = f'''MAIN_DB={self._middleware_out_path}/{self._name}_Main.db
VALUE_LOG_DB={self._middleware_out_path}/{self._name}_ValueLog.db

if [ -f "$MAIN_DB" ]; then
    rm -f $MAIN_DB
fi
if [ -f "$VALUE_LOG_DB" ]; then
    rm -f $VALUE_LOG_DB
fi

sqlite3 $MAIN_DB < {self._root_path}/src/middleware/MainDBCreate
sqlite3 $VALUE_LOG_DB < {self._root_path}/src/middleware/ValueLogDBCreate'''

        if not self._root_path:
            self._root_path = "/".join(
                str(get_project_root()).split("/")[:-1] + ['middleware'])
            if not os.path.exists(self._root_path):
                raise SOPTEST_LOG_DEBUG(f'middleware path was not exist!', -1)

    def make_file(self, text: str = None, target_file_path: str = None):
        os.makedirs(get_upper_path(target_file_path), exist_ok=True)
        with open(target_file_path, 'w') as f:
            f.writelines(text)

        # SOPTEST_LOG_DEBUG(
        #     f'{target_file_path} file is made', 1)
        return target_file_path

    def clean_remain_scenario(self, timeout: float = 10):
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(encode_MQTT_message(SoPProtocolType.WebClient.EM_REFRESH.value % self._mqtt_monitor_client._client_id, f'{{}}'),
                                                                                 SoPProtocolType.WebClient.ME_RESULT_SCENARIO_LIST.value % self._mqtt_monitor_client._client_id, timeout=timeout)
        for scenario_info in payload['scenarios']:
            scenario = SoPScenarioElement(
                data=SimulationData(name=scenario_info['name'], host=self._host, port=self._port))
            if scenario_info['state'] in [ScenarioStateType.RUNNING, ScenarioStateType.EXECUTING, ScenarioStateType.SCHEDULING]:
                scenario.stop()
            scenario.delete()
            # if scenario_info['name'] == scenario:
            #     return dict(id=scenario_info['id'], name=scenario_info['name'], code=scenario_info['contents'],
            #                 state=ScenarioStateType.get(scenario_info['state']), schedule_info=scenario_info['scheduleInfo'])

    def check_online_with_timeout(self, mqtt_monitor_client: SoPMQTTMonitor = None, timeout: int = 60, check_interval: float = 0.5):
        while timeout > 0:
            if self.check_online(mqtt_monitor_client=mqtt_monitor_client, timeout=check_interval):
                return True
            else:
                timeout -= check_interval
                time.sleep(check_interval)
        else:
            raise SOPTEST_LOG_DEBUG(
                f'[TIMEOUT] Running middleware {self._name} was failed...', -1)

    def check_online(self, mqtt_monitor_client: SoPMQTTMonitor = None, timeout: int = 60):
        topic, payload, timestamp = mqtt_monitor_client.publish_and_expect(
            encode_MQTT_message(SoPProtocolType.WebClient.EM_REFRESH.value %
                                (mqtt_monitor_client._client_id), f'{{}}'),
            SoPProtocolType.WebClient.ME_RESULT_SERVICE_LIST.value % (
                mqtt_monitor_client._client_id),
            timeout=timeout)

        if payload is not None:
            SOPTEST_LOG_DEBUG(
                f'Middleware {self._name} on {self._host}:{self._port} was online!', 0)
            return True
        else:
            SOPTEST_LOG_DEBUG(
                f'Middleware {self._name} on {self._host}:{self._port} was not online!', 1)
            return False

    def make_middleware_config_file(self):
        self._middleware_cfg_file_path = self.make_file(text=self._middleware_cfg, target_file_path=os.path.join(
            get_project_root(), 'big_thing_py/tests/middleware_config', f'{self._name}_middleware.cfg'))
        self._mosquitto_config_file_path = self.make_file(text=self._mosquitto_conf, target_file_path=os.path.join(
            get_project_root(), 'big_thing_py/tests/middleware_config', f'{self._name}_mosquitto.conf'))
        self._init_script_file_path = self.make_file(text=self._init_sh, target_file_path=os.path.join(
            get_project_root(), 'big_thing_py/tests/middleware_config', f'{self._name}_init.sh'))
        # self._run_script_file_path = self.make_file(text=self._run_sh, target_file_path=os.path.join(
        #     get_project_root(), 'big_thing_py/tests/middleware_config', f'run_{self._name}.sh'))

    def run(self, check: bool = True, timeout: int = 60):

        # check parent middleware was online
        def check_parent_online():
            if self._with_parent:
                if not self.check_online(mqtt_monitor_client=self._parent_mqtt_monitor_client):
                    raise SOPTEST_LOG_DEBUG(
                        'parent middelware was not online...', -1)

        # return True mean that middleware was online
        def check_clean_start():
            if self._clean_start:
                if self.check_online(mqtt_monitor_client=self._mqtt_monitor_client):
                    self.kill()
            else:
                if self.check_online(mqtt_monitor_client=self._mqtt_monitor_client, timeout=1):
                    self.clean_remain_scenario()
                    return True
                else:
                    SOPTEST_LOG_DEBUG(
                        'Middleware was not online... try to run middleware', 1)
                    # disconnect middleware was will be killed regaredless of clean_start
                    self.kill()
                    return False

        def send_file_to_remote():
            remote_middleware_cfg_file_path = os.path.join(
                self._middleware_out_path, os.path.basename(self._middleware_cfg_file_path))
            remote_mosquitto_config_file_path = os.path.join(
                self._middleware_out_path, os.path.basename(self._mosquitto_config_file_path))
            remote_init_script_file_path = os.path.join(
                self._middleware_out_path, os.path.basename(self._init_script_file_path))

            self._element_controller.send_file(
                self._middleware_cfg_file_path, remote_middleware_cfg_file_path)
            self._element_controller.send_file(
                self._mosquitto_config_file_path, remote_mosquitto_config_file_path)
            self._element_controller.send_file(
                self._init_script_file_path, remote_init_script_file_path)

            return remote_middleware_cfg_file_path, remote_mosquitto_config_file_path, remote_init_script_file_path

        def run_mosquitto(mosquitto_config_file_path):
            cnt = 0
            while True:
                # 프로세스 이름이 mosquitto이고 self._port 번호를 쓰는 프로세스가 있는지 확인하는 함수
                # command = f'netstat -nap 2>/dev/null | grep mosquitto | grep {self._port}'
                # result = os.popen(command).read().split('\n')
                # port_list = []
                # for line in result:
                #     if line:
                #         port_list.append(int(line.split()[3].split(':')[1]))
                target_mosquitto_pid_list = []
                target_mosquitto_pid_list += self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip=self._host, local_port=self._port) + self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip='0.0.0.0', local_port=self._port)
                target_mosquitto_pid_list += self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip=self._host, local_port=self._port + 1) + self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip='0.0.0.0', local_port=self._port)
                target_mosquitto_pid_list += self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip=self._host, local_port=self._port + 2) + self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip='0.0.0.0', local_port=self._port)
                target_mosquitto_pid_list += self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip=self._host, local_port=self._port + 3) + self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip='0.0.0.0', local_port=self._port)
                target_mosquitto_pid_list += self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip=self._host, local_port=self._port + 4) + self._element_controller.get_duplicate_proc_pid(
                    'mosquitto', local_ip='0.0.0.0', local_port=self._port)
                if len(target_mosquitto_pid_list) > 0:
                    break
                else:  # '/sbin/mosquitto -c /mnt/ramdisk/middleware_level3_1_mosquitto.conf'
                    mosquitto_log_path = mosquitto_config_file_path.replace(
                        '_mosquitto', '').replace('middleware', 'mosquitto').replace('conf', 'log')
                    self._element_controller.send_command(
                        f'/sbin/mosquitto -c {mosquitto_config_file_path} > {mosquitto_log_path}', ignore_result=True)
                    if cnt > 3:
                        print(
                            f'/sbin/mosquitto -c {mosquitto_config_file_path}')
                        time.sleep(1)
                    else:
                        time.sleep(0.2)
                    cnt += 1
# ''/sbin/mosquitto -c /mnt/ramdisk/middleware_level1_4122_mosquitto.conf'

        def make_db(init_script_file_path: str):
            self._element_controller.send_command(
                f'chmod +x {init_script_file_path}')
            self._element_controller.send_command(
                f'bash {init_script_file_path}')

            db_created = False
            while not db_created:
                file_list = self._element_controller.send_command(
                    f'ls {self._middleware_out_path}')
                for file in file_list:
                    if file == f'{self._name}_Main.db':
                        db_created = True
                time.sleep(0.1)

        def run_middleware(init_script_file_path: str, middleware_cfg_file_path: str):
            make_db(init_script_file_path)
            self._element_controller.send_command(
                f'{self._root_path}/src/middleware/sopiot_middleware -f {middleware_cfg_file_path}', ignore_result=True)

        ####################################################################################################################################

        self.make_middleware_config_file()

        # if not check_clean_start():
        #     # run mosquitto & middleware
        #     remote_middleware_cfg_file_path, remote_mosquitto_config_file_path, remote_init_script_file_path = send_file_to_remote()
        #     run_mosquitto(remote_mosquitto_config_file_path)
        #     run_middleware(remote_init_script_file_path,
        #                    remote_middleware_cfg_file_path)

        #     self._mqtt_monitor_client.run()
        #     if check:
        #         self.check_online_with_timeout(
        #             mqtt_monitor_client=self._mqtt_monitor_client, timeout=timeout, check_interval=0.5)
        #     else:
        #         SOPTEST_LOG_DEBUG(
        #             f'Middleware {self._name} was running... not checked, but we believe it...', 1)

        check_parent_online()
        remote_middleware_cfg_file_path, remote_mosquitto_config_file_path, remote_init_script_file_path = send_file_to_remote()
        run_mosquitto(remote_mosquitto_config_file_path)
        time.sleep(1)
        run_middleware(remote_init_script_file_path,
                       remote_middleware_cfg_file_path)

        self._mqtt_monitor_client.run()
        if check:
            self.check_online_with_timeout(
                mqtt_monitor_client=self._mqtt_monitor_client, timeout=timeout, check_interval=0.5)
        else:
            SOPTEST_LOG_DEBUG(
                f'Middleware {self._name} was running... not checked, but we believe it...', 1)

        return self

    # user name을 굳이 이용할 필요는 없어 보인다. 왜냐하면 ip port만 으로도 충분히 미들웨어를 특정할 수 있다. 어짜피 ip port가 겹치면 미들웨어가 실행이 안됨
    def kill(self):
        target_pid_list = self._element_controller.get_duplicate_proc_pid(
            'sopiot_mid', local_ip='0.0.0.0', local_port=self._local_server_port, foreign_ip=self._host, foreign_port=self._port,
            args=self._middleware_cfg_file_path.split('/')[-1])
        target_mosquitto_pid_list = self._element_controller.get_duplicate_proc_pid(
            'mosquitto', local_ip=self._host, local_port=self._port)

        if len(target_pid_list) == 0 and len(target_mosquitto_pid_list) == 0:
            pass
            # SOPTEST_LOG_DEBUG(
            #     f'middleware {self._host}:{self._port} was already killed!', 0)
        else:
            for target_pid in target_pid_list:
                self._element_controller.send_command(
                    f'kill -9 {target_pid} 2> /dev/null', ignore_result=True)
                SOPTEST_LOG_DEBUG(
                    f'middleware {self._host}:{self._port} {self._name} was killed!', 0)
            for target_pid in target_mosquitto_pid_list:
                self._element_controller.send_command(
                    f'kill -9 {target_pid} 2> /dev/null', ignore_result=True)
                # SOPTEST_LOG_DEBUG(
                #     f'mosquitto {self._host}:{self._port} {self._name} was killed!', 0)


class SoPThingElement(SoPElement):

    def __init__(self, mqtt_monitor_client: SoPMQTTMonitor = None, debug: bool = None, data: SimulationData = None,
                 clean_start: bool = None) -> None:
        super().__init__(mqtt_monitor_client, debug, data)

        self._element_controller.connect()

        self._is_super = data.is_super
        self._is_manager = data.is_manager
        self._is_parallel = data.is_parallel
        self._raw_thing_file_path = home_dir_append(
            data.raw_thing_file_path, self._remote_user).rstrip('/')
        self._thing_file_path = home_dir_append(
            data.thing_file_path, self._remote_user).rstrip('/')
        self._args = data.args

        self._function_list = None
        self._value_list = None
        self._alive_cycle = None
        self._middleware_name = None

        self._clean_start = clean_start
        self._total_energy_consumption = 0

        self._event_log: List[EventHolder] = []

    @exception_wrapper
    def check_register(self, timeout: int = 60):
        target_topic_list = [SoPProtocolType.Base.TM_REGISTER.value % self._name,
                             SoPProtocolType.Base.MT_RESULT_REGISTER.value % self._name]
        self._mqtt_monitor_client.subscribe(target_topic_list)

        if self._is_local:
            topic, payload, timestamp = self._mqtt_monitor_client.command_and_expect(
                trigger_command=f'python {home_dir_append(self._thing_file_path)} -n {self._name} -ip {self._host} -p {self._port} {" ".join(self._args if self._args is not None else [])}  > /dev/null 2>&1 &',
                target_topic=SoPProtocolType.Base.TM_REGISTER.value % self._name,
                auto_subscribe=True,
                timeout=timeout)
        else:
            self._element_controller.send_command(
                f'mkdir -p {os.path.dirname(self._thing_file_path)}')
            self._element_controller.send_file(
                self._raw_thing_file_path, self._thing_file_path)
            self._element_controller.send_command(
                f'python {home_dir_append(self._thing_file_path, self._remote_user)} -n {self._name} -ip {self._host} -p {self._port} {" ".join(self._args if self._args is not None else [])} > /dev/null 2>&1 &', ignore_result=True, background=True)

            # 'python /home/thsvkd/Workspace/generated_things/simulation1/Multicooker.py -n Multicooker -ip 127.0.0.1 -p 58210  2> /dev/null &'
            topic, payload, timestamp = self._mqtt_monitor_client.expect(
                target_topic=SoPProtocolType.Base.TM_REGISTER.value % self._name,
                auto_subscribe=True,
                timeout=timeout)

        if payload is not None:
            # thing_name = topic.split('/')[-1]
            alive_cycle = payload['alive_cycle']
            is_super = payload['is_super']
            value_list = payload['values']
            function_list = payload['functions']
            for function in function_list:
                function['total_energy_consumption'] = 0
                function['total_duration'] = 0
                function['utilization'] = 0
                function['call_count'] = 0
            # SOPTEST_LOG_DEBUG(f'All register element checked!', 0)
            # if is_super:
            #     SOPTEST_LOG_DEBUG(f'* Thing {self._name} is super! *', 0)

            topic, payload, timestamp = self._mqtt_monitor_client.expect(
                target_topic=SoPProtocolType.Base.MT_RESULT_REGISTER.value % self._name,
                auto_subscribe=False,
                timeout=timeout)
            if int(payload['error']) in [0, -4]:
                middleware_name = payload['middleware_name']
                # SOPTEST_LOG_DEBUG(
                #     f'Thing {self._name} register result checked!', 0)
                self._value_list = value_list
                self._function_list = function_list
                self._alive_cycle = alive_cycle
                self._middleware_name = middleware_name
                self._is_super = is_super

                return True
            else:
                SOPTEST_LOG_DEBUG(
                    f'Register failed... error code: {payload["error"]}', -1)
                return False
        else:
            return False

    @exception_wrapper
    def check_unregister(self, trigger_command: List[str] = None, timeout: int = 60):
        target_topic_list = [
            SoPProtocolType.Base.MT_RESULT_UNREGISTER.value % self._name]
        self._mqtt_monitor_client.subscribe(target_topic_list)

        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_msg=encode_MQTT_message(
                SoPProtocolType.Base.TM_UNREGISTER.value % self._name, '{}', time.time()),
            target_topic=SoPProtocolType.Base.MT_RESULT_UNREGISTER.value % self._name,
            auto_subscribe=False,
            timeout=timeout)

        if payload['error'] in [0, -1, -4]:
            SOPTEST_LOG_DEBUG(f'Thing unregister checked!', 0)
            return True
        else:
            SOPTEST_LOG_DEBUG(
                f'Thing register failed...', -1)
            return False

    def run(self, check: bool = True, timeout: int = 25):
        SOPTEST_LOG_DEBUG(f'Start run {self._name}...', 0)
        self._mqtt_monitor_client.run()

        self._mqtt_monitor_client.subscribe([SoPProtocolType.Base.TM_REGISTER.value % self._name,
                                             SoPProtocolType.Base.TM_UNREGISTER.value % self._name,
                                             SoPProtocolType.Base.MT_RESULT_REGISTER.value % self._name,
                                             SoPProtocolType.Base.MT_RESULT_UNREGISTER.value % self._name])
        self.kill()

        if check:
            if self.check_register(timeout=timeout):
                SOPTEST_LOG_DEBUG(
                    f'Register complete thing {self._name} on {self._middleware_name}', 0)

                for function in self._function_list:
                    self._mqtt_monitor_client.subscribe([SoPProtocolType.Base.MT_EXECUTE.value % (function['name'], self._name, '+', '#'),
                                                         (SoPProtocolType.Base.MT_EXECUTE.value % (
                                                             function['name'], self._name, '', '')).rstrip('/'),
                                                        SoPProtocolType.Base.TM_RESULT_EXECUTE.value % (
                                                            function['name'], self._name, '+', '#'),
                                                        (SoPProtocolType.Base.TM_RESULT_EXECUTE.value % (function['name'], self._name, '', '')).rstrip('/')])
                    if self._is_super:
                        self._mqtt_monitor_client.subscribe([
                            SoPProtocolType.Super.MS_EXECUTE.value % (
                                function['name'], self._name, self._middleware_name, '#'),
                            SoPProtocolType.Super.SM_EXECUTE.value % (
                                '+', '+', '+', self._name),
                            SoPProtocolType.Super.MS_RESULT_EXECUTE.value % (
                                '+', '+', '+', self._name),
                            SoPProtocolType.Super.SM_RESULT_EXECUTE.value % (
                                function['name'], self._name, self._middleware_name, '#'),
                            SoPProtocolType.Super.MS_SCHEDULE.value % (
                                function['name'], self._name, self._middleware_name, '#'),
                            SoPProtocolType.Super.SM_SCHEDULE.value % (
                                '+', '+', '+', self._name),
                            SoPProtocolType.Super.MS_RESULT_SCHEDULE.value % (
                                '+', '+', '+', self._name),
                            SoPProtocolType.Super.SM_RESULT_SCHEDULE.value % (
                                function['name'], self._name, self._middleware_name, '#')])
                # for value in self._value_list:
                #     self._mqtt_monitor_client.subscribe([SoPProtocolType.Default.TM_VALUE_PUBLISH.value % (self._name, value['name']),
                #                                         SoPProtocolType.Default.TM_VALUE_PUBLISH_OLD.value % (self._name, value['name'])])
            else:
                raise SOPTEST_LOG_DEBUG(
                    f'Thing {self._name} register failed...', -1)
        else:
            SOPTEST_LOG_DEBUG(
                f'Thing {self._name} was running... not checked, but we believe it...', 1)

        return self

    def kill(self):
        target_pid_list = self._element_controller.get_duplicate_proc_pid(
            'python', foreign_ip=self._host, foreign_port=self._port, args=f'-n {self._name}')

        if target_pid_list:
            for target_pid in target_pid_list:
                self._element_controller.send_command(
                    f'kill -9 {target_pid} 2> /dev/null')
                SOPTEST_LOG_DEBUG(
                    f'thing {self._host}:{self._port} {self._name} was killed!', 0)
        else:
            pass
            # SOPTEST_LOG_DEBUG(
            #     f'thing {self._host}:{self._port} {self._name} was already killed!', 0)

    def unregister(self,  check: bool = True, timeout: int = 60):
        self.kill()
        if check:
            if self.check_unregister(timeout=timeout):
                SOPTEST_LOG_DEBUG(
                    f'Thing {self._name} was unregister from {self._middleware_name}', 0)
            else:
                raise SOPTEST_LOG_DEBUG(
                    f'Thing {self._name} unregister failed...', -1)
        else:
            SOPTEST_LOG_DEBUG(
                f'Thing {self._name} was unregistered... not checked, but we believe it...', 1)

        return self

    def find_function(self, name: str):
        for function in self._function_list:
            if function['name'] == name:
                return function
        else:
            return False


class SoPScenarioElement(SoPElement):

    def __init__(self, mqtt_monitor_client: SoPMQTTMonitor = None, debug: bool = None, data: SimulationData = None, user_data=None) -> None:
        super().__init__(mqtt_monitor_client, debug, data)

        self._raw_scenario_file_path = home_dir_append(
            data.raw_scenario_file_path)
        self._scenario_file_path = home_dir_append(data.scenario_file_path)
        self._scenario_code = self.load_code(self._raw_scenario_file_path)
        self._period = data.period
        self._first_service = data.first_service
        self._last_service = data.last_service
        self._service_num = data.service_num

        self._loop_check: bool = False
        self._avg_latency: float = 0

        self._event_log: List[EventHolder] = []

        self._thing_list: List[SoPThingElement] = []

    def load_code(self, scenario_file_path: str = None):
        if scenario_file_path:
            with open(scenario_file_path, 'r') as f:
                scenario_file = f.readlines()
            if not self._name:
                self._name = scenario_file.pop(0).strip().strip('[').strip(']')
            else:
                scenario_file.pop(0)
            return ''.join(scenario_file)
        else:
            SOPTEST_LOG_DEBUG('[WARN] No scenario code!!!', 1)
            return False

    @exception_wrapper
    def update_state(self, timeout: int = 60):
        retry_period = 0.5
        while timeout:
            topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(encode_MQTT_message(SoPProtocolType.WebClient.EM_REFRESH.value % self._mqtt_monitor_client._client_id, f'{{}}'),
                                                                                     SoPProtocolType.WebClient.ME_RESULT_SCENARIO_LIST.value % self._mqtt_monitor_client._client_id,
                                                                                     auto_subscribe=True,
                                                                                     auto_unsubscribe=False,
                                                                                     timeout=timeout)
            for scenario_info in payload['scenarios']:
                if scenario_info['name'] == self._name:
                    return dict(id=scenario_info['id'], name=scenario_info['name'], code=scenario_info['contents'],
                                state=ScenarioStateType.get(scenario_info['state']), schedule_info=scenario_info['scheduleInfo'])
            else:
                SOPTEST_LOG_DEBUG(
                    f'Scenario {self._name} not found...', -1)
                timeout -= retry_period
                time.sleep(retry_period)
        else:
            raise SOPTEST_LOG_DEBUG(
                f'[{get_current_function_name()}] Update scenario state failed...', -1)

    @exception_wrapper
    def check_scenario_state(self, target_scenario_state: List[ScenarioStateType], timeout: int = 60):
        target_scenario_info = self.update_state(timeout=timeout)
        current_scenario_state: ScenarioStateType = target_scenario_info.get(
            'state', False)
        if not current_scenario_state:
            raise SOPTEST_LOG_DEBUG(
                f'[{get_current_function_name()}] Get scenario state failed...', -1)
        elif not target_scenario_state:
            raise SOPTEST_LOG_DEBUG(
                f'[{get_current_function_name()}] target_scenario_state is empty...', -1)

        if current_scenario_state in target_scenario_state:
            SOPTEST_LOG_DEBUG(
                f'scenario state matched! -- scenario: {self._name}, state: {current_scenario_state.value}', 0)
            return current_scenario_state
        else:
            SOPTEST_LOG_DEBUG(
                f'scenario state not matched! -- scenario: {self._name}, state: {current_scenario_state.value}', 1)
            return current_scenario_state

    @exception_wrapper
    def check_scenario_ready(self, stuck_handling: bool = False, timeout: int = 60):
        current_scenario_state = self.check_scenario_state(
            [ScenarioStateType.INITIALIZED, ScenarioStateType.COMPLETED], timeout)

        if current_scenario_state in [ScenarioStateType.INITIALIZED, ScenarioStateType.COMPLETED]:
            SOPTEST_LOG_DEBUG(
                f'scenario {self._name} is {current_scenario_state.value}...', 1)
            return True
        elif current_scenario_state in [ScenarioStateType.STUCKED]:
            if stuck_handling:
                SOPTEST_LOG_DEBUG(
                    f'scenario {self._name} is STUCKED... try to update scenario', 1)
                if self.update():
                    return True
                else:
                    raise SOPTEST_LOG_DEBUG(
                        f'scenario STUCKED resolve failed...', -1)
            else:
                SOPTEST_LOG_DEBUG(
                    f'scenario {self._name} is STUCKED... but skip to update scenario', 1)
        else:
            SOPTEST_LOG_DEBUG(
                f'scenario {self._name} is not ready -- state: {current_scenario_state.value}', 1)
            return False

    # verify, add, run, stop, update, delete scenario method
    # subscribe trigger topic for capture event log
    @exception_wrapper
    def verify(self, timeout: int = 60):
        trigger_topic = SoPProtocolType.WebClient.EM_VERIFY_SCENARIO.value % self._mqtt_monitor_client._client_id
        trigger_payload = json_string_to_dict(
            dict(name=self._name, text=self._scenario_code))
        trigger_message = encode_MQTT_message(trigger_topic, trigger_payload)
        target_topic = SoPProtocolType.WebClient.ME_RESULT_VERIFY_SCENARIO.value % self._mqtt_monitor_client._client_id

        self._mqtt_monitor_client.subscribe(trigger_topic)
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_message,
            target_topic,
            auto_unsubscribe=False,
            timeout=timeout)

        if check_result_payload(payload, ElementType.SCENARIO.value, self._name, ElementActionType.SCENARIO_VERIFY.value, True):
            return self

    @exception_wrapper
    def add(self, timeout: int = 60):
        trigger_topic = SoPProtocolType.WebClient.EM_ADD_SCENARIO.value % self._mqtt_monitor_client._client_id
        trigger_payload = json_string_to_dict(
            dict(name=self._name, text=self._scenario_code))
        trigger_message = encode_MQTT_message(
            trigger_topic, trigger_payload)
        target_topic = SoPProtocolType.WebClient.ME_RESULT_SCHEDULE_SCENARIO.value % self._mqtt_monitor_client._client_id

        self._mqtt_monitor_client.subscribe(trigger_topic)
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_message,
            target_topic,
            auto_unsubscribe=False,
            timeout=timeout)

        if check_result_payload(payload, ElementType.SCENARIO.value, self._name, ElementActionType.SCENARIO_ADD.value, True):
            # wait for scenario add to middleware's DB
            self._status = self.update_state(timeout)
            return self

    @exception_wrapper
    def run(self, timeout: int = 60):
        trigger_topic = SoPProtocolType.WebClient.EM_RUN_SCENARIO.value % self._mqtt_monitor_client._client_id
        trigger_payload = json_string_to_dict(
            dict(name=self._name, text=self._scenario_code))
        trigger_message = encode_MQTT_message(
            trigger_topic, trigger_payload)
        target_topic = SoPProtocolType.WebClient.ME_RESULT_RUN_SCENARIO.value % self._mqtt_monitor_client._client_id

        self._mqtt_monitor_client.subscribe(trigger_topic)
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_message,
            target_topic,
            auto_unsubscribe=False,
            timeout=timeout)

        if check_result_payload(payload, ElementType.SCENARIO.value, self._name, ElementActionType.SCENARIO_RUN.value, True):
            return self

    @exception_wrapper
    def stop(self, timeout: int = 60):
        trigger_topic = SoPProtocolType.WebClient.EM_STOP_SCENARIO.value % self._mqtt_monitor_client._client_id
        trigger_payload = json_string_to_dict(
            dict(name=self._name, text=self._scenario_code))
        trigger_message = encode_MQTT_message(trigger_topic, trigger_payload)
        target_topic = SoPProtocolType.WebClient.ME_RESULT_STOP_SCENARIO.value % self._mqtt_monitor_client._client_id

        self._mqtt_monitor_client.subscribe(trigger_topic)
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_message,
            target_topic,
            auto_unsubscribe=False,
            timeout=timeout)

        if check_result_payload(payload, ElementType.SCENARIO.value, self._name, ElementActionType.SCENARIO_STOP.value, True):
            return self

    @exception_wrapper
    def update(self, timeout: int = 60):
        trigger_topic = SoPProtocolType.WebClient.EM_UPDATE_SCENARIO.value % self._mqtt_monitor_client._client_id
        trigger_payload = json_string_to_dict(
            dict(name=self._name, text=self._scenario_code))
        trigger_message = encode_MQTT_message(trigger_topic, trigger_payload)
        target_topic = SoPProtocolType.WebClient.ME_RESULT_SCHEDULE_SCENARIO.value % self._mqtt_monitor_client._client_id

        self._mqtt_monitor_client.subscribe(trigger_topic)
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_message,
            target_topic,
            auto_unsubscribe=False,
            timeout=timeout)

        if check_result_payload(payload, ElementType.SCENARIO.value, self._name, ElementActionType.SCENARIO_UPDATE.value, True):
            return self

    @exception_wrapper
    def delete(self, timeout: int = 60):
        trigger_topic = SoPProtocolType.WebClient.EM_DELETE_SCENARIO.value % self._mqtt_monitor_client._client_id
        trigger_payload = json_string_to_dict(
            dict(name=self._name, text=self._scenario_code))
        trigger_message = encode_MQTT_message(trigger_topic, trigger_payload)
        target_topic = SoPProtocolType.WebClient.ME_RESULT_DELETE_SCENARIO.value % self._mqtt_monitor_client._client_id

        self._mqtt_monitor_client.subscribe(trigger_topic)
        topic, payload, timestamp = self._mqtt_monitor_client.publish_and_expect(
            trigger_message,
            target_topic,
            auto_unsubscribe=False,
            timeout=timeout)

        if check_result_payload(payload, ElementType.SCENARIO.value, self._name, ElementActionType.SCENARIO_DELETE.value, True):
            return self
