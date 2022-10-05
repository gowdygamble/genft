import matplotlib.pyplot as plt


EXPERIMENT_DIR

log_files = [
    'experiments/2022_10_04T16_04_35/train_loss.txt',
    'experiments/2022_10_04T21_32_29/train_loss.txt',

]

val_x = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190]
val_y =[
0.738,
0.294,
0.29,
0.279,
0.289,
0.327,
0.38,
0.433,
0.494,
0.544,
0.603,
0.584,
0.654,
0.64,
0.739,
0.69,
0.747,
0.718,
0.778,
0.736
]

plt.figure()

for lf in log_files:

    with open(lf, 'r') as f:
        z = f.readlines()

    losses = [float(x.split(',')[1]) for x in z]
    print(len(losses))
    plt.plot(losses)

plt.plot(val_x,val_y)

plt.show()
