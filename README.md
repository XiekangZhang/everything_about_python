# everything_about_python

pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

conda update --all

conda env update --name myenv --file local.yml --prune

conda env create -n env_name --file local.yml
conda activate env_name
conda deactivate
conda remove -n env_name --all

## IT terminology - concurrency & parallelism

### Concurrent vs. Parallel

- **Concurrency**: deals with managing multiple tasks at once
- **Parallelism**: deals with executing multiple tasks at the exact same instant

A system can be _concurrent_ without being _parallel_ (e.g., a single-core CPU rapidly switching between tasks). A system that is parallel is inherently concurrent.

### why is concurrency important in IT?

- Responsiveness: concurrency allows the UI to remain responsive
- Resource Utilization: concurrency allows the CPU to do other work while one task is waiting, rather than sitting idle
- Throughput: concurrency allows the server to process multiple requests without one blocking others
- Modularity: breaking down complex problems into smaller, independent tasks that can be managed concurrently

## functools - higher-order functions and operations on callable objects

- the _functools_ module is for higher-order functions: functions that act on or return other functions.
