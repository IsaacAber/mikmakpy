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
    assert all(
        s["name"] in {e.value for e in Server} for s in servers
    ), "Server names do not match expected enum values"


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
    msg = r"""{"b":{"r":-1,"o":{"level":1,"_cmd":"achivment_res","list":"[{'ach':1,'ass':1,'p':0,'prg':100},{'ach':1,'ass':2,'p':0,'prg':100},{'ach':1,'ass':3,'p':0,'prg':100},{'ach':1,'ass':5,'p':0,'prg':100},{'ach':1,'ass':8,'p':0,'prg':100},{'ach':1,'ass':9,'p':0,'prg':100},{'ach':1,'ass':16,'p':0,'prg':100},{'ach':1,'ass':17,'p':0,'prg':100},{'ach':2,'ass':1,'p':0,'prg':1},{'ach':6,'ass':1,'p':0,'prg':2},{'ach':10,'ass':1,'p':0,'prg':13},{'ach':15,'ass':1,'p':0,'prg':9},{'ach':16,'ass':1,'p':10,'prg':100},{'ach':26,'ass':1,'p':0,'prg':16},{'ach':30,'ass':1,'p':10,'prg':100},{'ach':32,'ass':1,'p':10,'prg':100},{'ach':33,'ass':1,'p':10,'prg':100},{'ach':38,'ass':1,'p':0,'prg':16},{'ach':97,'ass':1,'p':0,'prg':16},{'ach':106,'ass':1,'p':0,'prg':16},{'ach':213,'ass':1,'p':0,'prg':16},{'ach':235,'ass':1,'p':0,'prg':1},{'ach':236,'ass':1,'p':0,'prg':1},{'ach':237,'ass':1,'p':0,'prg':1},{'ach':299,'ass':1,'p':0,'prg':16},{'ach':313,'ass':1,'p':20,'prg':100},{'ach':314,'ass':1,'p':50,'prg':100},{'ach':361,'ass':1,'p':0,'prg':393150},{'ach':374,'ass':1,'p':0,'prg':16},{'ach':379,'ass':1,'p':0,'prg':100},{'ach':379,'ass':4,'p':0,'prg':100},{'ach':406,'ass':1,'p':10,'prg':100},{'ach':496,'ass':1,'p':0,'prg':16},{'ach':497,'ass':1,'p':0,'prg':16},{'ach':498,'ass':1,'p':0,'prg':393150},{'ach':501,'ass':1,'p':0,'prg':100},{'ach':505,'ass':1,'p':20,'prg':100},{'ach':3054,'ass':1,'p':20,'prg':100},{'ach':3312,'ass':1,'p':0,'prg':1}]","userId":16340305,"points":160}},"t":"xt"}"""
    res = parse.achievement_res(msg)
    assert res.ok, f"Error parsing achievement response A: {res.error}"

    res = res.value
    assert res["user_id"] == 16340305
    assert res["level"] == 1
    assert res["points_total"] == 160
    assert res["is_update"] is False
    assert isinstance(res["achievements"], list)
    assert len(res["achievements"]) > 0

    # Spot-check a few entries
    res = {a["key"]: a for a in res["achievements"]}
    assert res["1:1"]["progress"] == 100
    assert res["16:1"]["points"] == 10
    assert res["361:1"]["progress"] == 393150

    msg = r"""{"b":{"r":-1,"o":{"level":1,"_cmd":"achivment_res","update":"true","list":"[{'ach':15,'ass':1,'p':0,'prg':10},{'ach':26,'ass':1,'p':0,'prg':18},{'ach':38,'ass':1,'p':0,'prg':18},{'ach':97,'ass':1,'p':0,'prg':18},{'ach':106,'ass':1,'p':0,'prg':18},{'ach':213,'ass':1,'p':0,'prg':18},{'ach':299,'ass':1,'p':0,'prg':18},{'ach':374,'ass':1,'p':0,'prg':18},{'ach':496,'ass':1,'p':0,'prg':18},{'ach':497,'ass':1,'p':0,'prg':18}]","userId":16340305,"points":160}},"t":"xt"}"""
    res = parse.achievement_res(msg)
    assert res.ok, f"Error parsing achievement response B: {res.error}"

    res = res.value
    assert res["is_update"] is True
    res = {a["key"]: a for a in res["achievements"]}
    assert res["15:1"]["progress"] == 10
    assert res["26:1"]["progress"] == 18


def test_parse_join_ok():
    msg = r"""<msg t='sys'><body action='joinOK' r='12'><pid id='0'/><vars /><uLs r='12'><u i='92948' m='0'><n><![CDATA[סינוןפח]]></n><vars><var n='d' t='n'><![CDATA[3]]></var><var n='e' t='s'><![CDATA[201,0,14389,0,5983,0,45120,33090,0,0,0,0,0,0]]></var><var n='i' t='n'><![CDATA[16359409]]></var><var n='m' t='n'><![CDATA[0]]></var></vars></u></uLs></body></msg>"""

    res = parse.join_ok(msg)
    assert res.ok, f"Error parsing joinOK message: {res.error}"
    assert res.value["room_id"] == 12
    assert res.value["users"][0]["session_id"] == 92948
    assert res.value["users"][0]["username"] == "סינוןפח"
    assert res.value["users"][0]["age"] == 3
    assert isinstance(res.value["users"][0]["equipment"], list)
    assert res.value["users"][0]["equipment"] == [
        201,
        0,
        14389,
        0,
        5983,
        0,
        45120,
        33090,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    assert res.value["users"][0]["user_id"] == 16359409
    assert res.value["users"][0]["rank"] == 0
    assert (
        len(res.value["room_vars"]) == 0
    ), f"Expected no room vars, got: {res.value['room_vars']}"


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
    assert res.value["age"] == 865
    assert res.value["rank"] == 11
    assert res.value["user_id"] == 15586722
    assert res.value["equipment"] == [
        205,
        21152,
        1244,
        0,
        2493,
        0,
        0,
        0,
        0,
        0,
        6367,
        0,
        0,
        43022,
    ]
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


def test_parse_inv_list():
    msg = """{"b": {"r": -1,"o": {"_cmd": "inv_list","enc": "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"}},"t": "xt"}"""
    res = parse.inv_list(msg)
    assert res.ok, f"Error parsing inv_list: {res.error}"
    assert isinstance(res.value, list)
    assert res.value[0] == "7399"
    assert len(res.value) == 3247

    msg = (
        """{"b":{"r":-1,"o":{"_cmd":"inv_list","list":"9399-75,7142,205"}},"t":"xt"}"""
    )
    res = parse.inv_list(msg)
    assert res.ok, f"Error parsing inv_list: {res.error}"
    assert res.value == ["9399-75", "7142", "205"]


def test_parse_avt_get_res():
    msg = """{"b": {"r": -1,"o": {"a": 4643,"e": "205,0,14223,0,2310,0,45061,3911,0,8153,0,0,0,43013","_cmd": "avt_get_res","g": 29,"id": 4748175,"l": 11,"n": "79מיסי"}},"t": "xt"}"""
    res = parse.avt_get_res(msg)
    assert res.ok, f"Error parsing avt_get_res: {res.error}"
    res = res.value
    assert res["user_id"] == 4748175
    assert res["username"] == "79מיסי"
    assert res["age"] == 4643
    assert res["rank"] == 11
    assert res["equipment"] == "205,0,14223,0,2310,0,45061,3911,0,8153,0,0,0,43013"
    assert res["gallery_creation_count"] == 29
    assert res["gallery_followers_count"] == None
    assert isinstance(res["unparsed"], dict)


def test_parse_r_vars_update():
    # Countdown inside a magic..
    msg = """<msg t='sys'><body action='rVarsUpdate' r='1335'><vars><var n='CM' t='s'><![CDATA[13]]></var></vars></body></msg>"""
    res = parse.r_vars_update(msg)
    assert res.ok, f"Error parsing rVarsUpdate: {res.error}"
    res = res.value
    assert res["room_id"] == 1335
    assert res["room_vars"]["CM"] == "13"


# def test_parse_m_ui():
#     # the enc variant I'll keep for another day.. assume it's working! TODO: rework the m_ui and then finish the test for it
#     msg = """{"b":{"r":-1,"o":{"s":"[{\"i\":10,\"d\":\"במשחק\"},{\"i\":11,\"d\":\"החלפות?\"},{\"i\":12,\"d\":\"עושה שיעורים\"},{\"i\":13,\"d\":\"הלכתי לאכול במיקפה\"},{\"i\":15,\"d\":\"רוצים לשחק?\"},{\"i\":23,\"d\":\"מי רוצה לדבר?\"},{\"i\":25,\"d\":\"בהפסקה\"},{\"i\":31,\"d\":\"אפשר מתנה?\"},{\"i\":32,\"d\":\"קונה בקטלוג\"},{\"i\":34,\"d\":\"בלובי משחקים\"},{\"i\":36,\"d\":\"במשימה החדשה\"},{\"i\":37,\"d\":\"בשיחה במיקטוק\"},{\"i\":38,\"d\":\"בהופעה במיקפה\"},{\"i\":39,\"d\":\"בחלוקת מתנות\"},{\"i\":40,\"d\":\"ראיתי מנהל מחובר!\"},{\"i\":41,\"d\":\"לוק חדש למיקמק שלי\"},{\"i\":42,\"d\":\"יצירה חדשה בקהילה שלי!\"},{\"i\":43,\"d\":\"חג שמח!\"}]","_cmd":"m_ui","sl":"1-0-0,50-5-0,3-3-0,4-0-0,20-1-0,21-1-0,22-1-0,7-0-1,23-1-0,8-2-0,24-1-0,10-0-0","m":"@fr,אינדגים333,204;22107;1466;1512;0;0;0;0@"}},"t":"xt"}"""
