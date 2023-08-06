"""
@author axiner
@version v1.0.0
@created 2022/7/30 16:07
@abstract 全局唯一id
@description
@history
"""
import time
from datetime import datetime, timedelta

from toollib.common.error import InvalidSystemClock
from toollib.utils import Singleton, now2str

__all__ = [
    'SnowFlake',
    'RedisUid',
]


class SnowFlake(metaclass=Singleton):
    """
    雪花算法（全局唯一id）
    （最早是Twitter公司在其内部用于分布式环境下生成唯一ID）
    # Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
    # https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
    使用示例：
        from toollib.guid import SnowFlake
        snow = SnowFlake()
        uid = snow.gen_uid()
        +++++[更多详见参数或源码]+++++
    """

    def __init__(
            self,
            worker_id: int = 0,
            datacenter_id: int = 0,
            sequence=0,
            epoch_timestamp: int = 1639286040000,
            worker_id_bits: int = 5,
            datacenter_id_bits: int = 5,
            sequence_bits: int = 12,
            to_str: bool = False,
    ):
        """
        初始化
            注：分布式可通过映射指定不同的'worker_id'+'datacenter_id'来区分
        :param worker_id: 机器ID
        :param datacenter_id: 数据中心ID
        :param sequence: 序号
        :param epoch_timestamp: 纪元（[默认:1639286040000=>20211212131400][Twitter:1288834974657=>20101104094254]）
        :param worker_id_bits: 机器id位数
        :param datacenter_id_bits: 服务id位数
        :param sequence_bits: 序号位数
        :param to_str: 是否转为字符串
        """
        if not isinstance(worker_id, (int, type(None))):
            raise TypeError('"worker_id" only supported: int')
        if not isinstance(datacenter_id, (int, type(None))):
            raise TypeError('"datacenter_id" only supported: int')
        max_worker_id = -1 ^ (-1 << worker_id_bits)
        max_datacenter_id = -1 ^ (-1 << datacenter_id_bits)
        if worker_id > max_worker_id or worker_id < 0:
            raise ValueError(f'"worker_id" only supported: 0, {max_worker_id}')
        if datacenter_id > max_datacenter_id or datacenter_id < 0:
            raise ValueError(f'"datacenter_id" only supported: 0, {max_datacenter_id}')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence
        self.epoch_timestamp = epoch_timestamp
        self.last_timestamp = -1

        self.worker_id_shift = sequence_bits
        self.datacenter_id_shift = sequence_bits + worker_id_bits
        self.timestamp_left_shift = sequence_bits + worker_id_bits + datacenter_id_bits
        self.sequence_mask = -1 ^ (-1 << sequence_bits)

        self.to_str = to_str

    def gen_uid(self, to_str: bool = None):
        """
        生成唯一id
        :param to_str: 是否转为字符串(可覆盖cls中的to_str)
        :return:
        """
        if to_str is None:
            to_str = self.to_str
        timestamp = self._current_timestamp()
        if timestamp < self.last_timestamp:
            raise InvalidSystemClock("Clock moved backwards. Refusing to generate id for %s milliseconds" % (
                self.last_timestamp - timestamp))
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        uid = ((timestamp - self.epoch_timestamp) << self.timestamp_left_shift) | \
                 (self.datacenter_id << self.datacenter_id_shift) | \
                 (self.worker_id << self.worker_id_shift) | self.sequence
        if to_str is True:
            uid = str(uid)
        return uid

    def _til_next_millis(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    @staticmethod
    def _current_timestamp():
        return int(time.time() * 1000)


class RedisUid:
    """
    全局唯一id，基于redis实现（可用于分布式）
    使用示例：
        from toollib.guid import RedisUid
        ruid = RedisUid(redis_cli, 'ABC')
        uid = ruid.gen_uid()
        +++++[更多详见参数或源码]+++++
    """

    def __init__(
            self,
            redis_cli,
            prefix: str,
            beg_seqnum: int = 0,
            date_fmt: str = '%Y%m%d',
            zfill_len: int = 9,
            ex: datetime = None,
    ):
        """
        初始化
        :param redis_cli: redis客户端对象
        :param prefix: 前缀
        :param beg_seqnum: 开始序号
        :param date_fmt: 日期格式
        :param zfill_len: 0填充长度
        :param ex: 过期时间，不传则默认第二天凌晨
        """
        self.redis_cli = redis_cli
        self.prefix = prefix
        self.beg_seqnum = beg_seqnum
        self.date_fmt = date_fmt
        self.zfill_len = zfill_len
        self.ex = self._set_ex(ex)

    def gen_uid(self):
        """生成唯一id"""
        if self.redis_cli.ttl(self.prefix) < 0:
            self.redis_cli.set(self.prefix, self.beg_seqnum)
            self.redis_cli.expireat(self.prefix, self.ex)
        seqnum = self.redis_cli.incr(self.prefix)
        uid = "{prefix}{date}{seq_value}".format(
            prefix=self.prefix,
            date=now2str(self.date_fmt),
            seq_value=str(seqnum).zfill(self.zfill_len))
        return uid

    @staticmethod
    def _set_ex(ex):
        if not ex:
            ex = (datetime.now() + timedelta(days=1)).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        return ex
