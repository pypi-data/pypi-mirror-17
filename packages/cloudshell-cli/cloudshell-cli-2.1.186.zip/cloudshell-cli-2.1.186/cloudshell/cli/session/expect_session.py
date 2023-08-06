import socket
import time
from collections import OrderedDict

from abc import ABCMeta
from cloudshell.cli.session.session_exceptions import SessionLoopDetectorException, SessionLoopLimitException
import re
from cloudshell.cli.session.session import Session
from cloudshell.cli.helper.normalize_buffer import normalize_buffer
from cloudshell.cli.service.cli_exceptions import CommandExecutionException
import inject
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER
from cloudshell.shell.core.config_utils import override_attributes_from_config


class ExpectSession(Session):
    """
    Help to handle additional actions during send command
    """

    __metaclass__ = ABCMeta

    DEFAULT_ACTIONS = None
    HE_MAX_LOOP_RETRIES = 20
    HE_READ_TIMEOUT = 30
    HE_EMPTY_LOOP_TIMEOUT = 0.2
    HE_CLEAR_BUFFER_TIMEOUT = 0.1
    HE_LOOP_DETECTOR_MAX_ACTION_LOOPS = 3
    HE_LOOP_DETECTOR_MAX_COMBINATION_LENGTH = 4

    def __init__(self, handler=None, username=None, password=None, host=None, port=None,
                 timeout=None, new_line='\r', **kwargs):
        """

        :param handler:
        :param username:
        :param password:
        :param host:
        :param port:
        :param timeout:
        :param new_line:
        :param kwargs:
        :return:
        """
        self.session_type = 'EXPECT'
        self._handler = handler
        self._port = None
        if port and int(port) > 0:
            self._port = int(port)
        if host:
            temp_host = host.split(':')
            self._host = temp_host[0]
            if not self._port and len(temp_host) > 1:
                self._port = int(temp_host[1])
        else:
            self._host = host

        self._username = username
        self._password = password

        self._new_line = new_line
        self._timeout = timeout

        """Override constants with global config values"""
        overridden_config = override_attributes_from_config(ExpectSession)

        self._max_loop_retries = overridden_config.HE_MAX_LOOP_RETRIES
        self._empty_loop_timeout = overridden_config.HE_EMPTY_LOOP_TIMEOUT
        self._default_actions_func = overridden_config.DEFAULT_ACTIONS
        self._loop_detector_max_action_loops = overridden_config.HE_LOOP_DETECTOR_MAX_ACTION_LOOPS
        self._loop_detector_max_combination_length = overridden_config.HE_LOOP_DETECTOR_MAX_COMBINATION_LENGTH
        self._clear_buffer_timeout = overridden_config.HE_CLEAR_BUFFER_TIMEOUT
        if not self._timeout:
            self._timeout = overridden_config.HE_READ_TIMEOUT

    @property
    def logger(self):
        return inject.instance(LOGGER)

    def _receive_with_retries(self, timeout, retries_count):
        """Read session buffer with several retries

        :param timeout:
        :param retries_count:
        :return:
        """

        current_retries = 0
        current_output = None

        while current_retries < retries_count:
            current_retries += 1

            try:
                current_output = self._receive(timeout)
                if current_output == '':
                    time.sleep(0.5)
                    continue
            except socket.timeout:
                time.sleep(0.5)
                continue
            except timeout:
                break
            except Exception as err:
                raise err
            break

        if current_output is None:
            raise Exception('ExpectSession', 'Failed to get response from device')
        return current_output

    def _clear_buffer(self, timeout):
        """
        Clear buffer

        :param timeout:
        :return:
        """
        out = ''
        while True:
            try:
                read_buffer = self._receive(timeout)
            except socket.timeout:
                read_buffer = None
            if read_buffer:
                out += read_buffer
            else:
                break
        return out

    def send_line(self, data_str):
        """
        Add new line to the end of command string and send

        :param data_str:
        :return:
        """
        self._send(data_str + self._new_line)

    def hardware_expect(self, data_str=None, re_string='', expect_map=OrderedDict(), error_map=OrderedDict(),
                        timeout=None, retries=None, check_action_loop_detector=True, empty_loop_timeout=None,
                        **optional_args):

        """Get response form the device and compare it to expected_map, error_map and re_string patterns,
        perform actions specified in expected_map if any, and return output.
        Raise Exception if receive empty responce from device within a minute

        :param data_str: command to send
        :param re_string: expected string
        :param expect_map: dict with {re_str: action} to trigger some action on received string
        :param error_map: expected error list
        :param timeout: session timeout
        :param retries: maximal retries count
        :return:
        """

        retries = retries or self._max_loop_retries
        empty_loop_timeout = empty_loop_timeout or self._empty_loop_timeout

        if data_str is not None:
            self._clear_buffer(self._clear_buffer_timeout)

            self.logger.debug('Command: {}'.format(data_str))
            self.send_line(data_str)

        if re_string is None or len(re_string) == 0:
            raise Exception('ExpectSession', 'List of expected messages can\'t be empty!')

        # Loop until one of the expressions is matched or MAX_RETRIES
        # nothing is expected (usually used for exit)
        output_list = list()
        output_str = ''
        retries_count = 0
        is_correct_exit = False
        action_loop_detector = ActionLoopDetector(self._loop_detector_max_action_loops,
                                                  self._loop_detector_max_combination_length)

        while retries == 0 or retries_count < retries:

            try:
                read_buffer = self._receive(timeout)
            except socket.timeout:
                read_buffer = None

            if read_buffer:
                output_str += read_buffer
                retries_count = 0
            else:
                retries_count += 1
                time.sleep(empty_loop_timeout)
                continue

            if re.search(re_string, output_str, re.DOTALL):
                output_list.append(output_str)
                is_correct_exit = True

            for expect_string in expect_map:
                result_match = re.search(expect_string, output_str, re.DOTALL)
                if result_match:
                    output_list.append(output_str)

                    if check_action_loop_detector:
                        if action_loop_detector.loops_detected(expect_string):
                            self.logger.error('Loops detected, output_list: {}'.format(output_list))
                            raise SessionLoopDetectorException(self.__class__.__name__,
                                                               'Expected actions loops detected')
                    expect_map[expect_string](self)
                    output_str = ''
                    break

            if is_correct_exit:
                break

        if not is_correct_exit:
            raise SessionLoopLimitException(self.__class__.__name__,
                                            'Session Loop limit exceeded, {} loops'.format(retries_count))

        result_output = ''.join(output_list)

        for error_string in error_map:
            result_match = re.search(error_string, result_output, re.DOTALL)
            if result_match:
                self.logger.error(result_output)
                raise CommandExecutionException('ExpectSession',
                                                'Session returned \'{}\''.format(error_map[error_string]))

        # Read buffer to the end. Useful when re_string isn't last in buffer
        result_output += self._clear_buffer(self._clear_buffer_timeout)

        result_output = normalize_buffer(result_output)
        self.logger.debug(result_output)
        return result_output

    def reconnect(self, prompt):
        """
        Recconnect implementation

        :param prompt:
        :return:
        """
        self.disconnect()
        self.connect(prompt)

    def _default_actions(self):
        """
        Call default action
        :return:
        """
        if self._default_actions_func:
            self._default_actions_func(session=self)


class ActionLoopDetector(object):
    """Help to detect loops for action combinations"""

    def __init__(self, max_loops, max_combination_length):
        """

        :param max_loops:
        :param max_combination_length:
        :return:
        """
        self._max_action_loops = max_loops
        self._max_combination_length = max_combination_length
        self._action_history = []

    def loops_detected(self, action_key):
        """
        Add action key to the history and detect loops

        :param action_key:
        :return:
        """
        # """Added action key to the history and detect for loops"""
        loops_detected = False
        self._action_history.append(action_key)
        for combination_length in xrange(1, self._max_combination_length + 1):
            if self._is_combination_compatible(combination_length):
                if self._detect_loops_for_combination_length(combination_length):
                    loops_detected = True
                    break
        return loops_detected

    def _is_combination_compatible(self, combination_length):
        """
        Check if combinations may exist

        :param combination_length:
        :return:
        """
        if len(self._action_history) / combination_length >= self._max_action_loops:
            is_compatible = True
        else:
            is_compatible = False
        return is_compatible

    def _detect_loops_for_combination_length(self, combination_length):
        """
        Detect loops for combination length

        :param combination_length:
        :return:
        """
        reversed_history = self._action_history[::-1]
        combinations = [reversed_history[x:x + combination_length] for x in
                        xrange(0, len(reversed_history), combination_length)][:self._max_action_loops]
        is_loops_exist = True
        for x, y in [combinations[x:x + 2] for x in xrange(0, len(combinations) - 1)]:
            if x != y:
                is_loops_exist = False
                break
        return is_loops_exist
