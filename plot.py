import math
import random
import pandas as pd
import plotnine

# kétkoordinátás pontokat generálunk
# a) mindkettő 1 és -1 közötti véletlen
# b) egy koordináta két 0 és 1 közötti véletlen összege, mínusz 1
# legyen 500 pont mindkét fajtából
# a) egyenletes eloszlású lesz a 2*2 oldalú négyzetben
# b) az elemszám növelésével az egységkörön belülre koncentrálódik
# becsüljük a pí értékét:
# az a) esetben az egységkörön belülre eső pontok száma úgy aránylik az összes pont számához,
# mint az egységkör területe (pí) az egész négyzetéez (4)
# a b) eset pontjai nem is kellenek??

X = "x"
Y = "y"
IS_IN_CIRCLE = "is_in_circle"


def get_random_uniform(lower, higher):
    range_length = abs(higher - lower)
    return random.random() * range_length + lower


def get_random_sum(lower, higher):
    range_length = abs(higher - lower)
    multiplier = range_length / 2
    random_1 = random.random() * multiplier
    random_2 = random.random() * multiplier
    result = random_1 + random_2 + lower
    return result


def generate_point_data(generator, lower, higher, radius):
    x = generator(lower, higher)
    y = generator(lower, higher)
    is_in_circle = math.hypot(x, y) < radius
    return {X: x, Y: y, IS_IN_CIRCLE: is_in_circle}


def generate_dataset(random_generator, lower, higher, radius, multiplicity):
    data = [generate_point_data(random_generator, lower, higher, radius) for i in range(multiplicity)]
    return pd.DataFrame(data)


def draw_scatterplot(dataset):
    plot = (plotnine.ggplot(dataset)
            + plotnine.aes(x=X, y=Y, color=IS_IN_CIRCLE)
            + plotnine.geom_point(size=0.01)
            + plotnine.coord_fixed())
    return plot


def create_data():
    number_of_points = math.ceil(1e6)
    lower = -1
    higher = 1
    radius = 1

    dataset_uniform = generate_dataset(get_random_uniform, lower, higher, radius, number_of_points)
    dataset_sum = generate_dataset(get_random_sum, lower, higher, radius, number_of_points)
    return dataset_uniform, dataset_sum


def main():
    dataset_uniform, dataset_sum = create_data()
    print("Datasets generated")

    rates = dataset_uniform[IS_IN_CIRCLE].value_counts(normalize=True)
    area = 4

    print(f"Rate of points in circle (uniform): \n{rates}")
    print(f"\nEstimation for pi: {area * rates[True]}\n")
    print(f"Rate of points in circle (sum): \n{dataset_sum[IS_IN_CIRCLE].value_counts(normalize=True)}")

    draw_scatterplot(dataset_uniform).save("egyenletes.png")
    draw_scatterplot(dataset_sum).save("koros.png")


if __name__ == '__main__':
    main()
