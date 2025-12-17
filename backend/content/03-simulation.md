# Simulation Environments

## The Role of Simulation
Training robots in the real world is slow, expensive, and dangerous. Simulation allows us to train "Policies" in virtual worlds at accelerated time.

## Popular Simulators
1. **Gazebo**: The classic ROS simulator. Good for general robotics.
2. **Isaac Sim (NVIDIA)**: Photorealistic, physics-accurate simulator based on Omniverse. Great for Sim-to-Real.
3. **MuJoCo**: High-performance physics engine, often used in Reinforcement Learning research.

## Sim-to-Real Gap
Transferring a policy learned in sim to the real world is hard due to:
- **System Identification errors**: Mass, friction not matching perfectly.
- **Sensor Noise**: Real cameras have noise and lighting issues.
- **Latency**: Simulation is often synchronous, reality is asynchronous.

Techniques like Domain Randomization help bridge this gap.
