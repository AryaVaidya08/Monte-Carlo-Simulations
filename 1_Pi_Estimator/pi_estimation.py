import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import argparse
from datetime import datetime
import sys
import os

def generate_point():
    X = (np.random.random() * 2) - 1
    Y = (np.random.random() * 2) - 1
    return (X, Y)

def point_in_circle(X, Y):
    return math.dist((X, Y), (0.0, 0.0)) <= 1.0

def run_simulation(points, save_dir):
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

    if save_dir != None:
        fig.savefig(f"{save_dir}/results_{points}_sim.png")
    
    return pi_estimation, errors

def show_erorrs(points, errors, save_dir):
    errors_fig, errors_ax = plt.subplots(1, 1)

    abs_errors = [abs(e) for e in errors]
    smallest_error = min(abs_errors)
    point_index = abs_errors.index(smallest_error)

    errors_fig.suptitle("Error Development Across Simulation ")
    errors_ax.set_title(f"Smallest Error @ Point #{point_index + 1} ({(errors[point_index]):.3f}%)")
    errors_ax.set_xlabel("# Of Points Plotted")
    errors_ax.set_ylabel("Calculated Error (%)")

    errors_ax.plot(errors, color="red")
    errors_ax.set_yscale('symlog', linthresh=0.5)
    errors_ax.plot(np.zeros(shape=(points), dtype=np.float32), color="black", linestyle="dashed")

    if save_dir != None:
        errors_fig.savefig(f"{save_dir}/errors_{points}_sim.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--points", help="Set simulation points", default=500)
    parser.add_argument("-S", "--save", help="Save simulation plots", default=False)

    args = parser.parse_args()

    sim_points = 500
    save_plots = False
    save_dir = None

    if args.points:
        try:
            p = int(args.points)
        except:
            sys.exit("Error: Number of points must be an integer!")

        assert p != 0, "Number of points must be at least 1!"
        assert p > 0, "Number of points must be a positive integer!"

        sim_points = p

    if args.save:
        try:
            save_plots = bool(args.save)
        except:
            sys.exit("Error: Save parameter must be a boolean!")

    if save_plots:
        save_dir = f"./results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(save_dir, exist_ok=True)

    plt.ion()

    print(f"Running experiment using {sim_points} points...")

    final_estimation, calculated_erorrs = run_simulation(sim_points, save_dir)
    show_erorrs(sim_points, calculated_erorrs, save_dir)

    print(f"Final Estimated Pi Value: {final_estimation:.6f} ({'+' if (final_estimation > math.pi) else '-'}{abs(calculated_erorrs[-1]):.3f}%)")
    print("Press q to quit the simulation!")

    plt.waitforbuttonpress()
    plt.ioff()
    plt.close('all')
