# Projeto Final: Navegação Autônoma Avançada com ROS 2 e Docker

## 1. Introdução do Projeto

Este projeto final tem como objetivo consolidar e expandir os conhecimentos adquiridos durante a disciplina, levando seu robô a um novo nível de autonomia. Vocês irão implementar um sistema de navegação completo utilizando o **Nav2**, o stack de navegação padrão do ROS 2, e desenvolverão um nó para gerenciar missões de múltiplos waypoints. Além disso, aplicarão boas práticas de desenvolvimento ao empacotar toda a solução utilizando Docker e Docker Compose.

Este é um projeto que integra diversos conceitos e tecnologias em robótica móvel, preparando-os para problemas complexos do mundo real.

## 2. Objetivos Gerais

Ao final deste projeto, vocês serão capazes de:

* **Implementar e Configurar o Nav2:** Integrar e realizar o _tuning_ do stack Nav2 para permitir a navegação autônoma robusta do robô diferencial simulado.

* **Desenvolver um Gerenciador de Missões:** Criar um nó ROS 2 que envie sequencialmente waypoints para o Nav2, controlando o fluxo de uma missão de navegação.

* **Utilizar Docker para Deployment:** Empacotar todas as dependências de software e os nós desenvolvidos em contêineres Docker, orquestrando-os com Docker Compose.

* **Aplicar Conhecimentos Integrados:** Demonstrar a compreensão integrada dos diversos subsistemas de um robô móvel autônomo (percepção, localização, planejamento, controle e execução de missão).


## 3. Detalhamento das Etapas e Requisitos

Esta seção detalha cada componente do projeto que será avaliado.

### 3.1. Implementação e _Tuning_ do Nav2 (4 pontos)

* **Descrição:**

    O principal objetivo desta etapa é habilitar a navegação autônoma do seu robô diferencial utilizando o stack Nav2. Vocês deverão partir da configuração do Nav2 para o TurtleBot3 (apresentada em aula) e adaptá-la para as especificidades do robô que sua equipe desenvolveu.

* **Tarefas Essenciais:**

    * Adaptar os arquivos de configuração do Nav2 (parâmetros YAML, arquivos de _launch_, etc.) para utilizar os tópicos corretos de sensores (LIDAR, IMU, odometria) e os _frames_ TF do seu robô.

    * Ajustar os parâmetros físicos do robô no Nav2, como o _footprint_ (formato e dimensões), raio, velocidades e acelerações máximas/mínimas.

    * Configurar adequadamente os _costmaps_ (global e local), incluindo as camadas de inflação e de obstáculos, de acordo com as características do seu robô e do ambiente de simulação.

    * Realizar o _tuning_ dos algoritmos de planejamento global e local e do _controller_ para obter um comportamento de navegação eficiente e seguro.

* **Critério de Sucesso:**

    O robô deve ser capaz de receber uma pose de destino (_goal_) através da ferramenta "Nav2 Goal" no RViz2 e navegar de forma autônoma até ela, planejando rotas, desviando de obstáculos conhecidos e dinâmicos no mapa e atualizando seu planejamento conforme necessário.

### 3.2. Nó Publicador de Waypoints Sequenciais (3 pontos)

* **Descrição:**

    Desenvolver um nó em ROS 2 que gerencie uma missão de navegação, enviando uma sequência pré-definida de _waypoints_ (poses de destino) para o Nav2.

* **Tarefas Essenciais:**
    * O nó deve utilizar a _action_ `nav2_msgs/action/NavigateToPose` para enviar cada _waypoint_ individualmente ao Nav2.

    * A sequência de _waypoints_ deve ser definida no código do nó ou carregada de um arquivo de configuração externo (ex: YAML).

    * O início do envio da sequência de _waypoints_ deve ser acionado através de um serviço ROS 2, ou seja, quando iniciado, o nó deve ficar ativo aguardando o serviço ser chamado para iniciar a nevegação.

* **Critério de Sucesso:**

    Após acionar o serviço, o robô deve aguardar o serviço ser chamado para navegar sequencialmente por todos os comodos do seu ambiente de simulação. O nó deve gerenciar corretamente o fluxo da missão.

### 3.3. Dockerização do Projeto (2 pontos)

* **Descrição:**

    Criar um ambiente Dockerizado para facilitar o _deployment_ e a execução do sistema de localização, navegação e do nó publicador de _waypoints_.

* **Tarefas Essenciais:**

    * **`Dockerfile`:** Desenvolver um `Dockerfile` que configure um ambiente ROS 2 Foxy e instale todas as dependências necessárias, incluindo os pacotes do Nav2, do AMCL, do EKF e do novo nó publicador de _waypoints_.

    * **`docker-compose.yml`:** Criar um arquivo `docker-compose.yml` para orquestrar os seguintes serviços:

        * `localization`: Inicia o nós relacionados a localização do robô (AMCL e EKF)

        * `navigation`: Inicia o _stack_ de navegação Nav2 (Lifecycle Manager, planners, controllers, costmaps, BT navigator, etc.).

        * `waypoint_follower`: Inicia o nó publicador de _waypoints_ desenvolvido por vocês.

* **Critério de Sucesso:**

    O comando `docker-compose up` deve ser capaz de iniciar todos os serviços definidos, permitindo que o sistema completo (localização, navegação, missão) funcione corretamente, comunicando-se com o simulador Gazebo (que deve estar rodando separadamente, no host).

### 3.4. Estrutura do Workspace e Qualidade Geral (1 ponto)

* **Descrição:**

    A organização do _workspace_ ROS 2, a qualidade do código e a documentação são fundamentais para um bom projeto de engenharia.

* **Tarefas Essenciais:**

    O workspace do projeto deve **somente** conter os seguintes pacotes e arquivos:

    ```bash
    Projeto_Final/
    ├── src/
    │   ├── custom_interfaces/
    │   │   ├── action/
    │   │   ├── msg/
    │   │   ├── srv/
    │   │   ├── CMakeLists.txt
    │   │   └── package.xml
    │   │
    │   ├── rm_localization/
    │   │   ├── config/
    │   │   ├── launch/
    │   │   ├── map/
    │   │   ├── CMakeLists.txt
    │   │   └── package.xml
    │   │
    │   ├── rm_navigation/
    │   │   ├── config/
    │   │   ├── launch/
    │   │   ├── CMakeLists.txt
    │   │   └── package.xml
    │   │
    │   ├── robot_description/
    │   │   ├── launch/
    │   │   ├── rviz/
    │   │   ├── urdf/
    │   │   ├── world/
    │   │   ├── CMakeLists.txt
    │   │   └── package.xml
    │   │
    │   └── waypoint_navigation_pkg/
    │       ├── launch/
    │       ├── waypoint_navigation_pkg/
    │       ├── resource/
    │       ├── package.xml
    │       └── setup.py
    │
    ├── Dockerfile
    └── docker-compose.yml
    ```

* **Critério de Sucesso:**
    O _workspace_ deve ser bem organizado e os nomes de arquivos representativos, permitindo que outra pessoa (o avaliador) consiga entender, compilar e executar o projeto sem dificuldades.

## 4. Entregáveis e Avaliação

Os grupos (de até 3 pessoas) deverão entregar um **único arquivo ZIP** contendo:

1.  **_Workspace_ ROS 2 Completo:**

    * Workspace com todos os pacotes ROS 2 desenvolvidos e configurados pela equipe.

    * Incluir o `Dockerfile` na raiz do _workspace_ ou em um local apropriado.

    * Incluir o arquivo `docker-compose.yml` na raiz do _workspace_.

2.  **Vídeos de Demonstração (gravações de tela):** Os vídeos devem ser claros, objetivos e demonstrar o funcionamento de cada parte.

    * **Vídeo 1: Navegação com Nav2 (Goal via RViz2)**
        * Demonstração do item 3.1.

        * **Avaliação combinada (código + vídeo): 4 pontos**

        * _Roteiro Sugerido:_
            * Mostrar o robô no Gazebo e RViz2.
            * Exibir o AMCL localizando o robô corretamente no mapa (partículas convergidas).
            * Exibir cada uma das seguintes camadas referentes ao funcionamento correto do Nav2:
                * Mapa de custo Global
                * Mapa de custo Local
                * Footprint
                * Caminho planejado

                Para facilitar a visualização, adicione e remova uma por uma enquanto grava o vídeo 
            * Utilizar a ferramenta "Nav2 Goal" no RViz2 para enviar um ou mais destinos ao robô.
            * Mostrar o robô navegando até os objetivos, exibindo a trajetória planejada, e desviando de obstáculos presentes no mapa.

    * **Vídeo 2: Missão de _Waypoints_ Sequenciais**

        * Demonstração do item 3.2.

        * **Avaliação combinada (código + vídeo): 3 pontos**

        * _Roteiro Sugerido:_
            * Mostrar o robô no Gazebo e RViz2, já localizado.

            * Executar o comando para acionar o serviço que inicia a missão de _waypoints_.

            * Mostrar o robô navegando pela sequência completa de _waypoints_ definida.

            * Enquanto o robô navega, adicionar pelo menos dois obstáculos dinâmicos para demonstrar sua capacidade de replanejamento.

    * **Vídeo 3: Demonstração do Docker**

        * Demonstração do item 3.3.

        * **Avaliação combinada (arquivos Docker + vídeo): 2 pontos**

        * _Roteiro Sugerido:_

            * Mostrar a execução do comando `docker-compose up`.

            * Exibir os _logs_ dos _containers_ sendo iniciados.

            * Utilizar `docker ps` para mostrar os _containers_ dos serviços (`localization`, `navigation`, `waypoint_follower`) em execução.

            * Chamar o serviço para inicializar a navegação e mostrar sua execução no Rviz/Gazebo

**Prazo de Entrega:** 04/06/2025

**Formato de Entrega:** Arquivo ZIP enviado no Blackboard

## 5. Dicas para execução

* **Iteração e Testes Constantes:**
    * **Nav2 Primeiro:** Foquem em fazer a adaptação do Nav2 funcionar para um único _goal_ enviado pelo RViz2. Esta é a base para todo o resto
    * **Nó de Waypoints:** Implementem o envio de um único _waypoint_ via _action_ primeiro. Depois, adicionem a lógica de sequência e o serviço de acionamento.
* **Docker:** Recomenda-se ter o sistema funcionando localmente (fora de contêineres) antes de tentar a dockerização completa. Isso simplifica a depuração de problemas relacionados ao ROS/Nav2. Um membro pode começar a preparar o Dockerfile e o docker-compose.yml em paralelo, à medida que os pacotes são desenvolvidos.
* **Vídeos Objetivos:** Planejem os vídeos para serem claros e concisos, cobrindo todos os aspectos solicitados. Se possível, narrem brevemente o que está sendo demonstrado. Verifiquem a qualidade do áudio e do vídeo.
* **Consultem a Documentação Oficial:** As documentações do ROS 2 Foxy, Nav2 e Docker são seus melhores amigos. Muitos problemas comuns e exemplos de configuração estão lá. Além disso recursos como vídeos e tutoriais como, [deste link](https://automaticaddison.com/the-ultimate-guide-to-the-ros-2-navigation-stack/), podem ser extremamente úteis.


Boa sorte!