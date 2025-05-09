FROM osrf/ros:foxy-desktop
SHELL ["/bin/bash", "-c"]

# Instalar pacotes
RUN apt-get update && apt-get install -y \
    ros-foxy-navigation2 \
    ros-foxy-nav2-bringup \
    ros-foxy-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# Configurar ROS
RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Opcional: definir um domínio ID padrão
ENV ROS_DOMAIN_ID=42