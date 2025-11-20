# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "click",
#     "matplotlib",
#     "numpy",
#     "pywavelets",
# ]
# ///
import matplotlib.pyplot as plt
import numpy as np
import math
import click
import pywt
import os
import os.path


def add_rectangle(a, t1, t2, f1,f2,v):
    for row in range(t1,t2):
        for col in range(f1,f2):
            a[col][row] = v

def is_power_of_two(n:int) -> bool:
    nlog = round( math.log(n, 2) )
    return math.pow(2, nlog) == n

def plot_scalogram(ax:plt.Axes, v:list[float], abs_flag:bool)->None:
    """
    Expects a vector of Haar DWT coefficients
        (dc ; then low frequencies first)
    and plots the scalogram
    Caution: the image of scalogram is nxn patches - quadratic!
    :param v:  vector of length n = 2**L
    :return: nothing -plots the scalogram
    """
    n = len(v)
    L = round( math.log(n,2) ) # number of levels

    assert is_power_of_two(n), print(f'{n=} is not a power of 2 - exiting')
    # print(f'{v=}')
    scalogram_image = np.zeros( (n,n) )

    # plot the dc coefficient (father wavelet)
    t_offset = 0
    d_t = n
    f_offset = 0
    d_f = 1
    i = 0
    add_rectangle(scalogram_image, t_offset, t_offset + d_t, f_offset, f_offset + d_f, v[i])

    # now plot the diff coefficients (mother wavelet)
    f_offset = f_offset + d_f
    for level in range(1, L+1):
        # print(f'{level=} ------')
        t_offset = 0 # always start from t=0
        while t_offset < n:
            i = i+1 # next element of the vector 'v'
            add_rectangle(scalogram_image, t_offset, t_offset + d_t, f_offset, f_offset + d_f, v[i])
            # print(v[i], end=" ")
            t_offset = t_offset + d_t
        # print("")
        d_t = round(d_t / 2)
        f_offset = f_offset + d_f
        d_f = 2* d_f

    # plt.imshow(scalogram_image, cmap='jet')
    # plt.imshow(scalogram_image, cmap='Greys')
    # ax.imshow(scalogram_image, cmap='Blues', aspect='auto')
    vmax = max( [abs(i) for i in v] )
    if abs_flag:
        vmin = 0
        # cmap = 'Blues'
        # cmap = 'Reds'
        cmap = 'Greys'
        cmap = 'gist_yarg'
    else:
        vmin = - vmax
        cmap = 'seismic_r'
    # im = ax.imshow(scalogram_image, cmap='seismic', aspect='auto', vmin=vmin, vmax=vmax)
    im = ax.imshow(scalogram_image,
                   cmap=cmap,
                   aspect='auto',
                   # extent = [0,10,0,10], # didn't work - sigh!
                   vmin=vmin,
                   vmax=vmax)
    cb = plt.colorbar(im)
    cb.set_ticks( [vmin, 0, vmax])

    ax.set_xlabel('time')
    ax.set_ylabel('freq')
    # plt.title('DWT Haar scalogram')
    # plt.show()

def haar(s: list[float]) -> list[float]:
    """ expects a time sequence s of length n (power of 2)
    and returns the DWT coefficients
    """
    s = zero_pad(s)
    n = len(s)
    assert is_power_of_two(n)
    coeffs = pywt.wavedec(s, 'haar')
    return coeffs

def haar_and_plot(s: list[float],
                  wave_name: str = "blank",
                  abs_flag: bool = False,
                  print_flag: bool =False) ->None:
    """
    given a signal (list[float]) s
    plot its scalogram
    :param print_flag:
    :param s:           input signal
    :param wave_name:   signal name (for plt.title())
    :param abs_flag:    if true, plot abs values of Haar coefficients
    :return:            nothing - just plots
    """
    fig, axs = plt.subplots(2, 1)

    title=f'{wave_name}'
    if abs_flag:
        title = title+" (abs for Haar)"
    fig.suptitle(title)
    # plot the time sequence
    ax = axs[0]
    # ax.plot(s, 'b.')
    x = range(len(s))
    # ax.plot(s, 'b-', linewidth=0.1)
    # ax.bar(x, s, width=0.5)
    ax.stem(x,s, markerfmt="b.", basefmt="k-")
    ax.set_xlabel("time")

    # plot the scalogram
    coeffs = haar(s)
    dwt_haar = np.concatenate(coeffs).ravel()

    if abs_flag:
        dwt_haar = [ abs(x) for x in dwt_haar]
    ax = axs[1]
    plot_scalogram(ax, dwt_haar, abs_flag)

    plt.tight_layout()

    if print_flag:
        suffix = "_abs.png" if abs_flag else ".png"
        png_fname = wave_name + suffix
        plt.savefig(png_fname)

    plt.show()

def gen_spike(N:int) -> list[float]:
    """
    generates a spike: sequence of all zeros, of duration 'N',
    with a spike in the middle
    :param N:
    :return:
    """
    v = [0 for i in range(N)]
    half_point = round(N/2)
    v[half_point] = 1
    return v

def gen_prolonged_spike(N:int, s_start:int, s_width:int) -> list[float]:
    prolonged_spike = [0 for i in range(N)]
    assert s_start <= N
    assert s_start + s_width <= N
    for i in range( s_start, s_start+s_width):
        prolonged_spike[i] = 1
    return prolonged_spike

def gen_large_square_wave(N):
    half = round(N/2)
    large_square_wave = [0 for i in range(N)]
    for i in range(half):
        large_square_wave[i] = 1
    return large_square_wave

def gen_sine(N, f):
    '''
    returns a sine wave of frequency f and duration 'N'
    :param N:
    :param f:
    :return:
    '''
    sine_f= [ math.sin(2* math.pi * f *i / N ) for i in range(N)]
    return sine_f

def do_demo(abs_flag: bool, duration: int, print_flag:bool):
    if duration < 4:
        print(f'{duration=} should be >=4 - exiting')
        exit()

    if not is_power_of_two(duration):
        print(f'{duration=} should be power of 2 - exiting')
        exit()

    N = duration
    v = list(range(N))
    half = round(N / 2)

    single_spike = gen_spike(N)
    haar_and_plot(single_spike, "single_spike", abs_flag, print_flag)

    prolonged_spike = gen_prolonged_spike(N, half, math.floor(half/2))
    haar_and_plot(prolonged_spike, "prolonged_spike-aligned", abs_flag, print_flag)

    prolonged_spike = gen_prolonged_spike(N, half + 1, 10)
    haar_and_plot(prolonged_spike, "prolonged_spike-non-aligned", abs_flag, print_flag)

    large_square_wave = gen_large_square_wave(N)
    haar_and_plot(large_square_wave, "square_wave", abs_flag, print_flag)
    # need to make into functions, the ones below
    flip_flop_square_wave = [0 for i in v]
    for i in range(N):
        if i % 2 == 0:
            flip_flop_square_wave[i] = 1
    haar_and_plot(flip_flop_square_wave, "flip_flop", abs_flag, print_flag)

    zero_mean_flip_flop_square_wave = [-1 for i in v]
    for i in range(N):
        if i % 2 == 0:
            zero_mean_flip_flop_square_wave[i] = 1
        else:
            zero_mean_flip_flop_square_wave[i] = -1
    haar_and_plot(zero_mean_flip_flop_square_wave, "zero_mean_flip_flop", abs_flag, print_flag)
    # large_sine = [ math.sin(2* math.pi * i / N ) for i in v]

    slow_sine = gen_sine(N, 1)
    haar_and_plot(slow_sine, "slow_sine", abs_flag, print_flag)

    fast_sine = gen_sine(N, 4)
    haar_and_plot(fast_sine, "fast_sine", abs_flag, print_flag)

def zero_pad(s: list[float]) -> list[float]:
    duration = len(s)
    if is_power_of_two(duration):
        return s

    desired_len = int( math.pow(2, math.ceil( math.log(duration, 2))) )
    s_padded = [0 for i in range(desired_len)]
    for i in range(duration):
        s_padded[i] = s[i]
    return s_padded


def dwt_from_file(fname:str, abs_flag:bool, print_flag:bool) -> None:
    '''
    reads in the file fname (one number per line - no header)
    and plots the Haar scalogram
    :param fname:       input file name
    :param abs_flag:    plot abs() values, if true
    :param print_flag:    save to png file if true
    :return:
    '''

    # check for existing/readable filename
    if not os.path.isfile(fname):
        print(f'{fname=} does not exist - exiting')
        return

    if not os.access(fname, os.R_OK):
        print(f'{fname=} is unreadable - exiting')
        return

    with open (fname) as f:
        s = []
        for line in f:
            line = line.split()
            if line: # skip blank lines
                count = len(line)
                assert count == 1, print(f'should be 1 number per line not {count} - exiting')
                value = line[0]

                try:
                    num = float(value)
                except: #TypeError
                    print(f'{value=} in {fname=} should be a number - exiting')
                    exit()

                s.append(num)
        duration = len(s)
        if duration < 2:
            print(f'{duration=} < 2 - exiting')
            exit()
        s_padded = zero_pad(s)
        duration_padded = len(s_padded)
        assert is_power_of_two(duration_padded), print(f'{duration_padded=} is not power of 2')
        haar_and_plot(s_padded, fname, abs_flag, print_flag)

@click.command()
@click.option('-d', '--duration', default=64, help='length of generated sequence, if no filename given')
@click.option( '--abs_flag', '-a',  is_flag =True, help='give abs of haar coeff.')
@click.option( '-f', '--file_name', is_flag = False, default=None, help='file to process')
@click.option( '-v', '--verbose', is_flag = True, help='verbose')
@click.option( '-p', '--print_flag', is_flag = True, help='print to png')
def main(duration:int, abs_flag:bool , verbose:bool, file_name:str, print_flag:bool):
    if verbose:
        print(f'{duration=}')
        print(f'{abs_flag=}')
        print(f'{print_flag=}')
        print(f'{file_name=}')

    if file_name is None:
        # generating and plotting some demo waves: spike, etc
        do_demo(abs_flag, duration, print_flag)
    else:
        dwt_from_file(file_name, abs_flag, print_flag)

if __name__ == "__main__":
    main()
