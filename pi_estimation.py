import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import argparse
import sys

def generate_point():
    X = (np.random.random() * 2) - 1
    Y = (np.random.random() * 2) - 1
    return (X, Y)

def point_in_circle(X, Y):
    return math.dist((X, Y), (0.0, 0.0)) <= 1.0

def run_simulation(points):
    points_inside = 0

    Xs, Ys, colors = [], [], []
    errors = []

    fig, ax = plt.subplots(1, 1)
    fig.suptitle("Monte Carlo PI Simulation (0/0)", fontweight="bold")
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")

    circle = Circle((0.0, 0.0), 1, color='blue', fill=False)
    ax.add_patch(circle)
    ax.set_aspect('equal')

    scatter_data = ax.scatter([], [], s=1)


    for i in range(points):
        #start_time = time.time()

        X, Y = generate_point()
        inside = point_in_circle(X, Y)
        points_inside += 1 if inside else 0

        try:
            pi_estimation = 4 * (points_inside / (i + 1))
        except ZeroDivisionError:
            pi_estimation = 0.0

        error = ((math.pi - pi_estimation) / math.pi) * 100

        Xs.append(X)
        Ys.append(Y)
        colors.append('g' if inside else 'r')

        scatter_data.set_offsets(np.c_[Xs, Ys])
        scatter_data.set_color(colors)

        fig.suptitle(f"Pi Estimator w/ Monte Carlo Simulation ({points_inside}/{i+1})", fontweight="bold")
        ax.set_title(f"Estimated Pi Value: {pi_estimation:.6f} ({'+' if (pi_estimation > math.pi) else '-'}{abs(error):.3f}%)")
        
        #times_taken.append(time.time() - start_time)
        errors.append(error)

        plt.pause(0.001) 
    
    return pi_estimation, errors

def show_erorrs(points, errors : list[float]):
    new_fig, new_ax = plt.subplots(1, 1)

    abs_errors = [abs(e) for e in errors]
    smallest_error = min(abs_errors)
    point_index = abs_errors.index(smallest_error)

    new_fig.suptitle("Error Development Across Simulation ")
    new_ax.set_title(f"Smallest Error @ Point #{point_index + 1} ({(errors[point_index]):.3f}%)")
    new_ax.set_xlabel("# Of Points Plotted")
    new_ax.set_ylabel("Calculated Error (%)")

    new_ax.plot(errors, color="red")
    new_ax.set_yscale('symlog', linthresh=0.5)
    new_ax.plot(np.zeros(shape=(points), dtype=np.float32), color="black", linestyle="dashed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple CLI tool")
    parser.add_argument("-p", "--points", help="Set simulation points", default=1000)

    args = parser.parse_args()

    if args.points:
        try:
            p = int(args.points)
        except:
            sys.exit("Error: Number of points must be an integer!")

        assert p != 0, "Number of points must be at least 1!"
        assert p > 0, "Number of points must be a positive integer!"

        sim_points = p

    plt.ion()

    print(f"Running experiment using {sim_points} points...")

    final_estimation, calculated_erorrs = run_simulation(sim_points)
    show_erorrs(sim_points, calculated_erorrs)

    print(f"Final Estimated Pi Value: {final_estimation:.6f} ({'+' if (final_estimation > math.pi) else '-'}{abs(calculated_erorrs[-1]):.3f}%)")
    print("Press q to quit the simulation!")

    plt.waitforbuttonpress()
    plt.ioff()
    plt.close('all')
