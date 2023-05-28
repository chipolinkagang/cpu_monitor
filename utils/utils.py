import datetime


def fill_space(data_list: list[dict], all_data: int, interval: int) -> list[dict]:
    if len(data_list) == 0:
        return []

    end_date = datetime.datetime.now()
    start_date = datetime.timedelta(hours=1)
    last_date = end_date - start_date

    if (last_date + datetime.timedelta(seconds=3) > data_list[0]["time"]) and (
            last_date - datetime.timedelta(seconds=3) < data_list[0]["time"]):
        last_date = data_list[0]["time"]

    if len(data_list) < all_data:
        for index, point in enumerate(data_list):
            if index == (len(data_list)-1):
                break
            cur_time = point["time"]
            next_time = data_list[(index+1)]["time"]
            delta = abs(point["time"] - data_list[(index+1)]["time"])
            if delta.seconds > interval:
                data_list.insert(index + 1, {"time": point["time"] + datetime.timedelta(seconds=interval), "value": None})

    index = 0
    while last_date + datetime.timedelta(seconds=7) < data_list[index]["time"]:
        data_list.insert(index, {"time": data_list[index]["time"] - datetime.timedelta(seconds=interval), "value": None})

    for data in data_list:
        data["time"] = data["time"].strftime('%Y-%m-%d %H:%M:%S')

    return data_list


def get_average_values(data_list: list[dict], all_data: int, amount: int) -> list[dict]:
    new_data = []
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

