import email_server_handler

print("Testing email functionality")

e = email_server_handler.EmailHandler()
receiver = input("Who should I send this message to? ")
e.set_receiver(receiver)
files = ["test.csv", "test2.csv"]
e.send(files)
