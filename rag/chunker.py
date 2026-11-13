def read_log_file():
    logs = []
    with open("../data/sample_incident.log", "r", encoding="utf-8") as file:
        for log in file:
            logs.append(log)

    return logs

print(read_log_file())