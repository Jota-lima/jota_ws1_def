# Ações (actions) no ROS2

Este roteiro guiará você na criação de uma action (server e client) em ROS2 usando Python e uma interface de ação customizada. Siga cada passo cuidadosamente para compreender o funcionamento de actions no ROS2.

**Sugestão de Leitura**:

- [Understanding Actions](https://docs.ros.org/en/foxy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)

- [Writing an action server and client (Python)](https://docs.ros.org/en/foxy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)

## 1. Criar um workspace 

1. Escolha um diretório em sua máquina para criar seu workspace. No exemplo, vamos usar ~/aula9_ws, mas você pode usar outro se preferir.

2. No terminal, crie o diretório e a pasta src dentro dele:

    ```bash
    mkdir -p ~/aula9_ws/src
    cd ~/aula9_ws
    ```

- No ROS2, o conceito de **workspace** é usado para organizar os pacotes e compilar o código utilizando ```colcon build```.

- A pasta ```src``` é o diretório padrão onde os pacotes ROS2 devem ficar dentro do **workspace**.

## 2. Copiar a estrutura do pacote ```custom_interfaces```

No arquivo ```.zip``` da aula, vocês encontrarão o pacote ```custom interfaces```. Este pacote será responsável por definir e agrupar as interfaces customizadas que você precisa para este exercício. Ele possui a seguinte estrutura:

```css
    custom_interfaces
    ├── package.xml
    ├── CMakeLists.txt
    └── action
        └── (pasta para arquivos .action)
```

Nele, os arquivos ```CMakeLists.txt``` e ```package.xml``` já estarão com as dependências configuradas para a instalação de interfaces customizadas para o ROS2. No diretório ```action```, serão colocadas as interfaces de ações customizadas, que possuem extensão ```.action```.

1. Copie o pacote ```custom_interfaces``` fornecido para dentro de ```~/aula9_ws/src```. Ao final, a estrutura do seu workspace deve ficar assim:

    ```css
    ros2_ws
    └── src
        ├── custom_interfaces
        │   ├── package.xml
        │   ├── CMakeLists.txt
        │   └── action
        │       └── ...
    ```

## 3. Criar uma interface de serviço customizada

1. Dentro do diretório ```action``` do pacote ```custom_interfaces```, crie um arquivo chamado ```Aula9.action```
    - Normalmente, o nome de interfaces são escritas com todos os nomes juntos, com a primeira letra de cada nome em letra maiúscula e finalizado com a extensão do tipo da interface, por exemplo: ```AçãoCustomizada.action```

2. Adicione o seguinte conteúdo ao arquivo:

    ![action interface](imagens/action_interface.png)

    A interface de uma ação é dividida da seguinte forma:

    - **Objetivo (Goal)**: Composto pelos primeiros valores a serem declarados, um em cada linha. Cada valor é declarado pelo seu tipo, seguido do nome.

    - **Resultado (result)**: Valores enviados como resposta após a conclusão da ação.

    - **Feedback**: Mensagem parcial enviada durante a execução da ação

    - **Separador**: Resposável por separar, na interface, quais valores são parte do objetivo, feedback e resultado. O formato dele são três hífens seguidos: ```---```

    Neste caso, a ação receberá um inteiro (```count_up_to```) como objetivo, enviará um inteiro (```current_number```) como feedback, e, ao final, retornará um inteiro (```final_count```) como resultado.

3. No arquivo ```CMakeLists.txt```, declare a interface recém criada para ser instalada:

    ```bash
    rosidl_generate_interfaces(${PROJECT_NAME}
        "action/Aula9.action"
    )
    ```

## 4. Compilar o pacote ```custom_interfaces```

Agora vamos compilar o workspace para que o ROS2 gere as definições dessa nova interface de serviço.

1. No terminal, dentro de ```~/aula9_ws```, execute:

    ```bash
    colcon build
    ```

2. Em seguida, atualize o ambiente:

    ```bash
    source install/setup.bash
    ```

3. Verifique se a interface está disponível. No terminal, execute:

    ```bash
    ros2 interface list
    ```

    E veja se a nova interface criada está entre as disponíveis

    Agora, veja se a interface corresponde à que foi criada:

    ```bash
    ros2 interface show custom_interfaces/action/Aula9
    ```

## 5. Criar um novo pacote Python

Vamos criar um novo pacote **python** do ROS2, dentro do diretório ```~/aula9_ws/src```, para criarmos os nodes desta aula. 

1. No terminal, digite:

```bash
cd ~/aula9_ws/src
ros2 pkg create aula9 --build-type ament_python --dependencies rclpy custom_interfaces
```

Este comando irá criar um novo pacote chamado ```aula9```. O argumento ```--build-type ament_python``` irá definir a estrutura do pacote como python. Já o argumento ```--dependencies rclpy custom_interfaces``` adiciona automaticamente as dependências indicadas ao arquivo ```package.xml```.

2. O pacote criado deve conter a seguinte estrutura:

    ```css
    aula9
    ├── package.xml
    ├── setup.py
    ├── resource
    │   └── aula9
    ├── setup.cfg
    └── aula9
        ├── __init__.py
    ````

Os nodes serão criados no diretório homônimo do pacote, neste caso ```aula9/aula9/```.

## 6. Criar o nó de um servidor de ação (action server) em ROS2

Vamos criar um script Python que atuará como servidor da ação (action server). Ele ficará “escutando” os objetivos (goals) solicitados, executará a ação, enviando feedback durante e, ao final, retornará o resultado.

1. Dentro do diretório ```aula9/aula9/```, crie um arquivo chamado ```action_server.py``` com o seguinte conteúdo: 

    ![action_server](imagens/action_server.png)

### Explicação do código

O código define um Action Server em ROS2 que recebe uma meta (goal), conta até um número especificado e envia feedback periódico enquanto conta. Ao final, retorna o resultado da contagem.

**1. Importações**

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from custom_interfaces.action import Aula9
import time
```

- ```rclpy```: Biblioteca principal do ROS2 para Python.

- ```rclpy.node.Node```: Classe base para criar nós ROS2.

- ```rclpy.action.ActionServer```: Classe que permite criar um Action Server.

- ```custom_interfaces.action.Aula9```: Importa a interface da ação personalizada (Aula9.action), que contém a definição da ação (Goal, Feedback e Result).

- ```time```: Usado para criar uma pausa (time.sleep(1)) entre cada iteração da contagem.

**2. Definição do Nó do Servidor**

```python
class ActionServerNode(Node):
    def __init__(self):
        super().__init__('aula9_action_server')
        self.action_server = ActionServer(
            self, 
            Aula9, 
            'aula9_action', 
            self.my_action_callback
        )
```

- ```class ActionServerNode(Node)``` → Cria uma classe chamada ActionServerNode, que herda de Node, tornando-a um nó ROS2.

- ```super().__init__('aula9_action_server')``` → Inicializa o nó com o nome 'aula9_action_server'.

- **Criação do Action Server:**

    - ```self.action_server = ActionServer(...)``` cria um Action Server com os seguintes parâmetros:
        - ```self```: O nó onde o servidor será executado.
        - ```Aula9```: O tipo da ação, definido na interface .action.
        - ```'aula9_action'```: Nome do serviço de ação (é o nome que o cliente chamará para enviar um goal).
        - ```self.my_action_callback```: Função chamada quando uma meta (goal) é recebida.

**3. Callback da Ação**

```python
def my_action_callback(self, goal_handle):
    self.get_logger().info('Executing goal...')

    count_up_to = goal_handle.request.count_up_to
    current_number = 0

    while current_number < count_up_to:

        feedback_msg = Aula9.Feedback()
        feedback_msg.current_number = current_number
        goal_handle.publish_feedback(feedback_msg)
        self.get_logger().info(f'Publishing feedback: {current_number}')

        current_number += 1

        time.sleep(1)

    goal_handle.succeed()
    result = Aula9.Result()
    result.final_count = current_number
    self.get_logger().info('Goal succeeded!')
    return result
```

- ```my_action_callback(self, goal_handle)```
    - Função que executa a ação quando um cliente envia um goal.
    - ```goal_handle``` é o objeto que contém a requisição do cliente.

- Lê o valor do Objetivo (**Goal**):

    ```bash
    count_up_to = goal_handle.request.count_up_to
    ```
    - O cliente enviará um número como meta (```count_up_to```), que é o valor até onde o servidor deve contar.

- **Criação e envio de feedback**:

    ```bash
    feedback_msg = Aula9.Feedback()
    feedback_msg.current_number = current_number
    goal_handle.publish_feedback(feedback_msg)
    ```
    
    - Um objeto de feedback é criado e atualizado com ```current_number```.
    - O feedback é publicado para o cliente acompanhar o progresso.

- **Finaliza a ação com sucesso**:

    ```bash
    gal_handle.succeed()
    ```

    - Informa ao ROS2 que a meta foi atingida com sucesso.

- **Preenche e retorna o resultado**:

    ```bash
    result = Aula9.Result()
    result.final_count = current_number
    self.get_logger().info('Goal succeeded!')
    return result
    ```

    - Cria um objeto de resultado (result).
    - Define result.final_count como o número final contado.
    - Retorna ```result``` ao cliente

**4. Função principal (```main```)**:

```python
def main(args=None):
    rclpy.init(args=args)
    action_server = ActionServerNode()
    rclpy.spin(action_server)
    rclpy.shutdown()
```

- ```rclpy.init(args=args)``` → Inicializa o ROS2.

- ```action_server = ActionServerNode()``` → Cria uma instância do nó ActionServerNode, que inicia o servidor de ação.

- ```rclpy.spin(action_server)``` → Mantém o nó ativo para processar pedidos de clientes.

- ```rclpy.shutdown()``` → Finaliza o ROS2 quando o nó for encerrado.

### Resumo

1. O servidor é iniciado e fica aguardando goals.

2. Quando um cliente envia um goal:
    - O servidor começa a contar de ```0``` até ```count_up_to```.
    - A cada número contado, envia feedback ao cliente.
    - Aguarda 1 segundo entre cada incremento.

3. Quando o número final é atingido:
    - O servidor finaliza a ação com sucesso (```goal_handle.succeed()```).
    - Retorna ```result.final_count``` com o número final contado.

4. O nó continua rodando, pronto para receber novas metas.


## 7. Rodar o Servidor da Ação (action server)

1. Antes de rodar, edite o arquivo ```setup.py``` dentro de ```aula9```, para registrar este script como executável. Adicione em entry_points:

    ```python
    entry_points={
        'console_scripts': [
            'action_server = aula9.action_server:main',
        ],
    },
    ```

    Este passo é necessário sempre que um novo node for criado. O comando é estruturado da seguinte forma:
        
     - ```action_server```: Nome que será usado para execução do script

     - ```aula9```: Nome do pacote

     - ```action_server```: Nome do script em python a ser registrado

     - ```:main```: Função do script que será executada

2. Em um terminal, volte ao diretório raiz do workspace ```~/aula9_ws```, compile novamente e atualize o ambiente:

    ```bash
    colcon build
    source install/setup.bash
    ```

3. Agora, execute o serviço

    ```bash
    ros2 run aula9 action_server
    ````

## 8. Verificar se o action server está rodando pelo terminal

1. Em um novo terminal, sem intenrromper o anterior, atualize o ambiente com ```source install/setup.bash```

2. Liste os serviços disponíveis

    ```bash
    ros2 action list
    ``` 

    Você deve ver ```/aula9_action``` entre os serviços listados

3. Liste os nós ativos:

    ```bash
    ros2 node list
    ```

    Você deve ver ```/aula9_action_server``` entre os nodes listados

Com estes últimos passos é possível verificar a existência da ação, com a interface correta, e que o node está em execução.

### 9. Fazer uma chamada do serviço pelo terminal

Sem precisar criar um client em Python, podemos chamar a ação diretamente pelo terminal usando o comando ```ros2 action send_goal```.

1. No mesmo terminal onde você não está rodando o servidor (ou abra um terceiro terminal):

    ```bash
    ros2 action send_goal /aula9_action custom_interfaces/action/Aula9 "{count_up_to: 5}"
    ```

2. No terminal onde você digitou o comando, será exibido:

    ```bash 
    Waiting for an action server to become available...
    Sending goal:
        count_up_to: 5

    Goal accepted with ID: 88d788c4450245299e27ffbdb7d0b23e

    Result:
        final_count: 4

    Goal finished with status: SUCCEEDED
    ```

    ```ros2 service send_goal [ação] [interface] [goal]``` é uma ferramenta de linha de comando para enviar pedidos de serviço sem prcisar escrever o código de cliente. É um jeito simples de verificar se o servidor funciona.

## 10. Criar um cliente de ação (action client) em ROS2

Agora que verificamos que a ação funciona, vamos criar um **cliente (client)** em Python que envia a requisição para o nosso servidor.

1. Na pasta ```aula9/aula9```, crie um arquivo ```action_client.py``` e copie o código abaixo.

![action client](imagens/action_client.png)

### Explicação do código

O código define um Action Client em ROS2 que envia uma meta (goal) para o servidor, recebe feedback contínuo e imprime o resultado final quando a ação termina.

**1. Importação das bibliotecas**

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from custom_interfaces.action import Aula9
import sys
```

- ```rclpy```: Biblioteca principal do ROS2 para Python.

- ```rclpy.node.Node```: Classe base para criar nós ROS2.

- ```rclpy.action.ActionClient```: Classe que permite criar um Action Client.

- ```custom_interfaces.action.Aula9```: Importa a interface de ação (```Aula9.action```), que contém a definição da ação (Goal, Feedback e Result).

- ```sys```: Permite capturar argumentos passados pelo terminal (por exemplo, o número até o qual contar).

**2. Definição do Nó do Clente**

```python
class ActionClientNode(Node):
    def __init__(self):
        super().__init__('action_client')
        self.action_client = ActionClient(self, Aula9, 'aula9_action')
```

- ```class ActionClientNode(Node)``` → Define um nó chamado ```ActionClientNode```, que herda de ```Node```, tornando-o um nó ROS2.

- ```super().__init__('action_client')``` → Inicializa o nó com o nome 'action_client'.

- Criação do Action Client:

    - ```self.action_client = ActionClient(...)``` cria um cliente para enviar metas ao servidor.

    - ```Aula9```: Tipo da ação, definido na interface .action.

    - ```'aula9_action'```: Nome do Action Server que será chamado.

**3. Enviar um objetivo (goal)**

```python
def send_goal(self, count_up_to):
    self.get_logger().info('Sending goal...')
    goal_msg = Aula9.Goal()
    goal_msg.count_up_to = count_up_to

    self.action_client.wait_for_server()

    self.send_goal_future = self.action_client.send_goal_async(
        goal_msg, 
        feedback_callback=self.feedback_callback
    )
    self.send_goal_future.add_done_callback(self.goal_response_callback)
```

- **Cria a mensagem do objetivo**:

    ```bash
    goal_msg = Aula9.Goal()
    goal_msg.count_up_to = count_up_to
    ```

- **Aguarda o servidor estar disponível**:

    ```bash
    self.action_client.wait_for_server()
    ```
    - Se o servidor não estiver rodando, espera até que ele fique disponível.

- **Envia a meta de forma assíncrona**:

    ```bash
    self.send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
    ```
    
    - A meta é enviada ao servidor de forma assíncrona.
    
    - Se a meta for aceita, o servidor começa a processar a contagem.
    
    - Define ```feedback_callback``` para lidar com feedbacks durante a execução.

- **Aguarda a resposta do servidor**:

    ```bash
    self.send_goal_future.add_done_callback(self.goal_response_callback)
    ```

    - Quando o servidor aceita ou rejeita a meta, chama ```goal_response_callback```.

**4. Resposta do Servidor**

```python 
def goal_response_callback(self, future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        self.get_logger().info('Goal rejected')
        return

    self.get_logger().info('Goal accepted')
    self.get_result_future = goal_handle.get_result_async()
    self.get_result_future.add_done_callback(self.get_result_callback)
```

- **Recebe a resposta do servidor (```future.result()```) e armazena em ```goal_handle```**.

- **Se a meta for rejeitada, imprime**:

    ```bash
    if not goal_handle.accepted:
        self.get_logger().info('Goal rejected')
        return
    ```

- **Se a meta for aceita, imprime e aguarda o resultado final**:
    ```bash
    self.get_logger().info('Goal accepted')
    self.get_result_future = goal_handle.get_result_async()
    self.get_result_future.add_done_callback(self.get_result_callback)
    ```

    - O cliente aguarda a finalização do servidor.

    - Quando o servidor finaliza, ```get_result_callback``` é chamado.

**5. Recebendo o Feedback**

```python
def feedback_callback(self, feedback_msg):
    feedback = feedback_msg.feedback
    self.get_logger().info(f'Received feedback: {feedback.current_number}')
```

- **Recebe um feedback do servidor durante a execução**.

- **Extrai a informação do número atual contado (```current_number```)**.

- **Imprime o feedback**.

**6. Processando o resultado final**

```python
def get_result_callback(self, future):
    result = future.result().result
    self.get_logger().info(f'Final Result: {result.final_count}')
    rclpy.shutdown()
```

- **Aguarda o resultado final do servidor (```future.result().result```)**.

- **Imprime o número final contado**:

    ```python
    self.get_logger().info(f'Final Result: {result.final_count}')
    ```

- **Finaliza o nó**:

    ```pyhton
    rclpy.shutdown()
    ```

    - Depois que o resultado final é recebido, o nó encerra.

**7. Função Principal (```main```)**

```python
def main(args=None):
    rclpy.init(args=args)
    action_client = ActionClientNode()
    action_client.send_goal(int(sys.argv[1]))
    rclpy.spin(action_client)
```

- **Inicializa o ROS2**:

```python 
rclpy.init(args=args)
```

- **Cria o cliente**:

    ```python
    action_client = ActionClientNode()
    ```

- **Envia o objetivo como valor fornecido via terminal**:

    ```python
    action_client.send_goal(int(sys.argv[1]))
    ```

- **Mantém o cliente rodando para processar feedbacks**:

    ```python 
    rclpy.spin(action_client)
    ````

### Resumo geral

- O cliente se comunica com o servidor, enviando e recebendo metas.

- Monitora o progresso da execução via feedback.

- Recebe e exibe o resultado final após a conclusão da ação.

- Finaliza automaticamente após a execução.

## 11. Rodar o Cliente da Ação (action client)

1. Veja se nenhum terminal está executando algum node, caso esteja, interrompa-o.

2. Assim como o servidor, adicione este node como executável no arquivo ```setup.py```:

    ```python 
    entry_points={
        'console_scripts': [
            'action_server = aula9.action_server:main',
            'action_client = aula9.action_client:main',
        ],
    },
    ```
3. Em um terminal, volte ao diretório raiz do workspace ```~/aula9_ws```, compile novamente e atualize o ambiente:

    ```bash
    colcon build
    source install/setup.bash
    ```

4. Agora, execute a cliente

    ```bash
    ros2 run aula9 action_client count_up_to
    ````

    Substituindo os argumentos **count_up_to** pelo número que deseja fazer a contagem.

    Você deve ver algo no terminal como:

    ```bash
    [INFO] [1740333773.741903943] [action_client]: Sending goal...
    ```

## 12. Rodar o servidor em outro terminal

1. Abra outro terminal e rode o **servidor** novamente:

    ```bash
    ros2 run aula8 srv_server
    ```

2. Assim que o server iniciar, o client (no outro terminal) deve detectar a ação e enviar o objetivo.

3. No terminal do client, aparecerá algo como:

    ```bash
    [INFO] [1740334386.396987461] [action_client]: Sending goal...
    [INFO] [1740334390.931664366] [action_client]: Goal accepted
    [INFO] [1740334390.945446241] [action_client]: Received feedback: 0
    [INFO] [1740334391.947944393] [action_client]: Received feedback: 1
    [INFO] [1740334392.950042569] [action_client]: Received feedback: 2
    [INFO] [1740334393.954835811] [action_client]: Received feedback: 3
    [INFO] [1740334394.957405174] [action_client]: Received feedback: 4
    [INFO] [1740334395.961401636] [action_client]: Final Result: 5
    ```

## Exercício de fixação

### Objetivo Geral

**Criar uma action** (server e client) capaz de mover o robô diferencial até atingir uma distância específica de deslocamento (por exemplo, X metros para frente ou para trás), enviando feedback periódico sobre o progresso e permitindo cancelamento.

### Passos sugeridos:

1. Criar uma interface de ação customizada, contendo pelo menos as seguintes informações:

    **Goal**:
    
    - **distance (float64)**: Distância linear a ser percorrida.

    - **speed (float64)**: Velocidade linear desejada do robô.

    **Result**

    - **success (bool)**: Booleano indicando o sucesso da tarefa.

    - **message (string)**: Indica o que occoreu para finalização da ação.

    **Feedback**

    - **current_distance (float64)**: Distância percorrida.

2. Criar um Action server que:

    - Assina o tópico ```/odom``` para acompanhar a posição inicial e o quanto já se deslocou.

    - Ao receber uma goal, registra a posição inicial do robô (por exemplo, ```x0```, ```y0```).

    - Publica em ```/cmd_vel``` para mover o robô na direção solicitada.

    - Durante o deslocamento, envia feedback constante com a distância atual percorrida.

    - Ao atingir a distância desejada (ou próximo a ela), para o robô e retorna ```success=true```.

3. Criar o Action Client que:

    - Envia uma meta com a distância e velocidade desejadas.

    - Recebe feedback periódico (imprime a distância percorrida no terminal, por exemplo).

    - Ao final, mostra se concluiu com sucesso ou se foi cancelado.

## Conclusão

Nesta aula você criou e testou uma action em ROS2 do zero:

1. Definiu um pacote de interfaces customizadas (custom_interfaces) e compilou para gerar a interface de ação (Aula9.action).


2. Criou um pacote Python (aula9) com o código do action server e do action client.

3. Executou e validou a comunicação: envio de metas, recepção de feedback e resultado final.

**Actions** são muito úteis em ROS2 quando precisamos de tarefas de longa duração ou feedback contínuo (como navegação, movimentação de manipuladores robóticos ou cálculos prolongados). Esse é o grande diferencial em relação a Services, que tratam requisições rápidas e pontuais sem acompanhamento de progresso.

