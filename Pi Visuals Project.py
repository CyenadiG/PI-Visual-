import math
import random
import timeit
import matplotlib.pyplot as plt
import seaborn as sns

'''
The Monte Carlo method of approximating pi involves generating random points 
in a square and determining if they fall within the inscribed circle. The ratio 
of points within the circle to total points generated approximates pi/4, which 
is why we multiply the estimate by 4 at the end.
'''
def monteCarlo(points):
    circle = 0
    for i in range(points):
            #generating random x and y coordinates
            x = random.random()
            y = random.random()

            if x**2 + y**2 <=1:
                circle +=1
        #calculating ratio/pi (4*circle/runs)
    pi_estimate = 4 * (circle/points)
    return pi_estimate

'''
The accumulator method of approximating pi involves summing the Nilakantha series. As 
more terms are added, the approximation "accumulates" closer to pi, hence the name.
'''
def accumulator_approximation(terms):
    pi_estimate = 3  # initialize estimate with first term of the Nilakantha series (which is 3)
    sign = 1  

    for n in range(1, terms + 1): 
        # calculate current term in Nilakantha series
        term = 4 / (2 * n * (2 * n + 1) * (2 * n + 2))
        pi_estimate += sign * term  # add or subtract term based on current sign
        sign *= -1  # switch sign for next term

    return pi_estimate

'''
The original Archimedes method of approximating pi involves inscribing and
circumscribing polygons around a unit circle. As the number of sides of the 
polygons increases, the perimeter of the polygons approaches the circumference
of the circle, and the average of the perimeters approximates pi. Back then, 
Archimedes did not have the "true value" of pi to calculate with to, so he 
started with a known value (side length of inscribed hexagon) and iteratively
doubled the process to increase the number of sides.
'''
def Archimedes_old(iterations):
    sides = 6 # start with inscribed hexagon in unit circle
    side_length = 1  # known value

    for _ in range(iterations):
        # calculate length of side of new polygon
        side_length = math.sqrt(2 - math.sqrt(4 - side_length ** 2))
        sides *= 2  # double number of sides

    # calculate perimeter of inscribed polygon
    perimeter = sides * side_length

    # approximate pi as half the perimeter of the inscribed polygon, since C/2r = pi
    pi_approx = perimeter / 2
    return pi_approx

print(f"Approximation of pi using the oiginal Archimedes method: {Archimedes_old(10): .10f}")
exectime = timeit.timeit(lambda: Archimedes_old(10), number=1)
print(f"Execution time of original Archimedes method: {exectime: .10f} seconds")

'''
Since the original Archimedes method is not really something that can be 
measured and plotted at several side lengths (it's very short iterative 
process), we will use a modern version of the method that calculates the 
perimeter of both polygons at any given number of sides. Unfortunately, 
this method uses pi in the calculations, so it is not a fair comparison.
'''
def Archimedes(sides):
    angle = math.radians(360 / (2 * sides))
    
    # calc perimeter of inscribed and circumscribed polygons
    side_length_inscribed = 2 * math.sin(angle)
    perimeter_inscribed = sides * side_length_inscribed
    side_length_circumscribed = 2 * math.tan(angle)
    perimeter_circumscribed = sides * side_length_circumscribed
    
    # approximate pi by averaging perimeters and dividing by diameter (2)
    pi_approximation = (perimeter_inscribed + perimeter_circumscribed) / 2 / 2
    
    return pi_approximation

'''
The following function plots the runtimes and precisions of the three methods.
The y-axis is the runtime in seconds, and the x-axis is the precision in terms
of absolute error from the true value of pi.
'''
def plot_runtimes():
    # Monte Carlo Method
    monte_carlo_points = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
    num_runs = 5
    plt.figure(figsize=(10, 6))
    for run in range(num_runs):
        monte_carlo_runtimes = []
        monte_carlo_diffs = []
        for points in monte_carlo_points:
            runtime = timeit.timeit(lambda: monteCarlo(points), number=1)
            pi_estimate = monteCarlo(points)
            monte_carlo_runtimes.append(runtime)
            monte_carlo_diffs.append(abs(math.pi - pi_estimate))
        sns.lineplot(x=monte_carlo_diffs, y=monte_carlo_runtimes, marker='o', label=f'Run {run+1}')
    plt.xlabel('Precision (Absolute Error)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Monte Carlo Method: Runtime vs Precision')
    plt.legend()
    plt.grid(True)
    plt.show()
    # fluctuations in runtime are due to the random number generator, plotted 5 runs to show the variance
    
    # Accumulator Method
    accumulator_terms = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
    accumulator_runtimes = []
    accumulator_diffs = []
    for terms in accumulator_terms:
        runtime = timeit.timeit(lambda: accumulator_approximation(terms), number=1)
        pi_estimate = accumulator_approximation(terms)
        accumulator_runtimes.append(runtime)
        accumulator_diffs.append(abs(math.pi - pi_estimate))
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=accumulator_diffs, y=accumulator_runtimes, marker='^')
    plt.xlabel('Precision (Absolute Error)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Accumulator Method: Runtime vs Precision')
    plt.grid(True)
    plt.show()
    
    # Archimedes Method
    archimedes_sides = [3, 4, 5, 6, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    num_runs = 5
    plt.figure(figsize=(10, 6))
    for run in range(num_runs):
        archimedes_runtimes = []
        archimedes_diffs = []
        for sides in archimedes_sides:
            runtime = timeit.timeit(lambda: Archimedes(sides), number=1)
            pi_estimate = Archimedes(sides)
            archimedes_runtimes.append(runtime)
            archimedes_diffs.append(abs(math.pi - pi_estimate))
        sns.lineplot(x=archimedes_diffs, y=archimedes_runtimes, marker='s')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Precision (Absolute Error)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Archimedes Method: Runtime vs Precision')
    plt.grid(True)
    plt.show()
    # fluctuations in runtime are due to the nature of floating point arithmetic and trig functions

plot_runtimes()
