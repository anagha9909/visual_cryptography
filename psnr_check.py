import numpy as np
import cv2


orgg_file=cv2.imread(r"C:\Users\ASUS\Music\lock1.jpg")
final_img=cv2.imread(r"C:\Users\ASUS\Music\lock2.jpg")
# final_img=cv2.imread(r"C:\Users\ASLAM\Music\lockchange.jpg")
def PSNR(firstImage,secondImage):
    target_data = firstImage.astype(float)
    ref_data = secondImage.astype(float)
    diff = ref_data - target_data
    diff = diff.flatten('C')
    rmse = np.math.sqrt(np.mean(diff ** 2.))
    print("RMSE  ", rmse)
    psnrResultValue = 20 * np.math.log10(255. / rmse)
    print("PSNR:", + psnrResultValue)
    return psnrResultValue

print("PSNR   :  ", PSNR(orgg_file, orgg_file))