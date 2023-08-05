import os
import contextlib

with contextlib.redirect_stdout(open(os.devnull, 'w')):
    # useful imports without library messages
    import cv2
    import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt
    import glob
    from IPython.display import clear_output
    from sklearn.model_selection import train_test_split
    import pickle

class Nexd_img:
    def __init__(self, *args, **kwargs):
        super(Nexd_img, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs        
    
    def im_load(self, img_path):
        """
        Function that downloads the image in RGB.

        Parameters
        ----------
            - img_path: image path

        Returns
        -------
            - the image
        """

        if not(os.path.isfile(img_path)):
            print("Image not found")
            return np.array([])

        else :
            # the image is created with OpenCV
            img = cv2.imread(img_path)

            # we put the right color
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    def im_show(self, img, title="", dynamic=False, shape=False):
        """
        Function that displays the image.

        Parameters
        ----------
            - img: image
            - (title=""): image title
            - (dynamic=False): image update
            - (shape=True): size display

        Returns
        -------
            - None
        """

        img = np.array(img).copy()

        if shape:
            # we display the dimensions of the image
            print(np.array(img).shape)

        # if there is a title we display it
        if title:
            plt.title(title)

        # the axes are not displayed
        plt.axis('off')

        # delete old output
        if dynamic:
            clear_output(wait=True)

        # if the image is grayscale
        if len(np.array(img).shape) == 2 or np.array(img).shape[2] == 1:
            plt.imshow(img, cmap='gray')

        else:
            plt.imshow(img)
        plt.show()


    def im_redim(self, img, size, interpolator=cv2.INTER_LANCZOS4):
        """
        Function that resizes an image.

        Parameters
        ----------
            - img: image
            - size: size of the new image
            - (interpolator=cv2.INTER_LANCZOS4): interpolator that manages pixels
                  INTER_NEAREST: nearest neighbor
                  INTER_LINEAR: bilinear
                  INTER_AREA: pixel area relationship
                  INTER_CUBIC: bicubic over a 4×4 pixel neighborhood
                  INTER_LANCZOS4: Lanczos on an 8×8 pixel neighborhood

        Returns
        -------
            - resized image
        """

        return cv2.resize(img.copy(), (int(size[1]),int(size[0])), interpolation=interpolator)


    def im_save(self, filename, img):
        """
        Function that saves an image.

        Parameters
        ----------
            - filename: string representing the name of the image
            - img: image

        Returns
        -------
            - None
        """

        # if the image is grayscale
        if len(np.array(img).shape) == 2 or np.array(img).shape[2]==1:
            # normal order of parameters
            if isinstance(filename, str) and not isinstance(img, str):
                plt.imsave(filename, img, cmap='gray')

            # if the order of the parameters is wrong
            elif isinstance(img, str) and not isinstance(filename, str):
                plt.imsave(img, filename, cmap='gray')

        else:

            # normal order of parameters
            if isinstance(filename, str) and not isinstance(img, str):
                plt.imsave(filename, img)

            # if the order of the parameters is wrong
            elif isinstance(img, str) and not isinstance(filename, str):
                plt.imsave(img, filename)
    
    
    def im_2gray(self, img):
        """
        Function that returns the image in gray (0.299*R + 0.587*G + 0.114*B).

        Parameters
        ----------
            -img: image

        Returns
        -------
            - the image in gray
        """

        # we apply the transformation
        return cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    
    
    def im_draw_pixels(self, img, x, y, value=None, color=[0, 255, 0], radius=None):
        """
        Function that draws pixels on the image.

        Parameters
        ----------
            - img: image
            - x: list of x to draw
            - y: list of y to draw
            - (value=None): list of values for each pixel
            - (color=[0, 255, 0]): pixel color if there are no values for each pixel
            - (radius=None): pixel radius

        Returns
        -------
            - the image with the pixels
        """

        img = np.array(img).copy()

        if radius is None:
            radius = int(0.01*max(img.shape[0], img.shape[1]))

        if not(value is None):
            # linearly normalize data between 0.0 and 1.0
            norm = matplotlib.colors.Normalize(vmin=min(value), vmax=max(value))

            # transform values into colors
            rgba = plt.get_cmap('inferno')(norm(value.astype(np.float64)))

            # we draw a circle of 1% of the size of the image (of the color of the value)
            for i in range(len(x)):
                img = cv2.circle(img, (int(x[i]), int(y[i])), radius, rgba[i][:-1]*255, -1)

        else:
            # we draw a circle (in green) of 1% of the size of the image
            for i in range(len(x)):
                img = cv2.circle(img, (int(x[i]), int(y[i])), radius, color, -1)

        return img
    
    
    def im_draw_rect(self, img, coords, color=(255, 0, 0), thickness=1):
        """
        Function that draws rectangles on an image.
        
        Parameters
        ----------
            - img: image on which we want to draw rectangles
            - coords: list of rectangle coordinates (x_start, y_start, x_end, y_end)
            - (color=(255, 0, 0)): color of the rectangles to draw
            - (thickness=1): thickness of the rectangles (-1 for a full rectangle)
        
        Returns
        -------
            - the image with the rectangles
        """

        img = np.array(img).copy()

        # if there is only one rectangle
        if len(np.array(coords).shape) == 1:
            coordinates = np.array([coords])

        for coord in coordinates:
            # we draw all the rectangles
            img = cv2.rectangle(img, (coord[0], coord[1]), (coord[2], coord[3]), color, thickness)
        return img
    
    
    def im_stack(self, list_img):
        """
        Function that returns the overlay of images.

        Parameters
        ----------
            - list_img: list of images

        Returns
        -------
            - superposition of images
        """

        return np.stack(list_img, axis=3).mean(axis=3)/255
    
    
    def im_affine_transform(self, img, pts1, pts2):
        """
        Function that applies an affine transformation to the image.

        Parameters
        ----------
            - img: image
            - pts1: list of origin coordinates of the three points
            - pts2: list of destination coordinates of the three points

        Returns
        -------
            - the transformed image
        """

        rows, cols = img.shape[:2]

        M = cv2.getAffineTransform(np.float32(pts1), np.float32(pts2))
        return cv2.warpAffine(np.array(img).copy(), M, (cols, rows))
    
    
    def im_rotation(self, img, direction):
        """
        Function that applies a rotation of to the image.

        Parameters
        ----------
            -img:image
            - direction: direction of rotation of the image
                  "left" / -90
                  "right" / 90
                  "flip" / 180

        Returns
        -------
            - the rotated image
        """
        
        img = np.array(img).copy()

        if direction == "left" or direction == -90:
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

        elif direction == "right" or direction == 90:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        elif direction == "flip" or direction == 180:
            return cv2.rotate(img, cv2.ROTATE_180)
        else:
            return img
    
    
    def im_empty(self, size, value=0):
        """
        Function that returns an empty image.

        Parameters
        ----------
            - size: image size
            - (value=0): value (RGB possible) to set for each pixel

        Returns
        -------
            - the image
        """

        return value * np.ones(size, np.uint8)
    
    
    def im_square(self, img, maxi=224):
        """
        Function that returns the best square containing the image.

        Parameters
        ----------
            - img: image
            - (maxi=224): size of the square

        Returns
        -------
            - the image
        """
        
        img = np.array(img).copy()
        
        # create background image
        empty = self.im_empty((maxi, maxi, 3), value=0)
        
        coef = max(img.shape[0], img.shape[1])/maxi
        
        # resize
        redim = self.im_redim(np.array(img).copy(), (img.shape[0]/coef, img.shape[1]/coef))
        
        # add to the background
        empty[:redim.shape[0], :redim.shape[1], :] += redim
        return empty

    
    def im_crop(self, img):
        """
        Function that removes black edges from an image.

        Parameters
        ----------
            - img: image

        Returns
        -------
            - the image
        """
        
        img = np.array(img).copy()
        
        # create gray image
        gray = self.im_2gray(img)
        
        # mask the black value
        mask = gray>0
        
        return img[np.ix_(mask.any(1), mask.any(0))]


class Nexd_utils:
    def __init__(self, *args, **kwargs):
        super(Nexd_utils, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs

    def list_ext(self, path=None, list_ext=[".png", ".jpg", ".jpeg"]):
        """
        Function that lists the extensions of a folder.

        Parameters
        ----------
            - (path=None): path of the folder (None if current folder)
            - (list_ext=[".png", ".jpg", ".jpeg"]): list of possible extensions (default: list of images)

        Returns
        -------
            - the list of paths
        """
        
        return np.array([file for file in os.listdir(path) for ext in list_ext if file.endswith(ext)])
    
    
    def search_sub_folders(self, depth=1, path="", custom=None):
        """
        Function that searchs sub-folders.

        Parameters
        ----------
            - (depth=1): search depth
            - (path=""): path to search in a particular folder
            - (custom=None): custom request if needed

        Returns
        -------
            - the list of subfolder paths
        """
        
        if custom is None:
            where = path+"*/"*depth + "*"
        else:
            where = custom
        return [i.replace("\\","/") for i in glob.glob(where)]

    
    def save(self, name, p_object):
        """
        Function that saves an object.

        Parameters
        ----------
            - name: name of the expected file
            - p_object: the object to save

        Returns
        -------
            - None
        """
        
        open_file = open(name+".pkl", "wb")
        pickle.dump(p_object, open_file)
        open_file.close()

        
    def load(self, name):
        """
        Function that load a file.

        Parameters
        ----------
            - name: name of the file to load

        Returns
        -------
            - the object
        """
        
        open_file = open(name+".pkl", "rb")
        val = pickle.load(open_file)
        open_file.close()
        return val
    
    
    def ia_history(self, history_dic, figsize=(15, 5), title=""):
        """
        Function that displays the history of a history stored in a dictionary.

        Parameters
        ----------
            - history_dic: dictionary with loss and accuracy
            - (figsize=(15, 5)): figure size
            - (title=""): image title

        Returns
        -------
            - None
        """

        plt.figure(figsize=figsize)

        if title:
            plt.suptitle(title, fontsize=20)

        colors = ["red", "blue"]

        if len(history_dic) == 1:
            for key in history_dic:
                values = history_dic[key]
                X = range(len(values))
                plt.plot(X, values, color=colors[0], label=key)
                texte = str(key)
            
            plt.title("Evolution of " + texte)
            plt.xlabel("epochs")
            plt.ylabel(texte)
            plt.legend()
            plt.show()
        
        elif len(history_dic) == 2:
            if "acc" in history_dic:
                accuracy = history_dic["acc"]

            else:
                accuracy = history_dic["accuracy"]


            loss = history_dic["loss"]

            X = range(len(loss))

            plt.subplot(121)
            plt.plot(X, loss, color=colors[0], label='loss')
            plt.title("Evolution of loss")
            plt.xlabel("epochs")
            plt.ylabel("loss")
            plt.legend()

            plt.subplot(122)
            plt.plot(X, accuracy, color=colors[0], label='accuracy')
            plt.title("Evolution of accuracy")
            plt.xlabel("epochs")
            plt.ylabel("acc")
            plt.legend()
            plt.show()
            
        elif len(history_dic) == 4:
            if "acc" in history_dic:
                accuracy = history_dic["acc"]
                val_accuracy = history_dic["val_acc"]

            else:
                accuracy = history_dic["accuracy"]
                val_accuracy = history_dic["val_accuracy"]


            loss = history_dic["loss"]
            val_loss = history_dic["val_loss"]

            X = range(len(loss))

            plt.subplot(121)
            plt.plot(X, loss, color=colors[0], label='loss')
            plt.plot(X, val_loss, color=colors[1], label='val_loss')
            plt.title("Evolution of loss")
            plt.xlabel("epochs")
            plt.ylabel("loss")
            plt.legend()

            plt.subplot(122)
            plt.plot(X, accuracy, color=colors[0], label='accuracy')
            plt.plot(X, val_accuracy, color=colors[1], label='val_accuracy')
            plt.title("Evolution of accuracy")
            plt.xlabel("epochs")
            plt.ylabel("acc")
            plt.legend()
            plt.show()

            
    def rect_redim(self, coords, coef):
        """
        Function that multiplies the width and the height of each rectangle by a coefficient (0: no extension, 0.5: size*2, 1:size*3, ...).

        Parameters
        ----------
            - coords: list of coordinates of rectangles [[xmin, ymin, xmax, ymax]]
            - coef: multiplier coefficient

        Returns
        -------
            - the new coordinates
        """

        # where to put the new coordinates
        result = []

        # if there is only one rectangle
        if len(np.array(coords).shape) == 1:
            coords = np.array([coords])

        for coord in coords:

            width = coord[2] - coord[0]
            height = coord[3] - coord[1]

            result.append([ coord[0] - int((width*coef)/2),
                            coord[1] - int((height*coef)/2),
                            coord[2] + int((width*coef)/2),
                            coord[3] + int((height*coef)/2)
                          ] )

        return np.array(result)
    
    
    def draw_pixels(self, x, y, value=None, classes=None, title=None, xlabel=None, ylabel=None):
        """
        Function that draws the points.

        Parameters
        ----------
            - x: list of x to draw
            - y: list of y to draw
            - (value=None): list of values for each point
            - (classes=None): name of the classes of each point if value is not explicit
            - (title=None): image title
            - (xlabel=None): xlabel of the image
            - (ylabel=None): ylabel of the image

        Returns
        -------
            - None
        """

        # if there is a title we display it
        if title:
            plt.title(title)

        # if there is an xlabel we display it
        if xlabel:
            plt.xlabel(xlabel)

        # if there is a ylabel we display it
        if ylabel:
            plt.ylabel(ylabel)

        # we display the points
        scatter = plt.scatter(x, y, c=value, cmap=plt.cm.Set1)

        # if we have values
        if not(value is None):

            # if the values are not labeled
            if classes is None:
                classes = [str(val) for val in set(value)]

            # add the caption
            plt.legend(handles=scatter.legend_elements()[0], labels=classes)

        plt.show()
    
    
    def train_test_split(self, X, y, coef=0.2, seed=42):
        """
        Split arrays or matrices into random train and test subsets.

        Parameters
        ----------
            - X: data
            - y: label
            - (coef=0.2): size of test subsets
            - (seed=42): seed to have same split

        Returns
        -------
            - None
        """
        
        return train_test_split(X, y, test_size=coef, random_state=seed)


    def rgb_colors(self):
        """
        Function that returns an RGB color dictionary.

        Returns
        -------
            - the dictionary
        """
        
        return {
         'maroon': [128, 0, 0],
         'dark_red': [139, 0, 0],
         'brown': [165, 42, 42],
         'firebrick': [178, 34, 34],
         'crimson': [220, 20, 60],
         'red': [255, 0, 0],
         'tomato': [255, 99, 71],
         'coral': [255, 127, 80],
         'indian_red': [205, 92, 92],
         'light_coral': [240, 128, 128],
         'dark_salmon': [233, 150, 122],
         'salmon': [250, 128, 114],
         'light_salmon': [255, 160, 122],
         'orange_red': [255, 69, 0],
         'dark_orange': [255, 140, 0],
         'orange': [255, 165, 0],
         'gold': [255, 215, 0],
         'dark_golden_rod': [184, 134, 11],
         'golden_rod': [218, 165, 32],
         'pale_golden_rod': [238, 232, 170],
         'dark_khaki': [189, 183, 107],
         'khaki': [240, 230, 140],
         'olive': [128, 128, 0],
         'yellow': [255, 255, 0],
         'yellow_green': [154, 205, 50],
         'dark_olive_green': [85, 107, 47],
         'olive_drab': [107, 142, 35],
         'lawn_green': [124, 252, 0],
         'chartreuse': [127, 255, 0],
         'green_yellow': [173, 255, 47],
         'dark_green': [0, 100, 0],
         'green': [0, 128, 0],
         'forest_green': [34, 139, 34],
         'lime': [0, 255, 0],
         'lime_green': [50, 205, 50],
         'light_green': [144, 238, 144],
         'pale_green': [152, 251, 152],
         'dark_sea_green': [143, 188, 143],
         'medium_spring_green': [0, 250, 154],
         'spring_green': [0, 255, 127],
         'sea_green': [46, 139, 87],
         'medium_aqua_marine': [102, 205, 170],
         'medium_sea_green': [60, 179, 113],
         'light_sea_green': [32, 178, 170],
         'dark_slate_gray': [47, 79, 79],
         'teal': [0, 128, 128],
         'dark_cyan': [0, 139, 139],
         'aqua': [0, 255, 255],
         'cyan': [0, 255, 255],
         'light_cyan': [224, 255, 255],
         'dark_turquoise': [0, 206, 209],
         'turquoise': [64, 224, 208],
         'medium_turquoise': [72, 209, 204],
         'pale_turquoise': [175, 238, 238],
         'aqua_marine': [127, 255, 212],
         'powder_blue': [176, 224, 230],
         'cadet_blue': [95, 158, 160],
         'steel_blue': [70, 130, 180],
         'corn_flower_blue': [100, 149, 237],
         'deep_sky_blue': [0, 191, 255],
         'dodger_blue': [30, 144, 255],
         'light_blue': [173, 216, 230],
         'sky_blue': [135, 206, 235],
         'light_sky_blue': [135, 206, 250],
         'midnight_blue': [25, 25, 112],
         'navy': [0, 0, 128],
         'dark_blue': [0, 0, 139],
         'medium_blue': [0, 0, 205],
         'blue': [0, 0, 255],
         'royal_blue': [65, 105, 225],
         'blue_violet': [138, 43, 226],
         'indigo': [75, 0, 130],
         'dark_slate_blue': [72, 61, 139],
         'slate_blue': [106, 90, 205],
         'medium_slate_blue': [123, 104, 238],
         'medium_purple': [147, 112, 219],
         'dark_magenta': [139, 0, 139],
         'dark_violet': [148, 0, 211],
         'dark_orchid': [153, 50, 204],
         'medium_orchid': [186, 85, 211],
         'purple': [128, 0, 128],
         'thistle': [216, 191, 216],
         'plum': [221, 160, 221],
         'violet': [238, 130, 238],
         'magenta': [255, 0, 255],
         'orchid': [218, 112, 214],
         'medium_violet_red': [199, 21, 133],
         'pale_violet_red': [219, 112, 147],
         'deep_pink': [255, 20, 147],
         'hot_pink': [255, 105, 180],
         'light_pink': [255, 182, 193],
         'pink': [255, 192, 203],
         'antique_white': [250, 235, 215],
         'beige': [245, 245, 220],
         'bisque': [255, 228, 196],
         'blanched_almond': [255, 235, 205],
         'wheat': [245, 222, 179],
         'corn_silk': [255, 248, 220],
         'lemon_chiffon': [255, 250, 205],
         'light_golden_rod_yellow': [250, 250, 210],
         'light_yellow': [255, 255, 224],
         'saddle_brown': [139, 69, 19],
         'sienna': [160, 82, 45],
         'chocolate': [210, 105, 30],
         'peru': [205, 133, 63],
         'sandy_brown': [244, 164, 96],
         'burly_wood': [222, 184, 135],
         'tan': [210, 180, 140],
         'rosy_brown': [188, 143, 143],
         'moccasin': [255, 228, 181],
         'navajo_white': [255, 222, 173],
         'peach_puff': [255, 218, 185],
         'misty_rose': [255, 228, 225],
         'lavender_blush': [255, 240, 245],
         'linen': [250, 240, 230],
         'old_lace': [253, 245, 230],
         'papaya_whip': [255, 239, 213],
         'sea_shell': [255, 245, 238],
         'mint_cream': [245, 255, 250],
         'slate_gray': [112, 128, 144],
         'light_slate_gray': [119, 136, 153],
         'light_steel_blue': [176, 196, 222],
         'lavender': [230, 230, 250],
         'floral_white': [255, 250, 240],
         'alice_blue': [240, 248, 255],
         'ghost_white': [248, 248, 255],
         'honeydew': [240, 255, 240],
         'ivory': [255, 255, 240],
         'azure': [240, 255, 255],
         'snow': [255, 250, 250],
         'black': [0, 0, 0],
         'dim_gray': [105, 105, 105],
         'gray': [128, 128, 128],
         'dark_gray': [169, 169, 169],
         'silver': [192, 192, 192],
         'light_gray': [211, 211, 211],
         'gainsboro': [220, 220, 220],
         'white_smoke': [245, 245, 245],
         'white': [255, 255, 255]
         }

class Nexd(Nexd_img, Nexd_utils):

    def __init__(self, *args, **kwargs):
        super(Nexd, self).__init__()
        self.__author = "importFourmi"
        self.__args = args
        self.__kwargs = kwargs
        self.methods = [f for f in dir(self) if not f.startswith('_')]


        if self.__kwargs.get("verbose") == 1:
            print("Welcome to Nexd, the available functions are as follows and you can use help(function) for more information:")
            for fonction in self.methods:
                print("  -", fonction)