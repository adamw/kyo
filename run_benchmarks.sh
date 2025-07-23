#!/bin/bash

# JMH benchmark parameters (centralized configuration)
WARMUP_ITERATIONS=10      # -wi: warmup iterations
MEASUREMENT_ITERATIONS=10 # -i: measurement iterations
FORKS=1                   # -f: number of forks
THREADS=1                 # -t: number of threads
RUN_TIME=1                # -r: time to run each iteration (seconds)
WARMUP_TIME=1             # -w: time to run each warmup iteration (seconds)

# List of benchmarks to run
BENCHMARKS=(
    "BroadFlatMapBench"
    "CollectBench"
    "ForkChainedBench"
    "ForkJoinBench"
    "StreamAsyncBench"
    "StreamAsyncNoChunkBench"
    "StreamBench"
    "SemaphoreBench"
    "DeepBindBench"
    "PingPongBench"
)

# Create bench_results directory if it doesn't exist
mkdir -p bench_results

# Function to run a single benchmark
run_benchmark() {
    local benchmark_name=$1
    local output_file="bench_results/${benchmark_name}_results.txt"
    
    echo "Running benchmark: $benchmark_name"
    echo "Output will be saved to: $output_file"
    
    # Build the sbt command with parameters
    local sbt_command="sbt \"kyo-bench/jmh:run $benchmark_name -wi $WARMUP_ITERATIONS -i $MEASUREMENT_ITERATIONS -f $FORKS -t $THREADS -r $RUN_TIME -w $WARMUP_TIME\""
    
    # Run the benchmark and save output to file
    echo "Command: $sbt_command" > "$output_file"
    echo "Started at: $(date)" >> "$output_file"
    echo "----------------------------------------" >> "$output_file"
    
    eval $sbt_command >> "$output_file" 2>&1
    
    echo "Completed at: $(date)" >> "$output_file"
    echo "Benchmark $benchmark_name completed. Results saved to $output_file"
    echo ""
}

# Main execution
echo "Starting JMH benchmark runs..."
echo "Parameters:"
echo "  Warmup iterations: $WARMUP_ITERATIONS"
echo "  Measurement iterations: $MEASUREMENT_ITERATIONS"
echo "  Forks: $FORKS"
echo "  Threads: $THREADS"
echo "  Run time per iteration: ${RUN_TIME}s"
echo "  Warmup time per iteration: ${WARMUP_TIME}s"
echo ""

# Run all benchmarks
for benchmark in "${BENCHMARKS[@]}"; do
    run_benchmark "$benchmark"
done

echo "All benchmarks completed! Results are available in the bench_results directory." 