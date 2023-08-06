import os, datetime, logging
from inspect import getframeinfo, stack
from typing import List, Optional
import requests, json
from ddd_objects.infrastructure.ao import exception_class_dec
from ddd_objects.domain.exception import return_codes
from .do import LogItemDO, LogRecordDO


class LocalLogger:
    def __init__(self, name:Optional[str]=None, log_dir='/tmp/log') -> None:
        if name is None:
            name = 'root'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        info_file_handler = logging.FileHandler(
            os.path.join(os.path.join(log_dir, f'{name}_info.log'))
        ) 
        debug_file_handler = logging.FileHandler(
            os.path.join(os.path.join(log_dir, f'{name}_debug.log'))
        )
        print_handler = logging.StreamHandler()
        info_file_handler.setLevel(logging.INFO)
        debug_file_handler.setLevel(logging.DEBUG)
        print_handler.setLevel(logging.WARNING)
        print_handler.set_name('print')
        info_file_handler.set_name('info_file')
        debug_file_handler.set_name('debug_file')
        handler_names = [h.name for h in self.logger.handlers]
        
        if 'info_file' not in handler_names:
            self.logger.addHandler(info_file_handler)
        if 'debug_file' not in handler_names:
            self.logger.addHandler(debug_file_handler)
        if 'print' not in handler_names:
            self.logger.addHandler(print_handler)
        

    def _get_header(self, msg_type:str):
        date = datetime.datetime.utcnow().isoformat()
        caller = getframeinfo(stack()[2][0])
        line_num = caller.lineno
        fn = caller.filename
        fn = os.path.basename(fn)
        format_str = f'[{msg_type.upper()}]{date}-{fn}-{line_num}'
        return f'{format_str:<70}'

    def debug(self, msg, *kargs, **kwargs):
        header = self._get_header('debug')
        msg = header+msg
        self.logger.debug(msg, *kargs, **kwargs)

    def info(self, msg, *kargs, **kwargs):
        header = self._get_header('info')
        msg = header+msg
        self.logger.info(msg, *kargs, **kwargs)

    def warning(self, msg, *kargs, **kwargs):
        header = self._get_header('warning')
        msg = header+msg
        self.logger.warning(msg, *kargs, **kwargs)

    def error(self, msg, *kargs, **kwargs):
        header = self._get_header('error')
        msg = header+msg
        self.logger.error(msg, *kargs, **kwargs)

    def critical(self, msg, *kargs, **kwargs):
        header = self._get_header('critical')
        msg = header+msg
        self.logger.critical(msg, *kargs, **kwargs)

class LogController:
    def __init__(self, ip: str=None, port: int=None) -> None:
        if port is None:
            port = 8080
        if ip is None:
            ip = 'log-control-svc.system-service.svc.cluster.local'
        self.url = f"http://{ip}:{port}"
        self.logger = LocalLogger()

    def _check_error(self, status_code, info):
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_info = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_info = info['detail']['error_info']
            self.logger.error(f'Error detected by log-control-ao:\nreturn code: {return_code}\n'
                f'error info: {error_info}')

    @exception_class_dec(max_try=1)
    def add_record(self, record: LogRecordDO, timeout=3):
        data = json.dumps(record.dict())
        response=requests.post(f'{self.url}/record', data=data, timeout=timeout)
        succeed = json.loads(response.text)
        print(succeed)
        self._check_error(response.status_code, succeed)
        return succeed

    @exception_class_dec(max_try=1)
    def find_unprocessed_items(self, timeout=3):
        response=requests.get(f'{self.url}/unprocessed_items', timeout=timeout)
        items = json.loads(response.text)
        self._check_error(response.status_code, items)
        if items is None:
            return None
        else:
            return [LogItemDO(**m) for m in items]

    @exception_class_dec(max_try=1)
    def update_items_processed(self, items:List[LogItemDO], timeout=3):
        data = json.dumps([m.dict() for m in items])
        response=requests.post(f'{self.url}/items/processed', data=data, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

class Logger:
    def __init__(
        self, 
        domain, 
        location=None, 
        labels=None,
        keywords=[],
        controller_ip=None, 
        controller_port=None, 
        local:bool=False,
        combine_keywords=False,
    ) -> None:
        self.domain = domain
        self.location = location
        if labels is None:
            labels = ['default']
        self.labels = labels
        self.local = local
        self.keywords = keywords
        self.controller = LogController(controller_ip, controller_port)
        self.combine_keywords = combine_keywords
        self.logger = LocalLogger(domain)

    def _send_record(
        self, 
        content, 
        record_type, 
        domain=None, 
        location=None, 
        labels=None, 
        keywords=None,
        combine_keywords=None,
    ):
        if domain is None:
            domain = self.domain
        if location is None:
            location = self.location
        if labels is None:
            labels = self.labels
        if keywords is None:
            keywords = self.keywords
        if combine_keywords is None:
            combine_keywords = self.combine_keywords
        caller = getframeinfo(stack()[2][0])
        line_num = caller.lineno
        fn = caller.filename
        if location is None and self.location is None:
            location = fn
        record = LogRecordDO(
            log_type = record_type,
            log_domain = domain,
            log_location = location,
            log_line = line_num,
            log_inhalt = content,
            log_label = labels,
            log_keywords = keywords,
            creation_time = datetime.datetime.utcnow().isoformat(),
            combine_keywords=combine_keywords
        )
        result = self.controller.add_record(record)
        if result.succeed:
            return result.get_value()
        else:
            return False

    def info(
        self, 
        content, 
        domain=None, 
        location=None, 
        labels=None, 
        keywords=None,
        combine_keywords=None,
    ):
        if self.local:
            self.logger.info(content)
        return self._send_record(content, 'info', domain, location, labels, keywords, combine_keywords)

    def error(
        self, 
        content, 
        domain=None, 
        location=None, 
        labels=None, 
        keywords=None,
        combine_keywords=None,
    ):
        if self.local:
            self.logger.error(content)
        return self._send_record(content, 'error', domain, location, labels, keywords, combine_keywords)

