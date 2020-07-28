"""
Worker and Supervisor

Created by Jas Lau on 7/12/19.
Copyright © 2019 Jas Lau. All rights reserved.

"""

from enum import Enum
import numpy
import random


class Error(Exception):
    """Base class for other exceptions"""
    pass


class EmpNumError(Error):
    """Raised when the employee number is invalid"""
    pass


class IsFull(Error):
    """Raised when the supervisor array is full"""
    pass


# ====================== Base Class: Employee Class ======================
class Employee:
    # static member
    DEFAULT_NAME = "unidentified"
    DEFAULT_NUM = 1234
    BENEFIT_ID = 5000
    MIN_EMPLY_NUM = 1000
    MAX_EMPLY_NUM = 99999

    # constructor
    def __init__(self, name, number):
        self.employee_name = name
        self.employee_num = number

    # accessors
    @property
    def employee_name(self):
        return self.__name

    @property
    def employee_num(self):
        return self.__number

    def get_determine_benefits(self):
        return self.__benefits

    # mutators
    @employee_name.setter
    def employee_name(self, name):
        """Set the employee name.

        Args:
            name (str): Employee name
        """
        if self.validate_name(name):
            self.__name = name
        else:
            self.__name = self.DEFAULT_NAME

    @employee_num.setter
    def employee_num(self, number):
        """Set employee's number. This method will call determine_benefits().
           - benefits (bool): Hold the boolean value of the employee benefits.

        Args:
            number (int): Employee id 

        Returns:
            self.number = self.DEFAULT_NUM
        """
        if self.validate_id(number):
            self.__number = number
        else:
            self.__number = self.DEFAULT_NUM

        if self.determine_benefits(number):
            self.__benefits = True
        else:
            self.__benefits = False

    # helper function
    def __str__(self):
        """Print employees' information in format: 
           'Name #id (Benefits) Shift: DAY.'

        Returns:
            str: Return a string. 
        """
        if self.get_determine_benefits():
            ret_str_bnft = "Benefits"
        else:
            ret_str_bnft = "No Benefits"

        ret_str = '\n{} | ID #: {} | (*{})'.format(self.employee_name,
                                                   str(self.employee_num), ret_str_bnft)
        return ret_str

    def determine_benefits(self, number):
        """Determine if an employee can get benefits.

        Args:
            number (int): Employee id

        Returns:
            bool: True for eligible. False otherwise.
        """
        return number < Employee.BENEFIT_ID

    @classmethod
    def validate_name(cls, the_name):
        """Check if the input employee name is valid.

        Args:
            the_name (str): Employee name

        Returns:
            bool: True for valid. False otherwise.
        """
        return (type(the_name) is str and the_name.isnumeric() is False)

    @classmethod
    def validate_id(cls, employee_id):
        """Check if the input employee id is valid and if it is in range.

        Args:
            employee_id (int): Employee id

        Returns:
            bool: True for valid. False otherwise.
        """
        return (type(employee_id) is int and
                Employee.MIN_EMPLY_NUM <= employee_id <= Employee.MAX_EMPLY_NUM)


# ====================== End of Base Class: Employee Class ======================


# ================= Derived Class: Production Worker Class =================
# inherit from Enum
class Shift(Enum):
    DAY = 1
    SWING = 2
    NIGHT = 3

    def __str__(self):
        ret_str = self.__str__()
        return ret_str


class ProductionWorker(Employee):
    # class constant
    DEFAULT_SHIFT = Shift.DAY
    DEFAULT_HOURLY_RAY_RATE = 1
    DEFAULT_HOURS_WORKED = 0
    MIN_HOURLY_PAY_RATE = 0
    MAX_HOURLY_PAY_RATE = 20
    MIN_HOURS_WORKED = 0
    MAX_HOURS_WORKED = 40

    # constructor
    def __init__(self, name, number, shift, rate,
                 hour):
        """
        Instance variable:
        employee_shift: Hold the employee shift (Day, Swing, Night)
        rate: Hold the hourly pay rate of production workers
        hour: Hold the hours worked by production workers
        """

        # Derived Class attributes
        self.employee_shift = shift
        self.hourly_pay_rate = rate
        self.hours_worked = hour
        # Call Base Class
        super().__init__(name, number)

    # accessors
    @property
    def employee_shift(self):
        return self.__shift

    @property
    def hourly_pay_rate(self):
        return self.__rate

    @property
    def hours_worked(self):
        return self.__hour

    # mutators
    @employee_shift.setter
    def employee_shift(self, shift):
        """ Set employee shift.

        Args:
            shift (Enum): Employee shift.

        Returns:
            Shift: Set instance variable shift to input shift if valid. Set to default shift otherwise.
        """
        if shift in Shift:
            self.__shift = shift
        elif type(shift) is int and (1 <= shift <= 3):
            self.__shift = Shift(shift)
        else:
            self.__shift = self.DEFAULT_SHIFT

    @hourly_pay_rate.setter
    def hourly_pay_rate(self, rate):
        """Set the hourly pay rate.

        Args:
            rate (int): Hourly pay rate
        """
        if self.validate_rate(rate):
            self.__rate = rate
        else:
            self.__rate = self.DEFAULT_HOURLY_RAY_RATE

    @hours_worked.setter
    def hours_worked(self, hour):
        """Set the hour worked.

        Args:
            hour (int): Hour worked
        """
        if self.validate_hour(hour):
            self.__hour = hour
        else:
            self.__hour = self.DEFAULT_HOURS_WORKED

    def gross_pay(self, rate, hour):
        """ Calculate the gross pay for production workers.

        Args:
            rate (int): Hourly pay rate
            hour (int): Hour worked

        Returns:
            int: Return rate * hour for valid input. Zero otherwise.
        """
        if self.validate_rate(rate) and self.validate_hour(hour):
            return rate * hour
        else:
            return 0

    # stringizer and console output
    def __str__(self):
        """ Call Base Class to_string to display name and id. Concatenate
        Production Workers' shift, hourly rate, hours worked and gross pay. 

        Returns:
            str: Return a string.
        """
        me = super().__thisclass__
        mro = super().__self_class__.__mro__
        if len(mro) - mro.index(me) > 2:
            ret_str = super().__str__()
        ret_str += "\nTitle: Production Worker \nShift: {} \nWage: ${} /hr \nHours Worked: {} hrs this week \nGross Pay: ${}\n" \
                   "".format(str(self.employee_shift.name),
                             str(self.hourly_pay_rate), str(self.hours_worked),
                             str(self.gross_pay(self.hourly_pay_rate,
                                                self.hours_worked)))
        return ret_str

    # helper functions
    @classmethod
    def validate_rate(cls, rate):
        """Check if the hourly pay rate valid.

        Args:
            rate (int): hourly pay rate

        Returns:
            bool: True for valid. False otherwise.
        """
        return (type(rate) is int and
                cls.MIN_HOURLY_PAY_RATE <= rate <= cls.MAX_HOURLY_PAY_RATE)

    @classmethod
    def validate_hour(cls, hour):
        """Check if the hours worked valid.

        Args:
            rate (int): hour worked

        Returns:
            bool: True for valid. False otherwise.
        """
        return (type(hour) is int and
                cls.MIN_HOURS_WORKED <= hour <= cls.MAX_HOURS_WORKED)


# ================= Derived Class: Shift Supervisor Class =================


class ShiftSupervisor(Employee):
    DEFAULT_SALARY = 50000
    MIN_SALARY = 50000
    MAX_SALARY = 200000
    DEFAULT_SHIFT = Shift.DAY
    DEFAULT_CAPACITY = 10
    DEFAULT_NUM_OF_WORKERS = 0
    BONUS_ADD_TO_SALARY = 10000
    WORKERS_REQUIRED = 4

    # constructor
    def __init__(self, name=Employee.DEFAULT_NAME, number=Employee.DEFAULT_NUM, salary=DEFAULT_SALARY, shift=DEFAULT_SHIFT,
                 emp_array=DEFAULT_CAPACITY, num_worker=DEFAULT_NUM_OF_WORKERS):
        """
        Instance variable:
        salary: Hold the annual salary of supervisor
        shift: Hold the shift of supervisor
        emp_array: The array of employees
        num_workers: Hold the number of workers under the supervisor
        """

        self.annual_salary = salary
        self.supervisor_shift = shift
        self.emp_array = numpy.empty(
            shape=(1, self.valid_arr_capacity(emp_array)),
            dtype=ProductionWorker)
        self.number_of_workers = num_worker
        super().__init__(name, number)

    # accessors
    @property
    def annual_salary(self):
        return self.__salary

    @property
    def supervisor_shift(self):
        return self.__shift

    # @property
    # def add_to_array(self):
    #     return self.emp_array

    @property
    def number_of_workers(self):
        return self.__num_worker

    # mutators
    @annual_salary.setter
    def annual_salary(self, salary):
        """Set the annual salary.

        Args:
            salary (int): Annual salary of supervisor
        """
        if self.valid_salary(salary):
            self.__salary = salary
        else:
            self.__salary = self.DEFAULT_SALARY

    @supervisor_shift.setter
    def supervisor_shift(self, shift):
        """Set the shift of supervisor.

        Args:
            shift (Shift): Shift of supervisor
        """
        if type(shift) is Shift:
            self.__shift = shift
        elif type(shift) is int and (1 <= shift <= 3):
            self.__shift = Shift(shift)
        else:
            self.__shift = self.DEFAULT_SHIFT

    @number_of_workers.setter
    def number_of_workers(self, num_worker):
        if num_worker <= 0:
            self.__num_worker = self.DEFAULT_NUM_OF_WORKERS
        else:
            self.__num_worker = num_worker

    def add_to_array(self, production_worker):
        """ Determine if the production worker should be added to the
        supervisor array. Raise error if the array is full. If it is not full
        and is in shift, append to the supervisor array and then delete the
        extra length of 1. Increment self.num_worker by 1."""
        if not self.shift_valid(production_worker):
            return
        try:
            if self.emp_array.size <= self.number_of_workers:
                raise IsFull
        except ValueError:
            return

        # Append production worker to the array
        self.emp_array = numpy.append(self.emp_array, production_worker)

        # Remove extra space = 1, because using append method will increase
        # size by 1
        self.emp_array = numpy.delete(self.emp_array, 0)
        # update worker's number
        self.number_of_workers += 1

    # helper functions
    @classmethod
    def valid_salary(cls, salary):
        """Check if the salary input valid.

        Args:
            salary (int): Annul salary

        Returns:
            bool: True for valid. False otherwise.
        """        """ """
        return (type(salary) is int and cls.MIN_SALARY <= salary <= cls.MAX_SALARY)

    @classmethod
    def valid_arr_capacity(cls, emp_array):
        """Check if the array capacity of employee array valid.

        Args:
            emp_array (ProductionWorker): Employee array

        Returns:
            ProductionWorker: Array
        """
        if type(emp_array) is int and emp_array > 0:
            return emp_array
        # else
        return ShiftSupervisor.DEFAULT_CAPACITY

    def shift_valid(self, worker_obj):
        """ Check if the worker is in the same shift as supervisor."""
        return worker_obj.employee_shift is self.supervisor_shift

    def bonus(self):
        """Check if the supervisor get bonus or not."""
        if self.number_of_workers > self.WORKERS_REQUIRED:
            self.annual_salary = self.annual_salary + self.BONUS_ADD_TO_SALARY
            return True
        else:
            return False

    def __str__(self):
        """Call Base Class to_string to display employee's name, employee's
        id and benefits status. """
        me = super().__thisclass__
        mro = super().__self_class__.__mro__
        if len(mro) - mro.index(me) > 2:
            ret_str = super().__str__()
        ret_str += "\nTitle: Shift Supervisor \nAnnual Salary ${} \nShift: {} \n{} workers in their " \
                   "shift\n".format(self.annual_salary,
                                    self.supervisor_shift.name,
                                    self.number_of_workers)

        # Check if there's any worker under a supervisor
        # List Comprehension to obtain only Non-None type element
        the_array = numpy.array([i for i in self.emp_array if i is not None])
        if self.number_of_workers > 0:
            for i in range(len(the_array)):
                ret_str += "\nWorkers {}\n{}".format(i+1, the_array[i])

        return ret_str


# ====================== END OF SHIFT SUPERVISOR CLASS ======================


# ====================== MAIN ======================


def main():
    # Worker object
    worker1 = ProductionWorker('Marco Joseph', 1340, Shift.NIGHT, 20, 10)
    worker2 = ProductionWorker('Roselle Lambert', 6456, Shift.NIGHT, 13, 35)
    worker3 = ProductionWorker('Helen Arbeny', 7566, Shift.NIGHT, 11, 22)
    worker4 = ProductionWorker('Vickie Mclaughlin', 5854, Shift.DAY, 20, 25)
    worker5 = ProductionWorker('Maryrose Hoffman', 2131, Shift.DAY, 30, 10)
    worker6 = ProductionWorker('Gertrude Glass', 1000, Shift.DAY, 18, 23)
    worker7 = ProductionWorker('Ines Huynh', 5456, Shift.DAY, 40, 28)
    worker8 = ProductionWorker('Sharyl Nielsen', 1915, Shift.DAY, 21, 33)
    worker9 = ProductionWorker('Chantel Cantrell', 2638, Shift.SWING, 15, 6)
    worker10 = ProductionWorker('Andy Farrell', 3416, Shift.SWING, 15, 5)

    print("\n---------------- Supervisor ----------------")
    # Supervisor object
    supervisor1 = ShiftSupervisor('Zach Mccall', 2566, 68590, Shift.NIGHT, 3)
    supervisor2 = ShiftSupervisor('Helena Navarro', 6456, 71690, Shift.DAY, 5)
    supervisor3 = ShiftSupervisor(
        'Angela Pittman', 7566, 51680, Shift.SWING, 5)

    print(supervisor1)
    print(supervisor2)
    print(supervisor3)
    sup_array = numpy.array([supervisor1, supervisor2, supervisor3])

    # Adding 7 Workers to Supervisor 1, Only 5 of them in their shift
    print("\n---------------- Add Worker to Supervisor 1----------------")
    try:
        sup_array[0].add_to_array(worker1)
        sup_array[0].add_to_array(worker2)
        sup_array[0].add_to_array(worker3)

    except IsFull:
        print("Array is Full!\n ")
    print(sup_array[0])
    # Printing Bonus Status of Supervisor
    if sup_array[0].bonus() is True:
        print("Supervisor received bonus.")
    else:
        print("Supervisor didn't receive bonus.")
    print("New Salary of Supervisor 1: ", sup_array[
        0].annual_salary)

    # Adding 3 Workers to Supervisor 2, None of them in their shift
    print("\n---------------- Add Worker to Supervisor 2----------------")
    try:
        sup_array[1].add_to_array(worker4)
        sup_array[1].add_to_array(worker5)
        sup_array[1].add_to_array(worker6)
        sup_array[1].add_to_array(worker7)
        sup_array[1].add_to_array(worker8)
    except IsFull:
        print("Array is Full!\n ")
    print(sup_array[1])
    if sup_array[1].bonus() is True:
        print("Supervisor received bonus.")
    else:
        print("Supervisor didn't receive bonus.")
    print("New Salary of Supervisor 1: ", sup_array[
        1].annual_salary)

    # Adding 7 Workers to Supervisor 3, Only 6 of them in their shift
    print("\n---------------- Add Worker to Supervisor 3----------------")
    try:
        sup_array[2].add_to_array(worker9)
        sup_array[2].add_to_array(worker10)

    except IsFull:
        print("Array is Full!\n ")
    print(sup_array[2])
    if sup_array[2].bonus() is True:
        print("Supervisor received bonus.")
    else:
        print("Supervisor didn't receive bonus.")
    print("New Salary of Supervisor 1: ", sup_array[2].annual_salary)


# ====================== END OF MAIN ======================


if __name__ == "__main__":
    main()
