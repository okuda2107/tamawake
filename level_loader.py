from __future__ import annotations

import json
from typing import Any

from actor import *
from game import *
from playground import *
from point_manager import *
from result import *
from sprite_component import *
from title import *

LEVEL_VERSION = 1

# actor生成系関数のマップ
# actor_factory_map = {
#     'Actor': actor.create<Actor>
#     }

# component生成系関数のマップ
component_factory_map = {
    "Component": TypeID.t_component,
    "SpriteComponent": TypeID.t_sprite_component,
}


def load_level(game: Game, file_name: str) -> bool:
    with open(file_name, "r") as file_data:
        doc: dict[str, Any] = json.load(file_data)
    version: int = doc["version"]
    if version != LEVEL_VERSION:
        print("レベルファイルのバージョンが違います")
        return False
    # load_global_properties(game, doc['globalProperties'])
    load_actors(game, doc["actors"])
    return True


def load_global_properties(game: Game, obj: dict[str, Any]) -> None:
    pass


# 特別実装 画面サイズの値を外部からいじるために必要
def load_game_properties(game: Game, file_name: str) -> bool:
    with open(file_name, "r") as file_data:
        doc: dict[str, Any] = json.load(file_data)
    version: int = doc["version"]
    if version != LEVEL_VERSION:
        print("レベルファイルのバージョンが違います")
        return False
    data = doc.get("properties")
    if data != None:
        screen_size_data = data.get("screenSize")
        if screen_size_data != None:
            game.screen_size = np.array(screen_size_data)
        check_flag = data.get("cameraCheck")
        if check_flag != None:
            game.camera_check_mode = check_flag


def load_actors(game: Game, arr: list[dict[str, Any]]) -> None:
    for obj in arr:
        type_name: str = obj["type"]
        # 名前と対応する生成系関数を呼び出す
        # actor_factory = actor_factory_map[type_name]
        # actor = actor_factory(game, obj)
        actor = eval(type_name)(game)
        actor.load_properties(obj["properties"])
        comp_data = obj.get("components")
        if comp_data != None:
            load_components(actor, comp_data)


def load_components(actor: Actor, arr: list[dict[str, Any]]) -> None:
    for obj in arr:
        type_name: str = obj["type"]
        type_id = component_factory_map.get(type_name)
        if type_id != None:
            comp = actor.get_component_of_type(type_id)
            if comp == None:
                comp = eval(type_name)(actor)
                comp.load_properties(obj["properties"])
            else:
                comp.load_properties(obj["properties"])
        else:
            print("未知のコンポーネント型 : ", type_name)
