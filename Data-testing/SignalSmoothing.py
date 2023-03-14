import matplotlib.pyplot as plt
import random

def smoothing(sig = [], sample=1) -> tuple:
    sig_length = len(sig)
    if sig_length <= 0 or sample < 1 or sample > sig_length:
        return ()
    new_sig = []
    for i in range(0, sig_length):
        total = 0
        for j in range(0, sample):
            pos = i-j
            if pos < 0 or pos > sig_length - 1:
                pass
            total += sig[pos]
        new_sig.append(total / sample)
    return tuple(new_sig)

def generate_random_data(len=10) -> list:
    data = []
    for i in range(0, len):
        data.append(random.randint(0,100))
    return data

def main():
    data = generate_random_data(100)
    smoothed_data = smoothing(data, 5)
    
    #Plotting
    
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    ax.plot(range(0,100), data, smoothed_data)
    plt.show()
        
    return

if __name__ == "__main__":
    main()

