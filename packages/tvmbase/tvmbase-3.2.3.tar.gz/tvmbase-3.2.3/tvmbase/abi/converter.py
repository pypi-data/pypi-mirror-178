import copy
import json

from jsonizer import Jsonizer
from tonclient.types import AbiContract, AbiFunction, AbiEvent, AbiData, AbiParam


def file_to_abi(filename: str) -> AbiContract:
    with open(filename, 'r') as file:
        data = json.load(file)
    return json_to_abi(data, mutate=True)


def json_to_abi(data: dict, mutate: bool = False) -> AbiContract:
    # fix abi events - removing "outputs" field
    if len(data['events']) > 0:
        if not mutate:
            data = copy.deepcopy(data)
        for event in data['events']:
            event.pop('outputs', None)
    parser = Jsonizer(AbiContract, AbiFunction, AbiEvent, AbiData, AbiParam, lowercase_keys=True, replace_space='_')
    return parser.parse(data)


def abi_params_to_str(abi_params: list[AbiParam]) -> str:
    result = list()
    for abi_param in abi_params:
        sub_result = _abi_param_to_tuple(abi_param)
        result.append(sub_result)
    return ','.join(result)


def _abi_param_to_tuple(abi_param: AbiParam) -> str:
    type_ = abi_param.type
    if abi_param.components:
        components_str = abi_params_to_str(abi_param.components)
        type_ = type_.replace('tuple', '(' + components_str + ')')
    return type_
