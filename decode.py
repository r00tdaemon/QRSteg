import cv2
import pywt
import numpy as np

from aes import AESCipher


def recover(stego_path: str, cover_path: str):
    stego = cv2.imread(stego_path)
    stego = cv2.cvtColor(stego, cv2.COLOR_BGR2GRAY)
    coeff2 = pywt.dwt2(np.asarray(stego, dtype="float64"), 'haar')

    cover = cv2.imread(cover_path)
    cover = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
    size = stego.shape
    cover = cv2.resize(cover, (size[1], size[0]))
    coeff1 = pywt.dwt2(np.asarray(cover, dtype="float64"), 'haar')

    def fuse_coeff(coeff1, coeff2):
        cooef = (coeff2 - (coeff1 * 0.9950)) / 0.0050
        return cooef

    recovered = []
    recovered.append(fuse_coeff(coeff1[0], coeff2[0]))
    c1 = fuse_coeff(coeff1[1][0], coeff2[1][0])
    c2 = fuse_coeff(coeff1[1][1], coeff2[1][1])
    c3 = fuse_coeff(coeff1[1][2], coeff2[1][2])

    recovered.append((c1, c2, c3))
    cv2.imwrite("decoded.png", pywt.idwt2(recovered, 'haar'))


def aes_decrypt(key: str, data: str):
    cipher = AESCipher(key)
    dec = cipher.decrypt(data)
    return dec

