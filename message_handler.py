from search import Search
from redis_util import RedisUtil
import logging

logger = logging.getLogger(__name__)

class RequestMessageHandler(object):

    def __init__(self, message: str):
        self.message = message
        self.user_message_lower = message.content.lower()
        self.author_name = message.author.name

    def _handler_for_hi(self) -> str:
        """[Handler for hi message]

        Returns:
            [str]: [Returns Hey]
        """
        return f"Hey {self.author_name}"

    def _handler_for_google_search(self) -> str:
        """[Handler method for google search]

        Returns:
            [str]: [Top 5 Search results from google]
        """
        # Do some search using google
        # Using split from 1st word since search will look like

        # !google nodejs, !Google Mongo etc.
        list_of_words_to_search = self.user_message_lower.split(" ")[1:]
        word_to_search_combined = " ".join(list_of_words_to_search)
        search_result = Search().search_using_google(word_to_search_combined)
        return f"Hey {self.author_name}, We found these results for you. \n {search_result}"

    def _handler_for_recent_games(self) -> str:
        """[Returns the recent games searched by the user]

        Returns:
            [str]: [games with separator as \n]
        """
        return RedisUtil(self.message.author).get_all_games()

    def _insert_game_in_db_if_exists(self):
        """
        Insert game in redis if google query contains words like
        !google apple games, !google game of thrones etc.

        Otherwise does nothing.
        """
        if "game" in self.user_message_lower:
            game_name = " ".join(self.user_message_lower.split(" ")[1:])
            RedisUtil(self.message.author).insert_game(game_name)

    @property
    def response(self):

        if self.user_message_lower == "hi":
            return self._handler_for_hi()

        if self.user_message_lower.find("!google") != -1:
            try:
                self._insert_game_in_db_if_exists()
            except Exception as e:
                logger.error("Failed to insert game in redis. Error \n {e}")
            return self._handler_for_google_search()

        if self.user_message_lower.find("!recent") != -1:
            return self._handler_for_recent_games()

        # if none of above criteria fullfill then return
        return "We do not support these now but we will surely take these in consideration. Thank you"

