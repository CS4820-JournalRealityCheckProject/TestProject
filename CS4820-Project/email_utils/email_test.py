import email_handler

print("Testing email functionality")

e = email_handler.EmailHandler()
while not e.is_valid_sender():
    e.set_sender()
files = ["test.csv", "test2.csv"]
e.send(files)
