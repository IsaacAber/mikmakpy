from mikmakpy.protocol import parse
from mikmakpy.constants import Server

def test_parse_server_list():
    msg = r"""{"b":{"r":-1,"o":{"safeChat":false,"_cmd":"server_list","rank":1,"userName":"בוט11011","list":"[{\"id\":4,\"name\":'קיווי',\"ip\":'213.8.147.198',\"port\":443,\"capicity\":0.2,\"dt\":202602231555},{\"id\":7,\"name\":'קרמבו ',\"ip\":'213.8.147.201',\"port\":443,\"capicity\":0.0,\"safe\":true,\"dt\":202602231555},{\"id\":10,\"name\":'מנהלים',\"ip\":'213.8.147.214',\"port\":443,\"capicity\":-1.0,\"dt\":202602231555}]"}},"t":"xt"}"""
    servers = parse.server_list(msg)
    assert servers.ok, f"Error parsing server list: {servers.error}"
    servers = servers.value
    assert len(servers) == 3, f"Expected 3 servers, got {len(servers)}"
    assert all(s["name"] in {e.value for e in Server} for s in servers), "Server names do not match expected enum values"

