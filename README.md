# parallel-image-processor

Python multiprocessing pipeline that applies image filters in parallel across CPU cores, benchmarked against sequential processing.

## Overview

This project explores embarrassingly parallel computation — a class of problems where a workload can be split into independent units with no communication between them, making them ideal for parallel execution. The same principle underlies many high-performance computing (HPC) workflows, where tasks are distributed across hundreds or thousands of cores simultaneously.

Two parallelism strategies are implemented and benchmarked:

- **Strip-based**: one image split into horizontal strips, one strip per core
- **Multi-image**: multiple images processed simultaneously, one image per core

## Features

- Parallel image processing using `multiprocessing.Pool`
- Three filters: blur, grayscale, sharpen
- Two parallelism strategies: strip-based and multi-image
- Automatic core detection via `multiprocessing.cpu_count()`
- Sequential vs. parallel benchmark with speedup measurement
- Output saved as new image files

## Requirements

```
pip install Pillow numpy
```

## Usage

1. Place image files in the project directory
2. Activate your virtual environment:

```bash
source venv/bin/activate
```

3. Run the script:

```bash
python3 processor.py
```

## Benchmark Results

### Strategy 1: Strip-based (one image split across cores)

Parallel was slower than sequential across all tested environments. The filter computation per strip is lightweight enough that process spawning overhead dominates — a classic case of overhead dominance on small workloads.

### Strategy 2: Multi-image (one full image per core)

Processing multiple independent images in parallel outperformed sequential processing on Linux x86. With enough images, the total work per run grows while overhead stays fixed, allowing parallelism to pay off.

**Key finding:** multi-image parallelism outperforms strip-based parallelism for this workload because each worker receives a full, compute-heavy job with no inter-process dependencies.

## What I learned

**Parallel computing is not always faster.** When the computation per unit of work is small relative to the cost of spawning and coordinating processes, sequential processing wins. This is known as overhead dominance.

**Workload design matters.** Strip-based parallelism on a single image loses because each strip is too lightweight. Multi-image parallelism wins because each worker gets a complete, independent job.

**Architecture affects performance.** Apple Silicon's unified memory architecture makes Python multiprocessing less effective than on Linux x86 — the architecture used in production HPC clusters like Georgia Tech's PACE Phoenix cluster. The same code produces different results depending on the underlying hardware.

**Amdahl's Law is real.** The theoretical maximum speedup is bounded by the number of cores and the fraction of work that can be parallelized. Fixed overhead costs set a floor that parallelism cannot overcome on small workloads, no matter how many cores are available.

**More work favors parallelism.** As the number of images increases, the fixed overhead cost becomes a smaller fraction of total runtime and speedup improves. This mirrors how HPC schedulers like Slurm manage large job queues — parallelism pays off at scale.

## Project Structure

| File | Description |
|---|---|
| `processor.py` | Strip-based parallelism strategy with benchmark |
| `processor2.py` | Multi-image parallelism strategy with benchmark |

## License

MIT