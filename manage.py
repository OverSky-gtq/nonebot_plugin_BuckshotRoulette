import random

class Player:
    def __init__(self,id:str) -> None:
        self._id = id
        self._hp = 6
        self._item:list[str] = []


class Manager:
    def __init__(self):
        self._round_state: int = 0
        self._round_num:int = 0
        self._bullet_num = 3
        self._player_list: list[Player] = []
        self._bullet_list: list[int] = []
        self._solid_round:int = -1
    
    def add_player(self,id:str):
        self._player_list.append(Player(id))

    def invert_state(self):
        if self._solid_round == self._round_num:
            return
        if self._round_state == 0:
            self._round_state = 1
        else:
            self._round_state = 0
            
    def is_end(self):
        for index,player in enumerate(self._player_list):
            if player._hp <= 0:
                return index+1
        return False
    
    def is_player(self,id:str):
        for player in self._player_list:
            if player._id == id:
                return True
        return False
    
    def end(self):
        self._bullet_num = 3
        self._player_list = []
        self._round_state: int = 0
        self._bullet_list = []
        self._solid_round = -1
        self._round_num = 0

    def get_bullet(self):
        desc = ""
        for i in range(game._bullet_list.count(1)):
            desc += "🩸"
        for i in range(game._bullet_list.count(0)):
            desc += "💧"
        return desc
    def get_hp(self):
        ret = "1号："
        for i in range(game._player_list[0]._hp):
            ret += "⚡️"
        ret += "\n2号："
        for i in range(game._player_list[1]._hp):
            ret += "⚡️"
        return ret
    def get_item(self):
        ret = "1号："
        for i in self._player_list[0]._item:
            ret += f"【{i}】"
        ret += "\n2号："
        for i in self._player_list[1]._item:
            ret += f"【{i}】"
        return ret
               
    def new_bullet_list(self,num):
        red_num = random.randint(1,num-1)
        self._bullet_list.clear()
        for i in range(red_num):
            self._bullet_list.append(1)
        for i in range(num - red_num):
            self._bullet_list.append(0)
        random.shuffle(self._bullet_list)

    def flush_items(self,num:int):
        items = ["小刀","放大镜","香烟","啤酒","手铐"]
        for player in self._player_list:
            for i in range(num):
                if len(player._item) < 8:
                    player._item.append(random.choice(items))
                else:
                    break
            
    def shot(self,shoter:str,is_self:bool):
        shoter_index = 0
        counter_index = 0
        for index,player in enumerate(self._player_list):
            if player._id == shoter:
                shoter_index = index
            else:
                counter_index = index
        if shoter_index != self._round_state:
            return "不是你的回合"
        cur = self._bullet_list[-1]
        if is_self:
            if cur != 0:
                self._player_list[shoter_index]._hp -= cur
                self.invert_state()
            else:
                self._round_num -= 1 # 再来一次不算回合数
        else:
            self._player_list[counter_index]._hp -= cur
            self.invert_state()

        self._bullet_list.pop()
        self._round_num += 1
        return cur
    def use(self,user:str,item:str):
        for index,player in enumerate(self._player_list):
            if player._id == user:
                break
        if index != self._round_state:
            return False,"不是你的回合"
        if item in player._item:
            player._item.remove(item)
            if item == "放大镜":
                return True,self._bullet_list[-1]
            elif item == "小刀":
                if self._bullet_list[-1] != 0:
                    self._bullet_list[-1] = 2
                return True,True
            elif item == "香烟":
                if player._hp > 2 and player._hp <6:
                    player._hp += 1
                else:
                    return False,"虚弱状态无法回血"
                return True,player._hp
            elif item == "啤酒":
                return True,self._bullet_list.pop()
            elif item == "手铐":
                if self._round_num - self._solid_round >= 2:
                    self._solid_round = self._round_num
                    return True,True
                else:
                    player._item.append("手铐") # 手铐不减
                    return False,"对方还带着手铐呢"
        else:
            return False,"你没有这个道具"

game = Manager()
        