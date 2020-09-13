from tkinter import *
from details_db import *
from img_capture import *
from storage import *
from facial_recognition import *
from os import *
from payment import *

# App window options
root = Tk()
root.title('FacePay')
root.geometry('370x370')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Number of times the system can identify the user in a particular checkout
no_of_attempts = 3


# Show differnet frames based on requirements
def swap_callback(frame):
    frame.tkraise()

# Create a customer record in database


def create_record_callback():
    # Check wether all entries are not empty
    if email_entry.get() != '' and clientID_entry.get() != '' and secret_entry.get() != '':
        img_ref = upload_to_storage(email_entry.get())

        create_record(email_entry.get(), clientID_entry.get(), secret_entry.get(
        ), img_ref)
        swap_callback(success_frame)
        # Delete all entries after account creation
        email_entry.delete(0, END)
        clientID_entry.delete(0, END)
        secret_entry.delete(0, END)


# Capture customer images and store them
def capture_registration_callback():
    print('Image capturing......')
    # Check wether secret entry is not empty
    if secret_entry.get() != '':
        uid = secret_entry.get()
        capture_image(uid)
        # Disable capture button
        capture_button = Button(
            capture_frame, text='Capture', bg='black', fg='white', padx=10, pady=10, width=11, state=DISABLED)
        capture_button.grid(row=3, padx=120, pady=15)


# Capture test image of customer for facial recogniton
def capture_recognition_callback():
    global no_of_attempts
    if no_of_attempts == 0:
        open_lockdown_window()
        return
    print('Capturing test image...')
    capture_recognition_image()
    m_capture_button = Button(
        capture_frame, text='Capture', bg='black', fg='white', padx=10, pady=10, width=11, state=DISABLED)
    m_capture_button.grid(row=3, padx=120, pady=15)

# Display a dialog in case recognition failed or no match is found


def open_failure_window(message):
    failure_window = Toplevel()
    failure_window.title('Recognition Failed')
    failure_window.geometry('270x170')
    failure_window.columnconfigure(0, weight=1)
    failure_window.rowconfigure(0, weight=1)
    window_label = Label(failure_window, text=message,
                         font=('bold', 12), bg='lightgrey')
    window_button = Button(failure_window, text='Close Window', bg='black',
                           fg='white', padx=5, pady=5, command=failure_window.destroy)
    window_label.grid(row=0, column=0, sticky='NSEW')
    window_button.grid(row=1, column=0, sticky='NSEW')

# Display a dialog that locks down the application after 3 failed attempts


def open_lockdown_window():
    lockdown_window = Toplevel()
    lockdown_window.title('System Alert')
    lockdown_window.geometry('390x170')
    lockdown_window.columnconfigure(0, weight=1)
    lockdown_window.rowconfigure(0, weight=1)
    window_label = Label(lockdown_window, text='You have been locked out of the system.Please try later',
                         font=('bold', 12), bg='lightgrey')
    window_button = Button(lockdown_window, text='Close Window', bg='black',
                           fg='white', padx=5, pady=5, command=lockdown_window.destroy)
    window_label.grid(row=0, column=0, sticky='NSEW')
    window_button.grid(row=1, column=0, sticky='NSEW')
    delete_faces()
    # Disable the payment button after lockdown
    start_payment_button = Button(
        face_rec_frame, text='Initiate Payment', bg='black', fg='white', padx=10, pady=10, state=DISABLED)
    start_payment_button.grid(row=4, padx=120, pady=15)

    # The payment transaction takes place here


def payment_callback():
    global no_of_attempts
    # Check wether the merchant has enetered his credentials
    if m_name_entry.get() != '' and m_email_entry.get() != '' and amount_entry.get() != '':
        if path.exists('test_image.jpg'):
            print('Transaction initiated... for '+m_name_entry.get())
            ref_list = fetch_references()
            download_from_storage(ref_list)
            img_name = recognize_face()
            # Display a dialog in case app can't detect a face
            if img_name == 'Detection Error':
                open_failure_window('Can\'t Detect a Face')
                return
            # Display a dialog in case no match is found in database
            elif img_name == -1:
                open_failure_window('No Match Found')
                no_of_attempts = no_of_attempts-1
                print('ATTEMPTS '+str(no_of_attempts))
                # Update the attempts value in applition UI
                attempts_label = Label(
                    face_rec_frame, text='Attempts Remaining :'+str(no_of_attempts), font=('bold', 10), bg='lightgrey')
                attempts_label.grid(row=5, sticky='NSEW')
                return
            else:
                img_ref = 'customer_faces/'+img_name
                details = fetch_payment_details(img_ref)
                status_code = process_payment(
                    m_email_entry.get(), amount_entry.get(), details)
                delete_faces()
                # Based on response HTTP status code display the corresponding frame
                if status_code == 201:
                    swap_callback(payment_success_frame)
                else:
                    swap_callback(payment_failure_frame)


####################
# Home page frame
####################
home_frame = Frame(root, bg='lightgrey')
title_label = Label(
    home_frame, text='FacePay', font=('bold', 20), bg='lightgrey')
customer_button = Button(
    home_frame, text='For Customers', bg='black', fg='white', padx=10, pady=10, command=lambda: swap_callback(register_frame))
merchant_button = Button(
    home_frame, text='For Merchants', bg='black', fg='white', padx=10, pady=10, command=lambda: swap_callback(m_register_frame))

home_frame.grid(row=0, column=0, sticky='NSEW')
title_label.grid(row=1, column=0, sticky='NSEW', padx=120, pady=20)
customer_button.grid(row=2, padx=120, pady=15)
merchant_button.grid(row=3, padx=120, pady=15)


##############################
# Customer registration frame
##############################
register_frame = Frame(root, bg='lightgrey')
register_label = Label(register_frame, text='Registration',
                       font=('bold', 20), bg='lightgrey')
email_label = Label(register_frame, text='Email :',
                    font=('bold', 10), bg='lightgrey')
email_entry = Entry(register_frame, width=30)
clientID_label = Label(register_frame, text='Client ID:',
                       font=('bold', 10), bg='lightgrey')
clientID_entry = Entry(register_frame, width=30)
secret_label = Label(register_frame, text='Secret :',
                     font=('bold', 10), bg='lightgrey')
secret_entry = Entry(register_frame, width=30)
webcam_button = Button(register_frame, text='Capture Images', bg='black',
                       fg='white', padx=10, pady=10, command=lambda: swap_callback(capture_frame))
back_button = Button(register_frame, text='Go back', bg='black',
                     fg='white', padx=10, pady=10, command=lambda: swap_callback(home_frame))


register_frame.grid(row=0, column=0, sticky='NSEW')
register_label.grid(row=0, column=0, padx=100, pady=20)
email_label.grid(row=1, column=0, pady=15, sticky='W')
email_entry.grid(row=1, column=0,  pady=15, sticky='E')
clientID_label.grid(row=2, column=0, pady=15, sticky='W')
clientID_entry.grid(row=2, column=0, pady=15, sticky='E')
secret_label.grid(row=3, column=0,  pady=15, sticky='W')
secret_entry.grid(row=3, column=0, pady=15, sticky='E')
webcam_button.grid(row=4, column=0, padx=120, pady=15)
back_button.grid(row=5, column=0, padx=120, pady=15)


#######################
# Capture Images frame
#######################
capture_frame = Frame(root, bg='lightgrey')
capture_label = Label(
    capture_frame, text='Capture Images', font=('bold', 18), bg='lightgrey')
status_label = Label(capture_frame, text='Capture image of your face.Press \'C\' to capture',
                     font=('bold', 10), bg='lightgrey')
capture_button = Button(
    capture_frame, text='Capture', bg='black', fg='white', padx=10, pady=10, width=11, command=capture_registration_callback)
create_record_button = Button(
    capture_frame, text='Create Account', bg='black', fg='white', padx=10, pady=10, command=create_record_callback)

capture_frame.grid(row=0, column=0, sticky='NSEW')
capture_label.grid(row=1, column=0, sticky='NSEW', padx=95, pady=20)
status_label.grid(row=2, column=0, sticky='NSEW', padx=45, pady=20)
capture_button.grid(row=3, padx=120, pady=15)
create_record_button.grid(row=4, padx=120, pady=15)


#################
# Success frame
#################
success_frame = Frame(root, bg='lightgrey')
success_label = Label(
    success_frame, text='Account Created Successfully', font=('bold', 16), bg='lightgrey')
finish_button = Button(
    success_frame, text='Finish', bg='black', fg='white', padx=10, pady=10, width=11, command=root.destroy)

success_frame.grid(row=0, column=0, sticky='NSEW')
success_label.grid(row=1, column=0, sticky='NSEW', padx=45, pady=60)
finish_button.grid(row=3, padx=120, pady=15)


##############################
# Merchant registration frame
##############################
m_register_frame = Frame(root, bg='lightgrey')
m_register_label = Label(m_register_frame, text='Registration',
                         font=('bold', 20), bg='lightgrey')
m_name_label = Label(m_register_frame, text='Name :',
                     font=('bold', 10), bg='lightgrey')
m_name_entry = Entry(m_register_frame, width=30)
m_email_label = Label(m_register_frame, text='Email :',
                      font=('bold', 10), bg='lightgrey')
m_email_entry = Entry(m_register_frame, width=30)
amount_label = Label(m_register_frame, text='Amount to be paid :',
                     font=('bold', 10), bg='lightgrey')
amount_entry = Entry(m_register_frame, width=30)
dashboard_button = Button(m_register_frame, text='Go to Dashboard', bg='black',
                          fg='white', padx=10, pady=10, command=lambda: swap_callback(face_rec_frame))
m_back_button = Button(m_register_frame, text='Go back', bg='black',
                       fg='white', padx=10, pady=10, command=lambda: swap_callback(home_frame))


m_register_frame.grid(row=0, column=0, sticky='NSEW')
m_register_label.grid(row=0, column=0, padx=100, pady=20)
m_name_label.grid(row=1, column=0, pady=15, sticky='W')
m_name_entry.grid(row=1, column=0,  pady=15, sticky='E')
m_email_label.grid(row=2, column=0, pady=15, sticky='W')
m_email_entry.grid(row=2, column=0, pady=15, sticky='E')
amount_label.grid(row=3, column=0,  pady=15, sticky='W')
amount_entry.grid(row=3, column=0, pady=15, sticky='E')
dashboard_button.grid(row=4, column=0, padx=120, pady=15)
m_back_button.grid(row=5, column=0, padx=120, pady=15)


#########################
# Face recognition frame
#########################
face_rec_frame = Frame(root, bg='lightgrey')
face_rec_label = Label(
    face_rec_frame, text='Merchant Dashboard', font=('bold', 18), bg='lightgrey')
rec_label = Label(face_rec_frame, text='Capture image of your customer.Press \'C\' to capture',
                  font=('bold', 10), bg='lightgrey')
m_capture_button = Button(
    face_rec_frame, text='Capture', bg='black', fg='white', padx=10, pady=10, width=11, command=capture_recognition_callback)
start_payment_button = Button(
    face_rec_frame, text='Initiate Payment', bg='black', fg='white', padx=10, pady=10, command=payment_callback)
attempts_label = Label(
    face_rec_frame, text='Attempts Remaining :'+str(no_of_attempts), font=('bold', 10), bg='lightgrey')

face_rec_frame.grid(row=0, column=0, sticky='NSEW')
face_rec_label.grid(row=1, column=0, sticky='NSEW', padx=95, pady=20)
rec_label.grid(row=2, column=0, sticky='NSEW', padx=45, pady=20)
m_capture_button.grid(row=3, padx=120, pady=15)
start_payment_button.grid(row=4, padx=120, pady=15)
attempts_label.grid(row=5, sticky='NSEW')


#########################
# Payment Success frame
#########################
payment_success_frame = Frame(root, bg='lightgrey')
success_status_label = Label(
    payment_success_frame, text='Payment Status :', font=('bold', 18), bg='lightgrey')
pay_success_label = Label(
    payment_success_frame, text='Payment Successful', font=('bold', 12), bg='lightgrey')
pay_success_button = Button(
    payment_success_frame, text='Finish Payment', bg='black', fg='white', padx=10, pady=10, width=11, command=root.destroy)


payment_success_frame.grid(row=0, column=0, sticky='NSEW')
success_status_label.grid(row=1, column=0, sticky='NSEW', padx=95, pady=20)
pay_success_label.grid(row=2, column=0, padx=45, pady=20)
pay_success_button.grid(row=3, column=0, padx=45, pady=20)


#########################
# Payment Failure frame
#########################
payment_failure_frame = Frame(root, bg='lightgrey')
failure_status_label = Label(
    payment_failure_frame, text='Payment Status :', font=('bold', 18), bg='lightgrey')
pay_failure_label = Label(
    payment_failure_frame, text='Payment Failure', font=('bold', 12), bg='lightgrey')
pay_failure_button = Button(
    payment_failure_frame, text='Go Back', bg='black', fg='white', padx=10, pady=10, width=11, command=lambda: swap_callback(face_rec_frame))

payment_failure_frame.grid(row=0, column=0, sticky='NSEW')
failure_status_label.grid(row=1, column=0, sticky='NSEW', padx=95, pady=20)
pay_failure_label.grid(row=2, column=0, padx=45, pady=20)
pay_failure_button.grid(row=3, column=0, padx=45, pady=20)


# Show the home frame on application startup
home_frame.tkraise()


# App's main loop
root.mainloop()
