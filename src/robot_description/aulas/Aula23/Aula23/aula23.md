# Aula 23 - Docker

Docker é uma plataforma de *containerização* que empacota aplicações e todas as suas dependências em unidades portáveis chamadas **containers**.  
Suas principais vantagens são:

* **Reprodutibilidade**: Mantendo a mesma versão de bibliotecas e dependências.  
* **Isolamento**: Dependências do projeto não “poluem” o SO do host.  
* **Portabilidade**: a mesma imagem roda em PCs, nuvem ou Jetson (ARM), bastando definir `--platform`.

**O que você fará neste exercício**

1. **Instalar** o Docker no seu sistema.  
2. **Construir** uma imagem baseada no `ros:foxy`.  
3. **Rodar** um container interativo.  

## 1. Instalação do Docker

Siga o passo-a-passo descrito [neste link](https://docs.docker.com/engine/install/ubuntu/), na seção **Install using the apt repository**, e instale o Docker na sua mána virtual ou WSL.

## 2. Conceda permissões de administrador ao Docker

Para que não seja necessário utilizar permissão de administrador (```sudo```) toda vez vez que inicializar um docker, siga o passo-a-passo descrito [neste link](https://docs.docker.com/engine/install/linux-postinstall/), sob a seção **Manage Docker as a non-root user**. Este passo não é necessário, mas pode facilitar a inicialização.

## 3. Criando o primeiro container

Para começar, vamos importar uma imagem pronta de docker que já contem os pacotes necessário para executar o ros2 Foxy

1. **Compile a Imagem**

    Em um terminal, no mesmo diretório da Dockerfile, execute o comando:

    ```bash
    docker pull osrf/ros:foxy-desktop
    ```

2. **Execute o container**

    Com o download da imagem, podemos usa-la para abrir containers separados em cada terminal, e fazer com que cada um execute um comando/função.

    **Terminal 1**
    ```bash
    docker run --rm -it --name ros2_talker --network host osrf/ros:foxy-desktop bash
    ```

    **Terminal 2**
    ```bash
    docker run --rm -it --name ros2_listener --network host osrf/ros:foxy-desktop bash
    ```

    **Flags Utilizadas**:
    - **--rm**: Remove o container uma vez que paramos ele
    - **-it**: Deixa aberto um terminal interativo
    - **--name**: Atribui um nome ao container
    - **--network host**: Faz com que o container compartilhes as interfaces de rede com o host
    - **ros:foxy-desktop**: nome da imagem a ser usada para inicializar o container

3. **Rode os nós de exemplo**

    **Terminal 1**

    ```bash
    source /opt/ros/foxy/setup.bash
    ros2 run demo_nodes_cpp talker
    ```

    **Terminal 2**

    ```bash
    source /opt/ros/foxy/setup.bash
    ros2 run demo_nodes_cpp listener
    ```

    Note que ambos os containers, mesmo sendo "máquinas" diferentes, são capazes de se comunicar. Isso é possível pois eles estão compartilhando a mesma interface de rede, como foi definido na inicialização do container.

## 4. Criando uma Dockerfile

Além de executar uma imagem pronta, é possível criar as nossas próprias imagens. Isso é feito através de um arquivo chamado ```Dockerfile```. 

Um **Dockerfile** é um arquivo de texto que descreve, passo a passo, como construir uma imagem Docker — pense nele como a “receita” que o Docker usa para fazer o “bolo” (a imagem).  
Cada linha do Dockerfile é uma instrução declarativa; quando você executa `docker build`, o mecanismo cria uma **nova camada imutável** para cada instrução, resultando em uma pilha de camadas que forma a imagem final.  
Isso garante:

* **Reprodutibilidade**: qualquer pessoa, em qualquer máquina, que execute o mesmo `docker build` obterá exatamente a mesma imagem.  
* **Versionamento**: pequenas mudanças geram apenas novas camadas, economizando tempo e armazenamento.  
* **Transparência**: o histórico de cada modificação fica registrado — útil para auditoria e CI/CD.

As principais instruções para a construção da imagem são:

| Instrução   | Para que serve                                                                      | Exemplo mínimo                                                        |
|-------------|-------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| `FROM`      | Escolhe a imagem base (ponto de partida).                                           | `FROM ros:foxy-ros-base`                                              |
| `RUN`       | Executa comandos de shell em tempo de *build* (instala pacotes, compila código).    | `RUN apt-get update && apt-get install -y ros-foxy-gazebo-ros-pkgs`   |
| `COPY`      | Copia arquivos do host para a imagem.                                               | `COPY src/ /ws/src`                                                   |
| `ADD`       | Igual a `COPY`, mas também descompacta `.tar` e faz download via URL.               | `ADD https://site.com/file.tar.gz /tmp/`                              |
| `WORKDIR`   | Define o diretório em que instruções seguintes serão executadas.                    | `WORKDIR /ws`                                                         |
| `ENV`       | Cria variáveis de ambiente disponíveis no build **e** em tempo de execução.         | `ENV LANG=C.UTF-8`                                                    |
| `ARG`       | Declara variáveis só visíveis no build (passadas com `--build-arg`).                | `ARG UID=1000`                                                        |
| `USER`      | Troca o usuário que executará comandos (evita rodar como root).                     | `USER rosuser`                                                        |
| `VOLUME`    | Marca diretórios a serem montados como volumes persistentes.                        | `VOLUME ["/ws/maps"]`                                                 |
| `EXPOSE`    | Documenta portas que o container pretende usar (não publica automaticamente).       | `EXPOSE 11311/udp`                                                    |
| `LABEL`     | Adiciona metadados à imagem (autor, versão, commit).                                | `LABEL maintainer="lucas@example.com"`                                |
| `ENTRYPOINT`| Define o executável “fixo” do container.                                            | `ENTRYPOINT ["ros2"]`                                                 |
| `CMD`       | Parâmetros padrão do `ENTRYPOINT` ou comando final se não houver `ENTRYPOINT`.      | `CMD ["launch", "my_pkg", "bringup.launch.py"]`                       |
| `SHELL`     | Muda o interpretador usado nas instruções `RUN`.                                    | `SHELL ["/bin/bash", "-c"]`                                           |
| `HEALTHCHECK`| Define como o Docker verifica se o container está saudável.                        | `HEALTHCHECK CMD curl -f http://localhost/ || exit 1`                 |
| `ONBUILD`   | Gatilho que roda **quando outra imagem usa esta como base**.                        | `ONBUILD COPY . /app/src`                                             |


### Exercício:

1. **Crie a Dockerfile**:

    Em um diretório de sua preferência, crie um arquivo chamado ```Dockerfile````

    ```bash
    touch Dockerfile
    ```

2. **Crie a *"receita"***

    No arquivo recém criado, escreva a sequência de comandos para criar uma imagem com os seguintes requisitos:

    - Utilizar a imagem ```osrf/ros:foxy-desktop``` como ponto de partida (base)
    - Definir o interpretador como ```["/bin/bash", "-c"]```
    - Instalar os pacotes do ROS ```navigation2```, ```nav2-bringup``` e ```rmw-cyclonedds-cpp```
    - Adicionar o comando ```source /opt/ros/foxy/setup.py``` ao arquivo ```~/.bashrc```
    - Definir a variável de ambiente ```RMW_IMPLEMENTATION=rmw_cyclonedds_cpp```

3. **Compile a imagem**

No diretório da Dockerfile, rode o comando:

```bash
docker build -t ros2:foxy-min .
```

4. **Rode um container interativo**

Assim como na seção anterior, inicialize um container interativo em um terminal.

5. **Execute a simulação**

Em um terminal fora do container (no host) inicie a simulação do **turtlebot3** e defina a posição inicail do robô.

6. **Interação via Docker**

Agora, no terminal interativo do container, veja se consegue visualizar os tópicos, serviços e ações referentes à simulação. Depois, envie comandos de navegação da mesma forma que na última aula.









