import string
import argparse
import random

MAXSIZE = 2048

valid = list(string.printable)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-g",
        "--generatekeyfile",
        type=argparse.FileType("w"),
        help="path to the encryption key file to write to",
    )

    parser.add_argument(
        "-k",
        "--keyfile",
        type=argparse.FileType("r"),
        help="path to the encryption key file to use as key",
    )

    return parser.parse_args()


def key_gen():
    key = ""
    for i in range(0, MAXSIZE):
        key += random.choice(valid)
    return key


def check_txt(txt):
    if not all(c in string.printable for c in txt):
        raise Exception("invalid characters must be 'printable'")


def encrypt(txt, key):
    check_txt(txt)
    cyph_txt = ""
    for c in map(lambda i, j: valid[(valid.index(i) + valid.index(j)) %
                                    len(valid)], list(txt), key):
        cyph_txt += c
    return cyph_txt


def decrypt(txt, key):
    check_txt(txt)
    pln_txt = ""
    for c in map(lambda i, j: valid[(valid.index(i) - valid.index(j)) %
                                    len(valid)], txt, key):
        pln_txt += c
    return pln_txt


def main():
    args = get_args()
    if(args.generatekeyfile):
        print("\
        generating key and writing to", args.generatekeyfile.name)
        key = key_gen()
        args.generatekeyfile.write(key)
    elif(args.keyfile):
        print("reading key from", args.keyfile.name)
        key = args.keyfile.read()
    else:
        print("making temp key")
        key = key_gen()
    # *** test stuff ***
    # key = key_gen()
    # cyph_txt = encrypt("test string", key)
    # print('coded: [{}]'.format(cyph_txt))
    # pln_txt = decrypt(cyph_txt, key)
    # print('decoded: [{}]'.format(pln_txt))

    while True:
        txt = input("type some text: ")
        cyph_txt = encrypt(txt, key)
        print('coded: [{}]'.format(cyph_txt))
        pln_txt = decrypt(cyph_txt, key)
        print('decoded: [{}]'.format(pln_txt))


if __name__ == "__main__":
    main()
