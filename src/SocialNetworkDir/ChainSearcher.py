import abc
from src.ConfigDir.Config import Config
from collections import deque


class ChainSearcherFactory:
    """This class creates different types of ChainSearcher."""
    def __init__(self, get_friends_func):
        self.__config = Config()
        self.get_friends_func = get_friends_func

    def create_searcher(self):
        """Return a ChainSearcher-object for given algorithm."""
        searcher_type = self.__config.get_searcher_type()

        if searcher_type == 'bfs':
            return BidirBFSSearcher(self.get_friends_func)
        else:
            raise ValueError(f'Unsupported view type: {searcher_type}')


@abc.abstractmethod
class ChainSearcher:
    """An interface for ChainSearchers."""
    def __init__(self, get_friends_func):
        """Init of a function which takes user_id and return list of friend's user ids."""
        self.get_friends_func = get_friends_func

    def get_chain(self, user_id1, user_id2):
        """Return a list of user ids which is a chain between user_id1 and user_id2."""
        pass


class BidirBFSSearcher(ChainSearcher):
    """ChainSearcher which uses bidirectional bfs for searching."""
    def __get_chain_ends(self, user_id1, user_id2):
        # Словарь для хранения предыдущей вершины на пути
        # Ключ - вершина, значение - ее предыдущая вершина
        start_prev = {user_id1: None}
        end_prev = {user_id2: None}

        # Очереди для bfs
        start_queue = deque([user_id1])
        end_queue = deque([user_id2])

        while start_queue and end_queue:
            # bfs из стартовой вершины
            curr_start = start_queue.popleft()
            neighbors = self.get_friends_func(curr_start)
            for neighbor in neighbors:
                if neighbor not in start_prev:
                    start_prev[neighbor] = curr_start
                    start_queue.append(neighbor)
                # Проверяем, не достигли ли мы вершины из конечной очереди
                if neighbor in end_prev:
                    # Возвращаем путь от начала до конца, объединяя два пути
                    return start_prev, end_prev, curr_start, neighbor

            # bfs из конечной вершины
            curr_end = end_queue.popleft()
            neighbors = self.get_friends_func(curr_end)
            for neighbor in neighbors:
                if neighbor not in end_prev:
                    end_prev[neighbor] = curr_end
                    end_queue.append(neighbor)
                # Проверяем, не достигли ли мы вершины из стартовой очереди
                if neighbor in start_prev:
                    # Возвращаем путь от начала до конца, объединяя два пути
                    return start_prev, end_prev, neighbor, curr_end

        # Если путь не найден
        return [None, None, None, None]

    def __construct_chain(self, user_id1, user_id2):
        start_prev, end_prev, start, end = self.__get_chain_ends(user_id1, user_id2)
        if not start:
            return None
        # Список для хранения пути
        chain = []
        curr = start

        # Добавляем вершины от начала до общей вершины
        while curr is not None:
            chain.append(curr)
            curr = start_prev[curr]

        # Добавляем вершины от общей вершины до конца (в обратном порядке)
        curr = end
        while curr is not None:
            chain = [curr] + chain
            curr = end_prev[curr]

        # Возвращаем путь от начала до конца
        return chain[::-1]

    def get_chain(self, user_id1, user_id2):
        return self.__construct_chain(user_id1, user_id2)

