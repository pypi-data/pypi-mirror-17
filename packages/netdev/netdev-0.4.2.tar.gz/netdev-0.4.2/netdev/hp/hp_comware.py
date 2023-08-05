import re

from ..logger import logger
from ..netdev_base import NetDev


class HPComware(NetDev):
    async def connect(self):
        """
        Prepare the session after the connection has been established.

        Using 3 functions:
            establish_connection() for connecting to device
            set_base_prompt() for finding and setting device prompt
            disable_paging() for non interact output in commands
        """
        logger.info("Connecting to device")
        await self._establish_connection()
        await self._set_base_prompt()
        await self._disable_paging()
        logger.info("Connected to device")

    async def _set_base_prompt(self):
        """
        Setting two important vars
            base_prompt - textual prompt in CLI (usually hostname)
            base_pattern - regexp for finding the end of command. IT's platform specific parameter

        For Comware devices base_pattern is "[\]|>]prompt(\-\w+)?[\]|>]
        """
        logger.info("Setting base prompt")
        prompt = await self._find_prompt()
        # Strip off trailing terminator
        self._base_prompt = prompt[1:-1]
        priv_prompt = self._get_default_command('priv_prompt')
        unpriv_prompt = self._get_default_command('unpriv_prompt')
        self._base_pattern = r"[\[|<]{}[\-\w]*[{}|{}]".format(re.escape(self._base_prompt[:12]), re.escape(priv_prompt),
                                                              re.escape(unpriv_prompt))
        logger.debug("Base Prompt: {}".format(self._base_prompt))
        logger.debug("Base Pattern: {}".format(self._base_pattern))
        return self._base_prompt

    def _get_default_command(self, command):
        """
        Returning default commands for device

        :param command: command for returning
        :return: real command for this network device
        """
        # @formatter:off
        command_mapper = {
            'priv_prompt': ']',
            'unpriv_prompt': '>',
            'disable_paging': 'screen-length disable',
            'priv_enter': '',
            'priv_exit': '',
            'config_enter': 'system-view',
            'config_exit': 'return',
            'check_config_mode': ']'
        }
        # @formatter:on
        return command_mapper[command]
