import glob
import os
import sys
import time

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


# write the code for defining radar sensor function


def generate_radar_blueprint(blueprint_library):
    radar_blueprint = blueprint_library.find("sensor.other.radar")
    radar_blueprint.set_attribute("horizontal_fov", str(35))
    radar_blueprint.set_attribute("vertical_fov", str(20))
    radar_blueprint.set_attribute("points_per_second", str(1500))
    radar_blueprint.set_attribute("range", str(20))
    return radar_blueprint


try:
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter("model3")[0]
    spawn_point = world.get_map().get_spawn_points()[1]
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    simulator_camera_location_rotation = carla.Transform(
        spawn_point.location, spawn_point.rotation
    )
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 1
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)
    dropped_vehicle.set_autopilot(True)
    radar_sensor = generate_radar_blueprint(get_blueprint_of_world)
    sensor_radar_spawn_point = carla.Transform(carla.Location(x=-0.5, z=1.8))
    sensor = world.spawn_actor(
        radar_sensor, sensor_radar_spawn_point, attach_to=dropped_vehicle
    )

    # write code here for listen method
    sensor.listen(lambda data: radar_callback(data))

    # write code here for defining radar_callback function to display the data
    def radar_callback(data):
        for detection in data:
            print("Depth: ", str(detection.depth))
            print("Altitude: ", str(detection.altitude))
            print("Velocity: ", str(detection.velocity))
            print("Azimuth: ", str(detection.azimuth))

    actor_list.append(sensor)

    time.sleep(1000)
finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
    print("done.")
