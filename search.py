from googlesearch import search


class Search(object):

    def __init__(self, total_results: int = 5):
        self.total_results = total_results

    def search_using_google(self, word: str) -> str:
        if not word:
            return "Sorry. Looks like your search query is empty."

        results = ""
        for url in search(word, stop=self.total_results):
            results += (url + "\n")
        return results
