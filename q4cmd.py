import etcd3

def list_all_keys():
    """Connects to etcd and retrieves all keys, returning decoded strings."""
    try:
        etcd = etcd3.client()
        keys = etcd.get_all()
        return [key.decode('utf-8') for key, _ in keys]
    except Exception as e:
        return f"Error listing keys: {e}"

def get_value_for_key(key):
    """Connects to etcd, retrieves value for the provided key, and decodes it."""
    try:
        etcd = etcd3.client()
        value, _ = etcd.get(key.encode('utf-8'))
        if value is None:
            return f"Key '{key}' doesn't exist."
        return value.decode('utf-8')
    except Exception as e:
        return f"Error getting value: {e}"

def put_key_value_pair(key, value):
    """Connects to etcd and puts the key-value pair, returning a success message."""
    try:
        etcd = etcd3.client()
        etcd.put(key.encode('utf-8'), value.encode('utf-8'))
        return f"Key '{key}' with value '{value}' successfully added to etcd"
    except Exception as e:
        return f"Error putting key-value pair: {e}"

def delete_key(key):
    """Connects to etcd and attempts to delete the provided key."""
    try:
        etcd = etcd3.client()
        deleted = etcd.delete(key.encode('utf-8'))
        if deleted:
            return f"Key '{key}' successfully deleted."
        else:
            return f"Key '{key}' doesn't exist."
    except Exception as e:
        return f"Error deleting key: {e}"

def main():
    while True:
        print("\nOptions:")
        print("1. List all keys")
        print("2. Get value for a key")
        print("3. Put key-value pair")
        print("4. Delete key")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            keys = list_all_keys()
            if isinstance(keys, list):
                print("All keys:", keys)
            else:
                print(keys)

        elif choice == '2':
            key_to_get = input("Enter the key to get value: ")
            value = get_value_for_key(key_to_get)
            print(value)

        elif choice == '3':
            key_to_put = input("Enter the key to put: ")
            value_to_put = input("Enter the value to put: ")
            print(put_key_value_pair(key_to_put, value_to_put))

        elif choice == '4':
            key_to_delete = input("Enter the key to delete: ")
            print(delete_key(key_to_delete))

        elif choice == '5':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
