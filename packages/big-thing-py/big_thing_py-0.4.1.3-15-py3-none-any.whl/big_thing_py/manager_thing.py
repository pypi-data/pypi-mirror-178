from big_thing_py.big_thing import *
from big_thing_py.staff_thing import *
from big_thing_py.manager import *
import uuid


class SoPManagerThing(SoPBigThing, metaclass=ABCMeta):

    MANAGER_THREAD_TIME_OUT = THREAD_TIME_OUT

    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = False, log_name: str = None, log_enable: bool = True, log_mode: SoPPrintMode = SoPPrintMode.ABBR, append_mac_address: bool = True,
                 manager_mode: SoPManagerMode = SoPManagerMode.SPLIT, scan_cycle=5):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel, ip, port,
                         ssl_ca_path, ssl_enable, log_name, log_enable, log_mode, append_mac_address)

        self._scan_cycle = scan_cycle
        self._manager_mode = SoPManagerMode.get(
            manager_mode) if isinstance(manager_mode, str) else manager_mode

        self._staff_thing_list: list[SoPStaffThing] = []
        self._manager_mode_handler = ManagerModeHandler(
            mode=self._manager_mode)

        self._last_scan_time = 0

        # Threading
        self._thread_func_list += [
            self._scan_staff_message_thread_func,
            self._receive_staff_message_thread_func,
            self._publish_staff_message_thread_func
        ]

        # Queue
        self._staff_register_queue = Queue()
        self._staff_alive_queue = Queue()
        self._staff_value_queue = Queue()
        self._staff_receive_queue = Queue()
        self._staff_publish_queue = Queue()

    # override
    def run(self):
        try:
            # Start BigThing's Thread function
            for thread in self._waiting_thread_list:
                thread.start()
                self._running_thread_list.append(thread)

            # Register try
            if self._manager_mode == SoPManagerMode.JOIN:
                retry = 5
                while not self._registered and retry:
                    SOPLOG_DEBUG(f'Register try {6-retry}', 'yellow')
                    retry -= 1

                    self._subscribe_init_topics(self)
                    self._send_TM_REGISTER(
                        thing_name=self._name, payload=self.dump())

                    current_time = get_current_time()
                    while get_current_time() - current_time < 5:
                        if self._registered:
                            break
                        else:
                            time.sleep(0.1)
            elif self._manager_mode == SoPManagerMode.SPLIT:
                pass
            else:
                pass

            # Maintain main thread
            while not self._g_exit.wait(THREAD_TIME_OUT):
                time.sleep(1000)
        except KeyboardInterrupt as e:
            SOPLOG_DEBUG('Ctrl + C Exit', 'red')
            return self.wrapup()
        except ConnectionRefusedError as e:
            SOPLOG_DEBUG(
                'Connection error while connect to broker. Check ip and port', 'red')
            return self.wrapup()
        except Exception as e:
            print_error(e)
            return self.wrapup()

    # override
    def wrapup(self):
        try:
            for staff_thing in self._staff_thing_list:
                self._send_TM_UNREGISTER(staff_thing.get_name())

            cur_time = get_current_time()
            while not (self._publish_queue.empty() or get_current_time() - cur_time > 1):
                time.sleep(THREAD_TIME_OUT)

            self._g_exit.set()
            for thread in self._running_thread_list:
                thread.join()
                SOPLOG_DEBUG(f'{thread._name} is terminated', 'yellow')

            self._mqtt_client.disconnect()
            SOPLOG_DEBUG('Thing Exit', 'red')
            return True
        except Exception as e:
            print_error(e)
            return False

    # ===========================================================================================
    #  _    _                             _    __                      _    _
    # | |  | |                           | |  / _|                    | |  (_)
    # | |_ | |__   _ __   ___   __ _   __| | | |_  _   _  _ __    ___ | |_  _   ___   _ __   ___
    # | __|| '_ \ | '__| / _ \ / _` | / _` | |  _|| | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
    # | |_ | | | || |   |  __/| (_| || (_| | | |  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
    #  \__||_| |_||_|    \___| \__,_| \__,_| |_|   \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
    # ===========================================================================================

    # override
    def _alive_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                if self._manager_mode == SoPManagerMode.JOIN:
                    current_time = get_current_time()
                    if current_time - self._last_alive_time > self._alive_cycle:
                        for staff_thing in self._staff_thing_list:
                            self._send_TM_ALIVE(
                                thing_name=staff_thing.get_name())
                            staff_thing._last_alive_time = current_time
                elif self._manager_mode == SoPManagerMode.SPLIT:
                    # split 모드일 때는 staff thing이 alive 신호를 받아서 보내므로 생략
                    # current_time = get_current_time()
                    # for staff_thing in self._staff_thing_list:
                    #     if current_time - staff_thing._last_alive_time > self._alive_cycle:
                    #         self._send_TM_ALIVE(thing_name=self._name)
                    #         staff_thing._last_alive_time = current_time
                    pass
                else:
                    raise Exception('Invalid Manager Mode')
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    # override
    def _value_publish_thread_func(self, stop_event: Event) -> Union[bool, None]:
        try:
            while not stop_event.wait(THREAD_TIME_OUT):
                for staff_thing in self._staff_thing_list:
                    if not staff_thing._registered:
                        continue
                    current_time = get_current_time()
                    for value in staff_thing._value_list:
                        if not (current_time - value.get_last_update_time()) > value.get_cycle():
                            continue
                        arg_list = tuple(value.get_arg_list())
                        if value.update(*arg_list) is not None:
                            self._send_TM_VALUE_PUBLISH(
                                staff_thing._name, value.get_name(), value.dump_pub())
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    ############################################################################################################################

    def _scan_staff_message_thread_func(self, stop_event: Event):
        try:
            staff_thing_info_list = []

            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                if not (get_current_time() - self._last_scan_time > self._scan_cycle):
                    continue

                staff_thing_info_list = self._scan_staff_thing()
                if staff_thing_info_list == False:
                    raise Exception('Scan staff thing error')

                old_staff_thing_list = [
                    staff_thing for staff_thing in self._staff_thing_list]
                new_staff_thing_list: List[SoPStaffThing] = []
                latest_staff_thing_list: List[SoPStaffThing] = []
                removed_staff_thing_list: List[SoPStaffThing] = []
                for staff_thing_info in staff_thing_info_list:
                    staff_thing = self._create_staff(staff_thing_info)
                    self._connect_staff_thing(staff_thing)

                    staff_thing_level, staff_thing = self._check_staff_thing_duplicate(
                        staff_thing)
                    latest_staff_thing_list.append(staff_thing)
                    if staff_thing_level == SoPNewStaffThingLevel.NEW:
                        SOPLOG_DEBUG(
                            f'New staff_thing!!! name: [{staff_thing.get_name()}]', 'green')
                        new_staff_thing_list.append(staff_thing)
                    elif staff_thing_level == SoPNewStaffThingLevel.DUPLICATE:
                        SOPLOG_DEBUG(
                            f'Staff thing [{staff_thing.get_name()}] was still alive...', 'yellow')

                removed_staff_thing_list = [
                    item for item in old_staff_thing_list if item not in latest_staff_thing_list]
                for staff_thing in new_staff_thing_list:
                    self._staff_thing_list.append(staff_thing)
                    self._subscribe_init_topics(staff_thing)
                    self._send_TM_REGISTER(
                        staff_thing.get_name(), staff_thing.dump())
                for staff_thing in removed_staff_thing_list:
                    try:
                        self._staff_thing_list.remove(staff_thing)
                    except ValueError:
                        raise Exception(
                            f'[scan_staff_message_thread_func][{staff_thing.get_name()}] is not in staff thing list')
                    self._send_TM_UNREGISTER(staff_thing.get_name())

                staff_thing_info_list = None
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _receive_staff_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                staff_msg = self._receive_staff_message()
                if staff_msg is None:
                    continue
                self._handle_staff_message(staff_msg)
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def _publish_staff_message_thread_func(self, stop_event: Event):
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                for staff_thing in self._staff_thing_list:
                    if not staff_thing.is_connected() or not staff_thing.get_registered():
                        continue
                    staff_msg = staff_thing._publish_queue.get(
                        timeout=self.MANAGER_THREAD_TIME_OUT)
                    self._publish_staff_message(staff_msg)
        except Empty as e:
            pass
        except Exception as e:
            stop_event.set()
            print_error(e)
            return False

    def register_thread_func(self, stop_event: Event) -> Tuple[SoPNewStaffThingLevel, SoPStaffThing]:
        # TODO: There is a problem that Thing detect does not work well
        try:
            while not stop_event.wait(self.MANAGER_THREAD_TIME_OUT):
                register_info: SoPStaffThingInfo = self._staff_register_queue.get()
                new_staff_thing: SoPStaffThing = self._create_staff(
                    register_info)
                register_result = StaffRegisterResult(
                    staff_thing_name=new_staff_thing.get_name(), device_id=new_staff_thing.get_device_id(), assigned_device_id=None)

                # staff thing이 새로운 것인지 중복인지 업데이트인지 확인
                staff_thing_level, old_staff_thing = self._check_staff_thing_duplicate(
                    new_staff_thing)
                if staff_thing_level == SoPNewStaffThingLevel.NEW:
                    SOPLOG_DEBUG(
                        f'New staff_thing!!! name = {new_staff_thing.get_name()}', 'green')
                    self._staff_thing_list.append(new_staff_thing)
                    self._subscribe_init_topics(new_staff_thing)
                    register_result.assigned_device_id = new_staff_thing.get_device_id()
                elif staff_thing_level == SoPNewStaffThingLevel.DUPLICATE:
                    SOPLOG_DEBUG(
                        f'hue staff thing {new_staff_thing.get_name()} already in list', 'yellow')
                    continue
                elif staff_thing_level == SoPNewStaffThingLevel.UPDATE:
                    # SOPLOG_DEBUG(
                    #     f'staff_thing {new_staff_thing.get_name()} info was updated!!!', 'green')
                    # self._staff_thing_list.remove(old_staff_thing)
                    # self._staff_thing_list.append(new_staff_thing)
                    SOPLOG_DEBUG(
                        f'hue staff thing {new_staff_thing.get_name()} already in list', 'yellow')
                    continue

                # mode에 따라 동작 구분
                register_info = self._manager_mode_handler.dump_register_packet(
                    new_staff_thing)

                if register_info:
                    self._send_TM_REGISTER(register_info[0], register_info[1])

                self._staff_publish_queue.put(register_result)

        except Exception as e:
            # 'str' object has no attribute 'value'
            stop_event.set()
            print_error(e)
            return False

    # ====================================================================================================================
    #  _                        _  _        ___  ___ _____  _____  _____
    # | |                      | || |       |  \/  ||  _  ||_   _||_   _|
    # | |__    __ _  _ __    __| || |  ___  | .  . || | | |  | |    | |    _ __ ___    ___  ___  ___   __ _   __ _   ___
    # | '_ \  / _` || '_ \  / _` || | / _ \ | |\/| || | | |  | |    | |   | '_ ` _ \  / _ \/ __|/ __| / _` | / _` | / _ \
    # | | | || (_| || | | || (_| || ||  __/ | |  | |\ \/' /  | |    | |   | | | | | ||  __/\__ \\__ \| (_| || (_| ||  __/
    # |_| |_| \__,_||_| |_| \__,_||_| \___| \_|  |_/ \_/\_\  \_/    \_/   |_| |_| |_| \___||___/|___/ \__,_| \__, | \___|
    #                                                                                                         __/ |
    #                                                                                                        |___/
    # ====================================================================================================================

    # override
    def _handle_MT_RESULT_REGISTER(self, msg: mqtt.MQTTMessage):
        register_result_msg = SoPRegisterResultMessage(msg)
        target_staff_thing = self._find_staff_thing_by_name(
            register_result_msg._thing_name)

        if target_staff_thing is False:
            SOPLOG_DEBUG(
                f'Wrong payload arrive... {self._name} should be arrive, not {register_result_msg._thing_name}', 'red')
            raise

        if self._manager_mode == SoPManagerMode.JOIN:
            ret = self._check_register_result(
                register_result_msg._error, thing=target_staff_thing)
            if ret:
                self._middleware_name = register_result_msg._middleware_name
                self._registered = True
                self._subscribe_service_topics(self)
                self._send_RESULT_REGISTER_staff_message(
                    target_staff_thing, register_result_msg.payload())
            else:
                SOPLOG_DEBUG(
                    f'[handle_MT_RESULT_REGISTER] Register failed... error code : {register_result_msg._error}')
        elif self._manager_mode == SoPManagerMode.SPLIT:
            ret = self._check_register_result(
                register_result_msg._error, thing=target_staff_thing)
            if ret:
                target_staff_thing.set_middleware_name(
                    register_result_msg._middleware_name)
                target_staff_thing.set_registered(True)
                self._subscribe_service_topics(target_staff_thing)
                self._send_RESULT_REGISTER_staff_message(
                    target_staff_thing, register_result_msg.payload())
            else:
                SOPLOG_DEBUG(
                    f'[handle_MT_RESULT_REGISTER] Register failed... error code : {register_result_msg._error}')

    # override
    def _handle_MT_RESULT_UNREGISTER(self, msg: mqtt.MQTTMessage):
        unregister_result_msg = SoPUnregisterResultMessage(msg)
        target_staff_thing = self._find_staff_thing_by_name(
            unregister_result_msg._thing_name)

        if target_staff_thing is False:
            SOPLOG_DEBUG(
                f'Wrong payload arrive... {self._name} should be arrive, not {unregister_result_msg._thing_name}', 'red')
            raise

        if self._manager_mode == SoPManagerMode.JOIN:
            if self._check_register_result(unregister_result_msg._error):
                self._registered = False
                self._unsubscrube_all_topics(self)
                self._send_RESULT_UNREGISTER_staff_message(
                    target_staff_thing, unregister_result_msg.payload())
            else:
                SOPLOG_DEBUG(
                    f'[handle_MT_RESULT_UNREGISTER] Unregister failed... error code : {unregister_result_msg._error}')
        elif self._manager_mode == SoPManagerMode.SPLIT:
            # manager thing의 토픽중 해당 staff thing에 관련된 것만 unsubscribe한다
            if self._check_register_result(unregister_result_msg._error):
                target_staff_thing._registered = False
                self._unsubscrube_all_topics(target_staff_thing)
                for topic in self._subscribed_topic_set:
                    if target_staff_thing.get_name() in topic:
                        self._unsubscribe(topic, thing=target_staff_thing)
                self._send_RESULT_UNREGISTER_staff_message(
                    target_staff_thing, unregister_result_msg.payload())
            else:
                SOPLOG_DEBUG(
                    f'[handle_MT_RESULT_UNREGISTER] Unregister failed... error code : {unregister_result_msg._error}')

    # override
    def _handle_MT_EXECUTE(self, msg: mqtt.MQTTMessage):
        execute_msg = SoPExecuteMessage(msg)
        execute_request = SoPExecuteRequest(
            trigger_msg=execute_msg)
        execute_request.timer_start()

        target_staff_thing = self._find_staff_thing_by_name(
            execute_msg._thing_name)
        target_function = target_staff_thing._find_function(
            execute_msg._function_name)

        if target_function:
            target_function.execute(execute_request)
        else:
            SOPLOG_DEBUG('function not exist', 'red')
            return False

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    @abstractmethod
    def _scan_staff_thing(self, timeout: float) -> List[SoPStaffThing]:
        pass

    @abstractmethod
    def _receive_staff_message(self) -> str:
        pass

    @abstractmethod
    def _publish_staff_message(self, staff_msg) -> None:
        pass

    @abstractmethod
    def _parse_staff_message(self, staff_msg) -> Tuple[SoPProtocolType, str, str]:
        pass

    @abstractmethod
    def _create_staff(self, staff_thing_info) -> SoPStaffThing:
        pass

    @abstractmethod
    def _connect_staff_thing(self, staff_thing: SoPStaffThing) -> bool:
        pass

    @abstractmethod
    def _disconnect_staff_thing(self, staff_thing: SoPStaffThing) -> bool:
        pass

    @abstractmethod
    def _handle_REGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> Tuple[str, dict]:
        pass

    @abstractmethod
    def _handle_UNREGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> str:
        pass

    @abstractmethod
    def _handle_ALIVE_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> str:
        pass

    @abstractmethod
    def _handle_VALUE_PUBLISH_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> Tuple[str, str, dict]:
        pass

    @abstractmethod
    def _handle_RESULT_EXECUTE_staff_message(self, staff_thing: SoPStaffThing, payload: str) -> str:
        pass

    @abstractmethod
    def _send_RESULT_REGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: dict) -> str:
        pass

    @abstractmethod
    def _send_RESULT_UNREGISTER_staff_message(self, staff_thing: SoPStaffThing, payload: dict) -> str:
        pass

    @abstractmethod
    def _send_EXECUTE_staff_message(self, staff_thing: SoPStaffThing, payload: dict) -> str:
        pass

    ############################################################################################################################

    def _handle_staff_message(self, staff_msg):
        staff_protocol, staff_device_id, staff_payload = self._parse_staff_message(
            staff_msg)
        target_staff_thing = self._find_staff_thing_by_name(staff_device_id)

        if staff_protocol == SoPProtocolType.Base.TM_REGISTER:
            thing_name, payload = self._handle_REGISTER_staff_message(
                target_staff_thing, staff_payload)
            self._send_TM_REGISTER(thing_name, payload)
            target_staff_thing.set_registered(True)
            target_staff_thing._device_id = self._generate_device_id()
        elif staff_protocol == SoPProtocolType.Base.TM_UNREGISTER:
            thing_name = self._handle_UNREGISTER_staff_message(
                target_staff_thing, staff_payload)
            self._send_TM_UNREGISTER(thing_name)
        elif staff_protocol == SoPProtocolType.Base.TM_ALIVE:
            thing_name = self._handle_ALIVE_staff_message(
                target_staff_thing, staff_payload)
            self._send_TM_ALIVE(thing_name)
        elif staff_protocol == SoPProtocolType.Base.TM_VALUE_PUBLISH:
            thing_name, value_name, payload = self._handle_VALUE_PUBLISH_staff_message(
                target_staff_thing, staff_payload)
            self._send_TM_VALUE_PUBLISH(thing_name, value_name, payload)
        elif staff_protocol == SoPProtocolType.Base.TM_RESULT_EXECUTE:
            # TODO: complete this
            # TM/RESULT/EXECUTE/[FunctionName]/[ThingName]/([MiddlewareName]/[Request_ID])
            # Request_ID = requester_middleware@super_thing@super_function@subrequest_order
            function_name, thing_name, middleware_name, request_ID = self._handle_RESULT_EXECUTE_staff_message(
                target_staff_thing, staff_payload)
            self._send_TM_RESULT_EXECUTE(function_name, thing_name,)

    def _generate_device_id(self) -> str:
        return str(uuid.uuid4())

    def _find_staff_thing_by_name(self, staff_name: str) -> SoPStaffThing:
        for staff_thing in self._staff_thing_list:
            if staff_thing.get_name() == staff_name:
                return staff_thing
        return False

    def _find_staff_thing_by_device_id(self, device_id: str) -> SoPStaffThing:
        for staff_thing in self._staff_thing_list:
            if staff_thing._device_id == device_id:
                return staff_thing
        return False

    def _append_staff_thing_value(self, new_staff_thing: SoPStaffThing):
        self._staff_thing_list.append(new_staff_thing)
        for value in new_staff_thing.get_value_list():
            if not value in self._value_list:
                staff_value_name = f'{new_staff_thing.get_name()}/{value.get_name()}'
                value.set_name(staff_value_name)
                self._value_list.append(value)

    def _check_staff_thing_duplicate(self, new_staff_thing: SoPStaffThing) -> Tuple[SoPNewStaffThingLevel, SoPStaffThing]:
        for staff_thing in self._staff_thing_list:
            if new_staff_thing == staff_thing:
                return SoPNewStaffThingLevel.DUPLICATE, staff_thing
        else:
            return SoPNewStaffThingLevel.NEW, new_staff_thing

    def _print_packet(self, msg: mqtt.MQTTMessage, mode: SoPPrintMode = SoPPrintMode.FULL):

        def mode_select(mode: SoPPrintMode, payload: str):
            if mode == SoPPrintMode.SKIP:
                return colored(f'skip... (print_packet mode={mode})', 'yellow'), payload
            elif mode == SoPPrintMode.ABBR:
                payload_raw = payload
                if payload.count('\n') > 10:
                    payload = '\n'.join(payload.split('\n')[:10]) + '\n' + \
                        colored(
                            f'skip... (print_packet mode={mode})', 'yellow')
                    return payload, payload_raw
                elif len(payload) > 1000:
                    payload = payload[:1000] + '\n' + \
                        colored(
                            f'skip... (print_packet mode={mode})', 'yellow')
                    return payload, payload_raw
                else:
                    return payload, payload_raw
            elif mode == SoPPrintMode.FULL:
                return payload, payload
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unknown mode!!! mode should be [skip|abbr|full] mode : {mode}', 'red')

        def print_result_topic(topic, payload):
            topic_str = topic_join(topic)
            topic_indicator = f'{topic[0]}_{topic[1]}_{topic[2]}'

            payload, payload_raw = mode_select(mode, payload)
            payload = colored(payload, attrs=['bold'])

            SOPLOG_DEBUG(
                f'[{topic_indicator:20}] topic : {topic_str} payload : {payload}')

            return True

        def print_topic(topic, payload):
            topic_str = topic_join(topic)
            topic_indicator = f'{topic[0]}_{topic[1]}'

            payload, payload_raw = mode_select(mode, payload)
            payload = colored(payload, attrs=['bold'])

            SOPLOG_DEBUG(
                f'[{topic_indicator:20}] topic : {topic_str} payload : {payload}')

            return True

        topic, payload, timestamp = decode_MQTT_message(msg, str)
        topic = topic_split(topic)
        # target_staff_thing = self._find_staff_thing_by_name()

        payload = dict_to_json_string(payload)

        if topic[0] == 'MT':
            if topic[1] == 'RESULT':
                if topic[2] in ['REGISTER', 'UNREGISTER', 'BINARY_VALUE']:
                    print_result_topic(topic, payload)
                else:
                    pass
            else:
                if topic[1] in ['EXECUTE']:
                    return print_topic(topic, payload)
                else:
                    pass
        elif topic[0] == 'TM':
            if topic[1] == 'RESULT':
                if topic[2] in ['EXECUTE']:
                    print_result_topic(topic, payload)
                else:
                    pass
            else:
                if topic[1] in ['REGISTER', 'UNREGISTER', 'ALIVE', 'VALUE_PUBLISH']:
                    return print_topic(topic, payload)
                else:
                    pass
        elif topic[0] == 'MS':
            if topic[1] == 'RESULT':
                if topic[2] in ['SCHEDULE', 'EXECUTE', 'SERVICE_LIST']:
                    print_result_topic(topic, payload)
                else:
                    pass
            else:
                if topic[1] in ['SCHEDULE', 'EXECUTE']:
                    return print_topic(topic, payload)
                else:
                    pass
        elif topic[0] == 'SM':
            if topic[1] == 'RESULT':
                if topic[2] in ['SCHEDULE', 'EXECUTE']:
                    print_result_topic(topic, payload)
                else:
                    pass
            else:
                if topic[1] in ['SCHEDULE', 'EXECUTE', 'AVAILABILITY', 'REFRESH']:
                    return print_topic(topic, payload)
                else:
                    pass
        elif topic[0] == 'ME':
            if topic[1] == 'NOTIFY_CHANGE':
                return print_topic(topic, payload)
            else:
                pass
        else:
            target_staff_thing = self._find_staff_thing_by_name(topic[0])
            if target_staff_thing:
                if topic[1] in [value.get_name() for value in target_staff_thing._value_list]:
                    return print_topic(topic, payload)
                else:
                    SOPLOG_DEBUG(
                        f'[print_packet] Unexpected value VALUE_PUBLISH topic!!! value: {topic[1]} ', 'red')
                    return False
            else:
                SOPLOG_DEBUG(
                    f'[print_packet] Unexpected VALUE_PUBLISH topic!!! : {topic_join(topic)} ', 'red')
                return False

        SOPLOG_DEBUG(
            f'[print_packet] Unexpected topic!!! : {topic_join(topic)} ', 'red')
        return False
