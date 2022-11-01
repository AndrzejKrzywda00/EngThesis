import matplotlib.pyplot as plt

if __name__ == '__main__':
    ys = [8.12, 5.57, 4.62, 3.94, 3.53, 3.16, 2.96, 2.79, 2.46]
    xs = [100, 200, 300, 400, 500, 600, 700, 800, 1000]

    figure, axis = plt.subplots()
    axis.set_title('Average delivery time of packet \n depending on number of nanobots operating in bloodstream')
    axis.set_xlabel('Number of nanobots')
    axis.set_ylabel('Average delivery time [h]')
    axis.stem(xs, ys, use_line_collection=True)
    plt.show()
