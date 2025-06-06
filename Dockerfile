FROM osrf/ros:foxy-desktop
SHELL ["/bin/bash", "-c"]

# Set environment variables
ENV ROS_DISTRO=foxy
ENV RMW_IMPLEMENTATION=rmw_cyclonedx_cpp
ENV ROS_DOMAIN_ID=30

# Instalar pacotes necessários para nosso projeto
RUN apt-get update && apt-get install -y \
    # Nav2 e navegação (como na aula)
    ros-foxy-navigation2 \
    ros-foxy-nav2-bringup \
    ros-foxy-rmw-cyclonedx-cpp \
    # Pacotes adicionais para nosso robô
    ros-foxy-robot-localization \
    ros-foxy-tf2-tools \
    ros-foxy-robot-state-publisher \
    ros-foxy-joint-state-publisher \
    ros-foxy-xacro \
    # Ferramentas de desenvolvimento
    python3-pip \
    python3-colcon-common-extensions \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies para nosso waypoint publisher
RUN pip3 install \
    transforms3d \
    numpy

# Configurar ROS (como na aula)
RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc

# Create workspace para nosso projeto
WORKDIR /workspace

# Copy source code do nosso robô
COPY src/ /workspace/src/

# Build workspace do nosso projeto
RUN source /opt/ros/foxy/setup.bash && \
    colcon build --symlink-install

# Source workspace no bashrc
RUN echo "source /workspace/install/setup.bash" >> ~/.bashrc

# Set default command
CMD ["bash"]