import glob
import os
import sys
import time
import pickle


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


def generate_radar_blueprint(blueprint_library):
    radarBlueprint = blueprint_library.filter("sensor.other.radar")[0]
    radarBlueprint.set_attribute("horizontal_fov", str(10))
    radarBlueprint.set_attribute("vertical_fov", str(10))
    radarBlueprint.set_attribute("points_per_second", str(15000))
    radarBlueprint.set_attribute("range", str(10))
    return radarBlueprint


try:
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter("model3")[0]
    spawn_point = world.get_map().get_spawn_points()[6]
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    mustangCarBlueprint = get_blueprint_of_world.filter("mustang")[0]
    mustangSpawn = world.get_map().get_spawn_points()[4]
    mustang_car = world.spawn_actor(mustangCarBlueprint, mustangSpawn)
    mustang_car.apply_control(carla.VehicleControl(throttle=0.5))

    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5))

    simulator_camera_location_rotation = carla.Transform(
        spawn_point.location, spawn_point.rotation
    )
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    radar_sensor = generate_radar_blueprint(get_blueprint_of_world)
    sensor_radar_spawn_point = carla.Transform(carla.Location(x=-1.5, z=1.8))
    radar_sensor_data = world.spawn_actor(
        radar_sensor, sensor_radar_spawn_point, attach_to=dropped_vehicle
    )

    radar_sensor_data.listen(lambda radar_data: _Radar_callback(radar_data))

    def _Radar_callback(radar_data):
        distanceNameData = {}
        for detection in radar_data:
            distanceNameData["distance"] = detection.depth
            print(distanceNameData["distance"])

    actor_list.append(radar_sensor_data)
    actor_list.append(mustang_car)
    actor_list.append(dropped_vehicle)
    time.sleep(1000)
finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
    print("done.")
