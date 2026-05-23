import multiprocessing
import time
import numpy as np
from PIL import Image, ImageFilter

def apply_filter(args):
    strip, filter_name = args
    image = Image.fromarray(strip)
    if filter_name == "sharpen":
        image = image.filter(ImageFilter.SHARPEN)
    elif filter_name == "blur":
        image = image.filter(ImageFilter.GaussianBlur(radius=30))
    elif filter_name == "grayscale":
        image = image.convert("L").convert("RGB") 
    return np.array(image)

def process_multiple_parallel(image_arrays, filter_name, num_cores):
    args = [(image_array, filter_name) for image_array in image_arrays]
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(apply_filter, args)
    return results

def process_multiple_sequential(image_arrays, filter_name):
    return [apply_filter((image_array, filter_name)) for image_array in image_arrays]
    

if __name__ == "__main__":
    multiprocessing.set_start_method('fork')
    image_paths = ["input.jpg", "input1.jpg", "input2.jpg", "input3.jpg"]
    filter_name = "blur"
    num_cores = multiprocessing.cpu_count()
    #num_cores = 2
    image_arrays = [np.array(Image.open(image_path).convert("RGB")) for image_path in image_paths]
    start1 = time.time()
    result = process_multiple_sequential(image_arrays, filter_name)
    elapsed = time.time() - start1
    start_ = time.time()
    result_ = process_multiple_parallel(image_arrays, filter_name, num_cores)
    elapsed_ = time.time() - start_
    speedup = round(elapsed/elapsed_, 3)
    print(f"""
          Cores available: {num_cores}
          Sequential time: {elapsed}
          Parallel time: {elapsed_}
          Speedup: {speedup}
          """)
    for i, result in enumerate(result_):
        Image.fromarray(result).save(f"output{i+1}.jpg")