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

def test_parse_join_ok():
    msg = r"""<msg t='sys'><body action='joinOK' r='12'><pid id='0'/><vars /><uLs r='12'><u i='92948' m='0'><n><![CDATA[סינוןפח]]></n><vars><var n='d' t='n'><![CDATA[3]]></var><var n='e' t='s'><![CDATA[201,0,14389,0,5983,0,45120,33090,0,0,0,0,0,0]]></var><var n='i' t='n'><![CDATA[16359409]]></var><var n='m' t='n'><![CDATA[0]]></var></vars></u></uLs></body></msg>"""

    res = parse.join_ok(msg)
    assert res.ok, f"Error parsing joinOK message: {res.error}"
    assert res.value["room_id"] == 12
    assert res.value["users"][0]["session_id"] == 92948
    assert res.value["users"][0]["username"] == "סינוןפח"
    assert res.value["users"][0]["days_old"] == 3
    assert isinstance(res.value["users"][0]["equipment"], list)
    assert res.value["users"][0]["equipment"] == [201, 0, 14389, 0, 5983, 0, 45120, 33090, 0, 0, 0, 0, 0, 0]
    assert res.value["users"][0]["user_id"] == 16359409
    assert res.value["users"][0]["rank"] == 0
    assert len(res.value["room_vars"]) == 0, f"Expected no room vars, got: {res.value['room_vars']}"

def test_parse_join_ok_with_room_vars():
    msg = r"""<msg t='sys'><body action='joinOK' r='4'><pid id='0'/><vars><var n='YprT' t='s'><![CDATA[מחר כולם יהיו מלאכים ב -]]></var><var n='YprVotes2' t='s'><![CDATA[6]]></var><var n='YprVotes1' t='s'><![CDATA[5]]></var><var n='YprOpt1' t='s'><![CDATA[במיקפה]]></var><var n='YprOpt2' t='s'><![CDATA[פארק הוותיק]]></var></vars><uLs r='4'><u i='92948' m='0'><n><![CDATA[סינוןפח]]></n><vars><var n='d' t='n'><![CDATA[3]]></var><var n='e' t='s'><![CDATA[201,0,14389,0,5983,0,45120,33090,0,0,0,0,0,0]]></var><var n='i' t='n'><![CDATA[16359409]]></var><var n='m' t='n'><![CDATA[0]]></var></vars></u></uLs></body></msg>"""

    res = parse.join_ok(msg)
    assert res.ok, f"Error parsing joinOK message: {res.error}"
    assert res.value["room_id"] == 4
    assert res.value["room_vars"]["YprT"] == "מחר כולם יהיו מלאכים ב -"
    assert res.value["room_vars"]["YprVotes2"] == "6"
    assert res.value["room_vars"]["YprVotes1"] == "5"
    assert res.value["room_vars"]["YprOpt1"] == "במיקפה"
    assert res.value["room_vars"]["YprOpt2"] == "פארק הוותיק"
    assert len(res.value["users"]) == 1

def test_parse_u_vars_update():
    msg = r"""<msg t='sys'><body action='uVarsUpdate' r='12'><vars><var n='x' t='s'><![CDATA[910,529]]></var></vars><user id='92557' /></body></msg>"""

    res = parse.u_vars_update(msg)
    assert res.ok, f"Error parsing uVarsUpdate message: {res.error}"
    assert res.value["session_id"] == 92557
    assert res.value["updated"]["position"] == (910, 529)
    assert res.value["unparsed"] == {}

def test_parse_u_enter_room():
    msg = r"""<msg t='sys'><body action='uER' r='12'><u i ='92968' m='0'><n><![CDATA[עדן3C]]></n><vars><var n='d' t='n'><![CDATA[865]]></var><var n='t' t='n'><![CDATA[17]]></var><var n='e' t='s'><![CDATA[205,21152,1244,0,2493,0,0,0,0,0,6367,0,0,43022]]></var><var n='g' t='n'><![CDATA[1]]></var><var n='i' t='n'><![CDATA[15586722]]></var><var n='l' t='n'><![CDATA[11]]></var><var n='m' t='n'><![CDATA[111]]></var></vars></u></body></msg>"""

    res = parse.u_enter_room(msg)
    assert res.ok, f"Error parsing uER message: {res.error}"
    assert res.value["session_id"] == 92968
    assert res.value["username"] == "עדן3C"
    assert res.value["days_old"] == 865
    assert res.value["rank"] == 11
    assert res.value["user_id"] == 15586722
    assert res.value["equipment"] == [205, 21152, 1244, 0, 2493, 0, 0, 0, 0, 0, 6367, 0, 0, 43022]
    assert "t" in res.value["unparsed"]
    assert "g" in res.value["unparsed"]
    assert "m" in res.value["unparsed"]

def test_parse_user_gone():
    msg = r"""<msg t='sys'><body action='userGone' r='12'><user id='92963' /></body></msg>"""

    res = parse.user_gone(msg)
    assert res.ok, f"Error parsing userGone message: {res.error}"
    assert res.value["session_id"] == 92963

def test_parse_dmn_msg():
    msg = """<msg t='sys'>\n    <body action='dmnMsg' r='0'>\n        <user id='108431' />\n        <txt><![CDATA[invalid_action]]></txt>\n    </body>\n</msg>"""
    res = parse.dmn_msg(msg)
    assert res.ok, f"Error parsing dmnMsg: {res.error}"
    assert res.value["session_id"] == 108431
    assert res.value["text"] == "invalid_action"