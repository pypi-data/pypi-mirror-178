"""
    redis 批次爬虫

    注意：
        redis_key 为 spider_name:request 且不可更改
        若使用优先级队列，则放进去的数据形式应该为 {xxx:级别}
"""
import palp
from palp import sequence
from abc import abstractmethod


class BatchRedisSpider(palp.DistributiveSpider):
    spider_key = 'baidu:request'
    spider_queue = sequence.RequestRedisFIFOSequence()  # 队列类型

    def start_batch(self):
        """
        开启一个批次

        可以从任何地方获取批次

        :return:
        """
        while True:
            if self.__class__.spider_queue.empty():
                break

            url = self.__class__.spider_queue.get(timeout=5)

            if url:
                yield palp.RequestGet(url)

    def start_requests(self) -> None:
        """
        起始函数获取批次

        :return:
        """

    @abstractmethod
    def parse(self, request, response) -> None:
        """
        解析函数

        :param request:
        :param response:
        :return:
        """
        pass
