# Serviços (services) no ROS2

Este roteiro guiará você na criação de um serviço (server e client) em ROS2 usando Python e uma interface de serviço customizada. Siga cada passo cuidadosamente para compreender o funcionamento de services no ROS2.

## 1. Criar um workspace 

1. Escolha um diretório em sua máquina para criar seu workspace. No exemplo, vamos usar ~/aula8_ws, mas você pode usar outro se preferir.

2. No terminal, crie o diretório e a pasta src dentro dele:

    ```bash
    mkdir -p ~/aula8_ws/src
    cd ~/aula8_ws
    ```

- No ROS2, o conceito de **workspace** é usado para organizar os pacotes e compilar o código utilizando ```colcon build```.

- A pasta ```src``` é o diretório padrão onde os pacotes ROS2 devem ficar dentro do **workspace**.


## 2. Copiar a estrutura do pacote ```custom_interfaces```

No arquivo ```.zip``` da aula, vocês encontrarão o pacote ```custom interfaces```. Este pacote será responsável por definir e agrupar as interfaces customizadas que você precisa para este exercício. Ele possui a seguinte estrutura:

```css
    custom_interfaces
    ├── package.xml
    ├── CMakeLists.txt
    └── srv
        └── (pasta para arquivos .srv)
```

Nele, os arquivos ```CMakeLists.txt``` e ```package.xml``` já estarão com as dependências configuradas para a instalação de interfaces customizadas para o ROS2. No diretório ```srv```, serão colocadas as interfaces de serviços customizados, que possuem extensão ```.srv```.

1. Copie o pacote ```custom_interfaces``` fornecido para dentro de ```~/aula8_ws/src```. Ao final, a estrutura do seu workspace deve ficar assim:

    ```css
    ros2_ws
    └── src
        ├── custom_interfaces
        │   ├── package.xml
        │   ├── CMakeLists.txt
        │   └── srv
        │       └── ...
    ```

## 3. Criar uma interface de serviço customizada

1. Dentro do diretório ```srv``` do pacote ```custom_interfaces```, crie um arquivo chamado ```Aula8.srv```
    - Normalmente, o nome de interfaces são escritas com todos os nomes juntos, com a primeira letra de cada nome em letra maiúscula e finalizado com a extensão do tipo da interface, por exemplo: ```ServicoCustomizado.srv```

2. Adicione o seguinte conteúdo ao arquivo:

    ![service interface](imagens/srv_interface.png)

    A interface de um serviço é dividida da seguinte forma:
    - **Requisição (request)**: Composta pelos primeiros valores a serem declarados, um em cada linha. Cada valor é declarado pelo seu tipo, seguido do nome.

    - **Separador**: Resposável por separar, na interface, quais valores são parte da requisição e quias são parte da resposta. O formato dele são três hífens seguidos: ```---```

    - **Resposta (response)**: Composta pelos valores definidos após o separador.

    Neste caso, o serviço recebera dois números inteiros ```a``` e ```b```. A resposta também será o inteiro ```sum```.

3. No arquivo ```CMakeLists.txt```, declare a interface recém criada para ser instalada:

    ```bash
    rosidl_generate_interfaces(${PROJECT_NAME}
        "srv/Aula8.srv"
    )
    ```

## 4. Compilar o pacote ```custom_interfaces```

Agora vamos compilar o workspace para que o ROS2 gere as definições dessa nova interface de serviço.

1. No terminal, dentro de ```~/aula8_ws```, execute:

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
    ros2 interface show custom_interfaces/srv/Aula8
    ```

## 5. Criar um novo pacote Python

Vamos criar um novo pacote **python** do ROS2, dentro do diretório ```~/aula8_ws/src```, para criarmos os nodes desta aula. 

1. No terminal, digite:

```bash
cd ~/aula8_ws/src
ros2 pkg create aula8 --build-type ament_python --dependencies rclpy custom_interfaces
```

Este comando irá criar um novo pacote chamado ```aula8```. O argumento ```--build-type ament_python``` irá definir a estrutura do pacote como python. Já o argumento ```--dependencies rclpy custom_interfaces``` adiciona automaticamente as dependências indicadas ao arquivo ```package.xml```.

2. O pacote criado deve conter a seguinte estrutura:

    ```css
    aula8
    ├── package.xml
    ├── setup.py
    ├── resource
    │   └── aula8
    ├── setup.cfg
    └── aula8
        ├── __init__.py
    ````

Os nodes serão criados no diretório homônimo do pacote, neste caso ```aula8/aula8```.

## 6. Criar o nó de um servidor de serviço (service server) em ROS2

Vamos criar um script Python que atuará como servidor do serviço (service server). Ele ficará “escutando” chamadas de serviço e processará as requisições.

1. Dentro do diretório ```aula8/aula8/```, crie um arquivo chamado ```srv_server.py``` com o seguinte conteúdo: 

    ![srv_server](imagens/srv_server.png)

### Explicação do código

**1. Importações**

- ```import rclpy``` e ```from rclpy.node import Node```: Importamos as bibliotecas principais do ROS2 em Python.

- ```from custom_interfaces.srv import Aula8```: Importamos nossa interface de serviço, que contém as definições dos campos de requisição e resposta.

**2. Classe ```SrvServer```**

- ```class SrvServer(Node)```: Declaramos uma classe que herda de ```Node```, que é a estrutura básica para qualquer nó em ROS2. Ao inicializar, chamamos o construtor de ```Node``` passando ```aula8_srv_server``` como nome do nó.

- ```self.srv_server = self.create_service(Aula8, 'aula8_srv', self.srv_callback)```: Criamos um servidor de serviço (service server):
    - **Tipo de serviço**: ```Aula8```.

    - **Nome do serviço**: ```'aula8_srv'```.

    - **Callback**: ```self.srv_callback```, função responsável por lidar com os pedidos de serviço que chegarem.

**3. Callback ```srv_callback```**

- ```def srv_callback(self, request, response):```: Esta função é executada toda vez que alguém chama o serviço ```'aula8_srv'```.

- ```request.a``` e ```request.b``` são os valores inteiros enviados pelo cliente.

- ```response.sum = request.a + request.b```: Definimos o valor de ```sum``` para a soma dos valores recebidos.

- ```return response```: Retornamos a resposta com o campo ```sum``` preenchido.

**4. Função principal ```main```**

- ```rclpy.init(args=args)```: Inicializa o sistema de comunicação ROS2 em Python.

- ```srv_server = SrvServer()```: Cria instancia o nó.

- ```rclpy.spin(srv_server)```: Mantém o nó em execução, ouvindo e processando requisições de serviço até que seja interrompido (por exemplo, com ```Ctrl+C```).

- ```rclpy.shutdown()```: Finaliza de forma limpa o ROS2 após a interrupção do spin.

Em resumo, este **service server** fica “escutando” o tópico de serviço ```aula8_srv```. Quando um client enviar uma requisição (com dois valores ```a``` e ```b```), o servidor chamará a função de callback, fará o processamento (neste caso, soma) e enviará a resposta (```response.sum```).

## 7. Rodar o Servidor do Serviço (service server)

1. Antes de rodar, edite o arquivo ```setup.py``` dentro de ```aula8```, para registrar este script como executável. Adicione em entry_points:

    ```python
    entry_points={
        'console_scripts': [
            'srv_server = aula8.srv_server:main',
        ],
    },
    ```

    Este passo é necessário sempre que um novo node for criado. O comando é estruturado da seguinte forma:
        
     - ```srv_server```: Nome que será usado para execução do script

     - ```aula8```: Nome do pacote

     - ```srv_server```: Nome do script em python a ser registrado

     - ```:main```: Função do script que será executada

2. Em um terminal, volte ao diretório raiz do workspace ```~/aula8_ws```, compile novamente e atualize o ambiente:

    ```bash
    colcon build
    source install/setup.bash
    ```

3. Agora, execute o serviço

    ```bash
    ros2 run aula8 srv_server
    ````

## 8. Verificar se o service server está rodando pelo terminal

1. Em um novo terminal, sem interromper o anterior, atualize o ambiente com ```source install/setup.bash```

2. Liste os serviços disponíveis

    ```bash
    ros2 service list
    ``` 

    Você deve ver ```/aula8_srv``` entre os serviços listados

3. Liste os nós ativos:

    ```bash
    ros2 node list
    ```

    Você deve ver ```/aula8_srv_server``` entre os nodes listados

Com estes últimos passos é possível verificar a existência do serviço, com a interface correta, e que o node está em execução

### 9. Fazer uma chamada do serviço pelo terminal

Sem precisar criar um client em Python, podemos chamar o serviço diretamente pelo terminal usando o comando ```ros2 service call```.

1. No mesmo terminal onde você não está rodando o servidor (ou abra um terceiro terminal):

    ```bash
    ros2 service call /aula8_srv custom_interfaces/srv/Aula8 "{a: 2, b: 3}"
    ```

2. No terminal onde você digitou o comando, será exibido:

    ```bash 
    response:
    custom_interfaces.srv.Aula8_Response(sum=5)
    ```

    ```ros2 service call [serviço] [interface] [requisição]``` é uma ferramenta de linha de comando para enviar pedidos de serviço sem prcisar escrever o código de cliente. É um jeito simples de verificar se o servidor funciona.

## 10. Criar um cliente de serviço (service client) em ROS2

Agora que verificamos que o servidor funciona, vamos criar um **cliente (client)** em Python que envia a requisição para o nosso servidor.

1. Na pasta ```aula8/aula8```, crie um arquivo ```srv_client.py``` e copie o código abaixo.

![service client](imagens/srv_client.png)

### Explicação do código

**1. Importações**

- ```import rclpy``` e ```from rclpy.node import Node```: Importamos as bibliotecas principais do ROS2 em Python.

- ```from custom_interfaces.srv import Aula8```: Importamos nossa interface de serviço, que contém as definições dos campos de requisição e resposta.

- ```import sys```: Usado para ler parâmetros da linha de comando (no caso, ```sys.argv```).

**2. Classe ```SrvClient```**

- ```class SrvClient(Node)```: Declaramos uma classe que herda de ```Node```, que é a estrutura básica para qualquer nó em ROS2. Ao inicializar, chamamos o construtor de ```Node``` passando ```aula8_srv_client``` como nome do nó.

- ```self.srv_client = self.create_client(Aula8, 'aula8_srv')```: Criamos um cliente de serviço (service client):
    - **Tipo de serviço**: ```Aula8```.

    - **Nome do serviço**: ```'aula8_srv'```.

- O loop ```while not self.srv_client.wait_for_service(timeout_sec=1.0): ...``` verifica se o servidor de serviço já está disponível, repetindo mensagens de espera a cada 1 segundo, até encontrar o **service server**.

**3. Método ```send_request```**

- ```def send_request(self, a, b)```: define a função que enviará a requisição ao servidor.

- ```request = Aula8.Request()```: cria um objeto com as informações de requisição a partir de nossa interface ```Aula8```.

- ```request.a = a``` e ```request.b = b```: popula os campos a e b da interface de serviço, que receberemos como entrada pelo terminal.

- ```future = self.srv_client.call_async(request)```: envia a requisição de forma assíncrona. Isso retorna um objeto future que representará o resultado da chamada ao serviço.

- ```rclpy.spin_until_future_complete(self, future)```: mantém o nó em "escuta" de eventos até que o future seja concluído. Quando concluído, obtemos a resposta do servidor.

- ```return future.result()```: retorna o objeto de resposta do servidor, que contém o atributo ```sum```.

**4. Função principal ```main```**

- ```rclpy.init(args=args)```: Inicializa o sistema de comunicação ROS2 em Python.

- ```srv_client = SrvClient()```: Cria instancia o nó.

- ```result = srv_client.send_request(int(sys.argv[1]), int(sys.argv[2]))```: chama o método ```send_request``` passando os dois parâmetros definidos na linha de comando (por exemplo, 2 e 3).
    - Esses parâmetros são convertidos para inteiro usando ```int(sys.argv[1])``` e ```int(sys.argv[2])```.

- ```srv_client.get_logger().info(...)```: imprime no log o resultado recebido do servidor, que é ```result.sum```.

- ```srv_client.destroy_node()``` e ```rclpy.shutdown()```: encerram o nó e finalizam o ROS2.

Resumidamente, este client se conecta ao serviço chamado ```aula8_srv```, envia dois inteiros como requisição e aguarda a resposta (a soma). Se o serviço não estiver disponível imediatamente, ele ficará aguardando até que o servidor esteja rodando.

## 11. Rodar o Cliente do Serviço (service client)

1. Veja se nenhum terminal está executando algum node, caso esteja, interrompa-o.

2. Assim como o servidor, adicione este node como executável no arquivo ```setup.py```:

    ```python 
    entry_points={
        'console_scripts': [
            'srv_server = aula8.srv_server:main',
            'srv_client = aula8.srv_client:main',
        ],
    },
    ```
3. Em um terminal, volte ao diretório raiz do workspace ```~/aula8_ws```, compile novamente e atualize o ambiente:

    ```bash
    colcon build
    source install/setup.bash
    ```

4. Agora, execute o serviço

    ```bash
    ros2 run aula8 srv_client a b
    ````

    Substituindo os argumentos **a** e **b** pelos números que deseja somar.

    Você deve ver algo no terminal como:

    ```bash
    [aula8_srv_client]: Service not available, waiting...
    ```

## 12. Rodar o servidor em outro terminal

1. Abra outro terminal e rode o **servidor** novamente:

    ```bash
    ros2 run aula8 srv_server
    ```

2. Assim que o server iniciar, o client (no outro terminal) deve detectar o serviço e enviar a requisição.

3. No terminal do client, aparecerá algo como:

    ```bash
    [aula8_srv_client]: Result of add_two_ints: for 1 + 2 = 3
    ```

## Exercício de fixação

### Objetivo Geral

Criar um service server que, ao receber uma requisição simples, retorne dados atuais do robô — por exemplo, a pose atual (posição e orientação) e a menor distância detectada no LIDAR naquele instante.

### Passos sugeridos:

1. Criar uma interface de serviço customizada, cuja resposta contenha pelo menos as seguintes informações:

    - Posição x
    - Posição y
    - Orientação do robô
    - Menor distância medida pelo Lidar

    **Observação**: Na interface, a requisição pode ser vazia. Caso queira, pode adicionar outras informações à resposta, como velociades ou informações de IMU.

2. Crie um servidor de serviço (service server) que subscreva aos tópicos relevantes e, ao receber uma requisição, retorne as informações atuais.

3. Crie um cliente de serviço (service client) que requisite as informações atuias do robô ao servidor e, ao receber a resposta, imprima elas no terminal

### Testes

1. Em um primeiro terminal, execute a simulação do robô. Ela já deve deixar disponível nos tópicos as informações dos sensores

2. Em um segundo terminal, execute o servidor, que deve ficar aguardando uma requisição.

3. Em um terceiro terminal, faça a chamada do cliente e veja se ele execulta corretamente.

4. Para verificar se as informações recebidas pelo cliente estão corretas, é possível usar o comando ```ros2 topic echo``` e ver as informações solicitadas diretamente do tópico (caso o robô esteja estático).

## Conclusão

Nesta aula você criou e testou um serviço em ROS2 do zero:

1. Definiu um pacote de interfaces customizadas (custom_interfaces) e compilou para gerar a interface.

2. Criou um pacote Python (aula8) que contém o código do servidor (server) e do cliente (client).

3. Executou e validou a comunicação entre ambos.

Esses conceitos são fundamentais na robótica móvel para solicitar processos de forma síncrona, como cálculos, tomada de decisões, ou serviços de navegação dentro de um robô.




