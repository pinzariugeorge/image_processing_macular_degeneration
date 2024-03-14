import numpy as np
import cv2 as cv


def create_gradual_effect(src1, src2, mask):
    """
    Blend the original image with the blurred imageand the mask, for a gradual blur effect.

    """
    res_channels = []
    for c in range(0, src1.shape[2]):
        a = src1[:, :, c]
        b = src2[:, :, c]
        m = mask[:, :, c]
        res = cv.add(
            cv.multiply(b, cv.divide(np.full_like(m, 255) - m, 255.0, dtype=cv.CV_32F), dtype=cv.CV_32F),
            cv.multiply(a, cv.divide(m, 255.0, dtype=cv.CV_32F), dtype=cv.CV_32F),
            dtype=cv.CV_8U)
        res_channels += [res]
    res = cv.merge(res_channels)
    return res


def mouse_click(event, x, y,
                flags, param):
    """ Method used to handle left mouse click. """
    
    if event == cv.EVENT_LBUTTONDOWN:
        # Create the mask empty for inpaint
        mask = np.zeros((h, w), dtype='uint8')
        
        # Draw a circle where the inpainting shall take place
        cv.circle(mask, (x, y), radius, (255, 255, 255), -1)

        img_inpainted = cv.inpaint(img, mask, 3, cv.INPAINT_TELEA)

        # Blur effect for center area where user clicks
        # A combination of blur effects and inpaint have been used for desired effect
        
        img_blurred = cv.GaussianBlur(img_inpainted, (15, 15), 15)
        img_blurred = cv.inpaint(img_blurred, mask, 3, cv.INPAINT_TELEA)
        mask_blur = np.zeros_like(img_blurred)
        cv.circle(mask_blur, (x, y), radius, (255, 255, 255), -1)
        cv.GaussianBlur(mask_blur, (101, 101), 13, dst=mask_blur)
        img_blend = create_gradual_effect(img_blurred, img_inpainted, mask_blur)

        # Blur effect for peripheral area to mimmick human vision
        img_rim = cv.GaussianBlur(img_blend, (17, 17), 0)
        mask_rim = np.zeros_like(img_blend)
        cv.circle(mask_rim, (x, y), (radius+300), (255, 255, 255), -1)
        cv.GaussianBlur(mask_rim, (101, 101), 13, dst=mask_rim)
        img_final = create_gradual_effect(img_blend, img_rim, mask_rim)

        # Blur effect for peripheral area to mimmick human vision
        img_rim = cv.GaussianBlur(img_blend, (15, 15), 0)
        mask_rim = np.zeros_like(img_blend)
        cv.circle(mask_rim, (x, y), (radius+150), (255, 255, 255), -1)
        cv.GaussianBlur(mask_rim, (101, 101), 13, dst=mask_rim)
        img_final = create_gradual_effect(img_blend, img_rim, mask_rim)

        # Blur effect for peripheral area to mimmick human vision
        img_rim = cv.GaussianBlur(img_blend, (11, 11), 0)
        mask_rim = np.zeros_like(img_blend)
        cv.circle(mask_rim, (x, y), (radius+50), (255, 255, 255), -1)
        cv.GaussianBlur(mask_rim, (101, 101), 13, dst=mask_rim)
        img_final = create_gradual_effect(img_blend, img_rim, mask_rim)

        # Blur effect for peripheral area to mimmick human vision
        img_rim = cv.GaussianBlur(img_blend, (5, 5), 0)
        mask_rim = np.zeros_like(img_blend)
        cv.circle(mask_rim, (x, y), (radius+10), (255, 255, 255), -1)
        cv.GaussianBlur(mask_rim, (101, 101), 13, dst=mask_rim)
        img_final = create_gradual_effect(img_blend, img_rim, mask_rim)
        # Show result in window
        cv.imshow("Stargardt's Disease image processor", img_final)



def get_screen_resolution():

    try:
        # For Windows
        import ctypes
        user32 = ctypes.windll.user32
        width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return width, height
    except ImportError:
        pass

    try:
        # For Linux
        from subprocess import check_output
        output = check_output("xrandr | grep \* | cut -d' ' -f4", shell=True).decode("utf-8")
        width, height = map(int, output.split("x"))
        return width, height
    except ImportError:
        pass

    

    # Default fallback (if unable to determine screen resolution)
    return 800, 600  # Adjust these values according to your needs

if __name__ == "__main__":

    img = cv.imread('src/image.png')
    
    h, w, _ = img.shape
    radius = 50

    cv.imshow("Stargardt's Disease image processor", img)

    cv.setMouseCallback("Stargardt's Disease image processor", mouse_click)
#Photo by Tahir Osman: https://www.pexels.com/photo/elderly-woman-sitting-by-table-17058381/
    cv.waitKey(0)
    cv.destroyAllWindows()
   

