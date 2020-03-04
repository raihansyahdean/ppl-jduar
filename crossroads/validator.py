"""
Validate json payload before request
"""

IMAGE_TEMPLATE = "<image>"

PAYLOAD_TEMPLATE = {
    "data": [
        {
            "position": "front",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "right",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "left",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "bottom",
            "image": IMAGE_TEMPLATE
        },
        {
            "position": "top",
            "image": IMAGE_TEMPLATE
        }
    ]
}


def payload_isvalid(payload):
    """
    Validate payload based on template.
    :param payload: dictionary that will be dumped to json and sent as payload
    :return: True if valid. False otherwise
    """
    valid_position_flag = {
        "front": False,
        "right": False,
        "left": False,
        "bottom": False,
        "top": False}
    try:
        data = payload["data"]

        # Check json keys
        for photos in data:
            position = photos["position"]
            # Check for duplicate direction
            if valid_position_flag[position]:
                print("invalid flag")
                return False
            valid_position_flag[position] = True
            image = photos["image"]
            print(type(image))
            if not isinstance(image, str):
                print("invalid type")
                return False

        # Check if there's missing images
        for value in valid_position_flag.values():
            if not value:
                print("Missing direction")
                return False

        return True

    except KeyError:
        return False
