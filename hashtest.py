import hashlib

def main():
    pwd = hashlib.sha1(b"Hello")
    print(f"# of Locations: {pwd.hexdigest()}")
    if "f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0" == pwd.hexdigest():
        print("Match found")
if __name__ == "__main__":
    main()
