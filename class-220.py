import glob
import os
import sys
import time
import random
import math

try:
    sys.path.append(
        glob.glob(
            "../carla/dist/carla-*%d.%d-%s.egg"
            % (
                sys.version_info.major,
                sys.version_info.minor,
                "win-amd64" if os.name == "nt" else "linux-x86_64",
            )
        )[0]
    )
except IndexError:
    pass

import carla

actor_list = []


def generate_lidar_blueprint(blueprint_library):
    lidar_blueprint = blueprint_library.find("sensor.lidar.ray_cast_semantic")
    lidar_blueprint.set_attribute("channels", str(64))
    lidar_blueprint.set_attribute("points_per_second", str(56000))
    lidar_blueprint.set_attribute("rotation_frequency", str(40))
    lidar_blueprint.set_attribute("range", str(100))
    return lidar_blueprint


object_id = {
    0: "None",
    1: "Buildings",
    2: "Fences",
    3: "Other",
    4: "Pedestrians",
    5: "Poles",
    6: "RoadLines",
    7: "Roads",
    8: "Sidewalks",
    9: "Vegetation",
    10: "Vehicles",
    11: "Wall",
    12: "TrafficsSigns",
    13: "Sky",
    14: "Ground",
    15: "Bridge",
    16: "RailTrack",
    17: "GuardRail",
    18: "TrafficLight",
    19: "Static",
    20: "Dynamic",
    21: "Water",
    22: "Terrain",
}


def semantic_lidar_data1(point_cloud_data):
    distance_name_data = {}
    for detection in point_cloud_data:
        distance_name_data["distance"] = math.sqrt(
            (detection.point.x**2)
            + (detection.point.y**2)
            + (detection.point.z**2)
        )
        distance_name_data["name"] = object_id[detection.object_tag]
        if (
            distance_name_data["name"] == "Pedestrians"
            and distance_name_data["distance"] > 1
            and distance_name_data["distance"] < 8
        ):
            dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
            dropped_vehicle.set_light_state(
                carla.VehicleLightState(
                    carla.VehicleLightState.Brake
                    | carla.VehicleLightState.LeftBlinker
                    | carla.VehicleLightState.LowBeam
                )
            )
            dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.3, steer=0.2))
            time.sleep(1)
            dropped_vehicle.apply_control(
                carla.VehicleControl(throttle=0.3, steer=-0.2)
            )
            time.sleep(1)
            car_control()
        else:
            continue


def car_control():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.61))

    time.sleep(20)


try:
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    map = world.get_map()
    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter("model3")[0]
    spawn_point = world.get_map().get_spawn_points()[20]
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    walkers_blueprint = random.choice(get_blueprint_of_world.filter("walker"))
    walkers_spawn_point = world.get_map().get_spawn_points()[17]
    dropped_walker = world.spawn_actor(walkers_blueprint, walkers_spawn_point)
    control_walker = carla.WalkerControl()
    control_walker.speed = 0.8
    control_walker.direction.y = 0
    control_walker.direction.x = 1
    control_walker.direction.z = 0
    # dropped_walker.apply_control(control_walker)

    simulator_camera_location_rotation = carla.Transform(
        spawn_point.location, spawn_point.rotation
    )
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 60
    simulator_camera_location_rotation.location += spawn_point.get_up_vector() * -5
    simulator_camera_location_rotation.location += spawn_point.get_right_vector() * -1
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    lidar_sensor = generate_lidar_blueprint(get_blueprint_of_world)
    sensor_lidar_spawn_point = carla.Transform(
        carla.Location(x=0, y=0, z=2.0),
        carla.Rotation(pitch=0.000000, yaw=90.0, roll=0.000000),
    )
    sensor = world.spawn_actor(
        lidar_sensor, sensor_lidar_spawn_point, attach_to=dropped_vehicle
    )

    sensor.listen(lambda data2: semantic_lidar_data1(data2))
    car_control()
    actor_list.append(sensor)
    actor_list.append(dropped_walker)

    time.sleep(1000)
finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
    print("done.")
