# from tests.main import Web3CliTest
# from typing import List
# from tests.seeder import seed_chains
# from web3cli.core.exceptions import Web3CliError
# from web3cli.core.models.chain import Chain
# from web3cli.core.seeds.types import ChainSeed
# import pytest
# from web3cli.core.helpers.format import cut


# def test_rpc_list(chains: List[ChainSeed]) -> None:
#     with Web3CliTest() as app:
#         seed_chains(app, chains)
#         app.set_args(["rpc", "list"]).run()
#         data, output = app.last_rendered
#         for c in chains:
#             for rpc_url in c["rpcs"]:
#                 assert cut(rpc_url, 40, "") in output


# def test_rpc_add(chains: List[ChainSeed]) -> None:
#     for c in chains:
#         with Web3CliTest() as app:
#             # Add the chain without RPCs
#             Chain.create(name=c["name"], chain_id=c["chain_id"], coin=c["coin"])
#         # Add the chain again > exception!
#         with Web3CliTest(delete_db=False) as app:
#             with pytest.raises(Web3CliError, match=r"already exists"):
#                 app.set_args(argv).run()
#         # Add the chain again with --update option > ok!
#         with Web3CliTest(delete_db=False) as app:
#             updated_argv = argv + ["--update"]
#             updated_argv[4] = f"{c['coin']}_UPDATED"
#             print(updated_argv)
#             app.set_args(updated_argv).run()
#             assert Chain.select().count() == 1
#             updated_chain: Chain = Chain.get_by_name(c["name"])
#             assert updated_chain.chain_id == c["chain_id"]
#             assert updated_chain.coin == updated_argv[4]


# # def test_chain_get(chains: List[ChainSeed]) -> None:
# #     """With explicit argument > return argument value"""
# #     for chain in chains:
# #         with Web3CliTest() as app:
# #             seed_chains(app, chains)
# #             app.set_args(["--chain", chain["name"], "chain", "get"]).run()
# #             data, output = app.last_rendered
# #             assert data["out"] == chain["name"]


# # def test_chain_get_no_args(chains: List[ChainSeed]) -> None:
# #     """Without any argument > return the default chain"""
# #     for chain in chains:
# #         with Web3CliTest() as app:
# #             seed_chains(app, chains)
# #             app.config.set("web3cli", "default_chain", chain["name"])
# #             app.set_args(["chain", "get"]).run()
# #             data, output = app.last_rendered
# #             assert data["out"] == chain["name"]


# # def test_chain_delete(chains: List[ChainSeed]) -> None:
# #     for c in chains:
# #         with Web3CliTest() as app:
# #             seed_chains(app, chains)
# #             app.set_args(
# #                 [
# #                     "chain",
# #                     "delete",
# #                     c["name"],
# #                 ]
# #             ).run()
# #             assert Chain.select().count() == len(chains) - 1
