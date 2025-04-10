# APS 2 - Navegação Básica

Nesta APS, você irá consolidar os conhecimentos adquiridos sobre publishers, subscribers, services, actions e launch files. Seu objetivo será criar um sistema de navegação sequencial que navegue através de todos os comodos do ambiente de simulação criado. Sua solução deve conter:

1. **Um Nó Principal**

- Assina dados do LIDAR (por exemplo, em /scan) para detectar se há uma parede mais próxima do que um limite definido.

- Publica comandos de velocidade para frente em ```/cmd_vel``` quando não há parede detectada.

- Chama uma Ação (action client) quando for necessário fazer o robô girar.

- Servidor de um serviço que, quando chamado, através de uma interface vazia (Empty), inicia a navegação sequencial.

2. **Um Servidor de Ação**

- Recebe um objetivo (goal) para girar o robô por um determinado número de graus.

- Gira o robô de acordo com o objetivo, fornecendo feedback sobre quantos graus ainda faltam para completar a rotação.

3. **Um Arquivo de Lançamento (Launch File)**

- Inicia o nó principal, o servidor de ação e o nó do serviço em um único passo.

## Requisitos e Objetivos

1. **Lógica de Navegação**

- O node fica aguardando o serviço ser chamado para inicializar a navegação.

- O robô se move para frente até detectar uma parede a uma distância limite (por exemplo, 0,5 m).

- Ao detectar a parede, ele para e chama o Servidor de Ação para girar um ângulo definido (por exemplo, 90 graus).

- Depois que a rotação é concluída, o robô volta a se mover para frente até a próxima parede, explorando os cômodos.

2. **Servidor de Ação**

- Deve aceitar um objetivo indicando quantos graus girar.

- Deve responder ao client se o o objetivo foi aceito ou não.

- Deve fornecer feedback contínuo sobre o ângulo restante para girar.

- Deve sinalizar conclusão ou sucesso quando a rotação estiver finalizada.

3. **Arquivo de Lançamento**

- Deve lançar o nó principal e o servidor de ação.


## Entrega

A entrega desta APS deve ser feita até as 23:59 do dia 23/03 (Domingo). 

Deve ser entregue, através do BlackBoard, um arquivo .zip do seu **pacote em python** contendo os nodes especificados e o arquivo de lançamentode do ROS. Os diretórios, subdiretórios e arquivos devem estar configurados de forma que o professor seja capaz de compilar o código e rodar o arquivo de launch. Além disso, junto ao ```.zip```, deve estar um vídeo da simulação com o robô realizando a navegação.

## Avaliação

A Avaliação desta atividade será feita da seguinte forma:

1. **Funcionalidades Básicas (40%)**

- Presença de um nó principal que assine o LIDAR e publique comandos de velocidade corretamente.

- Movimentação do robô até a parede e parada ao detectar a distância-limite.

- Início da navegação apenas quando o serviço vazio for chamado.

2. **Servidor de Ação (40%)**

- Implementação correta do servidor de ação, recebendo o ângulo como objetivo, enviando resposta aceitando o objetivo, feedback e retornando sucesso ao final da rotação.

- Uso adequado de mensagens de objetivo (goal), feedback e resultado (result).

- Subscreve no tópico ```/odom``` e rotaciona corretamente

3. **Launch File (10%)**

- Arquivo de lançamento que inicia automaticamente o nó principal e o servidor de ação.

4. **Navegação (10%)**

- O robô foi capaz de completar o percurso

A nota final será a soma dos itens acima, considerando também eventuais penalizações por atraso ou requisitos não atendidos.


