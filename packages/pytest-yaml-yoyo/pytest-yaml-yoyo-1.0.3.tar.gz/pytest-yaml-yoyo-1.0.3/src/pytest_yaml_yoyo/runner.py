from . import create_funtion
import types
from inspect import Parameter
from . import validate
from . import extract
from . import my_builtins
from . import render_template_obj
from . import exceptions
import copy


class RunYaml(object):
    """ 运行yaml """

    def __init__(self, raw: dict, module: types.ModuleType):
        self.raw = raw   # 读取yaml 原始数据
        self.module = module   # 动态创建的 module 模型
        self.module_variable = {}  # 模块变量
        self.context = {}

    def run(self):
        # config 获取用例名称 name 和 base_url
        case_name = self.raw.get('config').get('name', '')
        base_url = self.raw.get('config').get('base_url', None)
        config_variables = self.raw.get('config').get('variables', {})
        config_fixtures = self.raw.get('config').get('fixtures', [])
        config_params = self.raw.get('config').get('parameters', [])
        # 模块变量渲染
        self.context.update(__builtins__)  # noqa 内置函数加载
        self.context.update(my_builtins.__dict__)  # 自定义函数对象
        self.module_variable = render_template_obj.rend_template_any(config_variables, **self.context)
        # 模块变量 添加到模块全局变量
        if isinstance(self.module_variable, dict):
            self.context.update(self.module_variable)
        teststeps = self.raw.get('teststeps', [])        # noqa
        # 支持 2 种参数化格式数据
        config_params = render_template_obj.rend_template_any(config_params, **self.context)
        config_fixtures = render_template_obj.rend_template_any(config_fixtures, **self.context)
        config_fixtures, config_params = self.parameters_date(config_fixtures, config_params)

        def execute_yaml_case(args):
            for step in teststeps:
                response = None
                for item, value in step.items():
                    # 执行用例里面的方法
                    if item == 'name':
                        pass          # noqa
                    elif item == 'request':
                        copy_value = copy.deepcopy(value)  # 深拷贝一份新的value
                        request_session = args.get('requests_session')  # session 请求会话
                        # 加载参数化的值和fixture的值
                        self.context.update(args)
                        request_value = render_template_obj.rend_template_any(copy_value, **self.context)
                        response = request_session.send_request(
                            base_url=base_url,
                            **request_value
                        )
                    elif item == 'extract':
                        # 提取变量
                        copy_value = copy.deepcopy(value)
                        extract_value = render_template_obj.rend_template_any(copy_value, **self.context)
                        extract_result = self.extract_response(response, extract_value)
                        # 添加到模块变量
                        self.module_variable.update(extract_result)
                        if isinstance(self.module_variable, dict):
                            self.context.update(self.module_variable)    # 加载模块变量
                    elif item == 'validate':
                        copy_value = copy.deepcopy(value)
                        validate_value = render_template_obj.rend_template_any(copy_value, **self.context)
                        self.validate_response(response, validate_value)
                    else:
                        try:
                            eval(item)(value)
                        except Exception as msg:
                            raise exceptions.ParserError(f'Parsers error: {msg}')

        f = create_funtion.create_function_from_parameters(
            func=execute_yaml_case,
            # parameters 传内置fixture
            parameters=self.function_parameters(config_fixtures),
            documentation=case_name,
            func_name=str(self.module.__name__),
            func_filename=f"{self.module.__name__}.py",
        )

        # 向 module 中加入函数
        setattr(self.module, str(self.module.__name__), f)
        if config_params:
            # 向 module 中加参数化数据的属性
            setattr(self.module, 'params_data', config_params)

    @staticmethod
    def function_parameters(config_fixtures) -> list:
        """测试函数传 fixture """
        # 测试函数的默认请求参数
        function_parameters = [
            Parameter('request', Parameter.POSITIONAL_OR_KEYWORD)  # 内置request fixture
        ]
        # 获取传给用例的 fixtures
        if isinstance(config_fixtures, str):
            config_fixtures = [item.strip(" ") for item in config_fixtures.split(',')]
        if not config_fixtures:
            function_parameters.append(
                Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
            )
        else:
            if 'requests_function' in config_fixtures:
                function_parameters.append(
                    Parameter('requests_function', Parameter.POSITIONAL_OR_KEYWORD),
                )
            elif 'requests_module' in config_fixtures:
                function_parameters.append(
                    Parameter('requests_module', Parameter.POSITIONAL_OR_KEYWORD),
                )
            else:
                function_parameters.append(
                    Parameter('requests_session', Parameter.POSITIONAL_OR_KEYWORD),
                )
            for fixture in config_fixtures:
                if fixture not in ['requests_function', 'requests_module']:
                    function_parameters.append(
                        Parameter(fixture, Parameter.POSITIONAL_OR_KEYWORD),
                    )
        return function_parameters

    @staticmethod
    def parameters_date(fixtures, parameters):
        """
            参数化实现2种方式：
        方式1：
            config:
               name: post示例
               fixtures: username, password
               parameters:
                 - [test1, '123456']
                 - [test2, '123456']
        方式2：
            config:
               name: post示例
               parameters:
                 - {"username": "test1", "password": "123456"}
                 - {"username": "test2", "password": "1234562"}
        :returns
        fixtures: 用例需要用到的fixtures:  ['username', 'password']
        parameters: 参数化的数据list of list : [['test1', '123456'], ['test2', '123456']]
        """
        if isinstance(fixtures, str):
            # 字符串切成list
            fixtures = [item.strip(" ") for item in fixtures.split(',')]
        if isinstance(parameters, list) and len(parameters) > 1:
            if isinstance(parameters[0], dict):
                # list of dict
                params = list(parameters[0].keys())
                new_parameters = []
                for item in parameters:
                    new_parameters.append(list(item.values()))
                # fixtures 追加参数化的参数
                for param in params:
                    if param not in fixtures:
                        fixtures.append(param)
                return fixtures, new_parameters
            else:
                # list of list
                return fixtures, parameters
        else:
            return fixtures, []

    @staticmethod
    def extract_response(response, extract_obj: dict):
        """提取返回结果, 添加到module_variable 模块变量"""
        extract_result = {}
        if isinstance(extract_obj, dict):
            for extract_var, extract_expression in extract_obj.items():
                extract_var_value = extract.extract_by_object(response, extract_expression)  # 实际结果
                extract_result[extract_var] = extract_var_value
            return extract_result
        else:
            return extract_result

    @staticmethod
    def validate_response(response, validate_check: list) -> None:
        """校验结果"""
        for check in validate_check:
            for check_type, check_value in check.items():
                actual_value = extract.extract_by_object(response, check_value[0])  # 实际结果
                expect_value = check_value[1]  # 期望结果
                if check_type in ["eq", "equals", "equal"]:
                    validate.equals(actual_value, expect_value)
                elif check_type in ["lt", "less_than"]:
                    validate.less_than(actual_value, expect_value)
                elif check_type in ["le", "less_or_equals"]:
                    validate.less_than_or_equals(actual_value, expect_value)
                elif check_type in ["gt", "greater_than"]:
                    validate.greater_than(actual_value, expect_value)
                elif check_type in ["ne", "not_equal"]:
                    validate.not_equals(actual_value, expect_value)
                elif check_type in ["str_eq", "string_equals"]:
                    validate.string_equals(actual_value, expect_value)
                elif check_type in ["len_eq", "length_equal"]:
                    validate.length_equals(actual_value, expect_value)
                elif check_type in ["len_gt", "length_greater_than"]:
                    validate.length_greater_than(actual_value, expect_value)
                elif check_type in ["len_ge", "length_greater_or_equals"]:
                    validate.length_greater_than_or_equals(actual_value, expect_value)
                elif check_type in ["len_lt", "length_less_than"]:
                    validate.length_less_than(actual_value, expect_value)
                elif check_type in ["len_le", "length_less_or_equals"]:
                    validate.length_less_than_or_equals(actual_value, expect_value)
                elif check_type in ["contains"]:
                    validate.contains(actual_value, expect_value)
                else:
                    if hasattr(validate, check_type):
                        getattr(validate, check_type)(actual_value, expect_value)
                    else:
                        print(f'{check_type}  not valid check type')
