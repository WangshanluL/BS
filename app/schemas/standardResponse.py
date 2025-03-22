from pydantic import BaseModel
from typing import Optional, Any

class StandardResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

"""
标准HTTP状态码

1xx - 信息性响应

100 - 继续
101 - 切换协议


2xx - 成功

200 - 成功/OK（最常用的成功状态码）
201 - 已创建（通常用于POST请求成功创建资源）
202 - 已接受（请求已接受但尚未处理完成）
204 - 无内容（请求成功但不返回任何内容）


3xx - 重定向

301 - 永久重定向
302 - 临时重定向
304 - 未修改（资源未变化，可使用缓存）


4xx - 客户端错误

400 - 错误请求（请求参数有误）
401 - 未授权（需要用户验证）
403 - 禁止访问（服务器拒绝请求）
404 - 未找到（请求的资源不存在）
409 - 冲突（请求与服务器当前状态冲突）
422 - 无法处理（通常是验证错误）


5xx - 服务器错误

500 - 服务器内部错误
502 - 网关错误
503 - 服务不可用
504 - 网关超时



"""