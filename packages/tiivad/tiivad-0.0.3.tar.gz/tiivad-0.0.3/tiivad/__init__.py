# from lib.file import File
# from lib.function import Function
# from lib.function_execution import FunctionExecution
# from lib.program_execution import ProgramExecution
# from lib.utils import create_input_file, execute_test, validate_files
import json

from lib.results import Results
#
# __all__ = ["File", "file", "function", "function_execution", "program", "program_execution", "utils",
#            "execute_test", "ProgramExecution", "Function", "create_input_file", "FunctionExecution", "Results",
#            "validate_files"]
from lib.utils import execute_test, validate_files
from lib.help_structures import StandardOutputChecks, OutputFileChecks


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'repr_json'):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)


__all__ = ["execute_test", "validate_files", "StandardOutputChecks", "OutputFileChecks", "Results", "json",
           "ComplexEncoder"]
