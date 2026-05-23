# parallel-image-processor

Python multiprocessing pipeline that applies image filters in parallel across CPU cores, benchmarked against sequential processing.

## Overview

This project explores embarrassingly parallel computation — a class of problems where a workload can be split into independent units with no communication between them, making them ideal for parallel execution. The same principle underlies many high-performance computing (HPC) workflows, where tasks are distributed across hundreds or thousands of cores simultaneously.

The program loads an image, splits it into horizontal strips (one per CPU core), applies a filter to each strip simultaneously using Python's `multiprocessing` module, and reassembles the result with NumPy. Both a parallel and sequential version are timed and compared.

## Features

- Parallel image processing using `multiprocessing.Pool`
- Three filters: blur, grayscale, sharpen
- Automatic core detection via `multiprocessing.cpu_count()`
- Sequential vs. parallel benchmark with speedup measurement
- Output saved as a new image file

## Requirements

```
pip install Pillow numpy
```

## Usage

1. Place any `.jpg` image in the project directory and rename it `input.jpg`
2. Run the script:

```bash
python image_processor.py
```

3. The processed image is saved as `output.jpg`

## Example Output

```
Image size: (4032, 3024)
Cores available: 8
Filter: blur

Sequential time: 3.8421s
Parallel time:   1.0243s
Speedup:         3.75x

Saved output.jpg
```

## How it works

The image array is split along the horizontal axis into N strips, where N equals the number of available CPU cores. Each strip is passed as an argument to a worker process via `multiprocessing.Pool.map()`. Each worker applies the filter independently — no data is shared between processes during execution. The processed strips are returned and reassembled using `numpy.vstack()`.

```
Original image
      │
      ▼
┌─────────────┐
│   Strip 1   │  → Core 0 → filter → result strip 1
│   Strip 2   │  → Core 1 → filter → result strip 2
│   Strip 3   │  → Core 2 → filter → result strip 3
│   Strip 4   │  → Core 3 → filter → result strip 4
└─────────────┘
      │
      ▼
numpy.vstack() → output image
```

## What I learned

Parallel speedup is not linear or guaranteed. Lightweight filters like grayscale show less speedup than compute-heavy ones like Gaussian blur because the overhead of spawning processes becomes significant relative to the work being done. This mirrors a key HPC concept: parallelism is most valuable when the computation per unit of work is high relative to the communication and coordination cost.

## Files

| File | Description |
|---|---|
| `image_processor.py` | Main script — parallel and sequential processing with benchmark |
| `input.jpg` | Input image (not tracked) |
| `output.jpg` | Processed output (not tracked) |

## License

MIT
