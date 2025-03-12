import hashlib
import itertools
import time
import string


class PasswordCracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        
    def hash_password(self, password, method='sha256'):
        if method == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif method == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        elif method == 'sha256':
            return hashlib.sha256(password.encode()).hexdigest()
        elif method == 'sha512':
            return hashlib.sha512(password.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hashing method")

    def brute_force(self, target_hash, method='sha256', max_length=4):
        characters = string.ascii_letters + string.digits + string.punctuation
        self.start_time = time.time()

        for length in range(1, max_length + 1):
            for guess in itertools.product(characters, repeat=length):
                guess_password = ''.join(guess)
                guess_hash = self.hash_password(guess_password, method)
                if guess_hash == target_hash:
                    self.end_time = time.time()
                    time_taken = self.end_time - self.start_time
                    print(f"Password found: {guess_password} (Hash: {guess_hash})")
                    print(f"Time taken: {time_taken:.2f} seconds")
                    return
        print("Password not found using brute force.")

    def dictionary_attack(self, target_hash, dictionary_file, method='sha256'):
        self.start_time = time.time()
        
        try:
            with open(dictionary_file, 'r') as file:
                for line in file:
                    password = line.strip()
                    guess_hash = self.hash_password(password, method)
                    if guess_hash == target_hash:
                        self.end_time = time.time()
                        time_taken = self.end_time - self.start_time
                        print(f"Password found: {password} (Hash: {guess_hash})")
                        print(f"Time taken: {time_taken:.2f} seconds")
                        return
        except FileNotFoundError:
            print(f"Dictionary file '{dictionary_file}' not found.")
            return
        print("Password not found using dictionary attack.")

    def main(self):
        print("Welcome to the Password Cracker.")
        mode = input("Select mode (1 for brute force, 2 for dictionary attack): ")
        
        if mode == '1':
            target_password = input("Enter the password to crack: ")
            method = input("Enter hash method (md5, sha1, sha256, sha512): ")
            hash_value = self.hash_password(target_password, method)
            print(f"Target hash is: {hash_value}")
            max_length = int(input("Enter maximum length for brute force: "))
            self.brute_force(hash_value, method, max_length)
        
        elif mode == '2':
            dictionary_file = input("Enter the path to the dictionary file: ")
            target_password = input("Enter the password to crack: ")
            method = input("Enter hash method (md5, sha1, sha256, sha512): ")
            hash_value = self.hash_password(target_password, method)
            print(f"Target hash is: {hash_value}")
            self.dictionary_attack(hash_value, dictionary_file, method)
        
        else:
            print("Invalid mode selected.")


if __name__ == "__main__":
    cracker = PasswordCracker()
    cracker.main()