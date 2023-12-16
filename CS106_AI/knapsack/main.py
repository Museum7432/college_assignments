from ortools.algorithms import pywrapknapsack_solver
from test_loader import test_loader
from results_saver import results_saver
import os
from os.path import join
from random import sample, choice
import time





def run_solver(loader, time_limit = 10):
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    solver.set_time_limit(time_limit)                    
    

    _ , capacities, values, weights = loader.parse_test()

    solver.Init(values, weights, capacities)

    start_time = time.time()

    computed_value = solver.Solve()

    duration = time.time() - start_time


    packed_items = [item for item in range(0, len(weights[0])) if solver.BestSolutionContains(item_id=item)]


    packed_values = [values[i] for i in packed_items]
    packed_weights = [weights[0][i] for i in packed_items]

    return duration, packed_values, packed_weights


# ./tests/kplib
kplib_path = join( "tests", "kplib")
results_path = "outputs"
time_limit = 90
offset = 2

def main():
    test = test_loader(kplib_path)


    # test.load_types()
    # test.set_types("02StronglyCorrelated")
    # test.load_sizes()
    # test.set_size("n02000")
    # test.load_ranges()
    # test.set_range("R01000")
    # test.load_tests()

    # test.set_test("s017.kp")
       
    # duration, packed_values, packed_weights  = run_solver(test)

    # print(duration)

    # test.set_test("s050.kp")

    # duration, packed_values, packed_weights  = run_solver(test)

    # print(duration)

    saver = results_saver(results_path)

    selected_sizes = [
        'n00050',
        'n00100',
        'n01000',
        'n05000',
        'n10000'
    ]


    
    for t in test.load_types():
        test.set_types(t)

        

        selected_sizes = [i for i in test.load_sizes() if i in selected_sizes]

        for s in selected_sizes:

            test.set_size(s)

            for r in test.load_ranges():
                test.set_range(r)

                test.set_test(choice(test.load_tests()))

                # for i in sample( test.load_tests(),2):

                #     test.set_test(i)
                
                print(test.get_test_path())

                duration, packed_values, packed_weights  = run_solver(test, time_limit)

                print("\tduration: ", f'{round(duration, 5):.5f}')

                saver.save(
                    test_info=test.get_info(),
                    total_value=sum(packed_values),
                    total_weight=sum(packed_weights),
                    runtime= f'{round(duration, 5):.5f}',
                    is_optimal= time_limit - duration > offset,
                    values=packed_values,
                    weights=packed_weights
                )





if __name__ == '__main__':
    main()