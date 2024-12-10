import cv2
import numpy as np
import pytesseract


class Recogniser:

    def __init__(self, image_path):
        self.col_cnt = 0
        self.row_cnt = 0
        self.recognized_text_array = []
        self.cropped_images = []
        self.image = None
        self.grayscale_image = None
        self.blurred_image = None
        self.thresholded_image = None
        self.inverted_image = None
        self.dilated_image = None
        self.contours, self.hierarchy = None, None
        self.image_with_all_contours = None
        self.rectangular_contours = []
        self.all_rectangular_contours = []
        self.image_with_only_rectangular_contours = None
        self.image_path = image_path
        self.width = 0
        self.height = 0
        self.channels = 0


    def rects_recognition_without_storage_steps(self):
        print("rectangular recognition is processing...")
        self.image = cv2.imread(self.image_path)
        self.height, self.width, self.channels = self.image.shape
        self.grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.thresholded_image = cv2.threshold(self.grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        self.inverted_image = cv2.bitwise_not(self.thresholded_image)
        self.dilated_image = cv2.dilate(self.inverted_image, None, iterations=5)

        # looking for contours
        self.contours, self.hierarchy = cv2.findContours(self.dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.image_with_all_contours = self.image.copy()
        cv2.drawContours(self.image_with_all_contours, self.contours, -1, (0, 255, 0), 3)

        # looking for rects in contours
        for contour in self.contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.005 * peri, True)
            if len(approx) == 4:
                self.all_rectangular_contours.append(approx)
        self.image_with_only_rectangular_contours = self.image.copy()
        # correct points ordering in rects
        for rect_cont in self.all_rectangular_contours:
            point = self.order_points(rect_cont)
            x1, y1 = (int(point[0][0]), int(point[0][1]))
            x2, y2 = (int(point[1][0]), int(point[1][1]))
            x3, y3 = (int(point[2][0]), int(point[2][1]))
            x4, y4 = (int(point[3][0]), int(point[3][1]))
            if (abs(x1 - x2) > self.width*0.01) and (abs(y1 - y4) > self.width*0.01) and (abs(x1 - x2) < self.width*0.8):#if (abs(x1 - x2) > 50) and (abs(y1 - y4) > 50) and (abs(x1 - x2) < 2000):
                self.rectangular_contours.append(rect_cont)
        cv2.drawContours(self.image_with_only_rectangular_contours, self.rectangular_contours, -1, (0, 255, 0), 3)
        self.rectangular_contours = self.rectangular_contours[::-1]

    def threshold_image(self):
        self.thresholded_image = cv2.threshold(self.grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def crop_image_to_cells_without_storage(self):
        print("cropping is processing...")
        for contour in self.rectangular_contours:
            point = self.order_points(contour)

            x1, y1 = (int(point[0][0]), int(point[0][1]))
            x2, y2 = (int(point[1][0]), int(point[1][1]))
            x3, y3 = (int(point[2][0]), int(point[2][1]))
            x4, y4 = (int(point[3][0]), int(point[3][1]))

            cropped_image = self.image.copy()
            cropped_image = cropped_image[y1:y3, x1:x2]
            self.cropped_images.append(cropped_image)

    def rects_recognition_with_storage_steps(self):
        print("rectangular recognition is processing...")

        self.image = cv2.imread(self.image_path)
        self.height, self.width, self.channels = self.image.shape
        self.store_process_image("0_original.jpg", self.image)

        self.grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.store_process_image("1_grayscaled.jpg", self.grayscale_image)

        self.thresholded_image = cv2.threshold(self.grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        self.store_process_image("2_thresholded.jpg", self.thresholded_image)

        self.inverted_image = cv2.bitwise_not(self.thresholded_image)
        self.store_process_image("3_inverteded.jpg", self.inverted_image)

        self.dilated_image = cv2.dilate(self.inverted_image, None, iterations=5)
        self.store_process_image("4_dialateded.jpg", self.dilated_image)

        # looking for contours
        self.contours, self.hierarchy = cv2.findContours(self.dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.image_with_all_contours = self.image.copy()
        cv2.drawContours(self.image_with_all_contours, self.contours, -1, (0, 255, 0), 3)
        self.store_process_image("5_all_contours.jpg", self.image_with_all_contours)

        # looking for rects in contours
        for contour in self.contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.005 * peri, True)
            if len(approx) == 4:
                self.all_rectangular_contours.append(approx)
        self.image_with_only_rectangular_contours = self.image.copy()
        # correct points ordering in rects
        for rect_cont in self.all_rectangular_contours:
            point = self.order_points(rect_cont)
            x1, y1 = (int(point[0][0]), int(point[0][1]))
            x2, y2 = (int(point[1][0]), int(point[1][1]))
            x3, y3 = (int(point[2][0]), int(point[2][1]))
            x4, y4 = (int(point[3][0]), int(point[3][1]))
            if (abs(x1 - x2) > self.width*0.001) and (abs(y1 - y4) > self.width*0.001) and (abs(x1 - x2) < self.width*0.8):#if (abs(x1 - x2) > 50) and (abs(y1 - y4) > 50) and (abs(x1 - x2) < 2000):
                self.rectangular_contours.append(rect_cont)
        cv2.drawContours(self.image_with_only_rectangular_contours, self.rectangular_contours, -1, (0, 255, 0), 3)
        self.rectangular_contours = self.rectangular_contours[::-1]
        self.store_process_image("6_only_rectangular_contours.jpg", self.image_with_only_rectangular_contours)

    def col_and_rows(self):
        flag_size_counted = False
        last_x = 0
        for contour in self.rectangular_contours:
            point = self.order_points(contour)

            x1, y1 = (int(point[0][0]), int(point[0][1]))
            x2, y2 = (int(point[1][0]), int(point[1][1]))
            x3, y3 = (int(point[2][0]), int(point[2][1]))
            x4, y4 = (int(point[3][0]), int(point[3][1]))

            if (last_x < x1) and (not flag_size_counted):
                self.col_cnt += 1
            else:
                flag_size_counted = True
            last_x = x1
            self.row_cnt = len(self.rectangular_contours) // self.col_cnt


    def crop_image_to_cells_with_storage(self):
        print("cropping is processing...")
        image_number = 0

        for i in range(len(self.rectangular_contours)):
            point = self.order_points(self.rectangular_contours[i])

            x1, y1 = (int(point[0][0]), int(point[0][1]))
            x2, y2 = (int(point[1][0]), int(point[1][1]))
            x3, y3 = (int(point[2][0]), int(point[2][1]))
            x4, y4 = (int(point[3][0]), int(point[3][1]))

            cropped_image = self.thresholded_image.copy()
            if (i % self.col_cnt == 0) or (i < 5):
                cropped_image = cropped_image[y1:y3, x1:x2]
            else:
                y1_cut = int(y1+(y3-y1)/2*0.3)
                y3_cut = int(y3 - (y3 - y1) / 2 * 0.3)
                x1_cut = int(x1 + (x2 - x1) / 2 * 0.3)
                x2_cut = int(x2 - (x2 - x1) / 2 * 0.3)

                cropped_image = cropped_image[y1_cut:y3_cut,x1_cut:x2_cut]
            self.cropped_images.append(cropped_image)
            image_slice_path = '../storage_steps/cells_recogniser/img_' + str(image_number) + '.jpg'
            cv2.imwrite(image_slice_path, cropped_image)

            image_number += 1


    def text_recognition_from_cells(self):
        print("text recognition is processing...")
        cnt = 0
        for cropped_image in self.cropped_images:
            if (cnt%self.col_cnt==0) or (cnt<5):
                pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'
                custom_config = r'--oem 3 --psm 6'

                text = pytesseract.image_to_string(cropped_image, lang='rus', config=custom_config)

            else:
                #print(cropped_image.shape)
                x = cropped_image.shape[0]
                y = cropped_image.shape[1]
                cnt_black = 0
                for j in range(x):
                    for k in range(y):
                        if cropped_image[j,k]!=255:
                            cnt_black +=1
                        if cnt_black>5:
                            break
                if cnt_black>0:
                    text = 'H\n'
                else:
                    text = '\n'
            self.recognized_text_array.append(text)
            cnt+=1


    def get_text(self):
        return self.recognized_text_array

    def get_rects(self):
        return self.rectangular_contours

    def get_cropped_images(self):
        return self.cropped_images

    @staticmethod
    def store_process_image(file_name, image):
        path = "../storage_steps/recogniser/" + file_name
        cv2.imwrite(path, image)

    @staticmethod
    def order_points(pts):
        # initialize a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        pts = pts.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect
