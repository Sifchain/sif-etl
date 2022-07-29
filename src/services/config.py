# postgres config
import os
from os.path import join, dirname, realpath

from dotenv import load_dotenv


class ConfigService:
    def __init__(self):
        if os.getenv("ENVIRONMENT") == "docker":
            env_path = realpath(join(dirname(__file__), "../../.env.docker"))
            load_dotenv(dotenv_path=env_path)
        else:
            env_path = realpath(join(dirname(__file__), "../../.env"))
            load_dotenv(dotenv_path=env_path)

        self.mongo_config_testnet = os.getenv("MONGO_CONFIG_TESTNET")

        self.mongo_config = os.getenv("MONGO_CONFIG_BETANET")
        self.mongo_config_test = os.getenv("MONGO_CONFIG_TESTNET")
        self.mongo_config_dev = os.getenv("MONGO_CONFIG_DEVNET")
        self.mongo_config_test_42 = os.getenv("MONGO_CONFIG_42_TESTNET")
        self.mongo_config_dev_42 = os.getenv("MONGO_CONFIG_42_DEVNET")
        self.mongo_config_beta_42 = os.getenv("MONGO_CONFIG_42_BETANET")

        self.pg_config = {
            "database": os.getenv("DATABASE"),
            "user": os.getenv("DBUSER"),
            "password": os.getenv("DBPASSWORD"),
            "host": os.getenv("DBHOST"),
            "port": os.getenv("DBPORT"),
        }

        self.hasura_config = {
            "url": os.getenv("HASURA_URL", ""),
            "password": os.getenv("HASURA_PASSWORD"),
        }

        # betanet api config
        self.api_config = {
            "RPC_SERVER_URL": os.getenv("RPC_SERVER_URL"),
            "RPC_SERVER_LPD_URL": os.getenv("RPC_SERVER_LPD_URL"),
            "LCD_SERVER_URL": os.getenv("LCD_SERVER_URL"),
            "LCD_SERVER_PMTP": os.getenv("LCD_SERVER_PMTP"),
            "LCD_SERVER_PMTP_HIST": os.getenv("LCD_SERVER_PMTP_HIST", ""),
            "TOKEN_LIST_URL": os.getenv("TOKEN_LIST_URL", ""),
            "TOKEN_LIST": os.getenv("TOKEN_LIST", ""),
            "COINMARKETCAP_URL": os.getenv("COINMARKETCAP_URL", ""),
            "CMC_PRO_API_KEY": os.getenv("CMC_PRO_API_KEY", ""),
            "CE_DISPENSATION_URL": os.getenv("CE_DISPENSATION_URL", ""),
        }

        self.slack_config = {
            "SLACK_CHANNEL_TEST": os.getenv("SLACK_CHANNEL_TEST", ""),
            "SLACK_CHANNEL": os.getenv("SLACK_CHANNEL", ""),
            "SLACK_ENG_DATA_PIPELINE_CHANNEL": os.getenv(
                "SLACK_ENG_DATA_PIPELINE_BOT_CHANNEL", ""
            ),
        }

        # betanet schema
        self.schema_config = {
            "EVENTS_TABLE_V2": os.getenv("EVENTS_TABLE_V2"),
            "PRICES_TABLE": os.getenv("PRICES_TABLE"),
            "TOKEN_PRICES_TABLE": os.getenv("TOKEN_PRICES_TABLE"),
            "SNAPSHOT_TABLE": os.getenv("SNAPSHOT_TABLE"),
            "SNAPSHOT_TABLE_PARTITION": os.getenv("SNAPSHOT_TABLE_PARTITION"),
            "SNAPSHOT_TABLE_PARTITION_RF": os.getenv("SNAPSHOT_TABLE_PARTITION_RF"),
            "SNAPSHOT_TABLE_DEV": os.getenv("SNAPSHOT_TABLE_DEV"),
            "POST_DISTRIBUTION": os.getenv("POST_DISTRIBUTION"),
            "PRE_DISTRIBUTION": os.getenv("PRE_DISTRIBUTION"),
            "POOL_TABLE": os.getenv("POOL_TABLE"),
            "SNAPSHOT_VALIDATORS_TABLE": os.getenv("SNAPSHOT_VALIDATORS_TABLE"),
            "SNAPSHOT_VALIDATORS_TABLE_RF": os.getenv("SNAPSHOT_VALIDATORS_TABLE_RF"),
            "SNAPSHOT_VALIDATORS_TABLE_DEV": os.getenv("SNAPSHOT_VALIDATORS_TABLE_DEV"),
            "SNAPSHOT_VS_CLAIMS_TABLE": os.getenv("SNAPSHOT_VS_CLAIMS_TABLE"),
            "SNAPSHOT_LM_CLAIMS_TABLE": os.getenv("SNAPSHOT_LM_CLAIMS_TABLE"),
            "SNAPSHOT_VS_CLAIMS_TABLE_RF": os.getenv("SNAPSHOT_VS_CLAIMS_TABLE_RF"),
            "SNAPSHOT_LM_CLAIMS_TABLE_RF": os.getenv("SNAPSHOT_LM_CLAIMS_TABLE_RF"),
            "SNAPSHOT_VS_DISPENSATION": os.getenv("SNAPSHOT_VS_DISPENSATION"),
            "SNAPSHOT_LM_DISPENSATION": os.getenv("SNAPSHOT_LM_DISPENSATION"),
            "SNAPSHOT_VS_DISPENSATION_RF": os.getenv("SNAPSHOT_VS_DISPENSATION_RF"),
            "SNAPSHOT_LM_DISPENSATION_RF": os.getenv("SNAPSHOT_LM_DISPENSATION_RF"),
            "EVENT_TXN_TABLE": os.getenv("EVENT_TXN_TABLE"),
            "AIRDROP_REC": os.getenv("AIRDROP_REC"),
            "AIRDROP_PREQUALIFY": os.getenv("AIRDROP_PREQUALIFY"),
            "COINMARKETCAP_TABLE": os.getenv("COINMARKETCAP_TABLE"),
        }

        # sandpit schema
        self.schema_config_sandpit = {
            "VALIDATOR_TABLE": os.getenv("VALIDATOR_SANDPIT_TABLE"),
            "PRICES_TABLE": "",
        }

        # api config sandpit
        self.api_config_sandpit = {
            "RPC_SERVER_URL": os.getenv("RPC_SERVER_SANDPIT_URL"),
            "LCD_SERVER_URL": os.getenv("LCD_SERVER_SANDPIT_URL"),
        }

        self.pnl = {"PNL_ADDRESSES": os.getenv("PNL_ADDRESSES", "").split(" ")}


config_service = ConfigService()
