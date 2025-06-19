# Question
# Design and implement a File Sharing Application that supports uploading, downloading, and sharing files.
#
# Your system should:
# - Represent users who can upload and share files.
# - Represent files with metadata such as name, size, uploader, and unique ID.
# - Allow users to:
#     - Upload files to the system.
#     - Share files with other users via a unique shareable link or user ID.
#     - Download files they have access to.
# - Handle permissions:
#     - Only the uploader can share a file.
#     - Only shared users can download the file (apart from uploader).
# - Maintain a mapping of users to the files they uploaded and the files shared with them.
# - (Optional/Stretch) Support expirable or single-use shareable links.
#
# Think about:
# - File ID generation.
# - How you would enforce permissions.
# - How to decouple storage (where files are) from access control.
# - How to structure the classes to encapsulate responsibilities cleanly.

class User:
    def __init__(self,id,name) -> None:
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.name}(ID:{self.id})"

class File:
    def __init__(self,file_id,name,size,uploader) -> None:
        self.file_id = file_id
        self.name = name
        self.size = size
        self.uploader = uploader
        self.allowed_users = set()

    def allow_access(self,target_user):
        if target_user not in self.allowed_users:
            self.allowed_users.add(target_user)
            return f"{target_user} allowed to access file {self.name}"
        else:
            return f"{target_user} already allowed to access file {self.name}"
        
    def check_access(self,user):
        if user in self.allowed_users:
            return True
        else:
            return False
        
class PermissionManager:
    @staticmethod
    def share_file(user,file,target_user):
        #first check user is the uploader
        if file.uploader == user:
            return file.allow_access(target_user)
        else:
            return f"{user} not allowed to give access on file {file.name}"

class DownloadManager:
    @staticmethod
    def download_file(user,file):
        if file.uploader == user:
            return f"{user} is the uploader and can download file, here is the file {file.name}"
        elif file.check_access(user):
            return f"{user} has access and can download file, here is the file {file.name}"
        else:
            return f"{user} do not have access and cannot download file {file.name}"

class FileSharingService:
    def __init__(self) -> None:
        self.files = []

    def upload_file(self,file,user):
        file.uploader = user
        self.files.append(file)

    def give_permission(self,user,file,target_user):
        return PermissionManager.share_file(user,file,target_user)
    
    def download_file(self,user,file):
        return DownloadManager.download_file(user,file)


if __name__ == "__main__":
    # Create users
    alice = User(1, "Alice")
    bob = User(2, "Bob")
    charlie = User(3, "Charlie")

    # Create file sharing service
    service = FileSharingService()

    # Upload file by Alice
    file1 = File(101, "design_doc", 500, uploader=None)
    service.upload_file(file1, alice)

    # Alice tries to share file with Bob
    print(service.give_permission(alice, file1, bob))

    # Bob downloads file
    print(service.download_file(bob, file1))

    # Charlie (no access) tries to download
    print(service.download_file(charlie, file1))

    # Charlie gets access from Bob (should fail)
    print(service.give_permission(bob, file1, charlie))  # Bob is not uploader

    # Alice shares with Charlie
    print(service.give_permission(alice, file1, charlie))

    # Charlie downloads
    print(service.download_file(charlie, file1))
