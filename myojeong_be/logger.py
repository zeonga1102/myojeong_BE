import logging
import json


class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, request):
        log_message = f'{request.path} ({request.method})'
        if request.method == 'GET':
            query_params = request.GET.dict()
            log_message += f'\n[Query parameter]\n{json.dumps(query_params, indent=1, ensure_ascii=False)}'
        elif request.method == 'POST':
            request_body = request.data.copy()
            log_message += f'\n[Request Body]\n{json.dumps(request_body, indent=1, ensure_ascii=False)}'
            
        self.logger.info(log_message)

    def error(self, errors):
        self.logger.error(f'\n[Errors]\n{json.dumps(errors, indent=1, ensure_ascii=False)}')