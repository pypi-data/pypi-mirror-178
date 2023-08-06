from axiom.__data import main as __data
from axiom.__import import main as __import
int_3 = __data('axiom/example/int_3')

int_4 = __data('axiom/example/int_4')
add = __import('axiom/example/int_add')
result = add({}, [int_3, int_4], given_name='axiom/example/some_number_1')
r2 = add({}, [int_3, result], given_name='axiom/example/some_number_2')
#print('result', result)

