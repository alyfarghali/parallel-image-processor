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

def process_parallel(image_array, filter_name, num_cores):
    #Image split horizontally
    strips = np.array_split(image_array, num_cores, axis = 0)
    args = [(strip, filter_name) for strip in strips]
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(apply_filter, args)
    return np.vstack(results)


def process_sequential(image_array, filter_name):
    return apply_filter((image_array, filter_name))

if __name__ == "__main__":
    multiprocessing.set_start_method('fork')
    image_path = "input2.jpg"
    filter_name = "blur"
    num_cores = multiprocessing.cpu_count()
    #num_cores = 2
    img = Image.open(image_path).convert("RGB")
    image_array = np.array(img)
    start1 = time.time()
    result = process_sequential(image_array, filter_name)
    elapsed = time.time() - start1
    start_ = time.time()
    result_ = process_parallel(image_array, filter_name, num_cores)
    elapsed_ = time.time() - start_
    speedup = round(elapsed/elapsed_, 3)
    print(f"""Image size: {img.size}
          Cores available: {num_cores}
          Sequential time: {elapsed}
          Parallel time: {elapsed_}
          Speedup: {speedup}
          """)
    output_ = Image.fromarray(result_).save("output.jpg")