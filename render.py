import re
import matplotlib.pyplot as plt
import os

# Sample input
benchmark_inputs = {
    "StreamAsyncNoChunkBench": """
[info] Benchmark                           Mode  Cnt   Score   Error  Units
[info] StreamAsyncNoChunkBench.forkCats   thrpt   10  16.487 ± 0.257  ops/s
[info] StreamAsyncNoChunkBench.forkKyo    thrpt   10   0.319 ± 0.001  ops/s
[info] StreamAsyncNoChunkBench.forkOx     thrpt   10  92.165 ± 2.629  ops/s
[info] StreamAsyncNoChunkBench.forkPekko  thrpt   10  82.519 ± 3.183  ops/s
[info] StreamAsyncNoChunkBench.forkZIO    thrpt   10  15.372 ± 0.182  ops/s
    """,
    "BroadFlatMapBench_fork": """
[info] Benchmark                     Mode  Cnt       Score      Error  Units
[info] BroadFlatMapBench.forkCats   thrpt   10   13278.073 ±  270.135  ops/s
[info] BroadFlatMapBench.forkKyo    thrpt   10   50765.430 ± 1342.197  ops/s
[info] BroadFlatMapBench.forkOx     thrpt   10   60294.940 ± 2452.709  ops/s
[info] BroadFlatMapBench.forkPekko  thrpt   10     568.547 ±   74.959  ops/s
[info] BroadFlatMapBench.forkZIO    thrpt   10   19675.681 ±  286.650  ops/s
    """,
    "BroadFlatMapBench_sync": """
[info] Benchmark                     Mode  Cnt       Score      Error  Units
[info] BroadFlatMapBench.syncCats   thrpt   10   20878.520 ±  444.123  ops/s
[info] BroadFlatMapBench.syncKyo    thrpt   10   84607.981 ±  972.432  ops/s
[info] BroadFlatMapBench.syncOx     thrpt   10  309252.461 ± 9832.979  ops/s
[info] BroadFlatMapBench.syncPekko  thrpt   10     424.984 ±   29.457  ops/s
[info] BroadFlatMapBench.syncZIO    thrpt   10   30228.969 ±  446.007  ops/s
    """,
    "CollectBench_fork": """
[info] Benchmark                Mode  Cnt           Score          Error  Units
[info] CollectBench.forkCats   thrpt   10       16726.883 ±       70.093  ops/s
[info] CollectBench.forkKyo    thrpt   10       35448.140 ±      324.462  ops/s
[info] CollectBench.forkOx     thrpt   10       80785.792 ±     3773.472  ops/s
[info] CollectBench.forkPekko  thrpt   10        2770.700 ±      117.491  ops/s
[info] CollectBench.forkZIO    thrpt   10       48409.531 ±      324.923  ops/s
    """,
    "CollectBench_sync": """
[info] Benchmark                Mode  Cnt           Score          Error  Units
[info] CollectBench.syncCats   thrpt   10       14289.507 ±      217.824  ops/s
[info] CollectBench.syncKyo    thrpt   10       37582.353 ±      177.207  ops/s
[info] CollectBench.syncOx     thrpt   10  1716993328.258 ± 17811878.441  ops/s
[info] CollectBench.syncPekko  thrpt   10        2746.965 ±      108.051  ops/s
[info] CollectBench.syncZIO    thrpt   10       93758.692 ±      529.905  ops/s
    """,
    "DeepBindBench_fork": """
[info] Benchmark                 Mode  Cnt           Score          Error  Units
[info] DeepBindBench.forkCats   thrpt   10        5950.458 ±      120.810  ops/s
[info] DeepBindBench.forkKyo    thrpt   10       11964.138 ±      302.519  ops/s
[info] DeepBindBench.forkOx     thrpt   10       75756.111 ±     2937.534  ops/s
[info] DeepBindBench.forkPekko  thrpt   10         270.885 ±       52.515  ops/s
[info] DeepBindBench.forkZIO    thrpt   10       13941.727 ±      193.413  ops/s
    """,
    "DeepBindBench_sync": """
[info] Benchmark                 Mode  Cnt           Score          Error  Units
[info] DeepBindBench.syncCats   thrpt   10        6320.526 ±       66.396  ops/s
[info] DeepBindBench.syncKyo    thrpt   10       15393.389 ±      172.519  ops/s
[info] DeepBindBench.syncOx     thrpt   10  1743671109.128 ± 34519553.249  ops/s
[info] DeepBindBench.syncPekko  thrpt   10         258.712 ±       11.751  ops/s
[info] DeepBindBench.syncZIO    thrpt   10       18726.225 ±      133.621  ops/s
    """,
    "ForkChainedBench": """
[info] Benchmark                    Mode  Cnt     Score    Error  Units
[info] ForkChainedBench.forkCats   thrpt   10   788.350 ± 11.585  ops/s
[info] ForkChainedBench.forkKyo    thrpt   10  1018.942 ±  6.848  ops/s
[info] ForkChainedBench.forkOx     thrpt   10    66.070 ±  5.565  ops/s
[info] ForkChainedBench.forkPekko  thrpt   10   312.897 ± 27.243  ops/s
[info] ForkChainedBench.forkZIO    thrpt   10   410.355 ± 10.158  ops/s
    """,
    "ForkJoinBench": """
[info] Benchmark                 Mode  Cnt    Score    Error  Units
[info] ForkJoinBench.forkCats   thrpt   10  418.316 ± 11.691  ops/s
[info] ForkJoinBench.forkKyo    thrpt   10  490.017 ±  7.562  ops/s
[info] ForkJoinBench.forkOx     thrpt   10  399.405 ±  6.489  ops/s
[info] ForkJoinBench.forkPekko  thrpt   10  133.771 ±  6.300  ops/s
[info] ForkJoinBench.forkZIO    thrpt   10  336.660 ± 12.902  ops/s
    """,
    "PingPongBench": """
[info] Benchmark                 Mode  Cnt     Score    Error  Units
[info] PingPongBench.forkCats   thrpt   10   966.939 ± 17.426  ops/s
[info] PingPongBench.forkKyo    thrpt   10  2049.779 ± 46.246  ops/s
[info] PingPongBench.forkOx     thrpt   10  1191.295 ± 53.232  ops/s
[info] PingPongBench.forkPekko  thrpt   10   628.412 ± 16.915  ops/s
[info] PingPongBench.forkZIO    thrpt   10  1680.333 ± 36.525  ops/s
    """,
    "PingPongBench": """
[info] Benchmark                 Mode  Cnt     Score    Error  Units
[info] PingPongBench.forkCats   thrpt   10   966.939 ± 17.426  ops/s
[info] PingPongBench.forkKyo    thrpt   10  2049.779 ± 46.246  ops/s
[info] PingPongBench.forkOx     thrpt   10  1191.295 ± 53.232  ops/s
[info] PingPongBench.forkPekko  thrpt   10   628.412 ± 16.915  ops/s
[info] PingPongBench.forkZIO    thrpt   10  1680.333 ± 36.525  ops/s
    """,
    "SemaphoreBench": """
[info] Benchmark                  Mode  Cnt     Score    Error  Units
[info] SemaphoreBench.forkCats   thrpt   10   497.968 ± 14.042  ops/s
[info] SemaphoreBench.forkKyo    thrpt   10  1290.729 ± 10.435  ops/s
[info] SemaphoreBench.forkOx     thrpt   10  6223.154 ± 76.774  ops/s
[info] SemaphoreBench.forkPekko  thrpt   10    18.245 ±  1.327  ops/s
[info] SemaphoreBench.forkZIO    thrpt   10   548.067 ±  2.942  ops/s
    """,
    "StreamAsyncBench": """
[info] Benchmark                    Mode  Cnt    Score   Error  Units
[info] StreamAsyncBench.forkCats   thrpt   10   17.375 ± 0.353  ops/s
[info] StreamAsyncBench.forkKyo    thrpt   10  584.885 ± 3.832  ops/s
[info] StreamAsyncBench.forkOx     thrpt   10   89.187 ± 2.090  ops/s
[info] StreamAsyncBench.forkPekko  thrpt   10   80.063 ± 6.499  ops/s
[info] StreamAsyncBench.forkZIO    thrpt   10   29.351 ± 0.347  ops/s
    """,
    "StreamBench_fork": """
[info] Benchmark               Mode  Cnt      Score     Error  Units
[info] StreamBench.forkCats   thrpt   10  11212.783 ± 361.879  ops/s
[info] StreamBench.forkKyo    thrpt   10  10129.109 ± 537.277  ops/s
[info] StreamBench.forkOx     thrpt   10  14265.670 ± 123.580  ops/s
[info] StreamBench.forkPekko  thrpt   10   2054.158 ±  13.465  ops/s
[info] StreamBench.forkZIO    thrpt   10   8390.066 ±  84.375  ops/s
    """,
    "StreamBench_sync": """
[info] Benchmark               Mode  Cnt      Score     Error  Units
[info] StreamBench.syncCats   thrpt   10  11315.357 ±  53.373  ops/s
[info] StreamBench.syncKyo    thrpt   10  14003.891 ± 100.194  ops/s
[info] StreamBench.syncOx     thrpt   10  28023.329 ± 176.337  ops/s
[info] StreamBench.syncPekko  thrpt   10   2057.335 ±   9.219  ops/s
[info] StreamBench.syncZIO    thrpt   10   8395.988 ± 107.166  ops/s
    """
}

# Directory to store output charts
output_dir = "benchmark_charts"
os.makedirs(output_dir, exist_ok=True)

# Use a modern style
plt.style.use("seaborn-v0_8-darkgrid")  # fallback to seaborn-compatible if seaborn unavailable

# Color palette
colors = plt.get_cmap("tab10")

def generate_chart(name: str, raw_text: str):
    # Parse benchmark results
    pattern = r"\.(\w+)\s+thrpt\s+\d+\s+([\d.]+)\s*±\s*([\d.]+)"
    matches = re.findall(pattern, raw_text)

    if not matches:
        print(f"No benchmark results found for '{name}'")
        return

    labels = [match[0] for match in matches]
    scores = [float(match[1]) for match in matches]
    errors = [float(match[2]) for match in matches]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_colors = [colors(i % 10) for i in range(len(labels))]
    bars = ax.bar(labels, scores, yerr=errors, capsize=10, color=bar_colors, edgecolor='black', linewidth=1)

    # Add value labels on top
    for bar, score in zip(bars, scores):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + max(errors)*0.05, f"{score:.1f}",
                ha='center', va='bottom', fontsize=10, weight='bold')

    # Labels and title
    ax.set_title(f"{name} Benchmark", fontsize=16, weight='bold')
    ax.set_xlabel("Implementation", fontsize=12)
    ax.set_ylabel("Throughput (ops/s)", fontsize=12)
    ax.set_ylim(0, max(scores) + max(errors)*2)
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(True, which='major', linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(output_dir, f"{name}.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Saved chart to: {output_path}")

# Generate charts for each benchmark group
for test_name, test_data in benchmark_inputs.items():
    generate_chart(test_name, test_data)