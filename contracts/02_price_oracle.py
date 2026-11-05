# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

# 模板 2：从外部 API 取数，再让验证者共识
#
# 用途：任何需要链下数据的合约都绕不开这一步。关键不是"请求 API"，
# 而是"多个验证者看到的价格不可能完全一样，怎么判定他们其实同意了"。
#
# 这里用自定义验证者做容差比较。strict_eq 只适合结果稳定到字节级别的数据，
# 价格这种每秒在变的数字必须用容差。

from genlayer import *
import json


class PriceOracle(gl.Contract):
    pair: str
    price: str       # 存字符串，避免不同节点浮点格式化差异
    updates: u32
    last_error: str

    def __init__(self, pair: str):
        self.pair = pair
        self.price = ""
        self.updates = u32(0)
        self.last_error = ""

    @gl.public.write
    def update(self, api_url: str):
        def leader_fn():
            res = gl.nondet.web.get(api_url)
            data = json.loads(res.body.decode("utf-8"))
            return str(round(float(data["price"]), 4))

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False

            try:
                lead = float(leaders_res.calldata)
                own = float(leader_fn())
            except (TypeError, ValueError):
                return False

            if lead <= 0 or own <= 0:
                return False

            # 0.5% 容差。太紧会让交易反复失败，太松等于没验证。
            return abs(own - lead) / lead <= 0.005

        agreed = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        # 注意：所有状态写入都必须在共识结束之后，非确定性块里写 self 会直接报错
        self.price = str(agreed)
        self.updates = u32(self.updates + 1)

    @gl.public.write
    def set_error(self, message: str):
        self.last_error = message

    @gl.public.view
    def get_price(self) -> str:
        return self.price

    @gl.public.view
    def get_pair(self) -> str:
        return self.pair

    @gl.public.view
    def update_count(self) -> u32:
        return self.updates
