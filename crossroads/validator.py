"""
Validate json payload before request
"""

VALID_POSITION_FLAG = {
    "front": False,
    "right": False,
    "left": False,
    "bottom": False,
    "top": False
}

def validate_regist_payload(payload):
    """
    Validate payload based on template.
    :param payload: dictionary that will be dumped to json and sent as payload
    :return: Raises error if invalid
    """
    data = payload["data"]

    for key in VALID_POSITION_FLAG:
        VALID_POSITION_FLAG[key] = False

    # Check json keys
    for photos in data:
        position = photos["position"]
        # Check for duplicate direction
        if VALID_POSITION_FLAG[position]:
            err_msg = "Invalid Payload Flag"
            raise Exception(err_msg)

        VALID_POSITION_FLAG[position] = True
        image = photos["image"]
        if not isinstance(image, str):
            err_msg = "Invalid Image Type"
            raise Exception(err_msg)

    # Check if there's missing images
    for value in VALID_POSITION_FLAG.values():
        if not value:
            err_msg = "Missing Payload Flag"
            raise Exception(err_msg)
