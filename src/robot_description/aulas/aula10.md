# Arquivos de lançamento (Launch Files) no ROS2

Este roteiro guiará você na criação de um launch file no ROS2, dentro de um pacote Python, com explicações passo a passo.

Um launch file no ROS 2 é um arquivo utilizado para automatizar a execução de múltiplos nós e configurar seu ambiente de forma organizada. Em vez de iniciar manualmente cada nó com comandos separados no terminal, o launch file permite iniciar todos os nós necessários de uma aplicação com um único comando.

## 1. Criar um workspace

1. Escolha um diretório em sua máquina para criar seu workspace.
No exemplo, vamos usar ~/aula10_ws, mas você pode usar outro se preferir.

2. No terminal, execute os seguintes comandos para criar o workspace e a pasta src/:

    ```bash
    mkdir -p ~/aula10_ws/src
    cd ~/aula10_ws
    ```

- No ROS2, o conceito de **workspace** é usado para organizar os pacotes e compilar o código utilizando ```colcon build```.

- A pasta ```src``` é o diretório padrão onde os pacotes ROS2 devem ficar dentro do **workspace**.

## 2. Criar um pacote Python chamado aula10

Agora, criaremos um pacote chamado ```aula10```, que armazenará o nosso launch file.

1. No terminal, digite:

    ```bash
    cd ~/aula10_ws/src
    ros2 pkg create aula10 --build-type ament_python --dependencies rclpy
    ```

2. O pacote criado terá a seguinte estrutura inicial:

    ```bash
    aula10/
    ├── package.xml
    ├── setup.py
    ├── resource/
    │   └── aula10
    ├── setup.cfg
    └── aula10/
        ├── __init__.py
    ```

## 3. Criar o diretório ```launch```

1. Dentro do diretório ```aula10```, crie a pasta ```launch``` para armazenar os arquivos de lançamento:

    ```bash
    mkdir ~/aula10_ws/src/aula10/launch
    ```

2. Agora, sua estrutura de diretórios deve ficar assim:

    ```bash
    aula10/
    ├── launch
    ├── package.xml
    ├── setup.py
    ├── resource/
    ├── setup.cfg
    └── aula10/
        ├── __init__.py
    ```

## 4. Criar o arquivo ```aula10.launch.py```

Agora vamos criar o launch file que inicializa os nós ```talker``` e ```listener```, remapeando o tópico ```/chatter``` para ```/new_chatter```.

1. Crie o arquivo ```aula10.launch.py``` dentro da pasta ```launch```:

    ```bash
    touch ~/aula10_ws/src/aula10/launch/aula10.launch.py
    ```

2. Abra o arquivo e adicione o seguinte código:

    ![Lanch File](./imagens/launch_file.png)

### Explicação do código

1. Importações

    ```python
    import launch
    from launch_ros.actions import Node
    from launch.actions import IncludeLaunchDescription
    from launch.launch_description_sources import PythonLaunchDescriptionSource
    import os
    from ament_index_python.packages import get_package_share_directory
    ```

- ```import launch``` → Importa a base do sistema de launch no ROS 2.

- ```from launch_ros.actions import Node``` → Permite criar e configurar nós ROS 2 dentro do launch file.

- ```from launch.actions import IncludeLaunchDescription``` → Permite incluir outro launch file dentro deste, tornando o código modular.

- ```from launch.launch_description_sources import PythonLaunchDescriptionSource``` → Especifica que o launch file incluído está em Python.

- ```import os``` → Usado para manipular caminhos de arquivos/diretórios.

- ```from ament_index_python.packages import get_package_share_directory``` → Localiza automaticamente o diretório share de um pacote ROS 2 instalado.

2. Função Principal: ```generate_launch_description()```

    ```python
    def generate_launch_description():
    ```

    Esta função retorna uma ```LaunchDescription```, que contém todos os elementos que devem ser executados ao rodar o launch file.

3. Criando o nó ```talker``` com remapeamento

    ```python
    talker_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='talker_remap',
        remappings=[('/chatter', '/new_chatter')]
    )
    ```

- ```package='demo_nodes_cpp'``` → Define em qual pacote está o nó, no caso ```demo_nodes_cpp``` (um pacote padrão de exemplos no ROS 2).

- ```executable='talker'``` → Define o nó que será executado.

- ```name='talker_remap'``` → Nome do nó no ROS 2.

- ```remappings=[('/chatter', '/new_chatter')]``` → Remapeia o nome do tópico.

4. Criando o nó ```listener``` com remapeamento

    ```python
        listener_node = Node(
        package='demo_nodes_cpp',
        executable='listener',
        name='listener_remap',
        remappings=[('/chatter', '/new_chatter')]
    )
    ```

    Semelhante ao node anterior

5. Incluindo outro launch file

    ```python
    talker_listener_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('demo_nodes_cpp'), 
                'launch',
                'topics', 
                'talker_listener.launch.py'
            )
        ])
    )
    ```

- ```IncludeLaunchDescription()``` → Inclui um outro launch file dentro deste.

- ```PythonLaunchDescriptionSource()``` → Define que o launch file incluído é um script Python (```.py```).

- ```get_package_share_directory('demo_nodes_cpp')``` → Obtém o caminho do diretório share do pacote demo_nodes_cpp.

- ```os.path.join(...)``` → Constrói o caminho para encontrar o launch file ```talker_listener.launch.py``` dentro do pacote ```demo_nodes_cpp```.

6. Retornando a ```LaunchDescription```

    ```python 
    return launch.LaunchDescription([
        talker_node,
        listener_node,
        talker_listener_launch,
    ])
    ```

    Este retorno define quais elementos serão lançados.

## 5. Adicionar o diretório **launch** ao **setup.py**

1. Para que o ROS2 reconheça os arquivos de launch na instalação do pacote, edite o arquivo ```setup.py``` e adicione a seguinte linha no campo ```data_files```:

    ```python
    (os.path.join('share', package_name, 'launch'), glob('launch/*.py'))
    ```

2. No topo do arquivo setup.py, certifique-se de importar as bibliotecas necessárias:

    ```python
    import os
    from glob import glob
    ```

- ```os.path.join()``` → Garante que o caminho para o diretório ```launch``` seja corretamente formatado em qualquer sistema operacional.

- ```glob('launch/*.py')``` → Busca automaticamente todos os arquivos ```.py``` dentro do diretório ```launch```, garantindo que eles sejam instalados no local correto.

## 6. Compilar o pacote e execultar o arquivo

1. No terminal, volte para o diretório do workspace e compile:

    ```bash
    cd ~/aula10_ws
    colcon build --packages-select aula10
    ```

2. Após a compilação, atualize o ambiente:

    ```bash
    source install/setup.bash
    ```

3. Agora vamos executar o launch file e verificar se os nós estão rodando corretamente:

    ```bash
    ros2 launch aula10 aula10.launch.py
    ```

## 7. Verificar a Comunicação Usando ```rqt_graph```

1. Em um segundo terminal, abra o ```rqt_graph```:

    ```bash
    rqt_graph
    ```

    Você deve ver algo como:

    ![rqt_graph](./imagens/rqt_graph.png)

    Note que temos os nós em que mudamos os nomes se comunicando através do tópico remapeado, e separadamente, os nós com os nomes originais, lançados pela launch file.


## Exercício de fixação

Para fixar os conceitos aprendidos nesta aula, vamos fazer mais um exercício.

Crie um **launch file** para iniciar os seguintes nós:

- **Publisher** e **Subscriber** criados em aulas anteriores.

- **Action Server** desenvolvido na aula sobre actions.

- **Service Server** desenvolvido na aula sobre serviços.

- **Launch file da APS1**




