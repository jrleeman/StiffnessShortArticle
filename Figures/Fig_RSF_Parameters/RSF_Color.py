import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from biaxread import *
from scipy.signal import medfilt

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

# Path to folders of biax data
data_path = '/Users/jleeman/Dropbox/PennState/BiaxExperiments'
#p4309 = ReadAscii(data_path + '/p4309/p4309_data.txt')
#p4309 = p4309[211642:220000]
#p4309 = p4309[95564:99876]

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

df = pd.read_excel('p4309_rsf_fits.xlsx')

data = df[df['Law']=='r']
data = data[data['k']==0.0055]
data =  data.query('Grade == ["A","B"]')

# Setup figure and axes
# Generally plots is ~1.33x width to height (10,7.5 or 12,9)
fig = plt.figure(figsize=(17,12))
ax1 = fig.add_subplot(1, 1, 1)


plt.subplots_adjust(wspace=0.3)
#fig.subplots_adjust(hspace=0.1, wspace=0.35)

#
# Velocity Step Plot
#

# Set labels and tick sizes
ax1.set_xlabel(r'Displacement [$\mu m$]',fontsize=36)
ax1.set_ylabel(r'Friction',fontsize=36)
ax1.tick_params(axis='both', which='major', labelsize=28)

# Turns off chart clutter

# Turn off top and right tick marks
# ax1.get_xaxis().tick_bottom()
# ax1.get_yaxis().tick_left()

# Turn off top and right splines
# ax1.spines["top"].set_visible(False)
# ax1.spines["right"].set_visible(False)

#ax1.plot(p4309['LP_Disp'] - p4309['LP_Disp'][0],savitzky_golay(np.ravel(p4309['mu']),201,5),color='k',linewidth=1,
#        label='p4309')

p4309 = np.loadtxt('step_35_model.txt',skiprows=5,usecols=[1,8,10])

p4309_mu_downsampled = p4309[:,1][7:]
p4309_mu_downsampled = p4309_mu_downsampled.reshape((60,10))
p4309_mu_downsampled = np.mean(p4309_mu_downsampled,axis=1)

p4309_disp_downsampled = p4309[:,0]-p4309[0,0]
p4309_disp_downsampled = p4309_disp_downsampled[7:].reshape((60,10))
p4309_disp_downsampled = np.mean(p4309_disp_downsampled,axis=1)

# row 215 to end for high velocity, 0-19 for red
ax1.scatter(p4309[215:,0]-p4309[0,0],p4309[215:,1],color=tableau20[6],s=60, label='p4309 Data')
ax1.scatter(p4309_disp_downsampled[0:19], p4309_mu_downsampled[0:19], color=tableau20[6],s=60, label='p4309 Data')
ax1.plot(p4309[:,0]-p4309[0,0],p4309[:,2],color='k',linewidth=3, label='p4309 Model')


ax1.set_ylim(0.680,0.71)
ax1.set_xlim(0,140)

plt.savefig('RSF_Color.png', bbox_inches="tight")
#plt.show()