import os

from regression_test.type1 import test_type1
from regression_test.type2 import test_type2
from regression_test.type3 import test_type3


def main():
    os.makedirs("./regression_test/output/", exist_ok=True)
    test_type1()
    test_type2()
    test_type3()


main()
