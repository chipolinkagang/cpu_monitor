import datetime


def fill_space(data_list: list[dict]) -> list[dict]:
    """
    :param data_list: points list,
    :return: full points list (720 pcs).
    """
    if len(data_list) == 0:
        return []

    interval = 5  # Interval of CPU calculating is 5 seconds
    end_date = datetime.datetime.now()
    start_date = datetime.timedelta(hours=1)
    last_date = end_date - start_date

    if (last_date + datetime.timedelta(seconds=3) > data_list[0]["time"]) and (
            last_date - datetime.timedelta(seconds=3) < data_list[0]["time"]):
        last_date = data_list[0]["time"]

    if len(data_list) < 720:
        for index, data in enumerate(data_list):
            if index == (len(data_list)-1):
                break
            delta = abs(data["time"] - data_list[(index+1)]["time"])
            if delta.seconds > interval:
                data_list.insert(index + 1, {"time": data["time"] + datetime.timedelta(seconds=interval), "value": None})

    index = 0
    while last_date + datetime.timedelta(seconds=7) < data_list[index]["time"]:
        data_list.insert(index, {"time": data_list[index]["time"] - datetime.timedelta(seconds=interval), "value": None})

    for data in data_list:
        data["time"] = data["time"].strftime('%Y-%m-%d %H:%M:%S')

    return data_list


def get_average_values(data_list: list[dict]) -> list[dict]:
    """
    :param data_list: data_list: points list,
    :return: avg points list (1 CPU calculating to 1 min)
    """
    new_data = []
    all_data = 60*60/5
    amount = 60  # AVG 1 CPU calculating to 1 min
    for i in range(int(all_data/amount)):
        count = 0
        value = 0
        for j in range(amount):
            if data_list[i * amount + j]["value"] is not None:
                count += 1
                value += data_list[i * amount + j]["value"]
        if count == 0:
            value = None
        new_data.append({"time": data_list[i]["time"], "value": value})
    return new_data

