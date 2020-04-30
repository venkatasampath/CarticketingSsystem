from unittest import TestLoader, TestSuite, TextTestRunner
from Customer_login import Car_Test1
from customerregister import Car_Test2
from Staff_login import Car_Test3
from Staff_register import Car_Test4
from Staff_Editcustomer import Car_Test7
from Staff_downloadreport import Car_Test8
from Staff_view_customertickets import Car_Test6
from Staff_viewcustomer_list import Car_Test5

if __name__ == "__main__":
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(Car_Test1),
        loader.loadTestsFromTestCase(Car_Test2),
        loader.loadTestsFromTestCase(Car_Test3),
        loader.loadTestsFromTestCase(Car_Test4),
        loader.loadTestsFromTestCase(Car_Test5),
        loader.loadTestsFromTestCase(Car_Test6),
        loader.loadTestsFromTestCase(Car_Test7),
        loader.loadTestsFromTestCase(Car_Test8),

    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)