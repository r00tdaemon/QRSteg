import cv2
import pywt
import qrcode
import numpy as np

from aes import AESCipher


def aes_encrypt(key: str, data: str):
    cipher = AESCipher(key)
    enc = cipher.encrypt(data)
    return enc


def embed(cover_path: str, key: str, data: str):
    enc = aes_encrypt(key, data)

    cover = cv2.imread(cover_path)
    cover = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
    datacover = np.asarray(cover, dtype="float64")
    coeff2 = pywt.dwt2(datacover, 'haar')

    qr = qrcode.make(enc)

    size = cover.shape
    qr = qr.resize((size[1], size[0]))
    qr = qr.convert("L")
    dataqr = np.asarray(qr, dtype="float64")
    coeff1 = pywt.dwt2(dataqr, 'haar')

    def fuse_coeff(coeff1, coeff2):
        coeff = (coeff1 * 0.0050 + coeff2 * 0.9950)
        return coeff

    stego = []
    stego.append(fuse_coeff(coeff1[0], coeff2[0]))

    c1 = fuse_coeff(coeff1[1][0], coeff2[1][0])
    c2 = fuse_coeff(coeff1[1][1], coeff2[1][1])
    c3 = fuse_coeff(coeff1[1][2], coeff2[1][2])
    stego.append((c1, c2, c3))

    cv2.imwrite("stego.png", pywt.idwt2(stego, 'haar'))

