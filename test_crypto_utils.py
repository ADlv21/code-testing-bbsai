import pytest
import crypto_utils as module_0


def test_case_0():
    str_0 = "l"
    with pytest.raises(RuntimeError):
        module_0.decode_base64_to_excel(str_0)


def test_case_1():
    none_type_0 = None
    with pytest.raises(RuntimeError):
        module_0.encrypt_file(none_type_0, none_type_0)


def test_case_2():
    str_0 = "'\tq}Ae0\t=2*zU9S-"
    with pytest.raises(RuntimeError):
        module_0.decrypt_file(str_0, str_0, str_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    bytes_0 = b""
    module_0.aes256_encrypt(bytes_0, bytes_0, bytes_0)


def test_case_4():
    str_0 = "prod"
    with pytest.raises(RuntimeError):
        module_0.encrypt_file(str_0, str_0)
