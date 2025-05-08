# APS 2 - Localização e SLAM

Nesta APS, você irá consolidar os conhecimentos adquiridos sobre a implementação em ROS2 de fusão de sensores utilizando filtro de kalman extendido, localização Monte Carlo (AMCL) e SLAM (Simultaneous Localization and Mapping).

Para realização desta APS, você deverá criar dois pacotes:

1. **rm_localization**

Este pacote deverá ter os seguintes diretórios e arquivos:

- **config**: contendo os arquivos de configuração do **EKF** e do **AMCL**, sendo eles:

    - **ekf.yaml**: Deve fundir os dados de odometria e imu, tendo como saída o tópico ```/odometry/filtered```.

    - **amcl.yaml**: Contendo os parâmetros de configuração do pacote **AMCL**.

- **launch**: Com os arquivos de inicialização refrentes a cada um dos pacotes:

    - **ekf.launch.py**: Deve inicializar o node **ekf** do pacote **robot_localization** passando como parâmtro o arquivo de configuração criado no diretório ```launch```.

    - **amcl.launch.py**: Deve inicializar node **AMCL** do pacote **nav2_amcl**, passando como parâmetro o arquivo de configuração, e o mapa criado utilizando **SLAM**, localizado no diretório ```map```.

- **map**: Contendo os arquivos ```.pgm``` e ```.yaml``` referentes ao mapa criado.

2. **rm_slam**

Este pacote deverá conter os seguintes diretórios e arquivos:

- **config**: Contendo o arquivo de configuração **slam_config.yaml** do pacote **slam_toolbox**.

- **launch**: Contendo o arquivo de lançamento, **slam.launch.py**, do node ```async_slam_toolbox_node```, pertencente ao pacote **slam_toolbox**.


## Entrega

A entrega desta APS deve ser feita até as 23:59 do dia 21/04 (Segunda-Feira). 

Deve ser entregue, através do BlackBoard, um arquivo ```.zip``` com os dois pacotes criados para esta APS, contendo os arquivos de configuração ```.yaml```, os arquivos ```.launch``` e o mapa criado. Além disso, junto ao ```.zip```, devem ser gravados dois vídeos da execução do código:

- **Vídeo 1**: Neste vídeo, deve ser gravado o processo de inicialização do ambiente de simulação, do nó contendo o **EKF** e do nó com o pacote **slam_toolbox**, cada um usando suas respectivas ***launch files*** e em um terminal próprio. Depois de inicializados os nós, deve ser realizado o mapeamento do ambiente através do **RVIZ** e o salvamento do mapa.

- **Vídeo 2**: No segundo vídeo, deve ser gravado o processo de inicialização do ambiente de simulação, do nó contendo o **EKF** e do nó com o pacote **AMCL**, cada um usando suas respectivas ***launch files*** e em um terminal próprio. Depois de inicializados os nós, deve ser realizada a navegação no ambiente, mostrando a localização bem sucedida utilizando o mapa criado e suas partículas.

Esta APS pode ser realizada em duplas. Neste caso, apenas uma pessoa da dupla deve realizar o envio pelo Blackboard, adicionando nos comentários da entrega o nome do segundo integrante.

## Avaliação

A Avaliação desta atividade será feita da seguinte forma:

1. **Fusão de sensores com pacote ```robot_localization``` (30%)**

2. **Localização com pacote ```nav2_amcl``` (30%)**

3. **Mapeamento com pacote ```slam_toolbox``` (40%)**