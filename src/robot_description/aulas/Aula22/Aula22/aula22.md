# Aula 22 - Interagindo com Nav2

Neste exercício, vamos interagir com o stack de navegação do ROS 2 (Nav2) pelo terminal e através de Nós, enviando via código comandos de navegação.

## 1. Enviando comandos via terminal

### 1.1 Modificando parâmetros

Os parâmetros do **Nav2**, definidos no arquivo de configuração ```.yaml```, podem ser alterados depois que os nós já foram inicializados. Essa é uma ferramenta útil caso seja necessário mudar o comportamento do robô em diferentes situações, sem ser necessário recompilar e reiniciar todo o código. 


Essa mudança pode ser feita tanto através do terminal, pelo comando 

```bash
ros2 param set [nó] [parâmetro]
```

como também utilizando a interface de serviço ```rcl_interfaces/srv/SetParameters```

Infelizmente, nesta versão do ROS2 (**Foxy**), a mudança da maioria dos parâmetros não surge efeito diretamente ao ser requisitada. É necessário desativar e reativar o nó em questão. Isto pode ser feito através do ```lifecycle_node```, responsável pela gestão dos nós referentes ao **Nav2**. Por isso, neste exercício vamos apenas setar a posição inicial.

1. **Inicie a simulação**

    Assim como nas aulas anteriores, inicie a simulação do **turtlebot3**, mas não defina a posição inicial do robô.

2. **Defina a posição inicial via terminal**

    Veja qual é estrutura da interface usada pelo tópico ```/initialpose``` e publique uma mensagem com a posição inical do robô.

3. **Verifique a mudança**

    No **Rviz** veja se a posição inical do robô foi definida sem a necessidade de fazer manualmente pela interface gráfica.

### 1.2 Enviando comandos de navegação

Também é possível enviar comandos de navegação fora da interface visual do **Rviz**. Como este comando normalmente leva mais tempo a ser executado, ele é feito através de **açoes (actions)**

1. **Verifique a ação**

    Com a simulação do **turtlebot3** ainda em execução, veja como é estruturada a interface utilizada para envio de um objetivo de navegação:

    ```bash
    ros2 interface show nav2_msgs/action/NavigateToPose
    ```

1. **Envio de Objetivo (Goal)**

    Agora, utilize a estrutura da interface vista no item anterir e envie um comando de navegação através da ação ```/navigate_to_pose```

3. **Visualização**

    No **Rviz**, veja se o robô planejou o caminho até o ponto desejado e começou a navegação.

### 1.3 Comandos extras

Ao inicializar o stack de navegação (**Nav2**), diversos serviços e ações são disponibilizadas para interação, como limpar os mapas de custo, limpar ou replanejar rota, trocar o mapa carregado, entre outros. Você pode visualizar a lista completa através dos comandos:

```bash
ros2 action list
```

e

```bash
ros2 service list
```

## 2. Enviando comandos através de Nós

Além comandos via terminal, é possível interagir com o **Nav2** através de Nós, possibilitando automatizar tarefas que desejamos que o robô realize.

### Exercício:

Crie um nó que envie um comando de navegação. Uma vez alcançado o objetivo, ele deve retornar ao ponto inicial.

1. **Crie um novo pacote chamado ```rm_navigator``` para escrever o nó**

    ```bash
    ros2 pkg create rm_navigator --build-type ament_python --dependencies rclpy
    ```

2. **Crie arquivo do Nó**

    ```bash
    cd rm_navigator/rm_navigator
    touch navigator.py
    ```

3. **Escreva o código**

    No arquivo recém criado, escreva o nó que realize o trajeto desejado.

4. **Rode o Nó**

    Em um terminal, inicialize a simulação do **turtlebot3**. Em um segundo, rode o nó criado e veja, no **rviz**, se o robô executa corretamente o trajeto desejado.

    Lembre-se de adcionar o nó como executável no arquivo ```setup.py```.





