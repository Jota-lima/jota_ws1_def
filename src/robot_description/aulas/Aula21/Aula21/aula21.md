# Aula 21 - Controladores (Local Planner)

Neste exercício vocês irão visualizar e entender o funcionamento do **Controller Server** do **Nav2** e de seu controlador padrão, o **Dynamic Window Based Controller (DWB).

## Parâmetros Básicos

O **Controller Server** do **Nav2** possuí alguns plugins e parâmetros de configuração que são independendentes do controlador utilizado. Antes de vermos os específicos do controlador, vamos passar por alguns dos principais parâmetros:

1. **Parâmetros Gerais**:

    ```use_sim_time```: Define se deve ser utilizado tempo de simulação

    ```controller_frequency```: Frequência desejada do controlador

    ```min_(x/y/theta)_velocity_threshold```: Limite de velocidade lido pela odometria para ser enviado ao controlador. Valores abaixo serão definidos como **0.0**

    ```progress_checker_plugin```: Nome do plugin utilizada para avaliar progresso do robô (se está em movimento)

    ```goal_checker_plugin```: Nome do plugin utilizado para avaliar se o robô alcançou o objetivo (**Goal**)

    ```controller_plugins```: Nome do plugin contendo o controlador a ser utilizado

2. ```progress_checker```

    Este plugin será resposáver por verificar se o robô está em movimento
    
    Seus principais parâmetros são:

    ```plugin```: Plugin do **ROS2** a ser utilizado

    ```required_movement_radius```: Distância mínima que o robô deve se mover.

    ```movement_time_allowance```: Tempo máximo em que o robô deve se mover a distância mínima para ser considerado em movimento.

3. ```goal_checker```

    Este plugin é responsável por avaliar se o robô alcançou seu objetivo.

    Seus parâmetros são:

    ```plugin```: Plugin do **ROS2** a ser utilizado
    
    ```xy_goal_tolerance```: Raio mínimo em que o robô deve se encontrar para que a posição seja considerada alcançada.

    ```yaw_goal_tolerance```: Diferença de ângulom ínima que o robô deve estar para que a orientação seja considerada alcançada.
      
    ```stateful```: Diz se o plugin deve verificar novamente a posição após realizar uma rotação de alinhamento ao objetivo (que pode causar pequenas movimentação de posição).

### Exercício:

1. Inicie a simulação do **turtlebot3** utilizada nas últimas aulas. Ao carregar, defina a posiÇão inicial do robô.

2. Envie um comando de navegação espere o robô alcançar até o ponto desejado. Preste atenção quão perto do objetivo seu robô chegou.

3. Pare a simulação e aumente os valores de ```xy_goal_tolerance``` e  ```yaw_goal_tolerance```. Repita os passos anteriores e avalie novamente quão perto o rbô chegou de seu objetivo.

4. Mais uma vez, altere o valor destes parâmetros, mas para valores bem baixos, próximos de zero. Veja agora se o robô é capaz de alcançar o objetivo.

5. Volte os parâmetros para os valores originais para continuar a próxima seção.


## Dynamic Window Based (DWB)

Agora vamos ver mais a fundo alguns parâmetros especificos do controlador e como eles influenciam a navegação.

Por padrão os parâmetros são definidos na seção ```FollowPath```, que é passado no parâmetro geral ```controller_plugins```, porém este nome pode ser alterado.

### Principais Parâmetros:

```max_vel_x/max_vel_theta```: Define as velocidades linear e angular máximas. Como nosso robô é diferencial, as outras velocidades devem ser definidas como **0.0**.

```acc_max_x/acc_max_theta```: Define as acelerações linear e angular máximas. Evita que comandos extrapolem capacidade física do robô.

```vx_samples/vy_samples/vtheta_samples```: Número de amostras em cada dimensão do **espaço de velicadades**. Quanto mais amostras, melhor e mais consistente será o traçado, porém exige mais procesamento.

```sim_time```: Tempo a frente que cada velocidade amostrada será estrapolada, genrando um possível caminho.

```critics```: Lista de críticos a serem utilizados para calcular o **custo** final de cada trajetória. A de menor custo será selecionada.

### Exercício:

1. Inicie a simulação do **turtlebot3** utilizada nas últimas aulas. Ao carregar, defina a posiÇão inicial do robô.

2. Na barra lateral do **rviz**, desabilite a visualização do ```Amcl Particle Swarm```, ```Global Planner```, e, dentro de ```Controller```, do ```Local Costmap```.

3. Envie um comando de navegação. O caminho escolhido pelo controlador **DWB** a cada iteração deve aparecer em uma linha azul que o robô deve seguir. É possível ver pequenos saltos da trajetória entre cada loop do controlador, isso acontece pois, como o controlador funciona com uma amostragem de trajetórias, nem sempre a mais otimizada estará disponível.

4. Habilite agora a visualização do caminho gerado pelo **Planner** e envie outro comando de navegação. Veja a diferença de rota entre o planejador local e global, principalmente perto de curvas.

5. Agora pare a simulação e altere o parâmetro ```sim_time```, no arquivo de configuração, para ```3.0```. Repita os útimos passos e veja como ele influência na planejamento de rota e na navegação.

6. Volte o parâmetro ```sim_time```para seu valor original.

7. Agora, reduza o número de amostras nos parâmetros ```vx_samples``` e ```vtheta_samples```. Rode a simulção novamente e veja o que acontece com os caminhos gerados a cada iteração.

8. Por último, extrapole para valores mais altos os parâmetros indicados no item anterior e avalie agora o impacto na navegação.



