from yzcore.core.storage import StorageController as _StorageController, StorageRequestError
from yzcore.logger import get_logger


__all__ = (
    'StorageController',
    StorageRequestError
)


logger = get_logger(__name__)


# 全局对象存储配置
global_storage_conf = {'mode': 'minio', 'access_key_id': 'eN4CbPQg0texMKQi', 'access_key_secret': 'vVXtZ2kONy0kaIbDa3xxzAVWBcLyg88o', 'endpoint': '192.168.6.203:9003', 'public_bucket_name': 'realibox-public', 'private_bucket_name': 'realibox-private', 'image_domain': '', 'asset_domain': '', 'private_domain': '', 'private_cname': '', 'download_path': '/tmp/realibox/download/', 'cache_path': '/tmp/realibox/cache/', 'private_expire_time': '3600', 'policy_expire_time': '30'}


class StorageController(_StorageController):
    """
    对象存储控制器
    组织自定义对象存储
    >>> storage_ctrl = await StorageController.init(organiz_id='organiz_id')
    >>> storage_ctrl.organiz_storage_conf  # 组织自定义对象存储配置，未配置则为空字典
    >>> storage_ctrl.storage_conf  # 组织自定义对象存储配置或全局配置
    >>> storage_ctrl.public_storage_manage  # 非加密存储控制器
    >>> storage_ctrl.private_storage_manage  # 加密存储控制器
    全局对象存储
    >>> global_storage_manage = await StorageController.init()
    >>> global_storage_manage.public_storage_manage  # 全局非加密存储控制器
    >>> global_storage_manage.private_storage_manage  # 全局加密存储控制器
    """

    @classmethod
    def global_storage_conf(cls):
        return global_storage_conf

    def _get_organiz_storage_conf(self):
        """获取组织的自定义对象存储配置"""
        pass
