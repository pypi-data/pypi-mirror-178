from typing import Any, TYPE_CHECKING

from tonclient.client import TonClient
from tonclient.types import (
    ClientConfig,
    NetworkConfig,
    AbiContract,
    Abi,
    CallSet,
    ParamsOfEncodeMessage,
    Signer,
    ExecutionOptions,
    ParamsOfRunTvm,
)

from tvmbase.exceptions import ClientRunLocalException
from tvmbase.models.network import Network
from tvmbase.utils.singleton import SingletonMeta

if TYPE_CHECKING:
    from tvmbase.models.tvm.account import Account


class Client(TonClient, metaclass=SingletonMeta):

    def __init__(self, network: Network):
        self.network = network
        config = self.create_config(network)
        super().__init__(config, is_async=True)

    @staticmethod
    def create_config(network: Network) -> ClientConfig:
        network_config = NetworkConfig(endpoints=network.endpoints)
        return ClientConfig(network=network_config)

    async def run_local(
            self,
            abi: AbiContract,
            method: str,
            account: 'Account' = None,
            account_params: tuple[str, str] = None,
            params: dict = None,
            auto_answer_id: bool = True,
            execution_options: dict = None,
            parse: bool = False,
    ) -> dict | Any:
        """
        Use account or address_params
        :return: dict in case of `parse` is False, otherwise parse response and return Any type
        """
        assert account is not None or account_params is not None, 'Arg `account` or `account_params` must be provided'
        if account is not None:
            address = account.address
            account_boc = account.data.boc
        else:
            address, account_boc = account_params

        if auto_answer_id:
            params = params or dict()
            self._set_answer_id(abi, method, params)

        abi = Abi.Contract(abi)
        call_set = CallSet(function_name=method, input=params)
        message_params = ParamsOfEncodeMessage(
            abi=abi,
            address=address,
            signer=Signer.NoSigner(),
            call_set=call_set,
        )
        message = await self.abi.encode_message(params=message_params)

        if execution_options is not None:
            execution_options = ExecutionOptions(**execution_options)

        run_params = ParamsOfRunTvm(
            message=message.message,
            account=account_boc,
            abi=abi,
            execution_options=execution_options,
        )
        result = await self.tvm.run_tvm(params=run_params)
        decoded = result.decoded.output

        if parse:
            if len(decoded) != 1:
                raise ClientRunLocalException('Must be exact one output param for automatic parse')
            return decoded.popitem()[1]
        else:
            return decoded

    @staticmethod
    def _set_answer_id(abi_contract: AbiContract, method: str, params: dict):
        function = next(filter(
            lambda f: f.name == method,
            abi_contract.functions
        ))
        if len(function.inputs) == 0:
            return
        first_arg_name = function.inputs[0].name
        if (first_arg_name in ('answerId', '_answer_id')) and (first_arg_name not in params):
            params[first_arg_name] = 0

    # todo
    # async def emulate_local(
    #         self,
    #         account: 'Account',
    #         abi: str,
    #         method: str,
    #         params: dict,
    #         value: int,
    #         bounce: bool = None,
    #         sender: str = None,  # todo jenkins
    # ) -> ResultOfRunTvm:
    #     # print(value / 1e9)
    #     if sender is None:
    #         sender = '0:' + '12' * 32  # todo
    #     abi = Abi.Json(abi)
    #     call_set = CallSet(function_name=method, input=params)
    #     message_params = ParamsOfEncodeInternalMessage(
    #         value=str(value),
    #         abi=abi,
    #         address=account.address,
    #         call_set=call_set,
    #         bounce=bounce,
    #         src_address=sender,
    #     )
    #     message = await self.abi.encode_internal_message(params=message_params)
    #     # run_params = ParamsOfRunTvm(
    #     #     message=message.message,
    #     #     account=account.data.boc,
    #     #     abi=abi,
    #     #     return_updated_account=True
    #     # )
    #     # return await self.tvm.run_tvm(params=run_params)
    #     account = AccountForExecutor.Account(boc=account.data.boc)
    #     run_params = ParamsOfRunExecutor(
    #         message=message.message,
    #         account=account,
    #         abi=abi,
    #         skip_transaction_check=True,
    #         return_updated_account=True,
    #     )
    #     return await self.tvm.run_executor(params=run_params)
