# Aula 17 - Mapas de Custo (Global e Local)

Neste exercício vocês irão visualizar e entender a  diferença dos dois algoritmos de planejamento de rota vistos em aula, **Dijkstra** e **A\***.

O planejador de rota padrão utilizado pelo **Nav2** é o **NavFnPlanner**, configurado na seção do ```planner_server``` do arquivo de configuração do **Nav2**

```yaml
planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true
```

Este planejador pode utilizar ambos algoritmos apresentados, sendo que por padrão ele utiliza o **Dijkstra**. Para utilizar o algoritmo **A\***, basta definir o parâmetro ```use_astar``` como ```true```

## 1. Comparando algoritmos

O objetivo principal deste exercício será comparar o tempo que o algoritmo leva para calcular a rota desejada e a distância total da rota calculada. Para isso, siga os próximos passos.

### 1.1 Definir pontos de navegação

Para realizar a comparação entre os dois algoritmos de forma precisa, defina 3 pontos de navegação para a rota ser calculada. Cada ponto deve conter um valor de posição ```x, y``` e uma **orientação**.

### 1.2 Iniciar a simulação

Assim como nas últimas aulas, em um terminal, inicie a simulação do **turtlebot3** e defina seu ponto inicial.

### 1.3 Calcular tempos de planejamento

Para ver o tempo de processamento do ```planner_server```, vamos mandar o comando de planejamento diretamente pelo terminal.

Em um novo terminal, digite o seguinte comando:

```bash
ros2 action send_goal /compute_path_to_pose nav2_msgs/action/ComputePathToPose \"{pose: {header: {frame_id: map}, pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}}\"
``` 

Substituindo os valores de posição e orientação pelo ponto desejado. Você deve ver no **rviz** que a rota até o objetivo foi feita, enquanto no terminal foi mostrado cada ponto do caminho e, ao final, quanto tempo levou para realizar o planejamento.

Anote este número e repita o processo, pelo menos 5 vezes, para o mesmo ponto. Ao final, tire uma média dos valores.

Faça o mesmo com os outros pontos escolhidos.

### 1.4 Troca de algoritmo

No arquivo de configuração do **Nav2**, defina o parâmetro ```use_astar``` do ```planner_server``` como ```true```. Depois repita o procedimento acima.

### 1.5 Comparação de resultados

Compare os resultados obtidos para cada ponto usando cada um dos algoritmos.