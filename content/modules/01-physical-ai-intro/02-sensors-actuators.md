# Chapter 2: Sensors and Actuators Deep Dive

## Learning Objectives
- Understand different sensor modalities and their tradeoffs
- Learn how to process raw sensor data into usable information
- Explore actuator types and control strategies
- Implement sensor fusion for robust perception

## Sensor Modalities

### LIDAR (Light Detection and Ranging)

**How it works**: Emits laser pulses and measures time-of-flight to calculate distances.

**Specs**:
- Range: 0.5m to 100m (depends on model)
- Accuracy: ±2-3 cm
- Scan rate: 10-20 Hz for 360° rotation
- Resolution: 0.1° - 1° angular resolution

**Advantages**:
- Works in darkness
- Precise distance measurements
- 360° field of view
- Unaffected by texture/color

**Disadvantages**:
- Expensive ($1000 - $10,000+)
- Poor performance in fog, rain, dust
- Cannot detect transparent surfaces (glass)
- High power consumption

```python
# Example: Processing LIDAR scan data
import numpy as np

class LIDARProcessor:
    def __init__(self, num_beams=360):
        self.num_beams = num_beams
        self.angle_resolution = 2 * np.pi / num_beams

    def detect_obstacles(self, ranges, threshold=2.0):
        """
        Identify obstacles within threshold distance.

        Args:
            ranges: Array of distance measurements (meters)
            threshold: Maximum safe distance (meters)

        Returns:
            List of (angle, distance) tuples for obstacles
        """
        obstacles = []
        for i, distance in enumerate(ranges):
            if distance < threshold:
                angle = i * self.angle_resolution
                obstacles.append((angle, distance))
        return obstacles

    def find_clear_path(self, ranges, min_gap_width=0.5):
        """
        Find the widest gap in LIDAR scan for navigation.

        Args:
            ranges: Distance measurements
            min_gap_width: Minimum width for passable gap (meters)

        Returns:
            (start_angle, end_angle, width) of best gap
        """
        best_gap = (0, 0, 0)
        current_gap_start = None

        for i, dist in enumerate(ranges):
            angle = i * self.angle_resolution

            if dist > min_gap_width and current_gap_start is None:
                current_gap_start = i
            elif dist <= min_gap_width and current_gap_start is not None:
                gap_width = (i - current_gap_start) * self.angle_resolution
                if gap_width > best_gap[2]:
                    best_gap = (
                        current_gap_start * self.angle_resolution,
                        angle,
                        gap_width
                    )
                current_gap_start = None

        return best_gap

# Usage
lidar = LIDARProcessor(num_beams=360)
scan_data = np.random.uniform(0.5, 10, 360)  # Simulated scan
obstacles = lidar.detect_obstacles(scan_data, threshold=2.0)
print(f"Found {len(obstacles)} obstacles within 2 meters")
```

### Cameras (Vision Sensors)

**Types**:
1. **RGB Cameras**: Standard color imaging
2. **Depth Cameras**: Provide distance to each pixel (e.g., Intel RealSense, Kinect)
3. **Stereo Cameras**: Two cameras for depth via triangulation
4. **Event Cameras**: Asynchronous pixel-level change detection (low latency)

**Depth Camera Comparison**:

| Technology | Range | FPS | Indoor/Outdoor | Price |
|------------|-------|-----|----------------|-------|
| Structured Light | 0.5-4m | 30-60 | Indoor only | $$ |
| Time-of-Flight | 0.3-8m | 30-90 | Both | $$$ |
| Stereo | 1-10m | 30-120 | Both | $ |

```python
# Example: Object detection with camera
import cv2
import numpy as np

class VisionProcessor:
    def __init__(self):
        # Using a pre-trained model (simplified)
        self.model = self.load_detection_model()

    def detect_objects(self, frame):
        """
        Detect objects in camera frame.

        Args:
            frame: BGR image from camera

        Returns:
            List of (label, confidence, bbox) tuples
        """
        # Preprocess image
        blob = cv2.dnn.blobFromImage(
            frame, 1/255.0, (416, 416), swapRB=True, crop=False
        )

        # Run inference (pseudo-code)
        detections = self.model.detect(blob)

        results = []
        for det in detections:
            if det['confidence'] > 0.5:
                results.append({
                    'label': det['class_name'],
                    'confidence': det['confidence'],
                    'bbox': det['box']  # (x, y, w, h)
                })
        return results

    def estimate_distance(self, bbox, focal_length, real_height):
        """
        Estimate object distance from bounding box size.

        Args:
            bbox: (x, y, width, height) in pixels
            focal_length: Camera focal length in pixels
            real_height: Known object height in meters

        Returns:
            Estimated distance in meters
        """
        pixel_height = bbox[3]
        distance = (real_height * focal_length) / pixel_height
        return distance
```

### IMU (Inertial Measurement Unit)

**Components**:
- **Accelerometer**: Measures linear acceleration (3 axes)
- **Gyroscope**: Measures angular velocity (3 axes)
- **Magnetometer**: Measures magnetic field (compass direction)

**Use Cases**:
- Drone stabilization
- Robot orientation tracking
- Dead reckoning navigation
- Vibration monitoring

```python
# Example: IMU-based orientation estimation
import numpy as np

class IMUProcessor:
    def __init__(self):
        self.orientation = np.array([0.0, 0.0, 0.0])  # roll, pitch, yaw
        self.dt = 0.01  # 100 Hz sample rate

    def update_orientation(self, gyro_data, accel_data):
        """
        Complementary filter for orientation estimation.

        Args:
            gyro_data: [gx, gy, gz] in rad/s
            accel_data: [ax, ay, az] in m/s²
        """
        # Integrate gyroscope for short-term accuracy
        gyro_orientation = self.orientation + np.array(gyro_data) * self.dt

        # Calculate tilt from accelerometer for long-term stability
        accel_roll = np.arctan2(accel_data[1], accel_data[2])
        accel_pitch = np.arctan2(
            -accel_data[0],
            np.sqrt(accel_data[1]**2 + accel_data[2]**2)
        )

        # Complementary filter: 98% gyro, 2% accel (high-pass + low-pass)
        alpha = 0.98
        self.orientation[0] = alpha * gyro_orientation[0] + (1-alpha) * accel_roll
        self.orientation[1] = alpha * gyro_orientation[1] + (1-alpha) * accel_pitch
        self.orientation[2] = gyro_orientation[2]  # Yaw from gyro only

        return self.orientation
```

## Sensor Fusion

**Why fuse sensors?**
- No single sensor is perfect
- Combine strengths, mitigate weaknesses
- Increase robustness and accuracy

### Kalman Filter Example

```python
class KalmanFilter1D:
    """
    Simple 1D Kalman filter for sensor fusion.
    """
    def __init__(self, process_variance, measurement_variance):
        self.q = process_variance  # Process noise
        self.r = measurement_variance  # Measurement noise
        self.x = 0.0  # State estimate
        self.p = 1.0  # Estimate uncertainty

    def update(self, measurement):
        # Prediction step
        self.p += self.q

        # Update step
        k = self.p / (self.p + self.r)  # Kalman gain
        self.x += k * (measurement - self.x)
        self.p *= (1 - k)

        return self.x

# Usage: Fuse noisy position measurements
kf = KalmanFilter1D(process_variance=0.01, measurement_variance=0.1)
measurements = [1.1, 0.9, 1.2, 0.95, 1.05]  # Noisy sensor readings
filtered = [kf.update(m) for m in measurements]
```

## Actuators and Control

### DC Motors

**Characteristics**:
- Speed proportional to voltage
- Torque proportional to current
- Require motor driver (H-bridge) for bidirectional control

**Control Methods**:
1. **Open-loop**: Set voltage → speed (no feedback)
2. **Closed-loop**: Use encoder feedback → PID control

```python
class PIDController:
    """
    Proportional-Integral-Derivative controller for motor speed.
    """
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, setpoint, measured_value, dt):
        """
        Compute control output.

        Args:
            setpoint: Desired value
            measured_value: Current sensor reading
            dt: Time since last update

        Returns:
            Control signal
        """
        error = setpoint - measured_value

        # Proportional term
        p_term = self.kp * error

        # Integral term (accumulated error)
        self.integral += error * dt
        i_term = self.ki * self.integral

        # Derivative term (rate of change)
        derivative = (error - self.prev_error) / dt
        d_term = self.kd * derivative

        # Update state
        self.prev_error = error

        # Compute output
        output = p_term + i_term + d_term
        return output

# Usage: Control motor to reach 100 RPM
pid = PIDController(kp=0.5, ki=0.1, kd=0.05)
target_speed = 100  # RPM
current_speed = 0

for _ in range(100):
    control_signal = pid.compute(target_speed, current_speed, dt=0.01)
    # Apply control_signal to motor (pseudo-code)
    # current_speed = motor.set_pwm(control_signal)
```

### Servo Motors

**Features**:
- Built-in position feedback (potentiometer)
- Controlled by PWM signal
- Typical range: 0° to 180°

**Use Cases**: Robot joints, camera gimbals, steering mechanisms

## Key Takeaways

1. Different sensors excel in different conditions (LIDAR in dark, cameras in textured environments)
2. Sensor fusion combines multiple modalities for robust perception
3. IMUs provide orientation but drift over time (need correction from other sensors)
4. PID control is the workhorse of motor control in robotics
5. Understanding sensor limitations is critical for reliable Physical AI systems

## Practice Problems

1. Implement a simple obstacle avoidance algorithm using LIDAR data
2. Write a complementary filter to fuse gyroscope and accelerometer data
3. Tune PID gains for a simulated motor control system
4. Design a sensor suite for a warehouse robot (justify each sensor choice)

## Next Steps
Next chapter: **ROS 2 Fundamentals** - Learn how to architect modular robot software using the Robot Operating System.
