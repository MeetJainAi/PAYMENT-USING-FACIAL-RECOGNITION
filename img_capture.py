import cv2
import os


def capture_image(uid):
    # Detects key press in milliseconds
    key = cv2. waitKey(1)
# Start webcam and configure options
    webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
# Placeholder name for images
    img_name = 'customer_images/'+str(uid)+'.jpg'

    while True:
        check, frame = webcam.read()
        cv2.imshow('Capturing Image......', frame)
        key = cv2.waitKey(1)
# Capture image and convert it to grayscale and resize on pressing 'C'
        if key == ord('c'):
            cv2.imwrite(filename=img_name, img=frame)
            _img = cv2.imread(img_name, cv2.IMREAD_ANYCOLOR)
           # gray = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)
            img_resize = cv2.resize(_img, (256, 256))
            img_resized = cv2.imwrite(
                filename=img_name, img=img_resize)
            break

    webcam.release()
    cv2.destroyAllWindows()


def capture_recognition_image():
    print('---------')
    # Detects key press in milliseconds
    key = cv2. waitKey(1)
# Start webcam and configure options
    webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
# Placeholder name for images
    img_name = 'test_image.jpg'

    while True:
        check, frame = webcam.read()
        cv2.imshow('Capturing Test Image......', frame)
        key = cv2.waitKey(1)
# Capture image and convert it to grayscale and resize on pressing 'C'
        if key == ord('c'):
            cv2.imwrite(filename=img_name, img=frame)
            _img = cv2.imread(img_name, cv2.IMREAD_ANYCOLOR)
           # gray = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)
            img_resize = cv2.resize(_img, (256, 256))
            img_resized = cv2.imwrite(
                filename=img_name, img=img_resize)
            break

    webcam.release()
    cv2.destroyAllWindows()

# Delete images after transaction


def delete_faces():
    images = os.listdir('customer_faces')
    os.remove('test_image.jpg')
    for image in images:
        delete_path = 'customer_faces/'+image
        os.remove(delete_path)
