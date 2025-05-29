# Aula 24 - Docker Compose

Docker Compose é uma ferramenta oficial da plataforma Docker que orquestra múltiplos containers a partir de um único arquivo docker-compose.yaml. Em vez de você iniciar cada container manualmente com comandos longos de docker run, o Compose descreve toda a aplicação — serviços, redes e volumes — de forma declarativa e versionada, facilitando o desenvolvimento, a execução e o compartilhamento de ambientes complexos.

Principais benefícios:

- Orquestração simplificada – Um único comando (docker compose up) cria, conecta e inicia todos os serviços necessários.

- Reprodutibilidade completa – O arquivo yaml versionado garante que o mesmo conjunto de containers, versões de imagem e variáveis de ambiente seja recriado em qualquer máquina.

- Escalabilidade rápida – Com --scale, replicas adicionais de um serviço são levantadas sem alterar código.

- Isolamento e redes internas – Compose gera automaticamente redes virtuais isoladas, assegurando que serviços conversem apenas entre si ou com o host quando permitido.

**O que você fará neste exercício**

1.	Criar um arquivo docker-compose.yaml com base na imagem ```osrf/ros:foxy-desktop``` que contenha dois serviços:

- O primeiro rodando o nó exemplo ```talker```.

- O segundo rodando o nó exemplo ```listener```.

- Visualizar ambos se comunicando.

2.	Criar um arquivo docker-compose.yaml com base em uma imagem criada localmente a partir de um arquivo ```Dockerfile```, que contenha um serviço que, quando inicializado, envie um comando de navegação ao Nav2.

## 1. Docker Compose Básico

1. Em um diretório de sua preferência crie um arquivo chamado ```docker-compose.yaml``` e copie o código abaixo:

    ```docker-compose
    services:
        base:
            image: osrf/ros:foxy-desktop
            stdin_open: true
            tty: true
            network_mode: host
            ipc: host
            privileged: true

        talker:
            extends: base
            container_name: ros2_talker
            command: ["bash", "-c", "source /opt/ros/foxy/setup.bash && ros2 run demo_nodes_cpp talker"]

        listener:
            extends: base
            container_name: ros2_listener
            command: ["bash", "-c", "source /opt/ros/foxy/setup.bash && ros2 run demo_nodes_cpp listener"]
    ```

    **Explicação**

    **image: osrf/ros:foxy-desktop**: Define a imagem base utilizada nos containers, que neste caso é a imagem oficial do ROS 2 Foxy 

    **stdin_open: true e tty: true**: Permitem que o container mantenha um terminal interativo aberto, o que é útil para depuração ou execução de comandos diretamente no container via docker attach ou docker exec.

    **network_mode: host**: Faz com que o container utilize diretamente a rede do host, permitindo que os nós ROS se comuniquem entre si usando multicast e outras funcionalidades de rede como se estivessem rodando no próprio sistema host.

    **ipc: host**: Compartilha o namespace de comunicação entre processos (IPC) com o host, permitindo acesso a memória compartilhada — necessário para algumas aplicações como Rviz e Gazebo que usam /dev/shm.

    **privileged: true**: Concede permissões elevadas ao container, permitindo acesso a dispositivos do host como portas USB, rede CAN ou interfaces seriais. Deve ser usado com cuidado, pois reduz o isolamento de segurança do container.

    **extends: base**: Indica que os serviços talker e listener reutilizam toda a configuração do serviço base, evitando repetição e facilitando a manutenção do Compose.

    **container_name**: Define nomes fixos para os containers, facilitando sua identificação e a execução de comandos como docker logs ou docker exec.

    **command**: Especifica o comando a ser executado ao iniciar o container. Neste caso, inicia um shell, configura o ambiente ROS 2 com source /opt/ros/foxy/setup.bash e executa o nó correspondente (talker ou listener) do pacote de demonstração demo_nodes_cpp.

2. Abra um terminal, no mesmo diretório do arquivo, e compile as imagens:

    ```bash
    docker compose build
    ```

3. No mesmo terminal, inicie o serviço ```talker```:

    ```bash
    docker compose up talker
    ```

4. Em um segundo terminal, inicie o serviço ```listener```:

    ```bash
    docker compose up listener
    ```

5. Veja se os nós inicializados estão se comunicando

6. Em um terceiro terminal, pare os serviços iniciados com o comando:

    ```bash
    docker compose down
    ```

## 2. Volumes e Docker exec

Nessa etapa, você irá aprender a montar um volume Docker em um container, permitindo que dados gravados dentro do container sejam persistidos ou compartilhados entre serviços. Isso é útil para logs, arquivos de configuração, resultados de experimentos, entre outros.

1. No mesmo diretório do ```docker-compose.yaml``` crie um diretório ```teste``` e, nele, um aquivo ```teste.py```. No arquivo recém criado, escreva o código:

    ```python
    print("Arquivo montado com sucesso!")
    ```

2. Crie o volume no arquivo ```docker-compose.yaml```. Na seção ```base```, adicione as linhas:

    ```docker-compose
    volumes:
        - ./teste:/teste
    ```

3. Em um terminal, rode o serviço ```talker```:

    ```bash
    docker compose up talker -d
    ```

    O argumento ```-d``` faz com que o serviço rode no background, deixando o terminal livre.

4. Entre no container:

    ```bash
    docker exec -it ros2_talker bash
    ```

5. Verifique que o arquivo está presente no container:

    ```bash
    cd teste
    ls
    ```

6. Execute o arquivo ```teste.py``` com o comando:

    ```bash
    python3 teste.py
    ```

    E veja se a mesagem é exibida no terminal.

7. Saia do container com o comando ```Ctrl + d``` e pare os serviços com o comando ```docker compose down```

## 3. Docker Compose a partir de uma Dockerfile

Semelhante às seções anteriores, é possível criar serviços com base em imagens criadas localmente, definidas em um arquivo ```Dockerfile```.

1. Modifique o arquivo ```docker-compose.yaml``` para usar como base a imagem criada na aula passada no arquivo ```Dockerfile```. Pesquise como faze-lo.

2. Seguindo o exemplo dos serviços ```talker``` e ```listener```, crie um novo serviço chamado ```nav2_goal``` que, quando iniciado, envie um comando de navegação ao nav2.

3. Compile o arquivo ```docker-compose.yaml```

4. Em um terminal, inicie a simulação do **turtlebot3** e defina a sua posição inicial.

5. Em um segundo terminal, inicie o serviço ```nav2_goal``` e verifique que o robô executou o comando.








