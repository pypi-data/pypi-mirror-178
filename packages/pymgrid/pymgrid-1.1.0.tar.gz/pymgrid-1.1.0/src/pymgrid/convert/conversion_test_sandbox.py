from pymgrid.MicrogridGenerator import MicrogridGenerator
from pymgrid.convert.convert import to_modular,  to_nonmodular
import pandas as pd

mgen = MicrogridGenerator(nb_microgrid=3)
mgen.generate_microgrid()
microgrid = mgen.microgrids[2]

modular_microgrid = to_modular(microgrid)
print(modular_microgrid)

nonmodular = to_nonmodular(modular_microgrid)
print(nonmodular)

mgen = MicrogridGenerator(nb_microgrid=3)
mgen.generate_microgrid()


def test_equals(obj_1, obj_2, name='', level=0):
    prefix = '--'*level
    equals = []
    not_equals = []
    non_existent = []
    for k_b, v_b in obj_1.__dict__.items():
        try:
            assert k_b in obj_2.__dict__
            v_a = obj_2.__dict__[k_b]
            if hasattr(v_b, '__dict__') and not isinstance(v_b, pd.DataFrame):
                if not (level > 3):
                    equal = test_equals(v_b, v_a, name=k_b, level=level+1)
            else:
                equal = v_b == v_a or (isinstance(v_b, list) and  set(v_b) == set(v_a))
            if equal:
                equals.append(k_b)
            else:
                print(f'{prefix} Key {name}.{k_b} before:\n{prefix}{v_b}')
                print(f'{prefix} Key {name}.{k_b} after:\n{prefix}{v_a}')
                print()
                not_equals.append(k_b)
        except ValueError:
            equal = False
            if isinstance(v_b, pd.DataFrame):
                try:
                    # equal = (v_b == v_a).all().item()
                    equal = v_b.squeeze().eq(v_a.squeeze()).all()
                except ValueError:
                    pass
                # print(f'Key {k_b} equal before and after?: {equal}')
            if not equal:
                print()
                print(f'{prefix} Key {name}.{k_b} before:\n{prefix}{v_b}')
                print()
                print(f'{prefix} Key {name}.{k_b} after:\n{prefix}{v_a}')
                not_equals.append(k_b)
            else:
                equals.append(k_b)
        except AssertionError:
            print(f'{prefix} Key {name}.{k_b} in before not in after')
            non_existent.append(k_b)

    if len(equals):
        print()
        print(f'{prefix} The following keys are all the same:')
        print('\n'.join([prefix + str(x) for x in equals]))
    if len(not_equals):
        print()
        print(f'{prefix} The following keys are not:')
        print('\n'.join([prefix + str(x) for x in not_equals]))
    if len(non_existent):
        print()
        print(f'{prefix} The following keys do not exist after:')
        print('\n'.join([prefix + str(x) for x in non_existent]))

    if len(equals) and not (len(not_equals) or len(non_existent)):
        return True
    return False


print('-----------------------------------')
print('Checking equality')
test_equals(microgrid, nonmodular)
print('done')
