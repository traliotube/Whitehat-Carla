import glob
import os
import sys
import random
import time
import numpy as np
import cv2

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

IM_WIDTH = 640
IM_HEIGHT = 480
actor_list = []

#Define function here named image
def image(image):
    matrix_representational_data = np.array(image.raw_data)
    reshape_of_image = matrix_representational_data.reshape((IM_HEIGHT, IM_WIDTH, 4))
    live_feed_from_camera = reshape_of_image[:, :, :3]
    cv2.imshow("", live_feed_from_camera)
    cv2.waitKey(1)
    return
    #Store data using save_to_disk(in output folder with jpg extension)

try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    get_blueprint_of_world = world.get_blueprint_library()
    #Define vehicle name here and store in car_model variable
    car_model = get_blueprint_of_world.filter("model3")[0]
    #Define spawn points for car and store in spawn_point variable
    spawn_point = random.choice(world.get_map().get_spawn_points())
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)


    dropped_vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    dropped_vehicle.set_transform(spawn_point)
    actor_list.append(dropped_vehicle)

    ## camera sensor
    ##Define camera sensor here and store in camera_sensor variable
    camera_sensor = get_blueprint_of_world.find("sensor.camera.rgb")
    # change the dimensions of the image
    camera_sensor.set_attribute('image_size_x',f"{IM_WIDTH}")
    camera_sensor.set_attribute('image_size_y',f"{IM_HEIGHT}")
    #Define width size of camera sensor
    #Define height size of camera sensor
    #Define FOV size here
    camera_sensor.set_attribute('fov', "110")
    # Adjust sensor relative to vehicle
    sensor_spawn_point = carla.Transform(carla.Location(x=2.5, y=0.7))
    #Declare location of carla transform and store in sensor_camera_spawn_point
    sensor = world.spawn_actor(camera_sensor, sensor_spawn_point, attach_to=dropped_vehicle)
    # spawn the sensor and attach to vehicle.
    #Attach sensor and location of spawn point to vehicle and store in sensor variable
    # add sensor to list of actors
    actor_list.append(sensor)
    #Add sensor in actor list
    # do something with this sensor
    #Define listen method to store sensor data
    sensor.listen(image)

    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')