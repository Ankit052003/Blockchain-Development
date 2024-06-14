import random
import uuid

def generate_random_bsm_data():
    # Generate random position with reasonable latitude and longitude values
    latitude = round(random.uniform(-90.0, 90.0), 6)
    longitude = round(random.uniform(-180.0, 180.0), 6)
    elevation = round(random.uniform(-50, 5000), 2)  # Elevation in meters

    # Generate other random BSM values
    position_accuracy = random.randint(1, 10)
    speed = round(random.uniform(0, 200), 2)  # Speed in km/h
    heading = random.randint(0, 360)  # Heading in degrees
    steering_wheel_angle = round(random.uniform(-180, 180), 2)  # Steering wheel angle in degrees
    acceleration = round(random.uniform(-10, 10), 2)  # Acceleration in m/s^2
    brake_system_status = random.choice(["active", "inactive"])
    vehicle_width = round(random.uniform(1.5, 2.5), 2)  # Width in meters
    vehicle_length = round(random.uniform(3.0, 5.0), 2)  # Length in meters
    yaw_rate = round(random.uniform(-1, 1), 2)  # Yaw rate in degrees per second

    bsm_data = {
        "message_count": random.randint(1, 1000),
        "temporary_id": uuid.uuid4().hex[:8],
        "position": {
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation
        },
        "position_accuracy": position_accuracy,
        "speed": speed,
        "heading": heading,
        "steering_wheel_angle": steering_wheel_angle,
        "acceleration": acceleration,
        "brake_system_status": brake_system_status,
        "vehicle_size": {
            "width": vehicle_width,
            "length": vehicle_length
        },
        "yaw_rate": yaw_rate
    }

    return bsm_data

# Example usage
random_bsm_data = generate_random_bsm_data()
print(random_bsm_data)
