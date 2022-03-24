from components.messenger.BaseMessenger import TextMessenger
from common.GlobalVariables import GV
from DialogAgents import agent_build_helper
from common.logprint import get_logger
import requests
import urllib.parse
import os 

logger = get_logger(__name__)


@GV.register_messenger("macaw_messenger")
# TODO: add supports for Dialog agents
class MacawMessenger(TextMessenger):
    def __init__(self, config):
        if not config.active:
            return
        config.topic = config.topic_in
        self.chat_id = os.getenv('BOT_CHAT_ID')
        self.bot_token_id = os.getenv('BOT_TOKEN_ID')
        super(MacawMessenger, self).__init__(config)

    def process_text(self, text):
        logger.debug(text)
        self.send_msg_to_telegram(text)
    
    def send_msg_to_telegram(self, text):
        safe_string = urllib.parse.quote_plus(text)
        api_url =  f'https://api.telegram.org/bot{self.bot_token_id}/sendMessage?chat_id={self.chat_id}&text={safe_string}'
        x = requests.post(api_url)
    
    def send_text(self, text):
        """
        Actively send a message through the communication manager
        :return: None
        """
        text = text.encode('utf-8')
        logger.debug(text)
        self.send(self.topic_out, text)
