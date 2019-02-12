import email_handler

print("Testing email functionality")

e = email_handler.EmailHandler()
while not e.is_valid_sender():
    sender = input("Enter the account of the sender: ")
    password = input("Please enter a password: ")
    e.set_sender(sender, password)
    if not e.is_valid_sender():
        print("The supplied address or password is incorrect.")
receiver = input("Who should I send this message to? ")
e.set_receiver(receiver)
files = ["test.csv", "test2.csv"]
e.send(files)
