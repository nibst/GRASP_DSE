# raise_dse

Design Space Exploration

# Usage

 
```
python main.py <heuristic> -c <c files of benchmark> -d <json of directives> -p <top function> -o <output file> -t <time limit for heuristic in seconds> -model <model of estimation chosen> 
```
`heuristic`: it's currently possible to choose between 5 heuristics. `hill`, `greedy`, `GRASP`, `genetic`and `random`
`model of estimation`: if the model of estimation with the name `<model of estimation chosen> ` don't exists, then the application train an estimator and create a model with the name specified.
## Modifying benchmark for usage
To apply directives to a C/C++ program we need to know where to apply these directives. That is what labels serves for. Here is an example:
```
sha_transform ()
{
  int i;
  INT32 temp, A, B, C, D, E, W[80];

  sha_transform_label1:for (i = 0; i < 16; ++i)
    {
      W[i] = sha_info_data[i];
    }
  sha_transform_label2:for (i = 16; i < 80; ++i)
    {
      W[i] = W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16];
    }
    ....
```
The piece of code above has two labels: `sha_transform_label1` and `sha_transform_label2`. They are needed for directives that are applied to these loops, like `pipeline`and `unroll`. However, not all directives need an additional label for them to work, some directives are applied to a function or a variable, in these case their own names will be the 'label'. An example of this would be a `loop_merge` on the `sha_transform`function above. 
For demonstration, if we had applied `pipeline`in the two loops above and a `loop_merge` on the function, the `directives.tcl`file generated would be like this: 
```
set_directive_loop_merge "sha_transform"
set_directive_pipeline "sha_transform/sha_transform_label1"
set_directive_pipeline "sha_transform/sha_transform_label2"
```

## Directives Json File

This file has the following format:
```
{

"directives":
	{
	
	"<directive_type> <label>": {
		"possible_directives":["",
		<directive1>,<directive2>],
		"function": <function in which directive is located>,
		"label": <label in which directive is applied>,
		"constraints":[<constraint1>,<constraint2>],
		"directive_type":<directive_type>
	},
	...

},
"nested_loops":
	[
	
		{
		    "function":<function where loop is located>,
		    "label":<loop label>,
		    "nest": {
		        "function":<function where loop is located>,
		        "label":<loop label>,
		        "nest": {
				        ...
		        }
		    }
		},
		...	
	]
}
```
Each dictionary inside `"directives"`is what I call a 'directive group', in other words, using the example above, this would be the directive group:
```
"<directive_type> <label>": {
		"possible_directives":["",
		<directive1>,<directive2>],
		"function": <function in which directive is located>,
		"label": <label in which directive is applied>,
		"constraints":[<constraint1>,<constraint2>],
		"directive_type":<directive_type>
	},
```
In each directive group, the primary information is the `"possible_directives"`, it lists all the directives in the directive group, including the empty directive `""`.
 The `constraints`is a list of constraints of using any of the directives of this directive group, each constraint currently is a directive group, i.e `<directive_type> <label>`. Therefore, applying one of the `possible_directives`in the directive group would remove the directives groups specified in `constraints`.
 In a concrete example: 
 ```
"pipeline flow_calc_label23": {
	   "possible_directives":["","set_directive_pipeline \"flow_calc/flow_calc_label23\""],
	   "function":"flow_calc",
	   "label": "flow_calc_label23",
	   "constraints":["unroll flow_calc_label23"],
	   "directive_type":"pipeline"
},
 ```
 This would mean that, if an heuristic choose any of the directives in the list: `
["","set_directive_pipeline \"flow_calc/flow_calc_label23\""]`, the heuristic cannot choose, for the currently design/solution, any of the directives in the `unroll flow_calc_label123`directive group.
