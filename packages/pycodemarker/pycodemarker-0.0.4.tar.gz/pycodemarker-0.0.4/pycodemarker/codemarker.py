import time
import datetime
import uuid
import inspect

import urllib.parse

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import (ConnectTimeout, ReadTimeout, SSLError, ProxyError)

from pycodemarker.publisher import Publisher
publisher = Publisher()

def droid_peek(func):

    def get_calling_stack_str(inspect_stack):
        calling_stack = list((x[1], x[2], x[3]) for x in inspect_stack)
        calling_stack = list(filter(lambda x: 'site-packages' not in x[0], calling_stack))
        return "{}:{}#{}".format(calling_stack[0][0].split("/")[-1:][0], calling_stack[0][2], str(calling_stack[0][1]))

    def get_caller_function_name():
        inspect_stack = inspect.stack()
        caller_function = get_calling_stack_str(inspect_stack)
        return caller_function

    def add_to_parsed(key, value, result, arg_type=None):

        if type(value) not in [str, int, float, bool, list, tuple]:
            return

        if not arg_type:
            key_name = "args.{}"
        elif arg_type == 'args':
            key_name = "args._args.{}"
        elif arg_type == 'kwargs':
            key_name = "args._kwargs.{}"

        if type(value) in [list, tuple]:
            key_name += "._size"
            value = len(value)

        result[key_name.format(key)] = value


    def parse_func_args(func, result, *args, **kwargs):
        parsed = []
        try:
            arguments = inspect.getfullargspec(func)

            all_args = arguments.args
            varargs_present = arguments.varargs
            varkw_present = arguments.varkw

            passed_args_len = len(args)
            all_args_len = len(all_args)
            arg_defaults = arguments.defaults
            kw_args_passed = kwargs.keys()

            kw_args_passed_len = len(kw_args_passed)

            args_default_values_dict = {}
            arg_defaults_len = 0

            if arg_defaults:
                arg_defaults_len = len(arg_defaults)
                for idx, x in enumerate(all_args):
                    if idx >= all_args_len - arg_defaults_len:
                        args_default_values_dict[all_args[idx]] = arg_defaults[idx - (all_args_len - arg_defaults_len)]

            simple_args_len = all_args_len - arg_defaults_len

            kw_args_passed_count = passed_args_len - simple_args_len
                
            for idx, x in enumerate(all_args):
                arg_name = all_args[idx]
                if passed_args_len > idx:
                    add_to_parsed(arg_name, args[idx], result)
                else:
                    if arg_name in kw_args_passed:
                        add_to_parsed(arg_name, kwargs[arg_name], result)
                    else:    
                        add_to_parsed(arg_name, args_default_values_dict[arg_name], result)

            if passed_args_len > all_args_len:
                for idx in range(all_args_len, passed_args_len):
                    add_to_parsed(idx - all_args_len, args[idx], result, 'args')

            for kwarg in kwargs.keys():
                if kwarg not in args_default_values_dict:
                    add_to_parsed(kwarg, kwargs[kwarg], result, 'kwargs')

        except:
            pass


    def parse_return_data(return_data, result):
        parsed = []
        try:
            if type(return_data) in [str, int, float, bool]:
                parsed.append(('return_value', return_data))
            if type(return_data) in [list, tuple]:
                parsed.append(('return_data._size', len(return_data)))

            # Adding parsed response data into instrumented
            for p in parsed:
                result[p[0]] = p[1]
        except:
            pass
     

    def intercept(*args, **kwargs):

        result = {}
        uid = uuid.uuid4().hex
        result['uid'] = uuid.uuid4().hex
        result['event_time'] = round(datetime.datetime.now().timestamp())*1000
        result['log_type'] = 'function_call'

        parse_func_args(func, result, *args, **kwargs)
         
        begin = time.time()

        # Call actual function
        f_value = func(*args, **kwargs)

        end = time.time()
        result['function_time'] = round((end - begin)*1000)
        result['function_name'] = func.__name__
        result['calling_source'] = get_caller_function_name()
        parse_return_data(f_value, result)

        publisher.send(result)
        return f_value
 
    return intercept


class DroidInstrumentor():

	def __init__(self):
		print('Initialised Droid Instrumentor')

	def get_calling_stack_str(self, inspect_stack):
		calling_stack = list((x[1], x[2], x[3]) for x in inspect_stack)
		calling_stack = list(filter(lambda x: 'site-packages' not in x[0], calling_stack))
		return "{}:{}#{}".format(calling_stack[0][0].split("/")[-1:][0], calling_stack[0][2], str(calling_stack[0][1]))


	def get_caller_function_name(self):
		inspect_stack = inspect.stack()
		caller_function = self.get_calling_stack_str(inspect_stack)
		return caller_function

	def requests_retry_session(self):
		import requests
		session = requests.Session()
		adapter = HTTPAdapter()
		session.mount('http://', adapter)
		session.mount('https://', adapter)
		return session

	def parse_response_data(self, content_type, response, result):
		parsed = []
		try:
			if content_type in ['application/json']:
				response_data = response.json()
				if type(response_data) == dict:
					for key in response_data.keys():
						if type(response_data[key]) in [str, int, float, bool]:
							parsed.append(('data.{}'.format(key), response_data[key]))
						if type(response_data[key]) in [list]:
							parsed.append(('data.{}._size'.format(key), len(response_data[key])))
				if type(response_data) == list:
					parsed.append(('data._size', len(response_data)))

			# Adding parsed response data into instrumented
			for p in parsed:
				result[p[0]] = p[1]
		except:
			pass


	def parse_endpoint(self, endpoint, result):
		result['endpoint'] = endpoint
		result['hostname'] = urllib.parse.urlsplit(endpoint).hostname

		query_params = urllib.parse.urlsplit(endpoint).query

		if query_params:
			query_params = query_params.split("&")
			for q in query_params:
				query = q.split("=")
				result["query.{}".format(query[0])] = query[1]


	def wrapped_get_request(self, url, params=None, **kwargs):
		result = {}
		uid = uuid.uuid4().hex
		result['uid'] = uuid.uuid4().hex
		self.parse_endpoint(url, result)
		result['method'] = 'GET'
		result['calling_source'] = self.get_caller_function_name()
		try:
			result['event_time'] = round(datetime.datetime.now().timestamp())*1000
			start = time.time()
			api_response = self.requests_retry_session().get(url, params=params, **kwargs)
			stop = time.time()     # seconds
			api_response_time = round((stop - start)*1000)
			result['response_time'] = api_response_time
			result['status_code'] = api_response.status_code
			content_type = api_response.headers['Content-Type'].split(";")[0]
			result['content_type'] = content_type
			result['log_type'] = 'api_request_response'
			self.parse_response_data(content_type, api_response, result)
			return api_response
		except Exception as x:
			print('Exception {} in GET call {} '.format(str(x), result))
		finally:
			publisher.send(result)


	def instrument_request(self, r):
		# print('Inside instrument_request')
		r.get = self.wrapped_get_request


	def log_event(self, ev):
		if ev.get('type') and ev.get('name') and ev.get('source'):
			result = {}
			uid = uuid.uuid4().hex
			result['uid'] = uuid.uuid4().hex
			result['log_type'] = 'event'

			result['event_type'] = ev.get('type')
			result['event_name'] = ev.get('name')

			result['event_time'] = round(datetime.datetime.now().timestamp())*1000

			result['calling_source'] = ev.get('source')

			result['event_data'] = ev.get('data', {})
			publisher.send(result)











