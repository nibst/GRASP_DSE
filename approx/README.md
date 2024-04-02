# Infos

## Como rodar IR do vitis compilando pra máquina:

1. Adicionar função main no código IR gerado pelo HLS (a.g.ld.5.gdce.bc)
2. Compilar para um executavel: clang a.g.ld.5.gdce.bc (ou .ll, tanto faz) -o a.out
3. Chamar executável ./a.out

  

## Como rodar input de IR transformado no HLS
###  Necessário OPT do hls-llvm-project

1.  Rodar síntese do programa c/c++
2.  Pegar o a.g.ld.5.bc bytecode gerado
3.  Fazer transformações nele
4.  Chamar síntese com tcl tendo:
    
```sh
set ::LLVM_CUSTOM_OPT <path/to/vitis_llvm_project/opt>
set ::LLVM_CUSTOM_INPUT <IR input>
set ::LLVM_CUSTOM_CMD {$LLVM_CUSTOM_OPT $LLVM_CUSTOM_INPUT -o $LLVM_CUSTOM_OUTPUT}
```


## O V2C pode ser aplicado através dos seguintes passos:

1.  Atribuir um identificador único para cada operação na IR através da inserção de metadados (UpdateMD.cpp);

2. Instrumentar o bytecode do código original com a inserção de chamadas de função para obter as estatísticas de execução de cada operação (Profiling.cpp)

3. Ligar o bytecode instrumentado com o bytecode das funções de instrumentação (profiler.c);

4. Compilar e executar o bytecode com as entradas de treinamento. Cada execução vai gerar um arquivo com as estatísticas de cada operação (número de execuções, média, variância e desvio padrão);

5. Substituir uma operação por uma constante utilizando o identificador e a média combinada (Pruning.cpp);

6. Aplicar otimizações da LLVM na IR aproximada (eliminação de código morto, propagação de constantes, combinação de instruções, etc);

7. Avaliar a redução de recursos obtida como o código aproximado e otimizado (estimativa ou síntese completa);

8. Compilar e executar o bytecode aproximado com as entradas de teste para avaliar a magnitude do erro.

 
### Ideia de heurística usando V2C:

``` 
Update metada
Run synthesis on bytecode -> default synthesis values
Profile bytecode
Start of heuristic:
	loop for all operations:
		apply v2c on that operation
		run synthesis
		get MSE values
		decide wheter to take or not this v2c pass (based on synthesis values and error)
end loop
```
## Estrutura do código
  

### Código base do Marcos:
LegupRCApprox/

### Código do Marcos levemente modificado :

Fiz pequenas modificações a algumas funções para funcionar no meu contexto. A seguir vou explicar alguns arquivos que considero importantes

#### lib/approxLib.py  
-Várias funções úteis como por exemplo:
`executeBytecode` executa o IR bytecode em questão
`compileBytecode` chama HLS para o IR bytecode
`getOutputsValues` linka o IR passado com populateIO.bc (serve para passar inputs e gerar outputs) e então executa o IR com os inputs que estão no parâmetro de inputsDir e passa o output para outputsDir;
`getOutputsValuesAndDataStats` mesma coisa do que o acima só que gera data stats de cada operação. Exemplo com operação de número 80:
`{'inputs': 80, 'bitwidth': 32, 'execCount': 640000.0, 'grandMean': 4000.5, 'sumOfSquared': 13655893440000.0, 'grandStdDev': 2309.4028629379986}`

#### lib/profiler.c

Para pegar os DataStats é necessário linkar esse profiler com o IR bytecode após o pass de Profiling (esse pass adiciona a chamada de função para pegar os stats mas a implementação tá no profiler.c)

  

#### passes/

Tem todos passes usados (alguns não foram usados do código original do Marcos), o usuário deve criar uma cópia deles ou fazer um symbolic link deles para a pasta `hls-llvm-project/llvm/lib/Transforms/Approx`. A pasta Approx deve ser criada no projeto llvm do hls e então devemos adicionar `add_subdirectory(Approx)`no `hls-llvm-project/llvm/lib/Transforms/CMakeLists.txt`

  

#### config.txt:

O código do Marcos usa algumas variáveis de ambiente, nesse config.txt que criei eu seto elas. Precisa modificar para os paths certos do computador que estiver usando. Ai é so fazer “source config.txt” para exportar as variáveis

#### IOLib/populateIO.c:
Modificar esse arquivo para cada benchmark se necessário. São a implementação das funções para receber inputs e gerar outputs do benchmark. Os benchmarks vão ter que ter uma main nesse estilo:


```
extern  "C"  void  populateInput (int  *inputVector,  int  numElts,  const  char  *fileName);
extern  "C"  void  populateOutput (int  *outputVector,  int  numElts,  const  char *fileName);

int  main (int  argc,  char  *argv[])
{
	int  indata[SIZE];
	int  outdata[SIZE];

	populateInput(indata,  SIZE,  argv[1]);
	example(indata,outdata);
	populateOutput(outdata,  SIZE,  argv[2]);

	return  0;
}
```
Exemplo de `populateIO.c`:
```
#include  <stdlib.h>
#include  <stdio.h>

void  populateInput (int  *inputVector,  int  numElts,  const  char  *fileName)
{
	FILE*  inputFile  =  fopen(fileName,  "r");
	int  i;
	for (i  =  0;  i  <  numElts;  i++){
		fscanf (inputFile,  "%i",  &inputVector[i]);
	}
	fclose(inputFile);
}
void  populateOutput (int  *outputVector,  int  numElts,  const  char  *fileName)
{
	FILE*  outputFile  =  fopen(fileName,  "w");

	int  i;
	for (i  =  0;  i  <  numElts;  i++)
		fprintf (outputFile,  "%i\n",  outputVector[i]);
	fclose(outputFile);
}
```

