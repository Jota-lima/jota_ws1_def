FROM osrf/ros:foxy-desktop
SHELL ["/bin/bash", "-c"]

# pacotes
RUN apt-get update && apt-get install -y \
    ros-foxy-navigation2 \
    ros-foxy-nav2-bringup \
    ros-foxy-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*


RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

ENV ROS_DOMAIN_ID=42