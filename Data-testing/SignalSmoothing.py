import matplotlib as mp

def smoothing(sig = [], sample=1) -> tuple:
    sig_length = len(sig)
    if sig_length <= 0 or sample < 1 or sample > sig_length:
        return ()
    new_sig = []
    for i in range(0, sig_length):
        total = 0
        for j in range(0, sample):
            pos = i-j
            if pos < 0:
                pass
            total += sig[pos]
        new_sig[i] = total / sample
    return tuple(new_sig)

def main():
    
    return

if __name__ == "__main__":
    main()

