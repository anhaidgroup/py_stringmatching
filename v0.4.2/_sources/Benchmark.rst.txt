Runtime Benchmark 
=================

For this package, we add a runtime benchmark (consisting of a script and several datasets) to measure the runtime performance of similarity measures. This benchmark can be used by users to judge whether similarity measures are fast enough for their purposes, and used by developers to speed up the measures.

Running the Benchmark
---------------------

The user can run the benchmark as follows:

Step 1: Clone the py_stringmatching package from GitHub using the following command::
    
    git clone https://github.com/anhaidgroup/py_stringmatching.git 

Step 2: Change the working directory to py_stringmatching/benchmarks/custom_benchmarks

Step 3: Run the benchmark using the following sequence of commands:

    >>> import py_stringmatching as sm
    >>> from run_benchmark import *
    # create an object for the similarity measure you need to benchmark
    >>> jaccard = sm.Jaccard()                                                                                   
    # create a tokenizer object (in case of token-based measures)            
    >>> ws = sm.WhitespaceTokenizer(return_set = True)
    # Set dataset paths
    >>> short_strings_path = 'datasets/short_strings.csv'
    >>> medium_strings_path = 'datasets/medium_strings.csv'
    >>> long_strings_path = 'datasets/long_strings.csv'
    # Data size (number of string pairs) over which the benchmark should be run
    >>> data_size = 10000
    # Number of times to repeat
    >>> num_repeat = 3
    # Output file where the benchmark results should be written
    >>> output_file = 'benchmark_results.csv'
    # run the benchmark
    >>> run_benchmark(short_strings_path, medium_strings_path, long_strings_path, data_size = data_size, jaccard.get_sim_score, ws.tokenize, num_repeat = num_repeat, output_file = output_file)

The benchmark contains three datasets in the `datasets` directory: (1) short_strings.csv, (2) medium_strings.csv, and (3) long_strings.csv. Each dataset contains 5000 strings. Specifically, short_strings.csv contains strings with length in the range of 2-15 (avg. of 10), medium_strings.csv contains strings with length in the range of 18-39 (avg. of 25), and
long_strings.csv contains strings with length in the range of 60-1726 (avg. of 127).

The above command will run the benchmark for 9 different configurations 
(short-short, short-medium, short-long, medium-short, medium-medium, medium-long, 
long-short, long-medium, long-long) for the provided similarity measure, and
writes the result to the provided output file. See below for additional details.

Interpreting the Results
--------------------------

The benchmark results will be a CSV file containing the following information:

   * Configuration
   * Runtime (in secs) for each run of a configuration (note that each configuration is run for `num_repeat` times)
   * Average runtime (in secs) for each configuration

An example output file will look like this::

    configuration,run_1 (in secs),run_2 (in secs),run_3 (in secs),average (in secs) 
    short_short,0.112642049789,0.112892866135,0.112852096558,0.112795670827         
    short_medium,0.115404129028,0.115512132645,0.115454912186,0.115457057953        
    short_long,0.194123983383,0.193922996521,0.193790912628,0.193945964177          
    medium_short,0.11647105217,0.116579055786,0.116438865662,0.116496324539         
    medium_medium,0.118470907211,0.118409156799,0.118496894836,0.118458986282       
    medium_long,0.206312894821,0.206974983215,0.206708908081,0.206665595373         
    long_short,0.205050945282,0.205410957336,0.205253124237,0.205238342285          
    long_medium,0.217441797256,0.21806883812,0.218235015869,0.217915217082          
    long_long,0.770321846008,0.76869893074,0.768806934357,0.769275903702  
