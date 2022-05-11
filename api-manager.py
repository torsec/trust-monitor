from quart import Quart, request

app = Quart(__name__)

@app.route('/add_entity', methods=['POST'])
async def route():
    """
    Body structure:
    {
        "entity_uuid": uuid,
        "att_tech": att_tech, (not mandatory)
        "name": name,
        "external_id": id,
        "type": type,
        "whitelist_uuid": wl_uuid, (not mandatory)
        "child": [                  (not mandatory)
            uuid_1, uuid_2, ...
        ],
        "parent": id,   (not mandatory)
        "metadata": {
            ...
        }
    }
    """

    body = await request.get_json()
    
    """
    Validation
    """
    if "entity_uuid" not in body:
        return "error"
    if "name" not in body:
        return "error"
    if "external_id" not in body:
        return "error"
    if "type" not in body:
        return "error"
    if "metadata" not in body:
        return "error"

    return "success"

if __name__ == "__main__":
    app.run()