# Mensagens Customizadas, Publishers e Subscribers

Neste exercício, você irá:

- Criar um workspace ROS2;
- Criar um pacote para interfaces customizadas.
- Criar um pacote para os nós em Python.
- Escrever dois nós: um publisher e um subscriber, utilizando a mensagem customizada.
- (Exercício Extra) Publicar velocidades em cmd_vel e ler odometria em /odom.

## 1. Criar um workspace 

1. Escolha um diretório em sua máquina para criar seu workspace. No exemplo, vamos usar ~/aula7_ws, mas você pode usar outro se preferir.

2. No terminal, crie o diretório e a pasta src dentro dele:

    ```bash
    mkdir -p ~/aula7_ws/src
    cd ~/aula7_ws
    ```

- No ROS2, o conceito de **workspace** é usado para organizar os pacotes e compilar o código utilizando ```colcon build```.

- A pasta ```src``` é o diretório padrão onde os pacotes ROS2 devem ficar dentro do **workspace**.

## 2. Copiar a estrutura do pacote ```custom_interfaces```

No arquivo ```.zip``` da aula, vocês encontrarão o pacote ```custom interfaces```. Este pacote será responsável por definir e agrupar as interfaces customizadas que você precisa para este exercício. Ele possui a seguinte estrutura:

```css
    custom_interfaces
    ├── package.xml
    ├── CMakeLists.txt
    └── msg
        └── (pasta para arquivos .msg)
```

Nele, os arquivos ```CMakeLists.txt``` e ```package.xml``` já estarão com as dependências configuradas para a instalação de interfaces customizadas para o ROS2. No diretório ```msg```, serão colocadas as interfaces de ações customizadas, que possuem extensão ```.msg```.

1. Copie o pacote ```custom_interfaces``` fornecido para dentro de ```~/aula7_ws/src```. Ao final, a estrutura do seu workspace deve ficar assim:

    ```css
    ros2_ws
    └── src
        ├── custom_interfaces
        │   ├── package.xml
        │   ├── CMakeLists.txt
        │   └── msg
        │       └── ...
    ```

## 3. Criar uma interface de serviço customizada

1. Dentro do diretório ```msg``` do pacote ```custom_interfaces```, crie um arquivo chamado ```Aula7.msg```
    - Normalmente, o nome de interfaces são escritas com todos os nomes juntos, com a primeira letra de cada nome em letra maiúscula e finalizado com a extensão do tipo da interface, por exemplo: ```MensagemCustomizada.msg```

2. Adicione o seguinte conteúdo ao arquivo:

    ![message interface](imagens/msg.png)

    A interface de uma mensagem é composta pelas informações que você deseja transportar, sendo definida pelo tipo da mensagem (int64, float32, string, etc) e pelo nome da variável que irá guardar a informação.

    Neste caso, a mensagem será composta por:
    - ```count```: do tipo ```int32```
    - ```menssage```: do tipo ```string```

3. No arquivo ```CMakeLists.txt```, declare a interface recém criada para ser instalada:

    ```bash
    rosidl_generate_interfaces(${PROJECT_NAME}
        "msg/Aula7.msg"
    )
    ```

## 4. Compilar o pacote ```custom_interfaces```

Agora vamos compilar o workspace para que o ROS2 gere as definições dessa nova mensagem.

1. No terminal, dentro de ```~/aula7_ws```, execute:

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
    ros2 interface show custom_interfaces/msg/Aula7
    ```

## 5. Criar um novo pacote Python

Vamos criar um novo pacote **python** do ROS2, dentro do diretório ```~/aula7_ws/src```, para criarmos os nodes desta aula. 

1. No terminal, digite:

```bash
cd ~/aula7_ws/src
ros2 pkg create aula7 --build-type ament_python --dependencies rclpy custom_interfaces
```

Este comando irá criar um novo pacote chamado ```aula7```. O argumento ```--build-type ament_python``` irá definir a estrutura do pacote como python. Já o argumento ```--dependencies rclpy custom_interfaces``` adiciona automaticamente as dependências indicadas ao arquivo ```package.xml```.

2. O pacote criado deve conter a seguinte estrutura:

    ```css
    aula7
    ├── package.xml
    ├── setup.py
    ├── resource
    │   └── aula7
    ├── setup.cfg
    └── aula7
        ├── __init__.py
    ````

Os nodes serão criados no diretório homônimo do pacote, neste caso ```aula7/aula7/```.

## 4. Criando um Publisher

Vamos criar um script Python (**Node**) que irá conter um **Publisher**. Ele será responsável por publicar (enviar) a mensagem ao tópico.

1. Na pasta ```aula7/aula7```, crie um arquivo ```publisher.py``` e copie o código abaixo.

![publisher](imagens/publisher.png)


### Explicação do código

O código define um nó ROS2 que publica mensagens periodicamente em um tópico chamado **aula7_topic**. Ele cria e envia mensagens do tipo **Aula7**, contendo um contador que se incrementa a cada segundo.

**1. Importações**

```python
import rclpy
from rclpy.node import Node
from custom_interfaces.msg import Aula7
```

- ```rclpy```: Biblioteca principal do ROS2 para Python.

- ```rclpy.node.Node```: Classe base para criar nós ROS2.

- ```custom_interfaces.msg.Aula7```: Importa a mensagem personalizada **Aula6**, que contém os campos definidos no arquivo ```.msg```.

**2. Definição do Nó do Publisher**

```python
class Publisher(Node):
    def __init__(self):
        super().__init__('aula7_publisher')
        self.publisher = self.create_publisher(Aula7, 'aula7_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.contador = 0
```

- ```class Publisher(Node)``` → Cria uma classe chamada Publisher, que herda de Node, tornando-a um nó ROS2.

- ```super().__init__('aula7_publisher')``` → Inicializa o nó com o nome 'aula7_publisher'.

- **Criação do Publisher**:

    - ```self.create_publisher(...)``` → Cria um publicador para enviar mensagens do tipo ```Aula7``` no tópico ```aula7_topic```.
	
    - ```10``` → Define o tamanho da fila de mensagens não entregues.

- ```self.create_timer(1.0, self.timer_callback)``` → Configura um temporizador que chama a função ```timer_callback``` a cada 1 segundo.

**3. Callback do Timer**

```python
def timer_callback(self):
        self.contador +=1
        msg = Aula7()
        msg.count = self.contador
        msg.message = 'A contagem é: ' 
        self.publisher.publish(msg)
        self.get_logger().info('Publicando: "%s%i"' % (msg.message, msg.count))
```

- **Cria uma nova mensagem do tipo Aula7**:

    ```python
    msg = Aula7()
    ```
    - Instancia um objeto da mensagem Aula6.

- **Define os valores da mensagem**:

    ```python
    msg.count = self.contador
    msg.message = 'A contagem é: '
    ```

    - O campo contagem recebe o valor atualizado do contador.

	- O campo mensagem recebe um texto fixo.
    
- **Publica a mensagem**:

    ```python
    self.publisher.publish(msg)
    ```

    - Envia a mensagem para o tópico aula7_topic.

**4. Função Principal (```main```)

```python
def main(args=None):
    rclpy.init(args=args)
    publisher = Publisher()
    rclpy.spin(publisher)
    rclpy.shutdown()
```

- **Inicializa o ROS2**:

    ```python
    rclpy.init(args=args)
    ```
    - Prepara o ROS2 para rodar.

- **Cria uma instância do nó**:

    ```python
    publisher = Publisher()
    ```

- **Mantém o nó rodando**:

    ```python
    rclpy.spin(publisher)
    ```

- **Finaliza o nó quando ele for interrompido**:

    ```python
    rclpy.shutdown()
    ```

### Resumo

1.	O nó publicador (Publisher) é criado.

2.	A cada 1 segundo, ele:

    - Incrementa o contador.
	
    - Cria e publica uma mensagem com a contagem no tópico aula7_topic.
	
    - Exibe a mensagem no log.
	
3.	O nó fica rodando até ser interrompido.

## 5. Execultar o nó com o publisher

1. Antes de rodar, edite o arquivo ```setup.py``` dentro de ```aula7```, para registrar este script como executável. Adicione em entry_points:

    ```python
    entry_points={
        'console_scripts': [
            'publisher = aula7.publisher:main',
        ],
    },
    ```

    Este passo é necessário sempre que um novo node for criado. O comando é estruturado da seguinte forma:
        
     - ```publisher```: Nome que será usado para execução do script

     - ```aula7```: Nome do pacote

     - ```publisher```: Nome do script em python a ser registrado

     - ```:main```: Função do script que será executada

2. Em um terminal, volte ao diretório raiz do workspace ```~/aula7_ws```, compile novamente e atualize o ambiente:

    ```bash
    colcon build
    source install/setup.bash
    ```

3. Agora, execute o serviço

    ```bash
    ros2 run aula7 publisher
    ````

## 6. Verificar pelo terminal se o publisher está rodando

1. Em um novo terminal, sem intenrromper o anterior, atualize o ambiente com ```source install/setup.bash```

2. Liste os nós ativos:

    ```bash
    ros2 node list
    ```

    Você deve ver ```/aula7_publisher``` entre os nodes listados

3. Veja qual é o tipo da interface do publisher criado:

    ```bash
    ros2 action type /aula7_publisher
    ```

    Este comando deve retornar ```custom_interfaces/msg/Aula7```

4. Veja o que está sendo publicado no tópico ```aula7_topic``` pelo terminal:

    ```bash
    ros2 topic echo /aula7_topic
    ```

## 7. Criando um subscriber

O processo de criar um **subscriber** é bem similar ao de um **publisher**. Ele será o responsável por receber as mensagens publicadas em um tópico.

1. Na pasta ```aula7/aula7```, crie um arquivo ```subscriber.py``` e copie o código abaixo.

![subscriber](imagens/subscriber.png)

### Explicação do código

O código define um nó com um **subscriber** que recebe mensagens de um tópico chamado **aula7_topic**. Ele escuta mensagens do tipo **Aula7** e exibe os valores recebidos no terminal.

**1. Importações**

```python
import rclpy
from rclpy.node import Node
from custom_interfaces.msg import Aula6
```

- ```rclpy```: Biblioteca principal do ROS2 para Python.

- ```rclpy.node.Node```: Classe base para criar nós ROS2.

- ```custom_interfaces.msg.Aula7```: Importa a mensagem personalizada **Aul7**, que contém os campos definidos no arquivo ```.msg```.

**2. Definição do Nó do Subscriber**

```python
class Subscriber(Node):
    def __init__(self):
        super().__init__('aula7_subscriber')
        self.subscription = self.create_subscription(Aula7, 'aula7_topic', self.subscription_callback, 10)
```

- ```class Subscriber(Node)``` →  Cria uma classe chamada Subscriber, que herda de Node, tornando-a um nó ROS2.

- ```super().__init__('aula7_subscriber')``` → Inicializa o nó com o nome 'aula7_subscriber'.

- **Criação do Subscriber**:

    - ```self.create_subscription(...)``` → Cria um subscriber que:
	
        - Escuta mensagens do tipo ```Aula7```.
	    
        - Se inscreve no tópico ```aula7_topic```.
	    
        - Executa a função ```self.subscription_callback``` sempre que uma nova mensagem for recebida.
	
        - Usa um tamanho de fila de ```10```, ou seja, pode armazenar até 10 mensagens antes de processá-las.

**3. Callback do Subscriber**

```python
def subscription_callback(self, msg):
    mensagem = msg.message
    contagem = msg.count
    self.get_logger().info('Recebendo: "%s%i"' % (mensagem, contagem))
```

- ```def subscription_callback(self, msg)```: → Função chamada sempre que o nó recebe uma mensagem no tópico ```aula7_topic```. A mensagem recebida é armazenada na variável ```msg```.

- **Lê os valores da mensagem recebida**:

    ```python
    mensagem = msg.message
    contagem = msg.count
    ```

**4. Função Principal (```main```)**

```python
def main(args=None):
    rclpy.init(args=args)
    subscriber = Subscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()
```

- **Inicializa o ROS2**:

    ```python
    rclpy.init(args=args)
    ```
    - Prepara o ROS2 para rodar.

- **Cria uma instância do nó**:

    ```python
    subscriber = Subscriber()
    ```

- **Mantém o nó rodando**:

    ```python
    rclpy.spin(subscriber)
    ```

- **Finaliza o nó quando ele for interrompido**:

    ```python
    rclpy.shutdown()
    ```

### Resumo

1.	O Subscriber é criado e se inscreve no tópico ```aula7_topic```.

2.	Quando uma nova mensagem é publicada nesse tópico:

    - A função subscription_callback é chamada.
	
    - A mensagem é lida e seus valores são armazenados.
	
    - Os dados são exibidos no terminal.
	
3.	O nó fica rodando até ser interrompido.

## 8. Execultar o nó com o subscriber

1. Antes de rodar, edite o arquivo ```setup.py``` dentro de ```aula7```, para registrar este script como executável. Adicione em entry_points:

    ```python
    entry_points={
        'console_scripts': [
            'publisher = aula7.publisher:main',
            'subscriber = aula7.subscriber:main',
        ],
    },
    ```

    Este passo é necessário sempre que um novo node for criado. O comando é estruturado da seguinte forma:
        
     - ```subscriber```: Nome que será usado para execução do script

     - ```aula7```: Nome do pacote

     - ```subscriber```: Nome do script em python a ser registrado

     - ```:main```: Função do script que será executada

2. Em um terminal, volte ao diretório raiz do workspace ```~/aula7_ws```, compile novamente e atualize o ambiente:

    ```bash
    colcon build
    source install/setup.bash
    ```

3. Agora, execute o node

    ```bash
    ros2 run aula7 subscriber
    ````

## 9. Verificar pelo terminal se o subscriber está rodando

1. Em um novo terminal, sem interromper o anterior, atualize o ambiente com ```source install/setup.bash```

2. Liste os nós ativos:

    ```bash
    ros2 node list
    ```

    Você deve ver ```/aula7_subscriber``` entre os nodes listados

3. Rode novamento o nó do publisher:

    ```bash
    ros2 run aula7 publisher
    ```

4. Agora você deve ver o subscriber recebendo as mensagens enviadas pelo publisher e imprimindo elas no terminal.

5. Em um terceiro terminal, abra o ```rqt_graph``` e veja a comunicação entre os nodes.

## 6. Exercício de fixação

Neste exercício vamos aplicar os conhecimentos adquiridos durante a aula em uma aplicação mais real, interagindo com a simulação desenvolvida nas últimas aulas.

### Objetivo

Criar um node que faça com que o robô diferencial simulado fique repetidamente realizando um quadrado de lado 5m, para isso, o node deverá subscrever no tópico ```/odom``` e publicar no tópico ```/cmd_vel```.

### Etapas

- Crie um novo pacote chamado ```ros_exercises``` no mesmo diretório de ```robot_description```.

- Em ```ros_exercises``` crie o node ```square.py```.

- Compile e teste o código

### Dicas

- Sempre que compilar o código ou abrir um novo terminal, não se esqueça de carregar as variáveis de ambiente.

- Não se esqueça de configurar os arquivos ```package.xml``` e ```setup.py```

- Não tente fazer o node inteiro de uma vez, isso dificulta o debbuging. Adicione e teste parte por parte o seu código, verificando se o resultado está saindo como o esperado.

