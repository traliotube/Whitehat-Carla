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


throttle = 0.5

modelFile = open("./class-237-classifier-model.pkl", "rb")
model = pickle.load(modelFile)


def generate_radar_blueprint(blueprint_library):
    radar_blueprint = blueprint_library.filter("sensor.other.radar")[0]
    radar_blueprint.set_attribute("horizontal_fov", str(10))
    radar_blueprint.set_attribute("vertical_fov", str(10))
    radar_blueprint.set_attribute("points_per_second", str(15000))
    radar_blueprint.set_attribute("range", str(10))
    return radar_blueprint


try:
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter("model3")[0]
    spawn_point = world.get_map().get_spawn_points()[6]
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)

    mustang_car_blueprint = get_blueprint_of_world.filter("mustang")[0]
    mustang_car_spawn_point = world.get_map().get_spawn_points()[4]
    mustang_car = world.spawn_actor(mustang_car_blueprint, mustang_car_spawn_point)
    mustang_car.apply_control(carla.VehicleControl(throttle=0.2))

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
            data = [[throttle, distanceNameData["distance"]]]
            prediction = int(model.predict(data)[0])

            if prediction == 1:
                print("Applying Brake")
                dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
                dropped_vehicle.apply_control(
                    carla.VehicleControl(throttle=0.3, steer=-0.2)
                )
                time.sleep(2)
                dropped_vehicle.apply_control(
                    carla.VehicleControl(throttle=0.3, steer=0.28)
                )
                time.sleep(2)
                dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
                time.sleep(10)
                print("Prediction 1")
                break
            elif prediction == 0:
                print("Applying Brake")
                dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
                dropped_vehicle.apply_control(
                    carla.VehicleControl(throttle=0.3, steer=0.2)
                )
                time.sleep(2)
                dropped_vehicle.apply_control(
                    carla.VehicleControl(throttle=0.3, steer=-0.27)
                )
                time.sleep(2)
                dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
                time.sleep(10)
                print("Prediction 0")
                break
            else:
                dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
                print("Prediction 2")
                break

    actor_list.append(radar_sensor_data)
    actor_list.append(dropped_vehicle)
    actor_list.append(mustang_car)
    time.sleep(1000)
finally:
    print("destroying actors")
    for actor in actor_list:
        actor.destroy()
    print("done.")
