# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

# 模板 1：最小可用的确定性合约
#
# 用途：不碰外部数据，只演示 GenLayer 的存储类型和权限检查。
# 适合拿来当基线，先确认工具链能跑通，再加非确定性逻辑。
#
# 用到的存储类型：
#   Address         部署者地址
#   u32             计数器
#   DynArray[str]   追加式数组（不能用 list）
#   TreeMap[str,str] 键值映射（不能用 dict）

from genlayer import *


class NoteRegistry(gl.Contract):
    owner: Address
    total: u32
    notes: DynArray[str]
    by_tag: TreeMap[str, str]

    def __init__(self):
        self.owner = gl.message.sender_address
        self.total = u32(0)

    @gl.public.write
    def add_note(self, text: str, tag: str):
        # 所有写方法默认有权限门槛，避免任何地址都能改状态
        if gl.message.sender_address != self.owner:
            raise gl.vm.UserError("only owner can write")

        if len(text) == 0 or len(tag) == 0:
            raise gl.vm.UserError("text and tag must not be empty")

        self.notes.append(text)
        self.by_tag[tag] = text
        self.total = u32(self.total + 1)

    @gl.public.view
    def get_note(self, index: u32) -> str:
        return self.notes[index]

    @gl.public.view
    def get_by_tag(self, tag: str) -> str:
        return self.by_tag.get(tag, "")

    @gl.public.view
    def count(self) -> u32:
        return self.total

    @gl.public.view
    def get_owner(self) -> Address:
        return self.owner
