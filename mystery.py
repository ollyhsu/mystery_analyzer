from mystery.printer import menu


# 递归创建所需要的目录
def create_dir():
    import os
    if not os.path.exists('.data'):
        os.mkdir('.data')
    if not os.path.exists('.data/etherscan'):
        os.mkdir('.data/etherscan')
    if not os.path.exists('.data/etherscan/code'):
        os.mkdir('.data/etherscan/code')
    if not os.path.exists('.data/etherscan/tmp'):
        os.mkdir('.data/etherscan/tmp')
    if not os.path.exists('.data/report'):
        os.mkdir('.data/report')


def main():
    try:
        create_dir()
        menu()
    except KeyboardInterrupt:
        print("\nBye~ User stopped the program.")


if __name__ == "__main__":
    main()
