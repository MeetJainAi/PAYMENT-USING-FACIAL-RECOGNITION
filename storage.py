import pyrebase
import os

# Upload customer image to firebase


def upload_to_storage(dirname):
    config = {
        "apiKey": "AIzaSyBv1R8RiNnUfc7JVWtod6L-ln6u_Fo6bNY",
        "authDomain": "facepay-cloud-storages.firebaseapp.com",
        "databaseURL": "https://facepay-cloud-storages.firebaseio.com",
        "projectId": "facepay-cloud-storages",
        "storageBucket": "facepay-cloud-storages.appspot.com",
        "serviceAccount": "facepay-cloud-storages-firebase-adminsdk-rop8o-5a7353d986.json",
        "messagingSenderId": "1044436837873",
        "appId": "1:881329142401:web:8d7b044a22c7c4904b6b80"
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    images = os.listdir('customer_images')

    for image in images:
        local_path = 'customer_images/'+image
        cloud_storage_path = 'customer_faces/'+image
        storage.child(cloud_storage_path).put(local_path)

    delete_images()

    return cloud_storage_path

# Delete customer image once it has beeen uploaded


def delete_images():
    images = os.listdir('customer_images')

    for image in images:
        delete_path = 'customer_images/'+image
        os.remove(delete_path)

# Download customer images from database for facial recogniton algorithm


def download_from_storage(ref_list):
    config = {
        "apiKey": "AIzaSyA0TGe0JV2yKUzxPO6IBySEvtZ6fAX8XQc",
        "authDomain": "facepay-cloud-storage.firebaseapp.com",
        "databaseURL": "https://facepay-cloud-storage.firebaseio.com",
        "projectId": "facepay-cloud-storage",
        "storageBucket": "facepay-cloud-storage.appspot.com",
        "messagingSenderId": "1044436837873",
        "appId": "1:1044436837873:web:c931218ab38db0897d5050"
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    for ref in ref_list:
        local_path = ref
        storage_path = ref
        storage.child(storage_path).download(local_path)
