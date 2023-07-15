import json, csv

with open("project-227-data-set.txt", "r") as f:
    data = json.loads(f.read())
    field_names = ["throttle", "brake", "hand_brake", "steer"]
    csvfilestore = open("project-227.csv", "w", newline="")
    writer = csv.DictWriter(csvfilestore, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)
