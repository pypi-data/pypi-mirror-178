from matplotlib.pyplot import figure, plot, legend, show

def plot_fourier(dfs, x: int = 50, y: int = 5):
    if not isinstance(dfs, list):
        dfs = [dfs]
        
    for df in dfs:
        figure(figsize = (x,y))
        plot(df.frequency, df.amplitude, label = "Waves")
        legend()

    show()