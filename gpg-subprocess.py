#https://stackoverflow.com/questions/13332268/python-subprocess-command-with-pipe

sp = subprocess.Popen(("echo", "<some_password>"), stdout=subprocess.PIPE)
output = subprocess.check_output(("gpg", "--batch", "--homedir", "<location_of_home_directory/.gnupg>", "--no-tty", "--yes", "--passphrase-fd", "0", "--symmetric", "-o", "<output_file>", "<input_file>"), stdin=sp.stdout)
sp.wait()
