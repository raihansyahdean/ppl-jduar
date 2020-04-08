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

VALID_FRUIT_TYPE = [
    "Apple",
    "Apricot",
    "Avocado",
    "Banana",
    "Cherry",
    "Dragon_Fruit",
    "Durian",
    "Grapes",
    "Kiwi",
    "Lemon",
    "Lychee"
    "Mango",
    "Mangosteen",
    "Orange",
    "Papaya",
    "Peach",
    "Pear",
    "Pineapple",
    "Pomegranate",
    "Pumpkin",
    "Rambutan",
    "Rose_Apple",
    "Star_Fruit",
    "Strawberry",
    "Watermelon"
]


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


def validate_regist_passcode_payload(payload):
    """
    Validate passcode payload received from FE
    :param payload: Chosen passcode by user from FE
    :return:
    """
    try:
        chosen_passcode = payload['chosen_passcode']

        if chosen_passcode not in VALID_FRUIT_TYPE:
            err_msg = "Invalid Fruit Type"
            raise Exception(err_msg)
    except KeyError:
        err_msg = "Invalid JSON Key"
        raise Exception(err_msg)
