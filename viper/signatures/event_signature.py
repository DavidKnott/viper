from viper.types import get_size_of_type, canonicalize_type, parse_type, \
    ByteArrayType
from viper.utils import fourbytes_to_int, sha3, is_varname_valid
import ast
from viper.function_signature import VariableRecord
from viper.exceptions import InvalidTypeException, TypeMismatchException, \
    VariableDeclarationException, StructureException, ConstancyViolationException, \
    InvalidTypeException, InvalidLiteralException, NonPayableViolationException


# Event signature object
class EventSignature():
    def __init__(self, name, args, indexed_list, output_type, sig, event_id):
        self.name = name
        self.args = args
        self.indexed_list = indexed_list
        self.output_type = output_type
        self.sig = sig
        self.arg_types = []
        # self.event_id = 1123
        self.method_id = 1232
        # self.gas = None

    # Get a signature from an event declaration
    @classmethod
    def from_declaration(cls, code):
        name = code.target.id
        pos = 0
        # Determine the arguments, expects something of the form def foo(arg1: num, arg2: num ...
        # topics = []
        args = []
        indexed_list = []
        if code.annotation.args:
            keys = code.annotation.args[0].keys
            values = code.annotation.args[0].values
            for i in range(len(keys)):
                typ = values[i]
                arg = keys[i].id
                if isinstance(typ, ast.Call):
                    if typ.func.id == 'indexed':
                        typ = values[i].args[0]
                        indexed_list.append(True)
                    else:
                        raise VariableDeclarationException("Only indexed keyword is allowed", arg)
                else:
                    indexed_list.append(False)
                # Check to see if argument is a topic
                if not isinstance(arg, str):
                    raise VariableDeclarationException("Argument name invalid", arg)
                if not typ:
                    raise InvalidTypeException("Argument must have type", arg)
                if not is_varname_valid(arg):
                    raise VariableDeclarationException("Argument name invalid or reserved: "+arg.arg, arg)
                if arg in (x.name for x in args):
                    raise VariableDeclarationException("Duplicate function argument name: "+arg.arg, arg)
                parsed_type = parse_type(typ, None)
                args.append(VariableRecord(arg, pos, parsed_type, False))
                if isinstance(parsed_type, ByteArrayType):
                    pos += 32
                else:
                    pos += get_size_of_type(parsed_type) * 32

        return cls(name, args, indexed_list, None, None, None)

    def to_abi_dict(self):
        return {
            "name": self.sig,
            "outputs": [{"type": canonicalize_type(self.output_type), "name": "out"}] if self.output_type else [],
            "inputs": [{"type": canonicalize_type(arg.typ), "name": arg.name} for arg in self.args],
            "constant": self.const,
            "payable": self.payable,
            "type": "constructor" if self.name == "__init__" else "function"
        }