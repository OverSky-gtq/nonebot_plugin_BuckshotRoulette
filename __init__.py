import random
from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    GROUP,
    Bot,
    GroupMessageEvent,
    MessageSegment,
    Message,
)
from nonebot.params import CommandArg
from .manage import game,Player
from .config import Config

__plugin_meta = PluginMetadata(
    name="Buckshot Roulette",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

shot = on_command("shot",aliases = {"射击"})
add = on_command("加入游戏")
item = on_command("道具")
use = on_command("使用",aliases = {"用","use"})
help = on_command("教程",aliases = {"帮助","help"})
set_item = on_command("增加道具")
end = on_command("结束游戏")

@help.handle()
async def _(event: GroupMessageEvent):
    await help.finish("【恐怖版俄罗斯轮盘赌，输了就会被机械怪物爆头！】 https://www.bilibili.com/video/BV1oG41167ho/?share_source=copy_web&vd_source=8571241919d092bf3ec1d88ad940043b")

@item.handle()
async def _(event: GroupMessageEvent):
    if not game.is_player(str(event.user_id)):
        return
    await item.finish(game.get_item())

@end.handle()
async def _(event: GroupMessageEvent):
    if str(event.user_id) in config.superusers:
        game.end()
        await end.finish("已清空缓存")
    else:
        await end.finish("无权")

@add.handle()
async def _(event: GroupMessageEvent):
    if len(game._player_list) < 2:
        game.add_player(str(event.user_id))
        await add.send(f"加入成功，你是{len(game._player_list)}号")
    else:
        await add.finish("已满两人")
    if len(game._player_list) == 2:
        game.new_bullet_list(game._bullet_num)
        await add.finish(f"本轮子弹一览：{game.get_bullet()}，随机装填。\n游戏开始，首先是1号的回合")

@shot.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    if not game.is_player(str(event.user_id)):
        return
    msg = arg.extract_plain_text().strip()
    if msg == "me":
        ret = game.shot(str(event.user_id),True)
    else:
        ret = game.shot(str(event.user_id),False)

    end_flag = game.is_end()
    if end_flag:
        game.end()
        await shot.finish(f"{end_flag}号玩家死亡，游戏结束")
    if ret == 0:
        await shot.send("虚弹")
        await shot.send(game.get_hp())
    elif ret == 1:
        await shot.send(f"实弹，生命-{ret}")
        await shot.send(game.get_hp())
    elif ret == 2:
        await shot.send(f"实弹，生命-{ret}")
        await shot.send(game.get_hp())
    else:
        await shot.send(ret)
    if len(game._bullet_list) == 0:
        game._bullet_num += random.randint(1,2)
        if game._bullet_num > 8:
            game._bullet_num = 8
        game.new_bullet_list(game._bullet_num)
        new_item = game._round_num % 3 + 2
        game.flush_items(new_item)
        await shot.send(f"新的一轮开始，发放道具{new_item}个，子弹一览：{game.get_bullet()}")
        await shot.finsih(game.get_item())

@use.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    if not game.is_player(str(event.user_id)):
        return
    msg = arg.extract_plain_text().strip()
    flag,ret = game.use(str(event.user_id),msg)
    if flag:
        print(ret)
        if msg == "放大镜":
            await use.finish(f"有趣，是{'💧' if ret == 0 else '🩸'}")
        elif msg == "小刀":
            await use.finish("你锯掉了枪管，霰弹枪威力加倍，下一回合恢复")
        elif msg == "香烟":
            await use.finish("你抽了根烟，生命+1")
        elif msg == "啤酒":
            await use.finish(f"你灌了瓶啤酒，从枪管退出了一颗{'💧' if ret == 0 else '🩸'}")
        elif msg == "手铐":
            await use.finish("给对方铐上手铐，下一回合不能行动")
    else:
        await use.finish(ret)

@set_item.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    id = str(event.user_id)
    if id in config.superusers:
        msg = arg.extract_plain_text().strip()
        for player in game._player_list:
            if player._id == id:
                player._item.append(msg)
        await set_item.finish("增加成功")
    else:
        await set_item.finish("无权")


