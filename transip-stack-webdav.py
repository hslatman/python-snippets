# https://github.com/amnong/easywebdav
import easywebdav

# login credentials
username = "<your_username>"
password = "<your_password>"

# create the client; this is the necessary format 
webdav = easywebdav.connect(host="<your_subdomain>.stackstorage.com", path="/remote.php/webdav", port=443, protocol="https", verify_ssl=True, username=username, password=password)

# ready for some action
webdav.mkdir("test_dir")
webdav.exists("test_dir")
webdav.upload("path/to/local_file", "test_dir/remote_file")
webdav.exists("test_dir/remote_file")
webdav.ls("test_dir")
webdav.download("test_dir/remote_file", "path/to/download_file")
webdav.delete("test_dir/remote_file")
webdav.rmdir("test_dir")

#webdav.mkdirs("nested/directory")

