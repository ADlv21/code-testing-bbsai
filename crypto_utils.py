import os
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

IV_LENGTH = 16


def aes256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data


def aes256_decrypt(data: str, key: bytes, iv: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data


def decode_base64_to_excel(encoded_content):
    try:
        return base64.b64decode(encoded_content)
    except Exception as e:
        raise RuntimeError(f"Error encoding file: {e}")


def encrypt_file(file_path, server):
    try:
        if server == 'prod':
            sym_key = b""
        else:
            sym_key = b""

        key = sym_key
        iv = key[:IV_LENGTH]

        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted_data = aes256_encrypt(data, key, iv)

        with open(file_path, 'wb') as f:
            f.write(encrypted_data)

        print("File encrypted and saved successfully!")
    except Exception as e:
        raise RuntimeError(f"Error during encryption: {e}")


def decrypt_file(data, file_path, sym_key):
    try:
        key = sym_key
        iv = key[:IV_LENGTH]
        decrypted_data = aes256_decrypt(data, key, iv)
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)
        print("File decrypted and saved successfully!")
    except Exception as e:
        raise RuntimeError(f"Error during decryption: {e}")


def decrypt_response(file_path, file_name, server, folder_name='new_output'):
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    enc_base64_res = json_data.get("enc_base64_res")
    data = decode_base64_to_excel(enc_base64_res)

    if server == 'prod':
        sym_key = b""
    else:
        sym_key = b""

    decrypt_file(data, file_path, sym_key)

    with open(file_path, 'r') as f:
        json_data = json.load(f)

    enc_base64_res = json_data["data"]["crfq_base64"]
    myra_missing_fields = json_data["data"]["missing_myra_field_list"]
    product_code = json_data["data"]["product_code"]
    product_name = json_data["data"]["product_name"]

    data = decode_base64_to_excel(enc_base64_res)

    os.remove(file_path)

    file_save_path = f'{folder_name}/{server}_output_{file_name}.xlsx'
    if os.path.exists(file_save_path):
        os.remove(file_save_path)

    with open(file_save_path, 'wb') as f:
        f.write(data)

    return [myra_missing_fields, product_code, product_name]