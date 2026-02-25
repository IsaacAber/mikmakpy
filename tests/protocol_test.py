from mikmakpy.protocol import parse
from mikmakpy.constants import Server

def test_parse_server_list():
    msg = r"""{"b":{"r":-1,"o":{"safeChat":false,"_cmd":"server_list","rank":1,"userName":"בוט11011","list":"[{\"id\":4,\"name\":'קיווי',\"ip\":'213.8.147.198',\"port\":443,\"capicity\":0.2,\"dt\":202602231555},{\"id\":7,\"name\":'קרמבו ',\"ip\":'213.8.147.201',\"port\":443,\"capicity\":0.0,\"safe\":true,\"dt\":202602231555},{\"id\":10,\"name\":'מנהלים',\"ip\":'213.8.147.214',\"port\":443,\"capicity\":-1.0,\"dt\":202602231555}]"}},"t":"xt"}"""

    res = parse.server_list(msg)
    assert res.ok, f"Error parsing server list: {res.error}"

    payload = res.value
    assert payload["safeChat"] is False
    assert payload["rank"] == 1
    assert payload["userName"] == "בוט11011"

    servers = payload["servers"]
    assert len(servers) == 3, f"Expected 3 servers, got {len(servers)}"
    assert all(s["name"] in {e.value for e in Server} for s in servers), "Server names do not match expected enum values"

def test_parse_room_list():
    msg = r"""<msg t='sys'><body action='rmList' r='0'><rmList><rm id='1' priv='0' temp='0' game='0' ucnt='1' lmb='1' maxu='10000' maxs='0'><n><![CDATA[game_lobby]]></n></rm><rm id='2' priv='0' temp='0' game='0' ucnt='0' lmb='1' maxu='100000' maxs='0'><n><![CDATA[lobby]]></n></rm><rm id='3' priv='0' temp='0' game='0' ucnt='0' maxu='50' maxs='0'><n><![CDATA[beach]]></n></rm></rmList></body></msg>"""
    res = parse.room_list(msg, clean=False)
    assert res.ok, f"Error parsing room list: {res.error}"
    assert isinstance(res.value, list)
    assert res.value[0]["id"] == 1
    assert res.value[0]["name"] == "game_lobby"
    assert res.value[0]["usercount"] == 1
    assert res.value[0]["maxusercount"] == 10000
    
def test_parse_inv_list():
    msg = r"""{"b":{"r":-1,"o":{"_cmd":"inv_list","list":"3501,1895,45020,4382,7426,7210,8178,3461-2,5524-2,14028-2,8184,2514,205"}},"t":"xt"}"""

    res = parse.inv_list(msg)
    assert res.ok, f"Error parsing inventory list: {res.error}"

    assert res.value == [
        {"item_id": 3501, "quantity": 1},
        {"item_id": 1895, "quantity": 1},
        {"item_id": 45020, "quantity": 1},
        {"item_id": 4382, "quantity": 1},
        {"item_id": 7426, "quantity": 1},
        {"item_id": 7210, "quantity": 1},
        {"item_id": 8178, "quantity": 1},
        {"item_id": 3461, "quantity": 2},
        {"item_id": 5524, "quantity": 2},
        {"item_id": 14028, "quantity": 2},
        {"item_id": 8184, "quantity": 1},
        {"item_id": 2514, "quantity": 1},
        {"item_id": 205, "quantity": 1},
    ], f"Unexpected inventory list: {res.value}"

def test_parse_login_res():
    msg = r"""{"b":{"r":-1,"o":{"date":"20260225","c":393150,"_cmd":"login_res","time":"225903","k":200311,"resoulationCtg":33,"resoulationVal":"beach"}},"t":"xt"}"""

    res = parse.login_res(msg)
    assert res.ok, f"Error parsing login response: {res.error}"

    payload = res.value
    assert payload["date"] == "20260225"
    assert payload["c"] == 393150
    assert payload["time"] == "225903"
    assert payload["k"] == 200311
    assert payload["resoulationCtg"] == 33
    assert payload["resoulationVal"] == "beach"

def test_parse_achievement_res():
    msgA = r"""{"b":{"r":-1,"o":{"level":1,"_cmd":"achivment_res","list":"[{'ach':1,'ass':1,'p':0,'prg':100},{'ach':1,'ass':2,'p':0,'prg':100},{'ach':1,'ass':3,'p':0,'prg':100},{'ach':1,'ass':5,'p':0,'prg':100},{'ach':1,'ass':8,'p':0,'prg':100},{'ach':1,'ass':9,'p':0,'prg':100},{'ach':1,'ass':16,'p':0,'prg':100},{'ach':1,'ass':17,'p':0,'prg':100},{'ach':2,'ass':1,'p':0,'prg':1},{'ach':6,'ass':1,'p':0,'prg':2},{'ach':10,'ass':1,'p':0,'prg':13},{'ach':15,'ass':1,'p':0,'prg':9},{'ach':16,'ass':1,'p':10,'prg':100},{'ach':26,'ass':1,'p':0,'prg':16},{'ach':30,'ass':1,'p':10,'prg':100},{'ach':32,'ass':1,'p':10,'prg':100},{'ach':33,'ass':1,'p':10,'prg':100},{'ach':38,'ass':1,'p':0,'prg':16},{'ach':97,'ass':1,'p':0,'prg':16},{'ach':106,'ass':1,'p':0,'prg':16},{'ach':213,'ass':1,'p':0,'prg':16},{'ach':235,'ass':1,'p':0,'prg':1},{'ach':236,'ass':1,'p':0,'prg':1},{'ach':237,'ass':1,'p':0,'prg':1},{'ach':299,'ass':1,'p':0,'prg':16},{'ach':313,'ass':1,'p':20,'prg':100},{'ach':314,'ass':1,'p':50,'prg':100},{'ach':361,'ass':1,'p':0,'prg':393150},{'ach':374,'ass':1,'p':0,'prg':16},{'ach':379,'ass':1,'p':0,'prg':100},{'ach':379,'ass':4,'p':0,'prg':100},{'ach':406,'ass':1,'p':10,'prg':100},{'ach':496,'ass':1,'p':0,'prg':16},{'ach':497,'ass':1,'p':0,'prg':16},{'ach':498,'ass':1,'p':0,'prg':393150},{'ach':501,'ass':1,'p':0,'prg':100},{'ach':505,'ass':1,'p':20,'prg':100},{'ach':3054,'ass':1,'p':20,'prg':100},{'ach':3312,'ass':1,'p':0,'prg':1}]","userId":16340305,"points":160}},"t":"xt"}"""
    msgB = r"""{"b":{"r":-1,"o":{"level":1,"_cmd":"achivment_res","update":"true","list":"[{'ach':15,'ass':1,'p':0,'prg':10},{'ach':26,'ass':1,'p':0,'prg':18},{'ach':38,'ass':1,'p':0,'prg':18},{'ach':97,'ass':1,'p':0,'prg':18},{'ach':106,'ass':1,'p':0,'prg':18},{'ach':213,'ass':1,'p':0,'prg':18},{'ach':299,'ass':1,'p':0,'prg':18},{'ach':374,'ass':1,'p':0,'prg':18},{'ach':496,'ass':1,'p':0,'prg':18},{'ach':497,'ass':1,'p':0,'prg':18}]","userId":16340305,"points":160}},"t":"xt"}"""

    resA = parse.achievement_res(msgA)
    assert resA.ok, f"Error parsing achievement response A: {resA.error}"

    dataA = resA.value
    assert dataA["user_id"] == 16340305
    assert dataA["level"] == 1
    assert dataA["points_total"] == 160
    assert dataA["is_update"] is False
    assert isinstance(dataA["achievements"], list)
    assert len(dataA["achievements"]) > 0

    # Spot-check a few entries
    by_keyA = {a["key"]: a for a in dataA["achievements"]}
    assert by_keyA["1:1"]["progress"] == 100
    assert by_keyA["16:1"]["points"] == 10
    assert by_keyA["361:1"]["progress"] == 393150

    resB = parse.achievement_res(msgB)
    assert resB.ok, f"Error parsing achievement response B: {resB.error}"

    dataB = resB.value
    assert dataB["is_update"] is True
    by_keyB = {a["key"]: a for a in dataB["achievements"]}
    assert by_keyB["15:1"]["progress"] == 10
    assert by_keyB["26:1"]["progress"] == 18

    # Update list should be shorter than full snapshot
    assert len(dataB["achievements"]) < len(dataA["achievements"])