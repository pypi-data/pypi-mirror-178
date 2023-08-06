def bar_plot_pyplot(x, y):
    # x = iterable of length N, used for x axis. Any type
    # y = iterable of length N. Used for y axis. numeric type.
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,10))  # width, height in inches.
    plt.bar(x=x, height=y, align='center', )
    plt.title('hello')
    plt.xlabel('x_label')
    plt.ylabel('y_label')
    plt.show()
