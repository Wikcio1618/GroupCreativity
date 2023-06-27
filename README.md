# GroupCreativity
Implementation of a group creativity model with visualisation and Gui for engineer thesis

---

### Universal rules
There is N agents that assume discrete positions in 1D space. All agents are performing a random walk with a dynamic jump(step) length.
There are also N target positions randomly selected. The goal of agents is to assume all targets. If one steps on it his step is permanently set to 0. There are 2 types of agents: creative (g) and conservative (1-g). After each time step (day) the feedback function is calculated: $d(t_i)=\sqrt{\sum_{n=0}^N{x^2_n}}$, where $x_n$ is distance of agent to the nearest free target. Agents that found a target don't contribute to this function.

### Distinct rules that may differ in other branches
1. Agents start at random positions
2. Space is looped
3. Each creative agent at the end of i-th day increases step of agents in range r by F, PROVIDED THAT d(t_i) is greater than their step
4. Conservative agents interact in a symmetrical way


## TODO
Wykres w funkcji czasu (wszyscy i kreatywni/konserwaty)