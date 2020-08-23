import redis
redisClient = redis.Redis(host='localhost', port=6379, db=0)


class RedisUtil(object):

    def __init__(self, author):
        self.list_name = author.id

    def insert_game(self, game: str) -> None:
        """[Insert game in the list]

        Args:
            game (str): [Game name]
        """
        redisClient.lpush(self.list_name, game)

    def get_all_games(self) -> str:
        """[Return all games from the list if exists else ""]

        Returns:
            [type]: [description]
        """
        games = ""
        for i in range(0, redisClient.llen(self.list_name)):
            games += redisClient.lindex(self.list_name, i).decode("utf-8") + "\n"

        games = games or "Sorry. No recent game found in your searches"
        return games