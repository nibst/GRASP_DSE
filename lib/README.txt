Alguns arquivos só fazem sentido no contexto do LegUp. Os que realmente interessam são esses:

 

Código da heurística: sources/rcapprox.py
Transformações LLVM: sources/transforms/{Profiling.cpp, Pruning.cpp, UpdateMD.cpp, RemoveIOFCall.cpp}

Funções de instrumentação: sources/lib/profiler.c

 

O V2C pode ser aplicado através dos seguintes passos:

1 – Atribuir um identificador único para cada operação na IR através da inserção de metadados (UpdateMD.cpp);
2 – Instrumentar o bytecode  do código original com a inserção de chamadas de função para obter as estatísticas de execução de cada operação (Profiling.cpp);

3 – Ligar o bytecode instrumentado com o bytecode das funções de instrumentação (profiler.c);

4 – Compilar e executar o bytecode com as entradas de treinamento. Cada execução vai gerar um arquivo com as estatísticas de cada operação (número de execuções, média, variância e desvio padrão);

5 – Substituir uma operação por uma constante utilizando o identificador e a média combinada (Pruning.cpp);

6 – Aplicar otimizações da LLVM na IR aproximada (eliminação de código morto, propagação de constantes, combinação de instruções, etc);

7 – Avaliar a redução de recursos obtida como o código aproximado e otimizado (estimativa ou síntese completa);

8 – Compilar e executar o bytecode aproximado com as entradas de teste para avaliar a magnitude do erro.

Lembrando que todos esses passos são executados pela heurística considerando o LegUp como ferramenta de HLS e o Quartus como ferramenta de síntese, então parte do código não vai fazer muito sentido. De qualquer forma, espero que ajude como modelo.

 

Qualquer dúvida é só perguntar :)

 

[]s,

Marcos
