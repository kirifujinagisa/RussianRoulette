from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived

import random

@register(name="RussianRoulette", description="A Russian Roulette game plugin", version="1.0", author="kirifujinagisa")
class RussianRoulettePlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.chamber = [False] * 6  # 初始时6个弹槽都为空
        self.bullet_index = random.randint(0, 5)  # 随机选择一个弹槽放入子弹

    async def initialize(self):
        pass

    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        if msg == "上弹":
            if False in self.chamber:  # 如果还有空弹槽
                empty_slots = [i for i, x in enumerate(self.chamber) if not x]
                slot_to_load = random.choice(empty_slots)
                self.chamber[slot_to_load] = True
                ctx.add_return("reply", ["上弹完成，当前弹槽情况：" + " ".join(["O" if x else "-" for x in self.chamber])])
                ctx.prevent_default()
            else:
                ctx.add_return("reply", ["弹槽已满，无法再上弹"])
                ctx.prevent_default()
        elif msg == "开枪":
            if self.chamber[self.bullet_index]:  # 如果当前弹槽中有子弹
                ctx.add_return("reply", ["砰！你中了一枪！游戏结束！"])
                self.chamber = [False] * 6  # 重置弹槽
                self.bullet_index = random.randint(0, 5)  # 重新选择一个弹槽放入子弹
                ctx.prevent_default()
            else:
                ctx.add_return("reply", ["砰！啥也没发生，你很幸运！"])
                ctx.prevent_default()
        elif msg == "弹槽情况":
            ctx.add_return("reply", ["当前弹槽情况：" + " ".join(["O" if x else "-" for x in self.chamber])])
            ctx.prevent_default()

    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        sender_id = ctx.event.sender_id  # 获取发送消息的用户 ID
        if "上弹" in msg:  # 如果群聊消息包含关键词"上弹"
            if False in self.chamber:  # 如果还有空弹槽
                empty_slots = [i for i, x in enumerate(self.chamber) if not x]
                slot_to_load = random.choice(empty_slots)
                self.chamber[slot_to_load] = True
                ctx.add_return("reply", ["[{} 上弹完成，当前弹槽情况：{}]".format(sender_id, " ".join(["O" if x else "-" for x in self.chamber]))])
                ctx.prevent_default()
            else:
                ctx.add_return("reply", ["[{} 弹槽已满，无法再上弹]".format(sender_id)])
                ctx.prevent_default()
        elif "开枪" in msg:  # 如果群聊消息包含关键词"开枪"
            if self.chamber[self.bullet_index]:  # 如果当前弹槽中有子弹
                ctx.add_return("reply", ["[{} 砰！你中了一枪！游戏结束！]".format(sender_id)])
                self.chamber = [False] * 6  # 重置弹槽
                self.bullet_index = random.randint(0, 5)  # 重新选择一个弹槽放入子弹
                ctx.prevent_default()
            else:
                ctx.add_return("reply", ["[{} 砰！啥也没发生，你很幸运！]".format(sender_id)])
                ctx.prevent_default()

    def __del__(self):
        pass
