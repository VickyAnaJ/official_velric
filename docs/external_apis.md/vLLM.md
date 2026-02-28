Architecture Overview¶

This document provides an overview of the vLLM architecture.

    Architecture Overview
        Entrypoints
            LLM Class
            OpenAI-Compatible API Server
        V1 Process Architecture
            API Server Process
            Engine Core Process
            GPU Worker Processes
            DP Coordinator Process (conditional)
            Process Count Summary
        LLM Engine
            LLMEngine
            AsyncLLMEngine
        Worker
        Model Runner
        Model
        Class Hierarchy

Entrypoints¶

vLLM provides a number of entrypoints for interacting with the system. The following diagram shows the relationship between them.

Entrypoints Diagram
LLM Class¶

The LLM class provides the primary Python interface for doing offline inference, which is interacting with a model without using a separate model inference server.

Here is a sample of LLM class usage:
Code

More API details can be found in the Offline Inference section of the API docs.

The code for the LLM class can be found in
vllm/entrypoints/llm.py.
OpenAI-Compatible API Server¶

The second primary interface to vLLM is via its OpenAI-compatible API server. This server can be started using the vllm serve command.

vllm
 serve <model>

The code for the vllm CLI can be found in
vllm/entrypoints/cli/main.py.

Sometimes you may see the API server entrypoint used directly instead of via the vllm CLI command. For example:

python
 -m vllm.entrypoints.openai.api_server --model <model>

Warning

python -m vllm.entrypoints.openai.api_server is deprecated and may become unsupported in a future release.

That code can be found in
vllm/entrypoints/openai/api_server.py.

More details on the API server can be found in the OpenAI-Compatible Server document.
V1 Process Architecture¶

vLLM V1 uses a multi-process architecture to separate concerns and maximize throughput. Understanding this architecture is important for properly sizing CPU resources in your deployment. The key processes are:
API Server Process¶

The API server process handles HTTP requests (e.g., the OpenAI-compatible API), performs input processing (tokenization, multi-modal data loading), and streams results back to clients. It communicates with the engine core process(es) via ZMQ sockets.

By default, there is 1 API server process, but when data parallelism is used, the API server count automatically scales to match the data parallel size. This can also be manually configured with the --api-server-count flag. Each API server connects to all engine cores via ZMQ in a many-to-many topology, enabling any API server to route requests to any engine core. Each API server process uses multiple CPU threads for media loading (controlled by VLLM_MEDIA_LOADING_THREAD_COUNT, default 8).

The code can be found in
vllm/entrypoints/openai/api_server.py and
vllm/v1/utils.py.
Engine Core Process¶

The engine core process runs the scheduler, manages KV cache, and coordinates model execution across GPU workers. It runs a busy loop that continuously schedules requests and dispatches work to the GPU workers.

There is 1 engine core process per data parallel rank. For example, with --data-parallel-size 4, there are 4 engine core processes.

The code can be found in
vllm/v1/engine/core.py and
vllm/v1/engine/utils.py.
GPU Worker Processes¶

Each GPU is managed by a dedicated worker process. The worker process loads model weights, executes forward passes, and manages GPU memory. Workers communicate with the engine core process that owns them.

There is 1 worker process per GPU. The total number of GPU worker processes equals tensor_parallel_size x pipeline_parallel_size per engine core.

The code can be found in
vllm/v1/executor/multiproc_executor.py and
vllm/v1/worker/gpu_worker.py.
DP Coordinator Process (conditional)¶

When using data parallelism (--data-parallel-size > 1), an additional coordinator process manages load balancing across DP ranks and coordinates synchronized forward passes for MoE models.

There is 1 DP coordinator process (only when data parallelism is enabled).

The code can be found in
vllm/v1/engine/coordinator.py.
Process Count Summary¶

For a deployment with N GPUs, TP tensor parallel size, DP data parallel size, and A API server count:
Process Type 	Count 	Notes
API Server 	A (default DP) 	Handles HTTP requests and input processing
Engine Core 	DP (default 1) 	Scheduler and KV cache management
GPU Worker 	N (= DP x TP) 	One per GPU, executes model forward passes
DP Coordinator 	1 if DP > 1, else 0 	Load balancing across DP ranks
Total 	A + DP + N (+ 1 if DP > 1) 	

For example, a typical single-node deployment with 4 GPUs (vllm serve -tp=4) has:

    1 API server + 1 engine core + 4 GPU workers = 6 processes

V1 Process Architecture - TP=4

A data parallel deployment with 8 GPUs (vllm serve -tp=2 -dp=4) has:

    4 API servers + 4 engine cores + 8 GPU workers + 1 DP coordinator = 17 processes

V1 Process Architecture - TP=2, DP=4

For CPU resource sizing recommendations, see CPU Resources for GPU Deployments.
LLM Engine¶

The LLMEngine and AsyncLLMEngine classes are central to the functioning of the vLLM system, handling model inference and asynchronous request processing.

LLMEngine Diagram
LLMEngine¶

The LLMEngine class is the core component of the vLLM engine. It is responsible for receiving requests from clients and generating outputs from the model. The LLMEngine includes input processing, model execution (possibly distributed across multiple hosts and/or GPUs), scheduling, and output processing.

    Input Processing: Handles tokenization of input text using the specified tokenizer.
    Scheduling: Chooses which requests are processed in each step.
    Model Execution: Manages the execution of the language model, including distributed execution across multiple GPUs.
    Output Processing: Processes the outputs generated by the model, decoding the token IDs from a language model into human-readable text.

The code for LLMEngine can be found in
vllm/engine/llm_engine.py.
AsyncLLMEngine¶

The AsyncLLMEngine class is an asynchronous wrapper for the LLMEngine class. It uses asyncio to create a background loop that continuously processes incoming requests. The AsyncLLMEngine is designed for online serving, where it can handle multiple concurrent requests and stream outputs to clients.

The OpenAI-compatible API server uses the AsyncLLMEngine. There is also a demo API server that serves as a simpler example in
vllm/entrypoints/api_server.py.

The code for AsyncLLMEngine can be found in
vllm/engine/async_llm_engine.py.
Worker¶

A worker is a process that runs the model inference. vLLM follows the common practice of using one process to control one accelerator device, such as GPUs. For example, if we use tensor parallelism of size 2 and pipeline parallelism of size 2, we will have 4 workers in total. Workers are identified by their rank and local_rank. rank is used for global orchestration, while local_rank is mainly used for assigning the accelerator device and accessing local resources such as the file system and shared memory.
Model Runner¶

Every worker has one model runner object, responsible for loading and running the model. Much of the model execution logic resides here, such as preparing input tensors and capturing cudagraphs.
Model¶

Every model runner object has one model object, which is the actual torch.nn.Module instance. See huggingface_integration for how various configurations affect the class we ultimately get.
Class Hierarchy¶

The following figure shows the class hierarchy of vLLM:

Class Hierarchy

There are several important design choices behind this class hierarchy:

1. Extensibility: All classes in the hierarchy accept a configuration object containing all the necessary information. The VllmConfig class is the main configuration object that is passed around. The class hierarchy is quite deep, and every class needs to read the configuration it is interested in. By encapsulating all configurations in one object, we can easily pass the configuration object around and access the configuration we need. Suppose we want to add a new feature (this is often the case given how fast the field of LLM inference is evolving) that only touches the model runner. We will have to add a new configuration option in the VllmConfig class. Since we pass the whole config object around, we only need to add the configuration option to the VllmConfig class, and the model runner can access it directly. We don't need to change the constructor of the engine, worker, or model class to pass the new configuration option.

2. Uniformity: The model runner needs a unified interface to create and initialize the model. vLLM supports more than 50 types of popular open-source models. Each model has its own initialization logic. If the constructor signature varies with models, the model runner does not know how to call the constructor accordingly, without complicated and error-prone inspection logic. By making the constructor of the model class uniform, the model runner can easily create and initialize the model without knowing the specific model type. This is also useful for composing models. Vision-language models often consist of a vision model and a language model. By making the constructor uniform, we can easily create a vision model and a language model and compose them into a vision-language model.

Note

To support this change, all vLLM models' signatures have been updated to:

def __init__(self, *, vllm_config: VllmConfig, prefix: str = ""):

To avoid accidentally passing incorrect arguments, the constructor is now keyword-only. This ensures that the constructor will raise an error if old configurations are passed. vLLM developers have already made this change for all models within vLLM. For out-of-tree registered models, developers need to update their models, for example by adding shim code to adapt the old constructor signature to the new one:
Code

This way, the model can work with both old and new versions of vLLM.

3. Sharding and Quantization at Initialization: Certain features require changing the model weights. For example, tensor parallelism needs to shard the model weights, and quantization needs to quantize the model weights. There are two possible ways to implement this feature. One way is to change the model weights after the model is initialized. The other way is to change the model weights during the model initialization. vLLM chooses the latter. The first approach is not scalable to large models. Suppose we want to run a 405B model (with roughly 810GB weights) with 16 H100 80GB GPUs. Ideally, every GPU should only load 50GB weights. If we change the model weights after the model is initialized, we need to load the full 810GB weights to every GPU and then shard the weights, leading to a huge memory overhead. Instead, if we shard the weights during the model initialization, every layer will only create a shard of the weights it needs, leading to a much smaller memory overhead. The same idea applies to quantization. Note that we also add an additional argument prefix to the model's constructor so that the model can initialize itself differently based on the prefix. This is useful for non-uniform quantization, where different parts of the model are quantized differently. The prefix is usually an empty string for the top-level model and a string like "vision" or "language" for the sub-models. In general, it matches the name of the module's state dict in the checkpoint file.

One disadvantage of this design is that it is hard to write unit tests for individual components in vLLM because every component needs to be initialized by a complete config object. We solve this problem by providing a default initialization function that creates a default config object with all fields set to None. If the component we want to test only cares about a few fields in the config object, we can create a default config object and set the fields we care about. This way, we can test the component in isolation. Note that many tests in vLLM are end-to-end tests that test the whole system, so this is not a big problem.

In summary, the complete config object VllmConfig can be treated as an engine-level global state that is shared among all vLLM classes.

Metrics¶

vLLM exposes a rich set of metrics to support observability and capacity planning for the V1 engine.
Objectives¶

    Provide comprehensive coverage of engine and request level metrics to aid production monitoring.
    Prioritize Prometheus integrations, as this is what we expect to be used in production environments.
    Offer logging support (i.e. printing metrics to the info log) for ad-hoc testing, debugging, development, and exploratory use cases.

Background¶

Metrics in vLLM can be categorized as follows:

    Server-level metrics: Global metrics that track the state and performance of the LLM engine. These are typically exposed as Gauges or Counters in Prometheus.
    Request-level metrics: Metrics that track the characteristics (e.g. size and timing) of individual requests. These are typically exposed as Histograms in Prometheus and are often the SLOs that an SRE monitoring vLLM will be tracking.

The mental model is that server-level metrics help explain the values of request-level metrics.
Metrics Overview¶
v1 Metrics¶

In v1, an extensive set of metrics are exposed via a Prometheus-compatible /metrics endpoint using the vllm: prefix, for example:

    vllm:num_requests_running (Gauge) - Number of requests currently running.
    vllm:kv_cache_usage_perc (Gauge) - Fraction of used KV cache blocks (0–1).
    vllm:prefix_cache_queries (Counter) - Number of prefix cache queries.
    vllm:prefix_cache_hits (Counter) - Number of prefix cache hits.
    vllm:prompt_tokens_total (Counter) - Total number of prompt tokens processed.
    vllm:generation_tokens_total (Counter) - Total number of generated tokens.
    vllm:request_success_total (Counter) - Number of finished requests (by finish reason).
    vllm:request_prompt_tokens (Histogram) - Histogram of input prompt token counts.
    vllm:request_generation_tokens (Histogram) - Histogram of generation token counts.
    vllm:time_to_first_token_seconds (Histogram) - Time to first token (TTFT).
    vllm:inter_token_latency_seconds (Histogram) - Inter-token latency.
    vllm:e2e_request_latency_seconds (Histogram) - End-to-end request latency.
    vllm:request_prefill_time_seconds (Histogram) - Request prefill time.
    vllm:request_decode_time_seconds (Histogram) - Request decode time.

These are documented under Inferencing and Serving -> Production Metrics.
Grafana Dashboard¶

vLLM also provides
a reference example for how to collect and store these metrics using Prometheus and visualize them using a Grafana dashboard.

The subset of metrics exposed in the Grafana dashboard gives us an indication of which metrics are especially important:

    vllm:e2e_request_latency_seconds_bucket - End to end request latency measured in seconds.
    vllm:prompt_tokens - Prompt tokens.
    vllm:generation_tokens - Generation tokens.
    vllm:inter_token_latency_seconds - Inter-token latency (Time Per Output Token, TPOT) in seconds.
    vllm:time_to_first_token_seconds - Time to First Token (TTFT) latency in seconds.
    vllm:num_requests_running (also, _swapped and _waiting) - Number of requests in the RUNNING, WAITING, and SWAPPED states.
    vllm:kv_cache_usage_perc - Percentage of used cache blocks by vLLM.
    vllm:request_prompt_tokens - Request prompt length.
    vllm:request_generation_tokens - Request generation length.
    vllm:request_success - Number of finished requests by their finish reason: either an EOS token was generated or the max sequence length was reached.
    vllm:request_queue_time_seconds - Queue time.
    vllm:request_prefill_time_seconds - Requests prefill time.
    vllm:request_decode_time_seconds - Requests decode time.
    vllm:request_max_num_generation_tokens - Max generation tokens in a sequence group.

See
the PR which added this Dashboard for interesting and useful background on the choices made here.
Prometheus Client Library¶

Prometheus support was initially added
using the aioprometheus library, but a switch was made quickly to
prometheus_client. The rationale is discussed in both linked PRs.

During those migrations we briefly lost a MetricsMiddleware to track HTTP metrics, but this was reinstated
using prometheus_fastapi_instrumentator:

$
 curl http://0.0.0.0:8000/metrics 2>/dev/null  | grep -P '^http_(?!.*(_bucket|_created|_sum)).*'
http_requests_total
{handler="/v1/completions",method="POST",status="2xx"} 201.0
http_request_size_bytes_count
{handler="/v1/completions"} 201.0
http_response_size_bytes_count
{handler="/v1/completions"} 201.0
http_request_duration_highr_seconds_count
 201.0
http_request_duration_seconds_count
{handler="/v1/completions",method="POST"} 201.0

Multi-process Mode¶

Historically, metrics were collected in the engine core process and multiprocess mode was used to make them available in the API server process. See
Pull Request #7279.

More recently, metrics are collected in the API server process and multiprocess mode is only used when --api-server-count > 1. See
Pull Request #17546 and details on API server scale-out.
Built in Python/Process Metrics¶

The following metrics are supported by default by prometheus_client, but they are not exposed when multiprocess mode is used:

    python_gc_objects_collected_total
    python_gc_objects_uncollectable_total
    python_gc_collections_total
    python_info
    process_virtual_memory_bytes
    process_resident_memory_bytes
    process_start_time_seconds
    process_cpu_seconds_total
    process_open_fds
    process_max_fds

Therefore, these metrics are unavailable when --api-server-count > 1. It's questionable how relevant these are since they do not aggregate these stats for all processes that make up a vLLM instance.
Metrics Design¶

The
"Even Better Observability" feature where was where much of the metrics design was planned. For example, see where
a detailed roadmap was laid out.
Legacy PRs¶

To help understand the background to the metrics design, here are some of the relevant PRs which added the original, now legacy, metrics:

    Pull Request #1890
    Pull Request #2316
    Pull Request #2730
    Pull Request #4464
    Pull Request #7279

Metrics Implementation PRs¶

For background, here are the relevant PRs relating to the metrics implementation
Issue #10582:

    Pull Request #11962
    Pull Request #11973
    Pull Request #10907
    Pull Request #12416
    Pull Request #12478
    Pull Request #12516
    Pull Request #12530
    Pull Request #12561
    Pull Request #12579
    Pull Request #12592
    Pull Request #12644

Metrics Collection¶

In v1, we wish to move computation and overhead out of the engine core process to minimize the time between each forward pass.

The overall idea of V1 EngineCore design is:

    EngineCore is the inner loop. Performance is most critical here
    AsyncLLM is the outer loop. This is overlapped with GPU execution (ideally), so this is where any "overheads" should be if possible. So AsyncLLM.output_handler_loop is the ideal place for the metrics bookkeeping if possible.

We will achieve this by collecting metrics in the frontend API server, and base these metrics on information we can glean from the EngineCoreOutputs returned by the engine core process to the frontend.
Interval Calculations¶

Many of our metrics are the time interval between various events in the processing of a request. It is best practice to use timestamps based on "monotonic time" (time.monotonic()) rather than "wall-clock time" (time.time()) to calculate intervals as the former is unaffected by system clock changes (e.g. from NTP).

It's also important to note that monotonic clocks differ between processes - each process has its own reference point. So it is meaningless to compare monotonic timestamps from different processes.

Therefore, in order to calculate an interval, we must compare two monotonic timestamps from the same process.
Scheduler Stats¶

The engine core process will collect some key statistics from the scheduler - e.g. the number of requests that were scheduled or waiting after the last scheduler pass - and include those statistics in EngineCoreOutputs.
Engine Core Events¶

The engine core will also record the timestamp of certain per-request events so that the frontend can calculate the interval between these events.

The events are:

    QUEUED - when the request was received by the engine core and added to the scheduler queue.
    SCHEDULED - when the request was first scheduled for execution.
    PREEMPTED - the request has been put back in the waiting queue in order to make room for other requests to complete. It will be re-scheduled in future and re-start its prefill phase.
    NEW_TOKENS - when the output included in EngineCoreOutput was generated. Since this is common to all requests in a given iteration, we use a single timestamp on EngineCoreOutputs to record this event.

And the calculated intervals are:

    Queue interval - between QUEUED and most recent SCHEDULED.
    Prefill interval - between most recent SCHEDULED and the subsequent first NEW_TOKENS.
    Decode interval - between first (after the most recent SCHEDULED) and last NEW_TOKENS.
    Inference interval - between most recent SCHEDULED and last NEW_TOKENS.
    Inter-token interval - between successive NEW_TOKENS.

Put another way:

Interval calculations - common case

We explored the possibility of having the frontend calculate these intervals using the timing of events visible by the frontend. However, the frontend does not have visibility into the timing of the QUEUED and SCHEDULED events and, since we need to calculate intervals based on monotonic timestamps from the same process ... we need the engine core to record timestamps for all of these events.
Interval Calculations vs Preemptions¶

When a preemption occurs during decode, since any already generated tokens are reused, we consider the preemption as affecting the inter-token, decode, and inference intervals.

Interval calculations - preempted decode

When a preemption occurs during prefill (assuming such an event is possible), we consider the preemption as affecting the time-to-first-token and prefill intervals.

Interval calculations - preempted prefill
Frontend Stats Collection¶

As the frontend processes a single EngineCoreOutputs - i.e. the output from a single engine core iteration - it collects various statistics relating to that iteration:

    The total number of new tokens generated in this iteration.
    The total number of prompt tokens processed by the prefills that completed in this iteration.
    The queue intervals for any requests that were scheduled in this iteration.
    The prefill intervals for any requests that completed prefill in this iteration.
    The inter-token intervals (Time Per Output Token, TPOT), for all requests included in this iteration.
    The Time-To-First-Token (TTFT) for any requests that completed prefill in this iteration. However, we calculate this interval relative to when the request was first received by the frontend (arrival_time) in order to account for input processing time.

For any requests that were completed in a given iteration, we also record:

    The inference and decode intervals - relative to the scheduled and first token events, as described above.
    End-to-end latency - the interval between frontend arrival_time and the frontend receiving the final token.

KV Cache Residency Metrics¶

We also emit a set of histograms that describe how long sampled KV cache blocks stay resident and how often they are reused. Sampling (--kv-cache-metrics-sample) keeps the overhead tiny; when a block is chosen we record:

    lifetime – allocation ⟶ eviction
    idle before eviction – last touch ⟶ eviction
    reuse gaps – the pauses between touches when the block gets reused

Those map directly to the Prometheus metrics:

    vllm:kv_block_lifetime_seconds – how long each sampled block exists.
    vllm:kv_block_idle_before_evict_seconds – idle tail after the final access.
    vllm:kv_block_reuse_gap_seconds – time between consecutive touches.

The engine core only ships raw eviction events via SchedulerStats; the frontend drains them, turns them into Prometheus observations, and also exposes the same data through LLM.get_metrics() when logging is on. Looking at lifetime and idle time on one chart makes it easy to spot stranded cache or workloads that pin prompts for a long decode.
Metrics Publishing - Logging¶

The LoggingStatLogger metrics publisher outputs a log INFO message every 5 seconds with some key metrics:

    The current number of running/waiting requests
    The current GPU cache usage
    The number of prompt tokens processed per second over the past 5 seconds
    The number of new tokens generated per second over the past 5 seconds
    The prefix cache hit rate over the most recent 1k kv-cache block queries

Metrics Publishing - Prometheus¶

The PrometheusStatLogger metrics publisher makes the metrics available via a /metrics HTTP endpoint in a Prometheus-compatible format. A Prometheus instance can then be configured to poll this endpoint (e.g. every second) and record the values in its time-series database. Prometheus is often used via Grafana, allowing these metrics to be graphed over time.

Prometheus supports the following metric types:

    Counter: a value that will increase over time, never reducing, and generally reset to zero when the vLLM instance restarts. For example, the number of tokens generated over the lifetime of the instance.
    Gauge: a value that goes up and down, for example the number of requests currently scheduled for execution.
    Histogram: a count of metric samples, recorded in buckets. For example, the number of requests whose TTFT was <1ms, <5ms, <10ms, <20ms, and so on.

Prometheus metrics can also be labelled, allowing metrics to be combined according to matching labels. In vLLM, we add a model_name label to every metric which includes the name of the model served by that instance.

Example output:

$
 curl http://0.0.0.0:8000/metrics
# HELP vllm:num_requests_running Number of requests in model execution batches.
# TYPE vllm:num_requests_running gauge
vllm:num_requests_running
{model_name="meta-llama/Llama-3.1-8B-Instruct"} 8.0
...
# HELP vllm:generation_tokens_total Number of generation tokens processed.
# TYPE vllm:generation_tokens_total counter
vllm:generation_tokens_total
{model_name="meta-llama/Llama-3.1-8B-Instruct"} 27453.0
...
# HELP vllm:request_success_total Count of successfully processed requests.
# TYPE vllm:request_success_total counter
vllm:request_success_total
{finished_reason="stop",model_name="meta-llama/Llama-3.1-8B-Instruct"} 1.0
vllm:request_success_total
{finished_reason="length",model_name="meta-llama/Llama-3.1-8B-Instruct"} 131.0
vllm:request_success_total
{finished_reason="abort",model_name="meta-llama/Llama-3.1-8B-Instruct"} 0.0
...
# HELP vllm:time_to_first_token_seconds Histogram of time to first token in seconds.
# TYPE vllm:time_to_first_token_seconds histogram
vllm:time_to_first_token_seconds_bucket
{le="0.001",model_name="meta-llama/Llama-3.1-8B-Instruct"} 0.0
vllm:time_to_first_token_seconds_bucket
{le="0.005",model_name="meta-llama/Llama-3.1-8B-Instruct"} 0.0
vllm:time_to_first_token_seconds_bucket
{le="0.01",model_name="meta-llama/Llama-3.1-8B-Instruct"} 0.0
vllm:time_to_first_token_seconds_bucket
{le="0.02",model_name="meta-llama/Llama-3.1-8B-Instruct"} 13.0
vllm:time_to_first_token_seconds_bucket
{le="0.04",model_name="meta-llama/Llama-3.1-8B-Instruct"} 97.0
vllm:time_to_first_token_seconds_bucket
{le="0.06",model_name="meta-llama/Llama-3.1-8B-Instruct"} 123.0
vllm:time_to_first_token_seconds_bucket
{le="0.08",model_name="meta-llama/Llama-3.1-8B-Instruct"} 138.0
vllm:time_to_first_token_seconds_bucket
{le="0.1",model_name="meta-llama/Llama-3.1-8B-Instruct"} 140.0
vllm:time_to_first_token_seconds_count
{model_name="meta-llama/Llama-3.1-8B-Instruct"} 140.0

Note

The choice of histogram buckets to be most useful to users across a broad set of use cases is not straightforward and will require refinement over time.
Cache Config Info¶

prometheus_client has support for Info metrics which are equivalent to a Gauge whose value is permanently set to 1, but exposes interesting key/value pair information via labels. This is used for information about an instance that does not change - so it only needs to be observed at startup - and allows comparing across instances in Prometheus.

We use this concept for the vllm:cache_config_info metric:

# HELP vllm:cache_config_info Information of the LLMEngine CacheConfig
# TYPE vllm:cache_config_info gauge
vllm:cache_config_info{block_size="16",cache_dtype="auto",calculate_kv_scales="False",cpu_offload_gb="0",enable_prefix_caching="False",gpu_memory_utilization="0.9",...} 1.0

However, prometheus_client has
never supported Info metrics in multiprocessing mode - for unclear reasons. We simply use a Gauge metric set to 1 and multiprocess_mode="mostrecent" instead.
LoRA Metrics¶

The vllm:lora_requests_info Gauge is somewhat similar, except the value is the current wall-clock time, and is updated every iteration.

The label names used are:

    running_lora_adapters: a per-adapter count of the number requests running using that adapter, formatted as a comma-separated string.
    waiting_lora_adapters: similar, except counting requests that are waiting to be scheduled.
    max_lora - the static "max number of LoRAs in a single batch." configuration.

Encoding a running/waiting counts for multiple adapters in a comma-separated string seems quite misguided - we could use labels to distinguish between per-adapter counts. This should be revisited.

Note that multiprocess_mode="livemostrecent" is used - the most recent metric is used, but only from currently running processes.

This was added in
Pull Request #9477 and there is
at least one known user. If we revisit this design and deprecate the old metric, we should coordinate with downstream users so they can migrate before the removal.
Prefix Cache metrics¶

The discussion in
Issue #10582 about adding prefix cache metrics yielded some interesting points which may be relevant to how we approach future metrics.

Every time the prefix cache is queried, we record the number of tokens queried and the number of queried tokens present in the cache (i.e. hits).

However, the metric of interest is the hit rate - i.e. the number of hits per query.

In the case of logging, we expect the user is best served by calculating the hit rate over a fixed number of the most recent queries (the interval is fixed to 1k most recent queries for now).

In the case of Prometheus though, we should take advantage of the time-series nature of Prometheus and allow the user to calculate the hit rate over an interval of their choosing. For example, a PromQL query to calculate the hit interval of the past 5 minutes:

rate(cache_query_hit[5m]) / rate(cache_query_total[5m])

To achieve this, we should record the queries and hits as counters in Prometheus, rather than recording the hit rate as a gauge.
Deprecated Metrics¶
How To Deprecate¶

Deprecating metrics shouldn't be taken lightly. Users may not notice a metric has been deprecated, and may be quite inconvenienced when it is suddenly (from their perspective) when it is removed, even if there is an equivalent metric for them to use.

As an example, see how vllm:avg_prompt_throughput_toks_per_s was
deprecated (with a comment in the code),
removed, and then
noticed by a user.

In general:

    We should be cautious about deprecating metrics, especially since it can be hard to predict the user impact.
    We should include a prominent deprecation notice in the help string that is included in the `/metrics' output.
    We should list deprecated metrics in user-facing documentation and release notes.
    We should consider hiding deprecated metrics behind a CLI argument in order to give administrators an escape hatch for some time before deleting them.

See the deprecation policy for the project-wide deprecation policy.
Unimplemented - vllm:tokens_total¶

Added by
Pull Request #4464, but apparently never implemented. This can just be removed.
Duplicated - Queue Time¶

The vllm:time_in_queue_requests Histogram metric was added by
Pull Request #9659 and its calculation is:

    
self.metrics.first_scheduled_time = now
    
self.metrics.time_in_queue = now - self.metrics.arrival_time

Two weeks later,
Pull Request #4464 added vllm:request_queue_time_seconds leaving us with:

if seq_group.is_finished():
    
if (seq_group.metrics.first_scheduled_time is not None and
            
seq_group.metrics.first_token_time is not None):
        
time_queue_requests.append(
            
seq_group.metrics.first_scheduled_time -
            
seq_group.metrics.arrival_time)
    
...
    
if seq_group.metrics.time_in_queue is not None:
        
time_in_queue_requests.append(
            
seq_group.metrics.time_in_queue)

This seems duplicative, and one of them should be removed. The latter is used by the Grafana dashboard, so we should deprecate or remove the former.
Prefix Cache Hit Rate¶

See above - we now expose 'queries' and 'hits' counters rather than a 'hit rate' gauge.
KV Cache Offloading¶

Two legacy metrics relate to a "swapped" preemption mode that is no longer relevant in v1:

    vllm:num_requests_swapped
    vllm:cpu_cache_usage_perc

In this mode, when a request is preempted (e.g. to make room in KV cache to complete other requests), we swap kv cache blocks out to CPU memory. This is also known as "KV cache offloading" and is configured with --swap-space and --preemption-mode.

Historically,
vLLM has long supported beam search. The SequenceGroup encapsulated the idea of N Sequences which all shared the same prompt kv blocks. This enabled KV cache block sharing between requests, and copy-on-write to do branching. CPU swapping was intended for these beam search like cases.

Later, the concept of prefix caching was introduced, which allowed KV cache blocks to be shared implicitly. This proved to be a better option than CPU swapping since blocks can be evicted slowly on demand and the part of the prompt that was evicted can be recomputed.

SequenceGroup was removed in V1, although a replacement will be required for "parallel sampling" (n>1).
Beam search was moved out of the core. There was a lot of complex code for a very uncommon feature.

In V1, with prefix caching being better (zero over head) and therefore on by default, the preemption and recompute strategy should work better.
Future Work¶
Parallel Sampling¶

Some legacy metrics are only relevant in the context of "parallel sampling". This is where the n parameter in a request is used to request multiple completions from the same prompt.

As part of adding parallel sampling support in
Pull Request #10980, we should also add these metrics.

    vllm:request_params_n (Histogram)

Observes the value of the 'n' parameter of every finished request.

    vllm:request_max_num_generation_tokens (Histogram)

Observes the maximum output length of all sequences in every finished sequence group. In the absence of parallel sampling, this is equivalent to vllm:request_generation_tokens.
Speculative Decoding¶

Some legacy metrics are specific to "speculative decoding". This is where we generate candidate tokens using a faster, approximate method or model and then validate those tokens with the larger model.

    vllm:spec_decode_draft_acceptance_rate (Gauge)
    vllm:spec_decode_efficiency (Gauge)
    vllm:spec_decode_num_accepted_tokens (Counter)
    vllm:spec_decode_num_draft_tokens (Counter)
    vllm:spec_decode_num_emitted_tokens (Counter)

There is a PR under review (
Pull Request #12193) to add "prompt lookup (ngram)" speculative decoding to v1. Other techniques will follow. We should revisit these metrics in this context.

Note

We should probably expose acceptance rate as separate accepted and draft counters, like we do for prefix caching hit rate. Efficiency likely also needs similar treatment.
Autoscaling and Load-balancing¶

A common use case for our metrics is to support automated scaling of vLLM instances.

For related discussion from the Kubernetes Serving Working Group, see:

    Standardizing Large Model Server Metrics in Kubernetes
    Benchmarking LLM Workloads for Performance Evaluation and Autoscaling in Kubernetes
    Inference Perf
    Issue #5041 and
    Pull Request #12726.

This is a non-trivial topic. Consider this comment from Rob:

    I think this metric should focus on trying to estimate what the max concurrency that will cause the average request length > queries per second ... since this is really what will "saturate" the server.

A clear goal is that we should expose the metrics required to detect this saturation point, so administrators can implement auto-scaling rules based on those. However, in order to do so, we need to have a clear view on how an administrator (and automated monitoring system) should judge an instance as approaching saturation:

    To identify, what is the saturation point for model server compute (the inflection point where we cannot get more throughput with a higher request rate, but start to incur additional latency) so we can autoscale effectively?

Metric Naming¶

Our approach to naming metrics probably deserves to be revisited:

    The use of colons in metric names seems contrary to "colons are reserved for user defined recording rules".
    Most of our metrics follow the convention of ending with units, but not all do.

    Some of our metric names end with _total:

    If there is a suffix of _total on the metric name, it will be removed. When exposing the time series for counter, a _total suffix will be added. This is for compatibility between OpenMetrics and the Prometheus text format, as OpenMetrics requires the _total suffix.

Adding More Metrics¶

There is no shortage of ideas for new metrics:

    Examples from other projects like TGI
    Proposals arising from specific use cases, like the Kubernetes auto-scaling topic above
    Proposals that might arise out of standardisation efforts like OpenTelemetry Semantic Conventions for Gen AI.

We should be cautious in our approach to adding new metrics. While metrics are often relatively straightforward to add:

    They can be difficult to remove - see the section on deprecation above.
    They can have a meaningful performance impact when enabled. And metrics are usually of very limited use unless they can be enabled by default and in production.
    They have an impact on development and maintenance of the project. Every metric added over time has made this effort more time-consuming, and perhaps not all metrics justify this ongoing investment in their maintenance.

Tracing - OpenTelemetry¶

Metrics provide an aggregated view over time of the system's performance and health. Tracing, on the other hand, tracks individual requests as they move through different services and components. Both fall under the more general heading of "Observability".

vLLM has support for OpenTelemetry tracing:

    Added by
    Pull Request #4687 and reinstated by
    Pull Request #20372
    Configured with --oltp-traces-endpoint and --collect-detailed-traces
    OpenTelemetry blog post
    User-facing docs
    Blog post
    IBM product docs

OpenTelemetry has a Gen AI Working Group.

Since metrics is a big enough topic on its own, we consider the topic of tracing to be quite separate from metrics.
OpenTelemetry Model Forward vs Execute Time¶

The current implementation exposes the following two metrics:

    vllm:model_forward_time_milliseconds (Histogram) - The time spent in the model forward pass when this request was in the batch.
    vllm:model_execute_time_milliseconds (Histogram) - The time spent in the model execute function. This will include model forward, block/sync across workers, cpu-gpu sync time and sampling time.

These metrics are only enabled when OpenTelemetry tracing is enabled and if --collect-detailed-traces=all/model/worker is used. The documentation for this option states:

    collect detailed traces for the specified modules. This involves use of possibly costly and or blocking operations and hence might have a performance impact.

The metrics were added by
Pull Request #7089 and who up in an OpenTelemetry trace as:

-> gen_ai.latency.time_in_scheduler: Double(0.017550230026245117)
-> gen_ai.latency.time_in_model_forward: Double(3.151565277099609)
-> gen_ai.latency.time_in_model_execute: Double(3.6468167304992676)

We already have inference_time and decode_time metrics, so the question is whether there are sufficiently common use cases for the higher-resolution timings to justify the overhead.

Since we are going to treat the question of OpenTelemetry support separately, we will include these particular metrics under that topic.
February 27, 2026
Made with Material for MkDocs

Paged Attention¶

Warning

This is a historical document based on the original paper for vLLM. It no longer describes the code used in vLLM today.

Currently, vLLM utilizes its own implementation of a multi-head query attention kernel (csrc/attention/attention_kernels.cu). This kernel is designed to be compatible with vLLM's paged KV caches, where the key and value cache are stored in separate blocks (note that this block concept differs from the GPU thread block. So in a later document, I will refer to vLLM paged attention block as "block", while refer to GPU thread block as "thread block").

To achieve high performance, this kernel relies on a specially designed memory layout and access method, specifically when threads read data from global memory to shared memory. The purpose of this document is to provide a high-level explanation of the kernel implementation step by step, aiding those who wish to learn about the vLLM multi-head query attention kernel. After going through this document, users will likely have a better understanding and feel easier to follow the actual implementation.

Please note that this document may not cover all details, such as how to calculate the correct index for the corresponding data or the dot multiplication implementation. However, after reading this document and becoming familiar with the high-level logic flow, it should be easier for you to read the actual code and understand the details.
Inputs¶

The kernel function takes a list of arguments for the current thread to perform its assigned work. The three most important arguments are the input pointers q, k_cache, and v_cache, which point to query, key, and value data on global memory that need to be read and processed. The output pointer out points to global memory where the result should be written. These four pointers actually refer to multidimensional arrays, but each thread only accesses the portion of data assigned to it. I have omitted all other runtime parameters here for simplicity.

template<typename scalar_t, int HEAD_SIZE, int BLOCK_SIZE, int NUM_THREADS, int PARTITION_SIZE = 0>
__device__ void paged_attention_kernel(
    ... // Other side args.
    const scalar_t* __restrict__ out,       // [num_seqs, num_heads, max_num_partitions, head_size]
    const scalar_t* __restrict__ q,         // [num_seqs, num_heads, head_size]
    const scalar_t* __restrict__ k_cache,   // [num_blocks, num_kv_heads, head_size/x, block_size, x]
    const scalar_t* __restrict__ v_cache,   // [num_blocks, num_kv_heads, head_size, block_size]
    ... // Other side args.
)

There are also a list of template arguments above the function signature that are determined during compilation time. scalar_t represents the data type of the query, key, and value data elements, such as FP16. HEAD_SIZE indicates the number of elements in each head. BLOCK_SIZE refers to the number of tokens in each block. NUM_THREADS denotes the number of threads in each thread block. PARTITION_SIZE represents the number of tensor parallel GPUs (For simplicity, we assume this is 0 and tensor parallel is disabled).

With these arguments, we need to perform a sequence of preparations. This includes calculating the current head index, block index, and other necessary variables. However, for now, we can ignore these preparations and proceed directly to the actual calculations. It will be easier to understand them once we grasp the entire flow.
Concepts¶

Just before we dive into the calculation flow, I want to describe a few concepts that are needed for later sections. However, you may skip this section and return later if you encounter any confusing terminologies.

    Sequence: A sequence represents a client request. For example, the data pointed to by q has a shape of [num_seqs, num_heads, head_size]. That represents there are total num_seqs of query sequence data are pointed by q. Since this kernel is a single query attention kernel, each sequence only has one query token. Hence, the num_seqs equals the total number of tokens that are processed in the batch.
    Context: The context consists of the generated tokens from the sequence. For instance, ["What", "is", "your"] are the context tokens, and the input query token is "name". The model might generate the token "?".
    Vec: The vec is a list of elements that are fetched and calculated together. For query and key data, the vec size (VEC_SIZE) is determined so that each thread group can fetch and calculate 16 bytes of data at a time. For value data, the vec size (V_VEC_SIZE) is determined so that each thread can fetch and calculate 16 bytes of data at a time. For example, if the scalar_t is FP16 (2 bytes) and THREAD_GROUP_SIZE is 2, the VEC_SIZE will be 4, while the V_VEC_SIZE will be 8.
    Thread group: The thread group is a small group of threads(THREAD_GROUP_SIZE) that fetches and calculates one query token and one key token at a time. Each thread handles only a portion of the token data. The total number of elements processed by one thread group is referred as x. For example, if the thread group contains 2 threads and the head size is 8, then thread 0 handles the query and key elements at index 0, 2, 4, 6, while thread 1 handles the elements at index 1, 3, 5, 7.
    Block: The key and value cache data in vLLM are split into blocks. Each block stores data for a fixed number(BLOCK_SIZE) of tokens at one head. Each block may contain only a portion of the whole context tokens. For example, if the block size is 16 and the head size is 128, then for one head, one block can store 16 * 128 = 2048 elements.
    Warp: A warp is a group of 32 threads(WARP_SIZE) that execute simultaneously on a stream multiprocessor (SM). In this kernel, each warp processes the calculation between one query token and key tokens of one entire block at a time (it may process multiple blocks in multiple iterations). For example, if there are 4 warps and 6 blocks for one context, the assignment would be like warp 0 handles the 0th, 4th blocks, warp 1 handles the 1st, 5th blocks, warp 2 handles the 2nd block and warp 3 handles the 3rd block.
    Thread block: A thread block is a group of threads(NUM_THREADS) that can access the same shared memory. Each thread block contains multiple warps(NUM_WARPS), and in this kernel, each thread block processes the calculation between one query token and key tokens of a whole context.
    Grid: A grid is a collection of thread blocks and defines the shape of the collection. In this kernel, the shape is (num_heads, num_seqs, max_num_partitions). Therefore, each thread block only handles the calculation for one head, one sequence, and one partition.

Query¶

This section will introduce how query data is stored in memory and fetched by each thread. As mentioned above, each thread group fetches one query token data, while each thread itself only handles a part of one query token data. Within each warp, every thread group will fetch the same query token data, but will multiply it with different key token data.

const scalar_t* q_ptr = q + seq_idx * q_stride + head_idx * HEAD_SIZE;

query

Each thread defines its own q_ptr which points to the assigned query token data on global memory. For example, if VEC_SIZE is 4 and HEAD_SIZE is 128, the q_ptr points to data that contains total of 128 elements divided into 128 / 4 = 32 vecs.

q_vecs

__shared__ Q_vec q_vecs[THREAD_GROUP_SIZE][NUM_VECS_PER_THREAD];

Next, we need to read the global memory data pointed to by q_ptr into shared memory as q_vecs. It is important to note that each vecs is assigned to a different row. For example, if the THREAD_GROUP_SIZE is 2, thread 0 will handle the 0th row vecs, while thread 1 handles the 1st row vecs. By reading the query data in this way, neighboring threads like thread 0 and thread 1 can read neighbor memory, achieving the memory coalescing to improve performance.
Key¶

Similar to the "Query" section, this section introduces memory layout and assignment for keys. While each thread group only handle one query token one kernel run, it may handle multiple key tokens across multiple iterations. Meanwhile, each warp will process multiple blocks of key tokens in multiple iterations, ensuring that all context tokens are processed by the entire thread group after the kernel run. In this context, "handle" refers to performing the dot multiplication between query data and key data.

const scalar_t* k_ptr = k_cache + physical_block_number * kv_block_stride
                    + kv_head_idx * kv_head_stride
                    + physical_block_offset * x;

Unlike to q_ptr, k_ptr in each thread will point to different key token at different iterations. As shown above, that k_ptr points to key token data based on k_cache at assigned block, assigned head and assigned token.

key

The diagram above illustrates the memory layout for key data. It assumes that the BLOCK_SIZE is 16, HEAD_SIZE is 128, x is 8, THREAD_GROUP_SIZE is 2, and there are a total of 4 warps. Each rectangle represents all the elements for one key token at one head, which will be processed by one thread group. The left half shows the total 16 blocks of key token data for warp 0, while the right half represents the remaining key token data for other warps or iterations. Inside each rectangle, there are a total 32 vecs (128 elements for one token) that will be processed by 2 threads (one thread group) separately.

k_vecs

K_vec k_vecs[NUM_VECS_PER_THREAD]

Next, we need to read the key token data from k_ptr and store them on register memory as k_vecs. We use register memory for k_vecs because it will only be accessed by one thread once, whereas q_vecs will be accessed by multiple threads multiple times. Each k_vecs will contain multiple vectors for later calculation. Each vec will be set at each inner iteration. The assignment of vecs allows neighboring threads in a warp to read neighboring memory together, which again promotes the memory coalescing. For instance, thread 0 will read vec 0, while thread 1 will read vec 1. In the next inner loop, thread 0 will read vec 2, while thread 1 will read vec 3, and so on.

You may still be a little confused about the overall flow. Don't worry, please keep reading the next "QK" section. It will illustrate the query and key calculation flow in a clearer and higher-level manner.
QK¶

As shown the pseudocode below, before the entire for loop block, we fetch the query data for one token and store it in q_vecs. Then, in the outer for loop, we iterate through different k_ptrs that point to different tokens and prepare the k_vecs in the inner for loop. Finally, we perform the dot multiplication between the q_vecs and each k_vecs.

q_vecs = ...
for ... {
    k_ptr = ...
    for ... {
        k_vecs[i] = ...
    }
    ...
    float qk = scale * Qk_dot<scalar_t, THREAD_GROUP_SIZE>::dot(q_vecs[thread_group_offset], k_vecs);
}

As mentioned before, for each thread, it only fetches part of the query and key token data at a time. However, there will be a cross thread group reduction happen in the Qk_dot<>::dot . So qk returned here is not just between part of the query and key token dot multiplication, but actually a full result between entire query and key token data.

For example, if the value of HEAD_SIZE is 128 and THREAD_GROUP_SIZE is 2, each thread's k_vecs will contain total 64 elements. However, the returned qk is actually the result of dot multiplication between 128 query elements and 128 key elements. If you want to learn more about the details of the dot multiplication and reduction, you may refer to the implementation of Qk_dot<>::dot. However, for the sake of simplicity, I will not cover it in this document.
Softmax¶

Next, we need to calculate the normalized softmax for all qks, as shown above, where each represents a qk. To do this, we must obtain the reduced value of qk_max() and the exp_sum() of all qks. The reduction should be performed across the entire thread block, encompassing results between the query token and all context key tokens.
qk_max and logits¶

Just right after we get the qk result, we can set the temporary logits result with qk (In the end, the logits should store the normalized softmax result). Also we can compare and collect the qk_max for all qks that are calculated by current thread group.

if (thread_group_offset == 0) {
    const bool mask = token_idx >= context_len;
    logits[token_idx - start_token_idx] = mask ? 0.f : qk;
    qk_max = mask ? qk_max : fmaxf(qk_max, qk);
}

Please note that the logits here is on shared memory, so each thread group will set the fields for its own assigned context tokens. Overall, the size of logits should be number of context tokens.

for (int mask = WARP_SIZE / 2; mask >= THREAD_GROUP_SIZE; mask /= 2) {
    qk_max = fmaxf(qk_max, VLLM_SHFL_XOR_SYNC(qk_max, mask));
}

if (lane == 0) {
    red_smem[warp_idx] = qk_max;
}

Then we need to get the reduced qk_max across each warp. The main idea is to make threads in warp to communicate with each other and get the final max qk .

for (int mask = NUM_WARPS / 2; mask >= 1; mask /= 2) {
    qk_max = fmaxf(qk_max, VLLM_SHFL_XOR_SYNC(qk_max, mask));
}
qk_max = VLLM_SHFL_SYNC(qk_max, 0);

Finally, we can get the reduced qk_max from whole thread block by compare the qk_max from all warps in this thread block. Then we need to broadcast the final result to each thread.
exp_sum¶

Similar to qk_max, we need to get the reduced sum value from the entire thread block too.

for (int i = thread_idx; i < num_tokens; i += NUM_THREADS) {
    float val = __expf(logits[i] - qk_max);
    logits[i] = val;
    exp_sum += val;
}
...
exp_sum = block_sum<NUM_WARPS>(&red_smem[NUM_WARPS], exp_sum);

Firstly, sum all exp values from each thread group, and meanwhile, convert each entry of logits from qk to exp(qk - qk_max). Please note, the qk_max here is already the max qk across the whole thread block. And then we can do reduction for exp_sum across whole thread block just like the qk_max.

const float inv_sum = __fdividef(1.f, exp_sum + 1e-6f);
for (int i = thread_idx; i < num_tokens; i += NUM_THREADS) {
    logits[i] *= inv_sum;
}

Finally, with the reduced qk_max and exp_sum, we can obtain the final normalized softmax result as logits. This logits variable will be used for dot multiplication with the value data in later steps. Now, it should store the normalized softmax result of qk for all assigned context tokens.
Value¶

value

logits_vec

v_vec

Now we need to retrieve the value data and perform dot multiplication with logits. Unlike query and key, there is no thread group concept for value data. As shown in diagram, different from key token memory layout, elements from the same column correspond to the same value token. For one block of value data, there are HEAD_SIZE of rows and BLOCK_SIZE of columns that are split into multiple v_vecs.

Each thread always fetches V_VEC_SIZE elements from the same V_VEC_SIZE of tokens at a time. As a result, a single thread retrieves multiple v_vecs from different rows and the same columns through multiple inner iterations. For each v_vec, it needs to be dot multiplied with the corresponding logits_vec, which is also V_VEC_SIZE elements from logits. Overall, with multiple inner iterations, each warp will process one block of value tokens. And with multiple outer iterations, the whole context value tokens are processed

float accs[NUM_ROWS_PER_THREAD];
for ... { // Iteration over different blocks.
    logits_vec = ...
    for ... { // Iteration over different rows.
        v_vec = ...
        ...
        accs[i] += dot(logits_vec, v_vec);
    }
}

As shown in the above pseudocode, in the outer loop, similar to k_ptr, logits_vec iterates over different blocks and reads V_VEC_SIZE elements from logits. In the inner loop, each thread reads V_VEC_SIZE elements from the same tokens as a v_vec and performs dot multiplication. It is important to note that in each inner iteration, the thread fetches different head position elements for the same tokens. The dot result is then accumulated in accs. Therefore, each entry of accs is mapped to a head position assigned to the current thread.

For example, if BLOCK_SIZE is 16 and V_VEC_SIZE is 8, each thread fetches 8 value elements for 8 tokens at a time. Each element is from different tokens at the same head position. If HEAD_SIZE is 128 and WARP_SIZE is 32, for each inner loop, a warp needs to fetch WARP_SIZE * V_VEC_SIZE = 256 elements. This means there are a total of 128 * 16 / 256 = 8 inner iterations for a warp to handle a whole block of value tokens. And each accs in each thread contains 8 elements that accumulated at 8 different head positions. For the thread 0, the accs variable will have 8 elements, which are 0th, 32nd … 224th elements of a value head that are accumulated from all assigned 8 tokens.
LV¶

Now, we need to perform reduction for accs within each warp. This process allows each thread to accumulate the accs for the assigned head positions of all tokens in one block.

for (int i = 0; i < NUM_ROWS_PER_THREAD; i++) {
    float acc = accs[i];
    for (int mask = NUM_V_VECS_PER_ROW / 2; mask >= 1; mask /= 2) {
        acc += VLLM_SHFL_XOR_SYNC(acc, mask);
    }
    accs[i] = acc;
}

Next, we perform reduction for accs across all warps, allowing each thread to have the accumulation of accs for the assigned head positions of all context tokens. Please note that each accs in every thread only stores the accumulation for a portion of elements of the entire head for all context tokens. However, overall, all results for output have been calculated but are just stored in different thread register memory.
Code

Output¶

Now we can write all of calculated result from local register memory to final output global memory.

scalar_t* out_ptr = out + seq_idx * num_heads * max_num_partitions * HEAD_SIZE
                + head_idx * max_num_partitions * HEAD_SIZE
                + partition_idx * HEAD_SIZE;

First, we need to define the out_ptr variable, which points to the start address of the assigned sequence and assigned head.

for (int i = 0; i < NUM_ROWS_PER_THREAD; i++) {
    const int row_idx = lane / NUM_V_VECS_PER_ROW + i * NUM_ROWS_PER_ITER;
    if (row_idx < HEAD_SIZE && lane % NUM_V_VECS_PER_ROW == 0) {
        from_float(*(out_ptr + row_idx), accs[i]);
    }
}

Finally, we need to iterate over different assigned head positions and write out the corresponding accumulated result based on the out_ptr.
Citation¶

@inproceedings{kwon2023efficient,
  title={Efficient Memory Management for Large Language Model Serving with PagedAttention},
  author={Woosuk Kwon and Zhuohan Li and Siyuan Zhuang and Ying Sheng and Lianmin Zheng and Cody Hao Yu and Joseph E. Gonzalez and Hao Zhang and Ion Stoica},
  booktitle={Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles},
  year={2023}
}

Automatic Prefix Caching¶

Prefix caching kv-cache blocks is a popular optimization in LLM inference to avoid redundant prompt computations. The core idea is simple – we cache the kv-cache blocks of processed requests, and reuse these blocks when a new request comes in with the same prefix as previous requests. Since prefix caching is almost a free lunch and won’t change model outputs, it has been widely used by many public endpoints (e.g., OpenAI, Anthropic, etc.) and most open source LLM inference frameworks (e.g., SGLang).

While there are many ways to implement prefix caching, vLLM chooses a hash-based approach. Specifically, we hash each kv-cache block by the tokens in the block and the tokens in the prefix before the block:

                    Block 1                  Block 2                  Block 3
         [A gentle breeze stirred] [the leaves as children] [laughed in the distance]
Block 1: |<--- block tokens ---->|
Block 2: |<------- prefix ------>| |<--- block tokens --->|
Block 3: |<------------------ prefix -------------------->| |<--- block tokens ---->|

In the example above, the KV cache in the first block can be uniquely identified with the token “A gentle breeze stirred”. The third block can be uniquely identified with the tokens in the block “laughed in the distance”, along with the prefix tokens “A gentle breeze stirred the leaves as children”. Therefore, we can build the block hash of hash(tuple[components]), where components are:

    Parent hash value: The hash value of the parent hash block.
    Block tokens: A tuple of tokens in this block. The reason to include the exact tokens is to reduce potential hash value collision.
    Extra hashes: Other values required to make this block unique, such as LoRA IDs, multi-modality input hashes (see the example below), and cache salts to isolate caches in multi-tenant environments.

Note 1

We only cache full blocks.

Note 2

In previous versions, the hash key was not guaranteed to be collision-free. As of v0.11, the default hashing algorithm is sha256, which addresses collision risks.

For vllm serve, you can control the hashing algorithm via --prefix-caching-hash-algo: - sha256 (default): Uses Python's pickle for serialization. Hashes may not be reproducible across different Python or vLLM versions. - sha256_cbor: Uses cbor2 for serialization, providing a reproducible, cross-language compatible hash. This is recommended for deterministic caching across environments. - xxhash: Uses Pickle serialization with xxHash (128-bit) for faster, non-cryptographic hashing. Requires the optionalxxhashpackage. IMPORTANT: Use of a hashing algorithm that is not considered cryptographically secure theoretically increases the risk of hash collisions, which can cause undefined behavior or even leak private information in multi-tenant environments. Even if collisions are still very unlikely, it is important to consider your security risk tolerance against the performance benefits before turning this on. -xxhash_cborcombines canonical CBOR serialization with xxHash for reproducible hashing. Requires the optionalxxhash` package.

A hashing example with multi-modality inputs
In this example, we illustrate how prefix caching works with multi-modality inputs (e.g., images). Assuming we have a request with the following messages:

messages = [
    {"role": "user",
     "content": [
         {"type": "text",
          "text": "What's in this image?"
         },
         {"type": "image_url",
          "image_url": {"url": image_url},
         },
    ]},
]

It will become the following prompt:

Prompt:
    <s>[INST]What's in this image?\n[IMG][/INST]

Tokenized prompt:
    [1, 3, 7493, 1681, 1294, 1593, 3937, 9551, 10, 4]

Prompt with placeholders (<P>):
    [1, 3, 7493, 1681, 1294, 1593, 3937, 9551, <P>, <P>, ..., <P>, 4]

As we can see, after the tokenization, the [IMG] will be replaced by a sequence of placeholder tokens, and these placeholders will be replaced by image embeddings during prefill. The challenge for prefix caching to support this case is we need to differentiate images from the placeholders. To address this problem, we encode the image hash generated by the frontend image processor. For example, the hash of the blocks in the above prompt would be (assuming block size 16, and we have 41 placeholder tokens):

Block 0
    Parent hash: None
    Token IDs: 1, 3, 7493, 1681, 1294, 1593, 3937, 9551, <p>, ..., <p>
    Extra hash: <image hash>
Block 1
    Parent hash: Block 0 hash
    Token IDs: <p>, ..., <p>
    Extra hash: <image hash>
Block 2
    Parent hash: Block 1 hash
    Token IDs: <p>, ..., <p>
    Extra hash: <image hash>
Block 3
    Parent hash: Block 2 hash
    Token IDs: <p>, ..., <p>, 4
    Extra hash: <image hash>

In the rest of this document, we first introduce the data structure used for prefix caching in vLLM v1, followed by the prefix caching workflow of major KV cache operators (e.g., allocate, append, free, eviction). Finally, we use an example to illustrate the end to end prefix caching workflow.

Cache Isolation for Security To improve privacy in shared environments, vLLM supports isolating prefix cache reuse through optional per-request salting. By including a cache_salt in the request, this value is injected into the hash of the first block, ensuring that only requests with the same salt can reuse cached KV blocks. This prevents timing-based attacks where an adversary could infer cached content by observing latency differences. This offers protection without compromising performance.

{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Here is a document with details about the world series: ..."},
    {"role": "user", "content": "Who won the world series in 2020?"}
  ],
  "cache_salt": "your-cache-salt"
}

With this setup, cache sharing is limited to users or requests that explicitly agree on a common salt, enabling cache reuse within a trust group while isolating others.
Data Structure¶

The prefix caching in vLLM v1 is implemented in the KV cache manager. The basic building block is the “Block” data class (simplified):

class KVCacheBlock:
    
# The block ID (immutable)
    
block_id: int
    
# The block hash (will be assigned when the block is full,
    
# and will be reset when the block is evicted).
    
block_hash: BlockHash
    
# The number of requests using this block now.
    
ref_cnt: int

    
# The pointers to form a doubly linked list for the free queue.
    
prev_free_block: "KVCacheBlock | None" = None
    
next_free_block: "KVCacheBlock | None" = None

There are two design points to highlight:

    We allocate all KVCacheBlock when initializing the KV cache manager to be a block pool. This avoids Python object creation overheads and can easily track all blocks all the time.
    We introduce doubly linked list pointers directly in the KVCacheBlock, so that we could construct a free queue directly. This gives us two benefits:
        We could have O(1) complexity moving elements in the middle to the tail.
        We could avoid introducing another Python queue (e.g., deque) which has a wrapper to the elements.

As a result, we will have the following components when the KV cache manager is initialized:

Component Overview

    Block Pool: A list of KVCacheBlock.
    Free Block Queue: Only store the pointers of head and tail blocks for manipulations.
    Cache blocks: Mapping from hash key to block IDs.
    Request blocks: Mapping from request ID to allocated block IDs.

Operations¶
Block Allocation¶

New request: Workflow for the scheduler to schedule a new request with KV cache block allocation:

    The scheduler calls kv_cache_manager.get_computed_blocks() to get a sequence of blocks that have already been computed. This is done by hashing the prompt tokens in the request and looking up cache blocks.
    The scheduler calls kv_cache_manager.allocate_slots(). It does the following steps:
        Compute the number of new required blocks, and return if there are no sufficient blocks to allocate.
        “Touch” the computed blocks. It increases the reference count of the computed block by one, and removes the block from the free queue if the block wasn’t used by other requests. This is to avoid these computed blocks being evicted. See the example in the next section for illustration.
        Allocate new blocks by popping the heads of the free queue. If the head block is a cached block, this also “evicts” the block so that no other requests can reuse it anymore from now on.
        If an allocated block is already full of tokens, we immediately add it to the cache block, so that the block can be reused by other requests in the same batch.

Running request: Workflow for the scheduler to schedule a running request with KV cache block allocation:

    The scheduler calls kv_cache_manager.allocate_slots(). It does the following steps:
        Compute the number of new required blocks, and return if there are no sufficient blocks to allocate.
        Allocate new blocks by popping the heads of the free queue. If the head block is a cached block, this also “evicts” the block so that no other requests can reuse it anymore from now on.
        Append token IDs to the slots in existing blocks as well as the new blocks. If a block is full, we add it to the cache block to cache it.

Duplicated blocks
Assuming block size is 4 and you send a request (Request 1) with prompt ABCDEF and decoding length 3:

Prompt: [A, B, C, D, E, F]
Output: [G, H, I]

Time 0:
  Tokens: [A, B, C, D, E, F, G]
  Block Table: [0 (ABCD), 1 (EFG)]
  Cache Blocks: 0
Time 1:
  Tokens: [A, B, C, D, E, F, G, H]
  Block Table: [0 (ABCD), 1 (EFGH)]
  Cache Blocks: 0, 1
Time 2:
  Tokens: [A, B, C, D, E, F, G, H, I]
  Block Table: [0 (ABCD), 1 (EFGH), 2 (I)]
  Cache Blocks: 0, 1

Now block 0 and block 1 are cached, and we send the same request again (Request 2) with greedy sampling, so that it will produce exactly the same outputs as the Request 1:

Prompt: [A, B, C, D, E, F]
Output: [G, H, I]

Time 0:
  Tokens: [A, B, C, D, E, F, G]
  Block Table: [0 (ABCD), 3 (EFG)]
  Cache Blocks: 0, 1
Time 1:
  Tokens: [A, B, C, D, E, F, G, H]
  Block Table: [0 (ABCD), 3 (EFGH)]
  Cache Blocks: 0, 1, 3

As can be seen, block 3 is a new full block and is cached. However, it is redundant as block 1, meaning that we cached the same block twice. In v0, when detecting block 3 is duplicated, we free block 3 and let Request 2 use block 1 instead, so its block table becomes [0, 1] in Time 1. However, the block table in vLLM v1 is append-only, meaning that changing the block table from [0, 3] to [0, 1] is not allowed. As a result, we will have duplicated blocks for the hash key E-H. This duplication will be eliminated when the request is freed.
Free¶

When a request is finished, we free all its blocks if no other requests are using them (reference count = 0). In this example, we free request 1 and block 2, 3, 4, 8 associated with it. We can see that the freed blocks are added to the tail of the free queue in the reverse order. This is because the last block of a request must hash more tokens and is less likely to be reused by other requests. As a result, it should be evicted first.

Free queue after a request us freed
Eviction (LRU)¶

When the head block (least recently used block) of the free queue is cached, we have to evict the block to prevent it from being used by other requests. Specifically, eviction involves the following steps:

    Pop the block from the head of the free queue. This is the LRU block to be evicted.
    Remove the block ID from the cache block.
    Remove the block hash.

Example¶

In this example, we assume the block size is 4 (each block can cache 4 tokens), and we have 10 blocks in the KV-cache manager in total.

Time 1: The cache is empty and a new request comes in. We allocate 4 blocks. 3 of them are already full and cached. The fourth block is partially full with 3 of 4 tokens.

Example Time 1

Time 2: Request 0 makes the block 3 full and asks for a new block to keep decoding. We cache block 3 and allocate block 4.

Example Time 2

Time 3: Request 1 comes in with the 14 prompt tokens, where the first 10 tokens are the same as request 0. We can see that only the first 2 blocks (8 tokens) hit the cache, because the 3rd block only matches 2 of 4 tokens.

Example Time 3

Time 4: Request 0 is finished and free. Blocks 2, 3 and 4 are added to the free queue in the reverse order (but block 2 and 3 are still cached). Block 0 and 1 are not added to the free queue because they are being used by Request 1.

Example Time 4

Time 5: Request 1 is finished and free.

Example Time 5

Time 6: Request 2 comes in with the 29 prompt tokens, where the first 12 tokens are the same as request 0. Note that even the block order in the free queue was 7 - 8 - 9 - 4 - 3 - 2 - 6 - 5 - 1 - 0, the cache hit blocks (i.e., 0, 1, 2) are touched and removed from the queue before allocation, so the free queue becomes 7 - 8 - 9 - 4 - 3 - 6 - 5. As a result, the allocated blocks are 0 (cached), 1 (cached), 2 (cached), 7, 8, 9, 4, 3 (evicted).

Hybrid KV Cache Manager¶

Warning

This document was written based on commit 458e74. This feature is still in its early stage and things may change.
What is a hybrid model?¶

Many recent "hybrid" LLMs combine multiple attention types within one model. For example:

    Sliding window attention (sw) + full attention (full): gpt-oss, Gemma 2/3, Ministral, cohere, etc.
    Mamba + full: Bamba, Jamba, Minimax, etc.
    Local chunked attention + full: Llama4

To serve these models efficiently, our KVCacheManager must:

    Allocate different slots to different layer type, for example:
        Full attention layers: reserve slots for all tokens.
        Sliding window layers: reserve slots only for the most recent sliding_window_size tokens.
    Support layer-specific prefix-cache rules, for example:
        Full attention: a cache hit prefix requires all tokens remain in the KV cache.
        Sliding window: a cache hit prefix only requires the last sliding_window_size tokens remain in the KV cache.

Definitions¶

    kv hidden size: The number of bytes to store one token's KV cache for a single layer.
    block: the memory reserved for kv cache are divided into multiple blocks with the same page size (defined below)
    block size: number of tokens inside a block

    page size: the physical memory size of a block, defined as:

    num_layers doesn't mean the total number of layers in the model. The exact number depends on the context in this doc.

    Note

    This is different from KVCacheSpec.page_size_bytes in the code, which is defined as:

Allocation¶
High level idea¶

We use a single memory pool for all layer types. The memory pool is split into multiple blocks with the same page size. KVCacheManager allocates different numbers of blocks to different layers according to its attention type.

The core challenge is ensuring every layer type uses the same page size. For full-attention-only models, the page size is straightforward, defined as:

However, in hybrid models, num_hidden_layers varies by attention type, which would normally produce mismatched page sizes. The cases below show how we unify them.
Case 1: toy model¶

Let's start with a toy example: a model has 1 full attention layer and 3 sliding window attention layers. All layers have the same kv_hidden_size.

We let each block to hold block_size tokens for one layer, so:

KVCacheManager allocates a different number of blocks to each layer.

This case is only a toy example. For real models, please refer to the following cases.
Case 2: same kv_hidden_size and a regular pattern¶

When the model has more layers, e.g., 20 sliding window attention layers and 10 full attention layers with the same kv_hidden_size. Calling the allocator once per layer (30 calls) is OK but becomes inefficient. As a solution, we group the allocation of layers that need the same number of blocks to reduce the number of calls.

The grouping is feasible because there is usually a beautiful ratio between the number of different types of layers. For example:

    Gemma-2: 1 sw : 1 full
    Llama 4: 3 local : 1 full

Our example can be regarded as 2 sw : 1 full. We can allocate blocks as if there are 2 sw and 1 full in the model, and repeat the result by 10 times to generate the block_ids for the 30 layers. The page size becomes:

Assume block_size 16, sliding window size 32, request length 112, then for the above example model, we need to allocate 11 blocks (0-6 for full, 7-8 for sw group 1, 9-10 for sw group 2).

Allocation Result

Here, "/" denotes no block needed (sliding‑window layers don't need slots for early tokens).

See the formal definition below. The layers are divided into multiple KV Cache Groups so that there is:

    Identical attention type inside each group: Each group only contains layers with the same attention type and thus need the same number of blocks for a given request. This enables layers in the same group share the same block ids without memory waste.
    Identical page size across groups: Because our memory pool only have one page size.

Our example model is divided into 3 KV cache groups:

    Group 0: 10 full attention layers (full.0 - full.9)
    Group 1: 10 sliding window attention layers (sw.0 - sw.9)
    Group 2: 10 sliding window attention layers (sw.10 - sw.19)

Obviously, it satisfies rule 1. For rule 2, all 3 groups have

as their page size.
Case 3: same kv_hidden_size and no regular pattern¶

Unfortunately, not all models have such a beautiful ratio, and approach in Case 2 will produce too many small groups. For example, Gemma-3-27b has 52 sliding window attention layers and 10 full attention layers. With the constraints in case 2, it would be 26 sliding window groups and 5 full attention groups, each contains 2 layers. The allocation is still inefficient. To reduce the number of kv cache groups, we group layers using the smallest layer count among all attention types. For example, min(52, 10)=10 layers per group in Gemma-3-27b. Then the grouping result is:

    Group 0: 10 full attention layers (full.0 - full.9)
    Group 1: 10 sliding window attention layers (sw.0 - sw.9)
    Group 2: 10 sliding window attention layers (sw.10 - sw.19)
    ...
    Group 6: 10 sliding window attention layers (sw.40 - sw.49)
    Group 7: 2 sliding window attention layers (sw.50 - sw.51) and 8 padding layers

We will update this algorithm if this heuristic leads to a bad result when a new model comes out (e.g., 20 full + 30 sw, the group size should be 10 instead of 20).

This case happens in Gemma-3 series models, and models in case 2 but with eagle speculative decoding which introduce one full attention layer. The solution has some memory waste and is not perfect. Please report any cases where padding overhead becomes unacceptable so we can refine the algorithm.
Case 4: different kv_hidden_size (mainly hybrid mamba models)¶

Some architectures (e.g., Bamba, Jamba, Minimax) interleave standard attention layers with Mamba layers, where each Mamba layer's state size per token can be much larger than the attention layers' kv_hidden_size. Because we only support a single page size across all groups, we must reconcile these differing hidden sizes.

The current algorithm is:

    Increase the block_size of attention layers until $$ \text{block_size} \times \text{kv_hidden_size}{\text{att}} \ge \text{state_size} $$}
    Pad the mamba state per layer to $$ \text{block_size} \times \text{kv_hidden_size}_{\text{att}} $$
    Apply the grouping strategy in case 3.

Note

This can lead to more than 400 block_size for attention layers, which is too large. Another padding strategy is to increase block_size until

This padding strategy is still a work in progress.
Case 5: KV sharing¶

KV sharing refers to a layer using the KV cache of another layer, e.g., gemma-3n. In these models, KVCacheManager ignores all layers with kv sharing and only allocates KV cache for layers that need kv cache, and some patches are made in model runner to apply the allocation result to kv sharing layers.
Prefix caching¶

For simplicity, we assume block_size=1 in this section.
High level idea¶

The block pool uses a dict similar to tuple(block_hash, group_id) -> block to catch the full blocks. That means the same tokens of different groups are cached and evicted independently.

When a new request comes in, we check the cache hit prefix of each group, and return the intersection of these groups as the cached prefix of the request. See below for the detailed algorithm for checking the cache hit of one group & performing the intersection.
Case 0: full attention only models¶

For full attention layers, blocks are allocated for all tokens in the request. For details on the underlying design, see Prefix Caching

To find the longest cache hit prefix of a request, we enumerate from left (the first block) to right (the last block), checking whether the block is cached, and exit when cache misses. For example, we will return the first 7 tokens (0-6) as the cache hit prefix in the below example (blue blocks are cached):

Prefix Caching of Full Attention
Case 1: sliding window attention only models¶

For sliding window attention layers, a naive implementation for memory allocation is to allocate sliding_window_size blocks and fill in the blocks in a round-robin way. But this naive implementation is not compatible with prefix caching so we didn't pick this design. In vLLM, we allocate different blocks for different tokens and free blocks that are outside the sliding window.

For a new request, the cache hit prefix only requires the last sliding_window_size - 1 tokens being cached. Let's say sliding_window_size = 4 and block_size = 1, and the request is a 15-token prompt (blue blocks are cached):

Prefix Caching of Sliding Window Attention

There are 3 possible cache hit prefixes:

    cache hit length 5, compute prefill with [2, 3, 4] → [5, 6, …, 14]
    cache hit length 6, compute prefill with [3, 4, 5] → [6, 7, …, 14]
    cache hit length 14, compute prefill with [11, 12, 13] → [14] (most efficient)

We can check the cache hit from right to left, and early exit when we find a match.This is opposite from full attention, where we check from left to right and early exit when the match fails. One potential cons (compared to full attention) is that we end up iterating over the entire list of tokens when there's no match, which is often a common case. This could potentially cause non-negligible overheads, but fine with full + swa, as discussed below.
Case 2: sliding window attention + full attention models¶

The first problem is how to find the cache hit prefix. We need to "intersect" the cache hits of global and sliding window attention layers by:

    Get the longest cache hit for full attention (scanning from left to right)
    Get the longest cache hit for sliding window attention that is within that length. Implemented by checking cache hits from right to left starting from the cache hit length of full attention.

It can be ensured that the resulting cache hit of sliding window attention layers is also a cache hit of full attention layers. This is more efficient than finding all possible prefixes of each group and doing the intersection, because our approach can exit early if there is no cache hit.

The algorithm applies to models with exactly two attention types full attention + X, where X can be an arbitrary efficient attention algorithm like sliding window, llama 4 local attention, and mamba. It doesn't support models without full attention layers, and models with more than 2 types of attention. This is enough for most hybrid models at the moment of writing this doc.

The second question is the cache eviction policy. For now, we use one LRU queue for all kv cache groups. The blocks are added to the LRU queue when freed, either because the request is finished or the block is out of the sliding window.
Case 3: mamba models¶

The prefix caching support of the mamba model is work in progress. Once implemented, models with mamba layer + full attention layer can be supported via the full attention + X algorithm in case 2.
Implementation¶
Overview¶

Overview of Hybrid KV Cache Manager

The KVCacheManager is organized into 3 layers:

    KVCacheManager: The interface between the scheduler and kv cache management system.
    KVCacheCoordinator: coordinate per-group SingleTypeKVCacheManagers to generate the allocation result of a request. Depending on the model's configuration, one of these coordinators is chosen:
        KVCacheCoordinatorNoPrefixCache: Used when prefix caching is disabled.
        UnitaryKVCacheCoordinator: If only one KV cache group. The prefix caching logic is simplified as no intersection is needed.
        HybridKVCacheCoordinator: Handles exactly two KV cache groups (must include one full‑attention group plus one other efficient‑attention group). Other cases are not implemented. You can disable prefix caching to use the KVCacheCoordinatorNoPrefixCache.
    SingleTypeKVCacheManager: Each instance manages allocation and prefix caching for one KV cache group, implementing the attention‑type–specific logic (e.g., full attention, sliding window, Mamba).

The blue box in the above figure shows the case with 10 full attention layers and 20 sliding window attention layers, thus:

    use HybridKVCacheCoordinator
    use 1 FullAttentionManager and 2 SlidingWindowManager for the 3 KVCacheGroups.

Memory Layout¶

For a model with n KVCacheGroups, each with m layers, we allocate m buffers. Each buffer is shared by n layers, one from each group.

The following figure is for a model with 10 full attention layers (full.0 - full.9) and 20 sliding window attention layers (sw.0-sw.19). It follows "case 2" in "Allocation" section and is divided into 3 groups:

    Group 0: 10 full attention layers (full.0 - full.9)
    Group 1: 10 sliding window attention layers (sw.0 - sw.9)
    Group 2: 10 sliding window attention layers (sw.10 - sw.19)

And for a request, we allocate 11 blocks with block_id 0-6 to group 0, 7-8 to group 1, and 9-10 to group 2.

With such an example, the physical memory is divided into 10 buffers (KVCacheTensor 0 - KVCacheTensor 9). Each buffer is shared by 3 layers (e.g., KVCacheTensor 0 is shared by full.0 from group 0, sw.0 from group 1, and sw.10 from group 2) and is divided into pieces with size block_size * kv_hidden_size. The KV cache of these 3 attention layers are saved to different pieces of the buffer based on the allocated block_ids:

Example Memory Layout

Note

One logic "block" is mapped to 10 pieces in the 10 buffers of the physical memory.

Optimization Levels¶
Overview¶

vLLM now supports optimization levels (-O0, -O1, -O2, -O3). Optimization levels provide an intuitive mechanism for users to trade startup time for performance. Higher levels have better performance but worse startup time. These optimization levels have associated defaults to help users get desired out-of-the-box performance. Importantly, defaults set by optimization levels are purely defaults; explicit user settings will not be overwritten.
Level Summaries and Usage Examples¶

# CLI usage
python
 -m vllm.entrypoints.api_server --model RedHatAI/Llama-3.2-1B-FP8 -O0

# Python API usage
from
 vllm.entrypoints.llm import LLM

llm = LLM(
    model="RedHatAI/Llama-3.2-1B-FP8",
    optimization_level=0
)

-O1: Quick Optimizations¶

    Startup: Moderate startup time
    Performance: Inductor compilation, CUDAGraphMode.PIECEWISE
    Use case: Balance for most development scenarios

# CLI usage
python
 -m vllm.entrypoints.api_server --model RedHatAI/Llama-3.2-1B-FP8 -O1

# Python API usage
from
 vllm.entrypoints.llm import LLM

llm = LLM(
    model="RedHatAI/Llama-3.2-1B-FP8",
    optimization_level=1
)

-O2: Full Optimizations (Default)¶

    Startup: Longer startup time
    Performance: -O1 + CUDAGraphMode.FULL_AND_PIECEWISE
    Use case: Production workloads where performance is important. This is the default use case. It is also very similar to the previous default. The primary difference is that noop & fusion flags are enabled.

# CLI usage (default, so optional)
python
 -m vllm.entrypoints.api_server --model RedHatAI/Llama-3.2-1B-FP8 -O2

# Python API usage
from
 vllm.entrypoints.llm import LLM

llm = LLM(
    model="RedHatAI/Llama-3.2-1B-FP8",
    optimization_level=2  # This is the default
)

-O3: Full Optimization¶

Still in development. Added infrastructure to prevent changing API in future release. Currently behaves the same O2.
Troubleshooting¶
Common Issues¶

    Startup Time Too Long: Use -O0 or -O1 for faster startup
    Compilation Errors: Use debug_dump_path for additional debugging information
    Performance Issues: Ensure using -O2 for production

Attention Backend Feature Support¶

This document is auto-generated by tools/pre_commit/generate_attention_backend_docs.py. It shows the feature support for each registered attention backend based on the checks in AttentionBackend.validate_configuration().

Do not edit this file manually. Run the following command to regenerate it:

python
 tools/pre_commit/generate_attention_backend_docs.py

Setting the Attention Backend¶
Command Line¶

There are two ways to specify the backend from the command line:

Option 1: Using --attention-backend (simple)

vllm
 serve <model> --attention-backend FLASH_ATTN

Option 2: Using --attention-config.backend / -ac.backend (structured config)

# Dot notation
vllm
 serve <model> --attention-config.backend FLASH_ATTN
vllm
 serve <model> -ac.backend FLASH_ATTN

# JSON format
vllm
 serve <model> --attention-config '{"backend": "FLASH_ATTN"}'
vllm
 serve <model> -ac '{"backend": "FLASH_ATTN"}'

    Note: --attention-backend and --attention-config.backend are mutually exclusive. Use one or the other, not both.

Python API¶

Use AttentionConfig with the LLM class:

from vllm import LLM
from vllm.config import AttentionConfig
from vllm.v1.attention.backends.registry import AttentionBackendEnum

# Method 1: Using AttentionConfig with enum
llm = LLM(
    
model="Qwen/Qwen3-0.6B",
    
attention_config=AttentionConfig(backend=AttentionBackendEnum.FLASH_ATTN),
)

# Method 2: Using attention_backend parameter with string
llm = LLM(
    
model="Qwen/Qwen3-0.6B",
    
attention_backend="FLASH_ATTN",
)

Backend Selection Behavior¶
Manual Selection¶

When you explicitly set a backend via --attention-backend or AttentionConfig:

    The backend is validated against your configuration (model dtype, head size, compute capability, etc.)
    If the backend doesn't support your configuration, an error is raised with the specific reason
    If valid, the backend is used

Example error when selecting an incompatible backend:

ValueError: Selected backend FLASHMLA is not valid for this configuration.
Reason: ['compute capability not supported']

Automatic Selection¶

When no backend is specified (the default):

    vLLM iterates through backends in priority order (see tables below)
    Each backend is validated against your configuration
    The first compatible backend is selected
    If no backend is compatible, an error is raised listing all backends and their incompatibility reasons

Backend Priority (CUDA)¶

When no backend is explicitly selected, vLLM chooses the first compatible backend from these priority-ordered lists.

Priority is 1 = highest (tried first).
Standard Attention (MHA, MQA, GQA)¶

Blackwell (SM 10.x):
Priority 	Backend
1 	FLASHINFER
2 	FLASH_ATTN
3 	TRITON_ATTN
4 	FLEX_ATTENTION

Ampere/Hopper (SM 8.x-9.x):
Priority 	Backend
1 	FLASH_ATTN
2 	FLASHINFER
3 	TRITON_ATTN
4 	FLEX_ATTENTION
MLA Attention (DeepSeek-style)¶

Blackwell (SM 10.x):
Priority 	Backend
1 	FLASHINFER_MLA
2 	CUTLASS_MLA
3 	FLASH_ATTN_MLA
4 	FLASHMLA
5 	TRITON_MLA
6 	FLASHMLA_SPARSE
7 	FLASHINFER_MLA_SPARSE

Ampere/Hopper (SM 8.x-9.x):
Priority 	Backend
1 	FLASH_ATTN_MLA
2 	FLASHMLA
3 	FLASHINFER_MLA
4 	TRITON_MLA
5 	FLASHMLA_SPARSE

    Note: ROCm and CPU platforms have their own selection logic. See the platform-specific documentation for details.

Legend¶
Column 	Description
Dtypes 	Supported model data types (fp16, bf16, fp32)
KV Dtypes 	Supported KV cache data types (auto, fp8, fp8_e4m3, etc.)
Block Sizes 	Supported KV cache block sizes (%N means multiples of N)
Head Sizes 	Supported attention head sizes
Sink 	Attention sink support (for StreamingLLM)
Sparse 	Sparse attention support (MLA only)
MM Prefix 	Multimodal prefix full attention support
DCP 	Decode Context Parallelism support (--decode-context-parallel-size)
Attention Types 	Supported attention patterns (Decoder, Encoder, Enc-Dec)
Compute Cap. 	Required CUDA compute capability (N/A for non-CUDA backends)

Symbols: ✅ = Supported, ❌ = Not supported
Standard Attention (MHA, MQA, GQA) Backends¶
Backend 	Version 	Dtypes 	KV Dtypes 	Block Sizes 	Head Sizes 	Sink 	MM Prefix 	DCP 	Attention Types 	Compute Cap.
CPU_ATTN 		fp16, bf16, fp32 	auto 	Any 	32, 64, 80, 96, 112, 128, 160, 192, 224, 256 	❌ 	❌ 	❌ 	All 	N/A
FLASHINFER 	Native† 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	16, 32, 64 	64, 128, 256 	❌ 	❌ 	✅ 	Decoder 	7.x-9.x
FLASHINFER 	TRTLLM† 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	16, 32, 64 	64, 128, 256 	✅ 	❌ 	✅ 	Decoder 	10.x
FLASH_ATTN 	FA2* 	fp16, bf16 	auto, bfloat16 	%16 	Any 	❌ 	❌ 	✅ 	All 	≥8.0
FLASH_ATTN 	FA3* 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	%16 	Any 	✅ 	❌ 	✅ 	All 	9.x
FLASH_ATTN_DIFFKV 		fp16, bf16 	auto 	Any 	Any 	❌ 	❌ 	✅ 	Decoder 	Any
FLEX_ATTENTION 		fp16, bf16, fp32 	auto, bfloat16 	Any 	Any 	❌ 	✅ 	❌ 	Decoder, Encoder Only 	Any
ROCM_AITER_FA 		fp16, bf16 	auto 	16, 32 	64, 128, 256 	❌ 	❌ 	❌ 	Decoder 	N/A
ROCM_AITER_UNIFIED_ATTN 		fp16, bf16 	auto 	Any 	Any 	❌ 	❌ 	❌ 	All 	N/A
ROCM_ATTN 		fp16, bf16, fp32 	auto 	16, 32, 544 	32, 64, 96, 128, 160, 192, 224, 256 	❌ 	❌ 	❌ 	All 	N/A
TREE_ATTN 		fp16, bf16 	auto 	%16 	32, 64, 96, 128, 160, 192, 224, 256 	❌ 	❌ 	❌ 	Decoder 	Any
TRITON_ATTN 		fp16, bf16, fp32 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	%16 	Any 	✅ 	✅ 	❌ 	All 	Any

    † FlashInfer uses TRTLLM attention on Blackwell (SM100), which supports sinks. Disable via --attention-config.use_trtllm_attention=0.

    * Specify the FlashAttention version via --attention-config.flash_attn_version=2 or 3. Default is FA3 on SM90, FA2 otherwise.

MLA (Multi-head Latent Attention) Backends¶

MLA uses separate backends for prefill and decode phases.
Prefill Backends¶

The prefill backend is selected at runtime based on hardware and configuration.
Backend 	Description 	Compute Cap. 	Enable 	Disable 	Notes
TRT-LLM Ragged‡ 	TensorRT-LLM ragged attention 	10.x 	Default on SM100 	-ac.use_trtllm_ragged_deepseek_prefill=0 	DeepSeek R1 dims only
FlashInfer 	FlashInfer CUTLASS backend 	10.x 	-ac.disable_flashinfer_prefill=0 	-ac.disable_flashinfer_prefill=1 	DeepSeek R1 dims only
cuDNN 	cuDNN-based attention 	10.x 	-ac.use_cudnn_prefill=1 	-ac.use_cudnn_prefill=0 	
FlashAttention 	FlashAttention varlen (FA2/FA3) 	Any 	Default fallback 	Use other backends 	FA3 on SM90, FA2 otherwise

    ‡ TRT-LLM Ragged is the default on Blackwell (SM100). On other GPUs, FlashAttention is used as the default.

Decode Backends¶
Backend 	Dtypes 	KV Dtypes 	Block Sizes 	Head Sizes 	Sink 	Sparse 	MM Prefix 	DCP 	Attention Types 	Compute Cap.
CUTLASS_MLA 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3 	128 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	10.x
FLASHINFER_MLA 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3 	32, 64 	Any 	❌ 	❌ 	❌ 	❌ 	Decoder 	10.x
FLASHINFER_MLA_SPARSE 	fp16, bf16 	auto, bfloat16 	32, 64 	576 	❌ 	✅ 	❌ 	❌ 	Decoder 	10.x
FLASHMLA 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3 	64 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	9.x-10.x
FLASHMLA_SPARSE 	bf16 	auto, bfloat16, fp8_ds_mla 	64 	576 	❌ 	✅ 	❌ 	❌ 	Decoder 	9.x-10.x
FLASH_ATTN_MLA 	fp16, bf16 	auto, bfloat16 	%16 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	9.x
ROCM_AITER_MLA 	fp16, bf16 	auto 	1 	Any 	❌ 	❌ 	❌ 	❌ 	Decoder 	N/A
ROCM_AITER_MLA_SPARSE 	fp16, bf16 	auto 	Any 	576 	❌ 	❌ 	❌ 	❌ 	Decoder 	N/A
ROCM_AITER_TRITON_MLA 	fp16, bf16 	auto 	Any 	Any 	❌ 	❌ 	❌ 	❌ 	Decoder 	N/A
TRITON_MLA 	fp16, bf16 	auto, bfloat16 	Any 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	Any

CUDA Graphs¶

This write-up introduces the new CUDA Graphs modes in vLLM v1 beyond previous torch.compile integration. To summarize, we:

    Added flexible cudagraph_mode configuration
    Made full CUDA Graphs support orthogonal to compilation
    Introduced a CUDA Graphs dispatcher as a central controller that picks the desired runtime mode and CUDA Graphs per batch automatically

In this document we will discuss the:

    Motivation
    CUDA Graphs modes
    Detailed design
    Example usage of the different CUDA Graphs modes

Note

In this document, we refer to pure decode (max_query_len=1) or speculative decode (max_query_len =1+num_spec_tokens) as uniform decode batches, and the opposite would be non-uniform batches (i.e., prefill or mixed prefill-decode batches).

Note

The following contents are mostly based on the last commit of
Pull Request #20059.
Motivation¶

Initial piecewise compilation was built to allow piecewise cudagraph capture, excluding cudagraph-unsupported operations (mainly attention). This allowed some speedup from cudagraphs while maintaining compatibility with all attention backends. We later added support for "full cudagraphs" by not compiling piecewise, so that we could further reduce the latency in cases where attention supported cudagraphs. However, this tight coupling between compilation and cudagraph capture led to an all-or-nothing experience with little flexibility. Many attention backends also weren’t ready for unified "full" CUDA Graphs capture (e.g., only FlashAttention 3 supports it currently) or only support CUDA Graphs for pure decode batches (e.g., Flashinfer, FlashMLA, and Mamba, etc.). That led to confusing performance/compatibility tradeoffs, inconsistent CUDA Graphs support, and increasingly complex code structure.

This led us to seek a more fine-grained CUDA Graphs solution with the following features:

    Explicitly aware of CUDA Graphs for prefill/mixed or (uniform-)decode batch and capture them separately.
    Separate CUDAGraph capture logic from compilation (as much as feasible) for feature orthogonality, which suggest:
        Capturing piecewise and full cudagraphs using the same compiled graph, and
        Full cudagraph capture without compilation.
    Dispatch between full and piecewise cudagraph at runtime depending on batch composition.
    Centralized control of CUDAGraph behavior for reduced code complexity and allowed more extendibility.

These features allow the most flexibility for cudagraph capture and compilation for all kinds of startup/performance tradeoffs and feature support.
CudagraphModes¶

CUDAGraphMode is the single knob you tune in CompilationConfig.cudagraph_mode:

    NONE — turn CUDA Graphs off. Good for debugging.
    PIECEWISE — a single-mode strategy (and past default). It is the most flexible: attention or other CUDA Graphs-incompatible operations stay eager, everything else goes into CUDA Graphs. Requires piecewise compilation.
    FULL — a single-mode strategy, which only captures full CUDA Graphs for non-uniform batches, then uniform-decode batches reuse the CUDA Graph of non-uniform batch of the same batch_size, since they are compatible; can be good for small models or workloads with small prompts.
    FULL_DECODE_ONLY — full CUDA Graph for uniform decode, no cudagraph for prefill/mixed etc.; suitable for decode instances in a P/D setup where prefill is not as important, this way we can save the memory needed for PIECEWISE CUDA Graphs.
    FULL_AND_PIECEWISE — (default mode) full CUDA Graph for uniform decode, piecewise CUDA Graphs for others; generally the most performant setting, especially for low latency with small models or MoEs, but also requires the most memory and takes the longest to capture.

Defaults: If you’re on v1 with piecewise compilation, we default to FULL_AND_PIECEWISE for better performance, (for pooling models, it's still PIECEWISE). Otherwise, e.g. if piecewise compilation unavailable, we default to NONE.

While NONE , PIECEWISE, and FULL are single-mode configurations and simply equivalent to past implementations of eager execution, piecewise CUDA Graphs, and full CUDA Graphs respectively, FULL_DECODE_ONLY and FULL_AND_PIECEWISE are newly appended dual-mode configurations, which require dispatching to switch between concrete runtime modes according to runtime batches dynamically.

Note

Here, the single-modes NONE, PIECEWISE, and FULL are treated as the runtime modes for CUDA Graphs dispatching. If using a dual-mode, the dispatcher will always dispatch to one of its member modes (plus a potential NONE if no suitable CUDA Graph available), depending on the batch composition.

While cascade attention is not cudagraph compatible, it is now compatible with all possible cudagraph mode configurations. If a batch uses cascade attention, it always gets dispatched to PIECEWISE mode if available (otherwise NONE).

Note

Not all CUDA Graph modes are compatible with every attention backend. We automatically "downgrade" modes to the closest supported mode. For example, if a backend only supports CUDA Graphs for pure decode/uniform batches, we convert FULL to FULL_AND_PIECEWISE if piecewise compilation is enabled, and FULL_DECODE_ONLY otherwise.
Detailed Design¶
Overview¶

The new CUDA Graphs logic is built on top of piecewise compilation and supports dual CUDA Graphs runtime mode switching. The system contains the following core components:

    CUDAGraphWrapper: wrapper that handles CUDAGraph capture & replay on the wrapped callable
    CudagraphDispatcher: the central controller that contains the single source of truth about CUDA Graphs and handles dispatching between them.
    CUDAGraphMode: enum describing the supported and runtime modes (introduced above).
    BatchDescriptor, serving as a unique representation of the runtime batch used for dispatching.

See the following figures for a quick comparison between the previous and current design patterns of CUDA Graphs with inductor compilation. We can see that previously the CUDA Graphs logic and compilation logic were tightly coupled into the vllm PiecewiseBackend, and CUDA Graphs was implicitly dispatched by batch_size idly. Now the CUDA Graphs logic is separated into the CUDAGraphWrapper class, responsible for both full and piecewise CUDA Graphs abilities, and dispatching is explicitly done via runtime mode plus the BatchDescriptor as the dispatch key via CudagraphDispatcher.

Before:

previous_design

After:

new_design
BatchDescriptor¶

BatchDescriptor is a component within ForwardContext, alongside the CUDA Graphs runtime modes, serving as the core structure for dispatching keys at runtime. The prototype is:

class BatchDescriptor(NamedTuple):
    
num_tokens: int
    
num_reqs: int
    
uniform: bool = False
    
has_lora: bool = False

where num_tokens can be the padded token length, and uniform indicates if all the requests have the same query lengths. Many attention backends only support full cudagraphs when the batches are uniform; pure decode batches are uniform but may not be query length 1 (i.e. num_tokens == num_reqs), this occurs in the validation pass of spec-decode where "decode" batches will have a query length of 1+num_spec_tokens.

The goal of this structure is to uniquely identify a (padded) batch with minimal possible items corresponding to a CUDA Graphs item.

Note

The prototype of BatchDescriptor may be extended for more general situations in the future, e.g., include more items, like uniform_query_len to support multiple different uniform decode lengths settings (
Pull Request #23679), or other modifications needed to support CUDA Graphs for models whose inputs are not necessarily token length aware (for example, some multi-modal inputs).
CudagraphDispatcher¶

The CudagraphDispatcher takes responsibility for maintaining two sets of valid dispatching keys, one set for FULL runtime mode and one set for PIECEWISE runtime mode, and dispatches the correct runtime mode and the dispatching keys before executing the model's forwards. It will take in the initial key (a rough batch_descriptor for the padded input) and return the selected runtime mode and the final batch_descriptor, then tell the CUDAGraphWarpper instances that decision through forward contexts. Notice that CudagraphDispatcher is the only source of truth for available CUDA Graph keys and CUDAGraphWrapper instances can blindly trust the forward context on what CUDA Graphs to dispatch to. This lets us simplify the wrapper code and centralize the logic in the dispatcher.

The dispatching keys are initialized through the dispatcher's initialize_cudagraph_keys method, which is called by the gpu_model_runner after all possible attention backends are initialized. This is where we can get much fancier in the future and “prepare” all kinds of CUDA Graphs combinations. For now, we just append available keys based on the valid combos of decode_mode/mixed_mode of cudagraph_mode and cudagraph_capture_sizes in the compilation config.

The dispatch code looks like:

batch_descriptor=BatchDescriptor(num_tokens=num_input_tokens, uniform_decode=...)
runtime_mode, batch_descriptor = cudagraphdispatcher.dispatch(batch_descriptor)
# execution
with set_forward_context(
    
..., 
    
cudagraph_runtime_mode=runtime_mode, 
    
batch_descriptor=batch_descriptor,
):
     
output = self.model(...)

Inside the dispatch() method, the dispatcher will search the proper CUDA Graphs runtime mode and existing dispatching keys for a return. We basically search the existing keys following the priority: FULL>PIECEWISE>None. If the dispatching key does not exist, default to return NONE mode for eager execution. The implementations can be found here.

Here is a simplified illustration of the workflow at runtime in the model executor: executor_runtime
CUDAGraphWrapper¶

A CUDAGraphWrapper instance wraps a runnable and simply mimics the runnable with appended CUDA Graphs abilities. Each wrapper instance is bound to a specific runtime_mode, which is restricted to PIECEWISE and FULL mode, and takes responsibility for capturing/replaying and passing through (directly calling) the runnable. At runtime, each wrapper would:

    inspect the runtime_mode and batch_descriptor(dispatching key) from the global forward context.
    If runtime_mode is NONE or runtime_mode does not match the mode of the wrapper, just call the runnable directly.
    Otherwise, i.e., the runtime_mode matches the mode of the wrapper, the wrapper will perform CUDA Graphs capture (if key does not exist, create a new entry and cache it) or replay (if key exists in the cache).

The above steps are based on the assumption that the CUDA Graphs wrapper would directly trust what’s in the forward context (controlled by the dispatcher). This lets us simplify and centralize the logic, reducing the complexity as well as the risk of mismatched state between the wrappers and the dispatcher. It also allows reusing the wrapper class for both FULL and PIECEWISE runtime modes. See the implementation here.
Nested Wrapper design¶

The core mechanism of making a full CUDA Graphs and piecewise CUDA Graphs coexist and compatible is the nested CUDA Graphs wrapper design, building on top of piecewise compilation with only a single piecewise FX graph. We wrap a FULL mode wrapper outside the entire model for the full CUDA Graphs functionality; meanwhile, each piecewise backend is wrapped via a PIECEWISE mode wrapper inside the compilation.

The flow chart below should clearly describe how it works. wrapper_flow

Therefore, for a FULL runtime mode, it is safe to capture/replay a full CUDA Graph since the piecewise wrapper is not activated. The situation is similar for PIECEWISE mode, as there are no conflicts between the FULL mode wrapper and PIECEWISE mode wrappers. For the NONE runtime mode, both FULL and PIECEWISE wrappers would not be activated, so we simply fall through to eager execution.
Full CUDA Graph capturing & warm-up¶

The CUDA Graphs capturing happens when the runner first calls the model forward (using _dummy_run) with a non-NONE runtime mode. For full CUDA Graph capture, we explicitly capture different cases (i.e., prefill/mixed batch or uniform_decode batch) by properly setting attention metadata to make sure the underlying attention backends launch the desired kernel routines. To distinguish prefill/mixed batch or uniform_decode batch, the most important property is the max_query_len in attn_metadata (true for most attention backends). We set it to the desired uniform_query_len for uniform_decode otherwise we make it just the num_tokens for a non-uniform_decode batch.

The CUDA Graphs wrapper no longer manages the warm-up logic. The warm-up process is now controlled directly by the GPU model runner, where the NONE runtime mode is assigned to play an eager execution for warm-up. When warming up for a full CUDA Graph, it is also important to explicitly run attention during the warmup dummy_run call.
CUDA Graphs Compatibility of Attention Backends¶

To signal the CUDA Graphs compatibility of the attention backends, we introduce a new enum type AttentionCGSupport, which is an enum type that tracks the capability of the attention backend to support CUDA Graphs. The value is sorted in the order of the capability, i.e., ALWAYS> UNIFORM_BATCH> UNIFORM_SINGLE_TOKEN_DECODE> NEVER.

class AttentionCGSupport(enum.Enum):
    """ Constants for the CUDA Graphs support of the attention backend
    Here we do not consider the cascade attention, as currently
    it is never CUDA Graphs supported."""

    
ALWAYS = 3
    """CUDA Graphs always supported; supports mixed-prefill-decode"""
    
UNIFORM_BATCH = 2
    """CUDA Graphs supported for batches the only contain query lengths that are
    the same, this can be used for spec-decode 
        i.e. "decodes" are 1 + num_speculative_tokens"""
    
UNIFORM_SINGLE_TOKEN_DECODE = 1
    """CUDA Graphs supported for batches the only contain query_len==1 decodes"""
    
NEVER = 0
    """NO CUDA Graphs support"""

Suppose we have hybrid attention backends (e.g., in mamba mixer models). In that case, we seek the minimum capability of all backends to determine the final capability of the model, and we might resolve the incompatible CUDA Graphs mode by downgrading the mode to the best fit one. For example, downgrading FULL mode to FULL_AND_PIECEWISE mode if the minimum capability is UNIFORM_BATCH, or PIECEWISE mode if the minimum capability is NEVER for -O3 compilation mode. For the complete fallback policy, please see the code for this.

The following table lists backends that support full CUDA Graphs at the time of writing.
Attention Backend 	cudagraph_support 	Comments
FlashAttention v2 	UNIFORM_BATCH 	Actually ALWAYS but workaround to fallback to FULL_AND_PIECEWISE for performance reason
FlashAttention v3 	ALWAYS 	has unified routine for both batches, so FULL mode is good
Triton Attention 	ALWAYS 	prefer FULL_AND_PIECEWISE since it has different kernels for prefill/mixed and pure decode batches
AITER FlashAttention 	UNIFORM_BATCH 	
FlashInfer 	UNIFORM_SINGLE_TOKEN_DECODE 	Will be set to UNIFORM_BATCH when using TRTLLM attention on Blackwell
FlashMLA 	UNIFORM_BATCH 	
FlashInferMLA 	UNIFORM_BATCH 	
FlashInferMLASparse 	UNIFORM_BATCH 	
AITER MLA 	UNIFORM_SINGLE_TOKEN_DECODE 	
CUTLASS MLA 	UNIFORM_SINGLE_TOKEN_DECODE 	
Mamba attention 	UNIFORM_SINGLE_TOKEN_DECODE 	

Unlisted backends are all declared as NEVER.
Usage guide¶

Now the CLI is directly using the uppercase string of cudagraph_mode for compilation_config: --compilation-config '{"cudagraph_mode": "..."}', where ... should be one of NONE, PIECEWISE, FULL, FULL_DECODE_ONLY, and FULL_AND_PIECEWISE. Note that all PIECEWISE related modes require piecewise compilation, and all FULL related modes need CUDA Graphs support of attention backends. For example:

vllm
 serve --model meta-llama/Llama-3.1-8B-Instruct --compilation-config '{"cudagraph_mode": "FULL_AND_PIECEWISE"}'

Python examples¶

import os
os.environ.setdefault("VLLM_LOGGING_LEVEL", "DEBUG")

import vllm
from vllm.config import CUDAGraphMode

compilation_config = {"mode": 3, "cudagraph_mode": "FULL_AND_PIECEWISE"}
model = vllm.LLM(
    
model="meta-llama/Llama-3.1-8B-Instruct",
    
dtype="auto",
    
compilation_config=compilation_config,
)
sampling_params = vllm.SamplingParams(
    
temperature=0,  # greedy decoding
    
max_tokens=1024,
)
outputs = model.generate(
    
["My name is John and"],
    
sampling_params=sampling_params,
)

Piecewise compilation and full graph custom passes (attention fusion, sequence parallelism)¶

Unfortunately, some custom compile passes have to see the whole graph to be effective and hence aren't compatible with piecewise compilation. This includes AttnFusionPass and SequenceParallelismPass. As a short-term solution, we automatically disable piecewise compilation (by setting splitting_ops=[]) when attention fusion is enabled. We use CUDA Graph modes FULL or FULL_DECODE_ONLY (depending on backend support). However, this leads to another optimization incompatibility and confusing performance tradeoffs.

Long term, we've added the ability to partition the graph in Inductor instead of right after Dynamo. It can be enabled with CompilationConfig.use_inductor_graph_partition=True but is currently experimental and only available with torch>=2.9. This also increases compilation time as it has to compile the whole graph and cannot reuse piecewise compilation artifacts. Once vLLM supports 2.9, we plan to make this the default approach as it will also speed up piecewise cudagraph capture.
About the Performance¶

See the following links for examples:

    20059#issuecomment-3160858458
    20059#issuecomment-3188735226
    20059#issuecomment-3219888738

Python Multiprocessing¶
Debugging¶

Please see the Troubleshooting page for information on known issues and how to solve them.
Introduction¶

Important

The source code references are to the state of the code at the time of writing in December 2024.

The use of Python multiprocessing in vLLM is complicated by:

    The use of vLLM as a library and the inability to control the code using vLLM
    Varying levels of incompatibilities between multiprocessing methods and vLLM dependencies

This document describes how vLLM deals with these challenges.
Multiprocessing Methods¶

Python multiprocessing methods include:

    spawn - spawn a new Python process. The default on Windows and macOS.

    fork - Use os.fork() to fork the Python interpreter. The default on Linux for Python versions prior to 3.14.

    forkserver - Spawn a server process that will fork a new process on request. The default on Linux for Python version 3.14 and newer.

Tradeoffs¶

fork is the fastest method, but is incompatible with dependencies that use threads. If you are under macOS, using fork may cause the process to crash.

spawn is more compatible with dependencies, but can be problematic when vLLM is used as a library. If the consuming code does not use a __main__ guard (if __name__ == "__main__":), the code will be inadvertently re-executed when vLLM spawns a new process. This can lead to infinite recursion, among other problems.

forkserver will spawn a new server process that will fork new processes on demand. This unfortunately has the same problem as spawn when vLLM is used as a library. The server process is created as a spawned new process, which will re-execute code not protected by a __main__ guard.

For both spawn and forkserver, the process must not depend on inheriting any global state as would be the case with fork.
Compatibility with Dependencies¶

Multiple vLLM dependencies indicate either a preference or requirement for using spawn:

    https://pytorch.org/docs/stable/notes/multiprocessing.html#cuda-in-multiprocessing
    https://pytorch.org/docs/stable/multiprocessing.html#sharing-cuda-tensors
    https://docs.habana.ai/en/latest/PyTorch/Getting_Started_with_PyTorch_and_Gaudi/Getting_Started_with_PyTorch.html?highlight=multiprocessing#torch-multiprocessing-for-dataloaders

It is perhaps more accurate to say that there are known problems with using fork after initializing these dependencies.
Current State (v0)¶

The environment variable VLLM_WORKER_MULTIPROC_METHOD can be used to control which method is used by vLLM. The current default is fork.

    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/envs.py#L339-L342

When we know we own the process because the vllm command was used, we use spawn because it's the most widely compatible.

    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/scripts.py#L123-L140

The multiproc_xpu_executor forces the use of spawn.

    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/executor/multiproc_xpu_executor.py#L14-L18

There are other miscellaneous places hard-coding the use of spawn:

    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/distributed/device_communicators/all_reduce_utils.py#L135
    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/entrypoints/openai/api_server.py#L184

Related PRs:

    Pull Request #8823

Prior State in v1¶

There was an environment variable to control whether multiprocessing is used in the v1 engine core, VLLM_ENABLE_V1_MULTIPROCESSING. This defaulted to off.

    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/envs.py#L452-L454

When it was enabled, the v1 LLMEngine would create a new process to run the engine core.

    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/v1/engine/llm_engine.py#L93-L95
    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/v1/engine/llm_engine.py#L70-L77
    https://github.com/vllm-project/vllm/blob/d05f88679bedd73939251a17c3d785a354b2946c/vllm/v1/engine/core_client.py#L44-L45

It was off by default for all the reasons mentioned above - compatibility with dependencies and code using vLLM as a library.
Changes Made in v1¶

There is not an easy solution with Python's multiprocessing that will work everywhere. As a first step, we can get v1 into a state where it does "best effort" choice of multiprocessing method to maximize compatibility.

    Default to fork.
    Use spawn when we know we control the main process (vllm was executed).
    If we detect cuda was previously initialized, force spawn and emit a warning. We know fork will break, so this is the best we can do.

The case that is known to still break in this scenario is code using vLLM as a library that initializes cuda before calling vLLM. The warning we emit should instruct users to either add a __main__ guard or to disable multiprocessing.

If that known-failure case occurs, the user will see two messages that explain what is happening. First, a log message from vLLM:

WARNING 12-11 14:50:37 multiproc_worker_utils.py:281] CUDA was previously
    initialized. We must use the `spawn` multiprocessing start method. Setting
    VLLM_WORKER_MULTIPROC_METHOD to 'spawn'. See
    https://docs.vllm.ai/en/latest/usage/troubleshooting.html#python-multiprocessing
    for more information.

Second, Python itself will raise an exception with a nice explanation:

RuntimeError:
        An attempt has been made to start a new process before the
        current process has finished its bootstrapping phase.

        This probably means that you are not using fork to start your
        child processes and you have forgotten to use the proper idiom
        in the main module:

            if __name__ == '__main__':
                freeze_support()
                ...

        The "freeze_support()" line can be omitted if the program
        is not going to be frozen to produce an executable.

        To fix this issue, refer to the "Safe importing of main module"
        section in https://docs.python.org/3/library/multiprocessing.html

Alternatives Considered¶
Detect if a __main__ guard is present¶

It has been suggested that we could behave better if we could detect whether code using vLLM as a library has a __main__ guard in place. This post on stackoverflow was from a library author facing the same question.

It is possible to detect whether we are in the original, __main__ process, or a subsequent spawned process. However, it does not appear to be straight forward to detect whether a __main__ guard is present in the code.

This option has been discarded as impractical.
Use forkserver¶

At first it appears that forkserver is a nice solution to the problem. However, the way it works presents the same challenges that spawn does when vLLM is used as a library.
Force spawn all the time¶

One way to clean this up is to just force the use of spawn all the time and document that the use of a __main__ guard is required when using vLLM as a library. This would unfortunately break existing code and make vLLM harder to use, violating the desire to make the LLM class as easy as possible to use.

Instead of pushing this on our users, we will retain the complexity to do our best to make things work.
Future Work¶

We may want to consider a different worker management approach in the future that works around these challenges.

    We could implement something forkserver-like, but have the process manager be something we initially launch by running our own subprocess and a custom entrypoint for worker management (launch a vllm-manager process).

    We can explore other libraries that may better suit our needs. Examples to consider:

    https://github.com/joblib/loky

IO Processor Plugins¶

IO Processor plugins are a feature that allows pre- and post-processing of the model input and output for pooling models. The idea is that users are allowed to pass a custom input to vLLM that is converted into one or more model prompts and fed to the model encode method. One potential use-case of such plugins is that of using vLLM for generating multi-modal data. Say users feed an image to vLLM and get an image in output.

When performing an inference with IO Processor plugins, the prompt type is defined by the plugin and the same is valid for the final request output. vLLM does not perform any validation of input/output data, and it is up to the plugin to ensure the correct data is being fed to the model and returned to the user. As of now these plugins support only pooling models and can be triggered via the encode method in LLM and AsyncLLM, or in online serving mode via the /pooling endpoint.
Writing an IO Processor Plugin¶

IO Processor plugins implement the IOProcessor interface:

IOProcessorInput = TypeVar("IOProcessorInput")
IOProcessorOutput = TypeVar("IOProcessorOutput")

class IOProcessor(ABC, Generic[IOProcessorInput, IOProcessorOutput]):
    
def __init__(self, vllm_config: VllmConfig):
        
super().__init__()

        
self.vllm_config = vllm_config

    
@abstractmethod
    
def parse_data(self, data: object) -> IOProcessorInput:
        
raise NotImplementedError

    
def merge_sampling_params(
        
self,
        
params: SamplingParams | None = None,
    
) -> SamplingParams:
        
return params or SamplingParams()

    
def merge_pooling_params(
        
self,
        
params: PoolingParams | None = None,
    
) -> PoolingParams:
        
return params or PoolingParams()

    
@abstractmethod
    
def pre_process(
        
self,
        
prompt: IOProcessorInput,
        
request_id: str | None = None,
        
**kwargs,
    
) -> PromptType | Sequence[PromptType]:
        
raise NotImplementedError

    
async def pre_process_async(
        
self,
        
prompt: IOProcessorInput,
        
request_id: str | None = None,
        
**kwargs,
    
) -> PromptType | Sequence[PromptType]:
        
return self.pre_process(prompt, request_id, **kwargs)

    
@abstractmethod
    
def post_process(
        
self,
        
model_output: Sequence[PoolingRequestOutput],
        
request_id: str | None = None,
        
**kwargs,
    
) -> IOProcessorOutput:
        
raise NotImplementedError

    
async def post_process_async(
        
self,
        
model_output: AsyncGenerator[tuple[int, PoolingRequestOutput]],
        
request_id: str | None = None,
        
**kwargs,
    
) -> IOProcessorOutput:
        
# We cannot guarantee outputs are returned in the same order they were
        
# fed to vLLM.
        
# Let's sort them by id before post_processing
        
sorted_output = sorted(
            
[(i, item) async for i, item in model_output], key=lambda output: output[0]
        
)
        
collected_output = [output[1] for output in sorted_output]
        
return self.post_process(collected_output, request_id=request_id, **kwargs)

The parse_data method is used for validating the user data and converting it into the input expected by the pre_process* methods. The merge_sampling_params and merge_pooling_params methods merge input SamplingParams or PoolingParams (if any) with the default one. The pre_process* methods take the validated plugin input to generate vLLM's model prompts for regular inference. The post_process* methods take PoolingRequestOutput objects as input and generate a custom plugin output.

An example implementation of a plugin that enables generating geotiff images with the PrithviGeospatialMAE model is available here. Please, also refer to our online (
examples/pooling/plugin/prithvi_geospatial_mae_online.py) and offline (
examples/pooling/plugin/prithvi_geospatial_mae_io_processor.py) inference examples.
Using an IO Processor plugin¶

IO Processor plugins are loaded at engine startup and there are two methods for specifying the name of the plugin to be loaded:

    Via vLLM's EngineArgs: setting the io_processor_plugin argument in the EngineArgs used to initialize the AsyncLLM. The same can be achieved by passing the io_processor_plugin argument to LLM in offline mode, or by passing the --io-processor-plugin argument in serving mode.
    Via the model HF configuration: adding an io_processor_plugin field to the model config (config.json).

The order also determines method priority. i.e., setting the plugin name via EngineArgs will override any plugin name specified in the model HF config (config.json).

LoRA Resolver Plugins¶

This directory contains vLLM's LoRA resolver plugins built on the LoRAResolver framework. They automatically discover and load LoRA adapters from a specified local storage path, eliminating the need for manual configuration or server restarts.
Overview¶

LoRA Resolver Plugins provide a flexible way to dynamically load LoRA adapters at runtime. When vLLM receives a request for a LoRA adapter that hasn't been loaded yet, the resolver plugins will attempt to locate and load the adapter from their configured storage locations. This enables:

    Dynamic LoRA Loading: Load adapters on-demand without server restarts
    Multiple Storage Backends: Support for filesystem, S3, and custom backends. The built-in lora_filesystem_resolver requires a local storage path, while the built-in hf_hub_resolver will pull LoRA adapters from Huggingface Hub and proceed in an identical manner. In general, custom resolvers can be implemented to fetch from any source.
    Automatic Discovery: Seamless integration with existing LoRA workflows
    Scalable Deployment: Centralized adapter management across multiple vLLM instances

Prerequisites¶

Before using LoRA Resolver Plugins, ensure the following environment variables are configured:
Required Environment Variables¶

    VLLM_ALLOW_RUNTIME_LORA_UPDATING: Must be set to true or 1 to enable dynamic LoRA loading

    export VLLM_ALLOW_RUNTIME_LORA_UPDATING=true

    VLLM_PLUGINS: Must include the desired resolver plugins (comma-separated list)

    export VLLM_PLUGINS=lora_filesystem_resolver

    VLLM_LORA_RESOLVER_CACHE_DIR: Must be set to a valid directory path for filesystem resolver

    export VLLM_LORA_RESOLVER_CACHE_DIR=/path/to/lora/adapters

Optional Environment Variables¶

    VLLM_PLUGINS: If not set, all available plugins will be loaded. If set to empty string, no plugins will be loaded.

Available Resolvers¶
lora_filesystem_resolver¶

The filesystem resolver is installed with vLLM by default and enables loading LoRA adapters from a local directory structure.
Setup Steps¶

    Create the LoRA adapter storage directory:

    mkdir
     -p /path/to/lora/adapters

    Set environment variables:

    export VLLM_ALLOW_RUNTIME_LORA_UPDATING=true
    export VLLM_PLUGINS=lora_filesystem_resolver
    export VLLM_LORA_RESOLVER_CACHE_DIR=/path/to/lora/adapters

    Start vLLM server: Your base model can be meta-llama/Llama-2-7b-hf. Please make sure you set up the Hugging Face token in your env var export HF_TOKEN=xxx235.

    python
     -m vllm.entrypoints.openai.api_server \
        --model your-base-model \
        --enable-lora

Directory Structure Requirements¶

The filesystem resolver expects LoRA adapters to be organized in the following structure:

/path/to/lora/adapters/
├── adapter1/
│   ├── adapter_config.json
│   ├── adapter_model.bin
│   └── tokenizer files (if applicable)
├── adapter2/
│   ├── adapter_config.json
│   ├── adapter_model.bin
│   └── tokenizer files (if applicable)
└── ...

Each adapter directory must contain:

    adapter_config.json: Required configuration file with the following structure:

    {
      "peft_type": "LORA",
      "base_model_name_or_path": "your-base-model-name",
      "r": 16,
      "lora_alpha": 32,
      "target_modules": ["q_proj", "v_proj"],
      "bias": "none",
      "modules_to_save": null,
      "use_rslora": false,
      "use_dora": false
    }

    adapter_model.bin: The LoRA adapter weights file

Usage Example¶

    Prepare your LoRA adapter:

    # Assuming you have a LoRA adapter in /tmp/my_lora_adapter
    cp
     -r /tmp/my_lora_adapter /path/to/lora/adapters/my_sql_adapter

    Verify the directory structure:

    ls
     -la /path/to/lora/adapters/my_sql_adapter/
    # Should show: adapter_config.json, adapter_model.bin, etc.

    Make a request using the adapter:

    curl
     http://localhost:8000/v1/completions \
        -H "Content-Type: application/json" \
        -d '{
            "model": "my_sql_adapter",
            "prompt": "Generate a SQL query for:",
            "max_tokens": 50,
            "temperature": 0.1
        }'

How It Works¶

    When vLLM receives a request for a LoRA adapter named my_sql_adapter
    The filesystem resolver checks if /path/to/lora/adapters/my_sql_adapter/ exists
    If found, it validates the adapter_config.json file
    If the configuration matches the base model and is valid, the adapter is loaded
    The request is processed normally with the newly loaded adapter
    The adapter remains available for future requests

Advanced Configuration¶
Multiple Resolvers¶

You can configure multiple resolver plugins to load adapters from different sources:

'lora_s3_resolver' is an example of a custom resolver you would need to implement

export VLLM_PLUGINS=lora_filesystem_resolver,lora_s3_resolver

All listed resolvers are enabled; at request time, vLLM tries them in order until one succeeds.
Custom Resolver Implementation¶

To implement your own resolver plugin:

    Create a new resolver class:

    from vllm.lora.resolver import LoRAResolver, LoRAResolverRegistry
    from vllm.lora.request import LoRARequest

    class CustomResolver(LoRAResolver):
        
    async def resolve_lora(self, base_model_name: str, lora_name: str) -> Optional[LoRARequest]:
            
    # Your custom resolution logic here
            
    pass

    Register the resolver:

    def register_custom_resolver():
        
    resolver = CustomResolver()
        
    LoRAResolverRegistry.register_resolver("Custom Resolver", resolver)

Troubleshooting¶
Common Issues¶

    "VLLM_LORA_RESOLVER_CACHE_DIR must be set to a valid directory"
    Ensure the directory exists and is accessible

    Check file permissions on the directory

    "LoRA adapter not found"
    Verify the adapter directory name matches the requested model name
    Check that adapter_config.json exists and is valid JSON

    Ensure adapter_model.bin exists in the directory

    "Invalid adapter configuration"
    Verify peft_type is set to "LORA"
    Check that base_model_name_or_path matches your base model

    Ensure target_modules is properly configured

    "LoRA rank exceeds maximum"
    Check that r value in adapter_config.json doesn't exceed max_lora_rank setting

Debugging Tips¶

    Enable debug logging:

    export VLLM_LOGGING_LEVEL=DEBUG

    Verify environment variables:

    echo $VLLM_ALLOW_RUNTIME_LORA_UPDATING
    echo $VLLM_PLUGINS
    echo $VLLM_LORA_RESOLVER_CACHE_DIR

    Test adapter configuration:

    python
     -c "
    import json
    with open('/path/to/lora/adapters/my_adapter/adapter_config.json') as f:
        config = json.load(f)
    print('Config valid:', config)
    "

Plugin System¶

The community frequently requests the ability to extend vLLM with custom features. To facilitate this, vLLM includes a plugin system that allows users to add custom features without modifying the vLLM codebase. This document explains how plugins work in vLLM and how to create a plugin for vLLM.
How Plugins Work in vLLM¶

Plugins are user-registered code that vLLM executes. Given vLLM's architecture (see Arch Overview), multiple processes may be involved, especially when using distributed inference with various parallelism techniques. To enable plugins successfully, every process created by vLLM needs to load the plugin. This is done by the load_plugins_by_group function in the vllm.plugins module.
How vLLM Discovers Plugins¶

vLLM's plugin system uses the standard Python entry_points mechanism. This mechanism allows developers to register functions in their Python packages for use by other packages. An example of a plugin:
Code

For more information on adding entry points to your package, please check the official documentation.

Every plugin has three parts:

    Plugin group: The name of the entry point group. vLLM uses the entry point group vllm.general_plugins to register general plugins. This is the key of entry_points in the setup.py file. Always use vllm.general_plugins for vLLM's general plugins.
    Plugin name: The name of the plugin. This is the value in the dictionary of the entry_points dictionary. In the example above, the plugin name is register_dummy_model. Plugins can be filtered by their names using the VLLM_PLUGINS environment variable. To load only a specific plugin, set VLLM_PLUGINS to the plugin name.
    Plugin value: The fully qualified name of the function or module to register in the plugin system. In the example above, the plugin value is vllm_add_dummy_model:register, which refers to a function named register in the vllm_add_dummy_model module.

Types of supported plugins¶

    General plugins (with group name vllm.general_plugins): The primary use case for these plugins is to register custom, out-of-the-tree models into vLLM. This is done by calling ModelRegistry.register_model to register the model inside the plugin function. For an example of an official model plugin, see the bart-plugin which adds support for BartForConditionalGeneration.

    Platform plugins (with group name vllm.platform_plugins): The primary use case for these plugins is to register custom, out-of-the-tree platforms into vLLM. The plugin function should return None when the platform is not supported in the current environment, or the platform class's fully qualified name when the platform is supported.

    IO Processor plugins (with group name vllm.io_processor_plugins): The primary use case for these plugins is to register custom pre-/post-processing of the model prompt and model output for pooling models. The plugin function returns the IOProcessor's class fully qualified name.

    Stat logger plugins (with group name vllm.stat_logger_plugins): The primary use case for these plugins is to register custom, out-of-the-tree loggers into vLLM. The entry point should be a class that subclasses StatLoggerBase.

Guidelines for Writing Plugins¶

    Being re-entrant: The function specified in the entry point should be re-entrant, meaning it can be called multiple times without causing issues. This is necessary because the function might be called multiple times in some processes.

Platform plugins guidelines¶

    Create a platform plugin project, for example, vllm_add_dummy_platform. The project structure should look like this:

    vllm_add_dummy_platform/
    ├──
     vllm_add_dummy_platform/
    │
       ├── __init__.py
    │
       ├── my_dummy_platform.py
    │
       ├── my_dummy_worker.py
    │
       ├── my_dummy_attention.py
    │
       ├── my_dummy_device_communicator.py
    │
       ├── my_dummy_custom_ops.py
    ├──
     setup.py

    In the setup.py file, add the following entry point:

    setup(
        
    name="vllm_add_dummy_platform",
        
    ...
        
    entry_points={
            
    "vllm.platform_plugins": [
                
    "my_dummy_platform = vllm_add_dummy_platform:register"
            
    ]
        
    },
        
    ...
    )

    Please make sure vllm_add_dummy_platform:register is a callable function and returns the platform class's fully qualified name. for example:

    def register():
        
    return "vllm_add_dummy_platform.my_dummy_platform.MyDummyPlatform"

    Implement the platform class MyDummyPlatform in my_dummy_platform.py. The platform class should inherit from vllm.platforms.interface.Platform. Please follow the interface to implement the functions one by one. There are some important functions and properties that should be implemented at least:
        _enum: This property is the device enumeration from PlatformEnum. Usually, it should be PlatformEnum.OOT, which means the platform is out-of-tree.
        device_type: This property should return the type of the device which pytorch uses. For example, "cpu", "cuda", etc.
        device_name: This property is set the same as device_type usually. It's mainly used for logging purposes.
        check_and_update_config: This function is called very early in the vLLM's initialization process. It's used for plugins to update the vllm configuration. For example, the block size, graph mode config, etc., can be updated in this function. The most important thing is that the worker_cls should be set in this function to let vLLM know which worker class to use for the worker process.
        get_attn_backend_cls: This function should return the attention backend class's fully qualified name.
        get_device_communicator_cls: This function should return the device communicator class's fully qualified name.

    Implement the worker class MyDummyWorker in my_dummy_worker.py. The worker class should inherit from WorkerBase. Please follow the interface to implement the functions one by one. Basically, all interfaces in the base class should be implemented, since they are called here and there in vLLM. To make sure a model can be executed, the basic functions should be implemented are:
        init_device: This function is called to set up the device for the worker.
        initialize_cache: This function is called to set cache config for the worker.
        load_model: This function is called to load the model weights to device.
        get_kv_cache_spec: This function is called to generate the kv cache spec for the model.
        determine_available_memory: This function is called to profiles the peak memory usage of the model to determine how much memory can be used for KV cache without OOMs.
        initialize_from_config: This function is called to allocate device KV cache with the specified kv_cache_config
        execute_model: This function is called every step to inference the model.

    Additional functions that can be implemented are:
        If the plugin wants to support sleep mode feature, please implement the sleep and wakeup functions.
        If the plugin wants to support graph mode feature, please implement the compile_or_warm_up_model function.
        If the plugin wants to support speculative decoding feature, please implement the take_draft_token_ids function.
        If the plugin wants to support lora feature, please implement the add_lora,remove_lora,list_loras and pin_lora functions.
        If the plugin wants to support data parallelism feature, please implement the execute_dummy_batch functions.

    Please look at the worker base class WorkerBase for more functions that can be implemented.

    Implement the attention backend class MyDummyAttention in my_dummy_attention.py. The attention backend class should inherit from AttentionBackend. It's used to calculate attentions with your device. Take vllm.v1.attention.backends as examples, it contains many attention backend implementations.

    Implement custom ops for high performance. Most ops can be run by pytorch native implementation, while the performance may not be good. In this case, you can implement specific custom ops for your plugins. Currently, there are kinds of custom ops vLLM supports:

        pytorch ops there are 3 kinds of pytorch ops:
            communicator ops: Device communicator op. Such as all-reduce, all-gather, etc. Please implement the device communicator class MyDummyDeviceCommunicator in my_dummy_device_communicator.py. The device communicator class should inherit from DeviceCommunicatorBase.
            common ops: Common ops. Such as matmul, softmax, etc. Please implement the common ops by register oot way. See more detail in CustomOp class.
            csrc ops: C++ ops. This kind of ops are implemented in C++ and are registered as torch custom ops. Following csrc module and vllm._custom_ops to implement your ops.

        triton ops Custom way doesn't work for triton ops now.

    (optional) Implement other plugable modules, such as lora, graph backend, quantization, mamba attention backend, etc.

Compatibility Guarantee¶

vLLM guarantees the interface of documented plugins, such as ModelRegistry.register_model, will always be available for plugins to register models. However, it is the responsibility of plugin developers to ensure their plugins are compatible with the version of vLLM they are targeting. For example, "vllm_add_dummy_model.my_llava:MyLlava" should be compatible with the version of vLLM that the plugin targets.

The interface for the model/module may change during vLLM's development. If you see any deprecation log info, please upgrade your plugin to the latest version.
Deprecation announcement¶

Deprecations

    use_v1 parameter in Platform.get_attn_backend_cls is deprecated. It has been removed in v0.13.0.
    _Backend in vllm.attention is deprecated. It has been removed in v0.13.0. Please use vllm.v1.attention.backends.registry.register_backend to add new attention backend to AttentionBackendEnum instead.
    seed_everything platform interface is deprecated. It has been removed in v0.16.0. Please use vllm.utils.torch_utils.set_random_seed instead.
    prompt in Platform.validate_request is deprecated and will be removed in v0.18.0.

February 18, 2026 

Attention Backend Feature Support¶

This document is auto-generated by tools/pre_commit/generate_attention_backend_docs.py. It shows the feature support for each registered attention backend based on the checks in AttentionBackend.validate_configuration().

Do not edit this file manually. Run the following command to regenerate it:

python
 tools/pre_commit/generate_attention_backend_docs.py

Setting the Attention Backend¶
Command Line¶

There are two ways to specify the backend from the command line:

Option 1: Using --attention-backend (simple)

vllm
 serve <model> --attention-backend FLASH_ATTN

Option 2: Using --attention-config.backend / -ac.backend (structured config)

# Dot notation
vllm
 serve <model> --attention-config.backend FLASH_ATTN
vllm
 serve <model> -ac.backend FLASH_ATTN

# JSON format
vllm
 serve <model> --attention-config '{"backend": "FLASH_ATTN"}'
vllm
 serve <model> -ac '{"backend": "FLASH_ATTN"}'

    Note: --attention-backend and --attention-config.backend are mutually exclusive. Use one or the other, not both.

Python API¶

Use AttentionConfig with the LLM class:

from vllm import LLM
from vllm.config import AttentionConfig
from vllm.v1.attention.backends.registry import AttentionBackendEnum

# Method 1: Using AttentionConfig with enum
llm = LLM(
    
model="Qwen/Qwen3-0.6B",
    
attention_config=AttentionConfig(backend=AttentionBackendEnum.FLASH_ATTN),
)

# Method 2: Using attention_backend parameter with string
llm = LLM(
    
model="Qwen/Qwen3-0.6B",
    
attention_backend="FLASH_ATTN",
)

Backend Selection Behavior¶
Manual Selection¶

When you explicitly set a backend via --attention-backend or AttentionConfig:

    The backend is validated against your configuration (model dtype, head size, compute capability, etc.)
    If the backend doesn't support your configuration, an error is raised with the specific reason
    If valid, the backend is used

Example error when selecting an incompatible backend:

ValueError: Selected backend FLASHMLA is not valid for this configuration.
Reason: ['compute capability not supported']

Automatic Selection¶

When no backend is specified (the default):

    vLLM iterates through backends in priority order (see tables below)
    Each backend is validated against your configuration
    The first compatible backend is selected
    If no backend is compatible, an error is raised listing all backends and their incompatibility reasons

Backend Priority (CUDA)¶

When no backend is explicitly selected, vLLM chooses the first compatible backend from these priority-ordered lists.

Priority is 1 = highest (tried first).
Standard Attention (MHA, MQA, GQA)¶

Blackwell (SM 10.x):
Priority 	Backend
1 	FLASHINFER
2 	FLASH_ATTN
3 	TRITON_ATTN
4 	FLEX_ATTENTION

Ampere/Hopper (SM 8.x-9.x):
Priority 	Backend
1 	FLASH_ATTN
2 	FLASHINFER
3 	TRITON_ATTN
4 	FLEX_ATTENTION
MLA Attention (DeepSeek-style)¶

Blackwell (SM 10.x):
Priority 	Backend
1 	FLASHINFER_MLA
2 	CUTLASS_MLA
3 	FLASH_ATTN_MLA
4 	FLASHMLA
5 	TRITON_MLA
6 	FLASHMLA_SPARSE
7 	FLASHINFER_MLA_SPARSE

Ampere/Hopper (SM 8.x-9.x):
Priority 	Backend
1 	FLASH_ATTN_MLA
2 	FLASHMLA
3 	FLASHINFER_MLA
4 	TRITON_MLA
5 	FLASHMLA_SPARSE

    Note: ROCm and CPU platforms have their own selection logic. See the platform-specific documentation for details.

Legend¶
Column 	Description
Dtypes 	Supported model data types (fp16, bf16, fp32)
KV Dtypes 	Supported KV cache data types (auto, fp8, fp8_e4m3, etc.)
Block Sizes 	Supported KV cache block sizes (%N means multiples of N)
Head Sizes 	Supported attention head sizes
Sink 	Attention sink support (for StreamingLLM)
Sparse 	Sparse attention support (MLA only)
MM Prefix 	Multimodal prefix full attention support
DCP 	Decode Context Parallelism support (--decode-context-parallel-size)
Attention Types 	Supported attention patterns (Decoder, Encoder, Enc-Dec)
Compute Cap. 	Required CUDA compute capability (N/A for non-CUDA backends)

Symbols: ✅ = Supported, ❌ = Not supported
Standard Attention (MHA, MQA, GQA) Backends¶
Backend 	Version 	Dtypes 	KV Dtypes 	Block Sizes 	Head Sizes 	Sink 	MM Prefix 	DCP 	Attention Types 	Compute Cap.
CPU_ATTN 		fp16, bf16, fp32 	auto 	Any 	32, 64, 80, 96, 112, 128, 160, 192, 224, 256 	❌ 	❌ 	❌ 	All 	N/A
FLASHINFER 	Native† 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	16, 32, 64 	64, 128, 256 	❌ 	❌ 	✅ 	Decoder 	7.x-9.x
FLASHINFER 	TRTLLM† 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	16, 32, 64 	64, 128, 256 	✅ 	❌ 	✅ 	Decoder 	10.x
FLASH_ATTN 	FA2* 	fp16, bf16 	auto, bfloat16 	%16 	Any 	❌ 	❌ 	✅ 	All 	≥8.0
FLASH_ATTN 	FA3* 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	%16 	Any 	✅ 	❌ 	✅ 	All 	9.x
FLASH_ATTN_DIFFKV 		fp16, bf16 	auto 	Any 	Any 	❌ 	❌ 	✅ 	Decoder 	Any
FLEX_ATTENTION 		fp16, bf16, fp32 	auto, bfloat16 	Any 	Any 	❌ 	✅ 	❌ 	Decoder, Encoder Only 	Any
ROCM_AITER_FA 		fp16, bf16 	auto 	16, 32 	64, 128, 256 	❌ 	❌ 	❌ 	Decoder 	N/A
ROCM_AITER_UNIFIED_ATTN 		fp16, bf16 	auto 	Any 	Any 	❌ 	❌ 	❌ 	All 	N/A
ROCM_ATTN 		fp16, bf16, fp32 	auto 	16, 32, 544 	32, 64, 96, 128, 160, 192, 224, 256 	❌ 	❌ 	❌ 	All 	N/A
TREE_ATTN 		fp16, bf16 	auto 	%16 	32, 64, 96, 128, 160, 192, 224, 256 	❌ 	❌ 	❌ 	Decoder 	Any
TRITON_ATTN 		fp16, bf16, fp32 	auto, bfloat16, fp8, fp8_e4m3, fp8_e5m2 	%16 	Any 	✅ 	✅ 	❌ 	All 	Any

    † FlashInfer uses TRTLLM attention on Blackwell (SM100), which supports sinks. Disable via --attention-config.use_trtllm_attention=0.

    * Specify the FlashAttention version via --attention-config.flash_attn_version=2 or 3. Default is FA3 on SM90, FA2 otherwise.

MLA (Multi-head Latent Attention) Backends¶

MLA uses separate backends for prefill and decode phases.
Prefill Backends¶

The prefill backend is selected at runtime based on hardware and configuration.
Backend 	Description 	Compute Cap. 	Enable 	Disable 	Notes
TRT-LLM Ragged‡ 	TensorRT-LLM ragged attention 	10.x 	Default on SM100 	-ac.use_trtllm_ragged_deepseek_prefill=0 	DeepSeek R1 dims only
FlashInfer 	FlashInfer CUTLASS backend 	10.x 	-ac.disable_flashinfer_prefill=0 	-ac.disable_flashinfer_prefill=1 	DeepSeek R1 dims only
cuDNN 	cuDNN-based attention 	10.x 	-ac.use_cudnn_prefill=1 	-ac.use_cudnn_prefill=0 	
FlashAttention 	FlashAttention varlen (FA2/FA3) 	Any 	Default fallback 	Use other backends 	FA3 on SM90, FA2 otherwise

    ‡ TRT-LLM Ragged is the default on Blackwell (SM100). On other GPUs, FlashAttention is used as the default.

Decode Backends¶
Backend 	Dtypes 	KV Dtypes 	Block Sizes 	Head Sizes 	Sink 	Sparse 	MM Prefix 	DCP 	Attention Types 	Compute Cap.
CUTLASS_MLA 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3 	128 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	10.x
FLASHINFER_MLA 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3 	32, 64 	Any 	❌ 	❌ 	❌ 	❌ 	Decoder 	10.x
FLASHINFER_MLA_SPARSE 	fp16, bf16 	auto, bfloat16 	32, 64 	576 	❌ 	✅ 	❌ 	❌ 	Decoder 	10.x
FLASHMLA 	fp16, bf16 	auto, bfloat16, fp8, fp8_e4m3 	64 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	9.x-10.x
FLASHMLA_SPARSE 	bf16 	auto, bfloat16, fp8_ds_mla 	64 	576 	❌ 	✅ 	❌ 	❌ 	Decoder 	9.x-10.x
FLASH_ATTN_MLA 	fp16, bf16 	auto, bfloat16 	%16 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	9.x
ROCM_AITER_MLA 	fp16, bf16 	auto 	1 	Any 	❌ 	❌ 	❌ 	❌ 	Decoder 	N/A
ROCM_AITER_MLA_SPARSE 	fp16, bf16 	auto 	Any 	576 	❌ 	❌ 	❌ 	❌ 	Decoder 	N/A
ROCM_AITER_TRITON_MLA 	fp16, bf16 	auto 	Any 	Any 	❌ 	❌ 	❌ 	❌ 	Decoder 	N/A
TRITON_MLA 	fp16, bf16 	auto, bfloat16 	Any 	Any 	❌ 	❌ 	❌ 	✅ 	Decoder 	Any