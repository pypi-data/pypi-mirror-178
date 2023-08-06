import math
import numpy
import matplotlib.pyplot as plt
import control


def damping_ratio_from_os(overshoot_percent):
    """Calculates damping ratio from overshoot percentage.
    
    Divides overshoot percentage by 100 and computes damping ratio.
    
    Parameters
    ----------
    overshoot_percent : int or float
        percentage in integer or floating point value.
        
    Returns
    -------
    float
        damping ratio for a second order or higher order system approximated as second order.
        
    Examples
    --------
    >>> damping_ratio_from_os(25)
    """
    os = overshoot_percent
    damp_ratio=-math.log(os/100)/(math.pi**2+math.log(os/100)**2)**0.5
    
    return round(damp_ratio,3)


def order_tf(G):
    """Gives order of transfer function.
    
    Computes order from control transfer function object numerator and denominator.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package transfer function object.
        
    Returns
    -------
    int
        order of control transfer function object, representing highest power of 's'.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 4])
    >>> order_tf(G)
    """
    num_power=len(G.num[0][0])-1
    den_power=len(G.den[0][0])-1
    
    return max(num_power, den_power)


def stability_gain_range(G, initial_gain=0.01, final_gain=2000):
    """Gives upper limit of gain for stability from forward-path transfer function.
    
    Takes forward-path transfer function without gain variable 'K' and returns the upper limit K_upper,
    where system is stable for 0 < K < K_upper.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package forward-path transfer function object.
        
    intial_gain: float
        start from intial value of gain (default=2000).
        
    final_gain: float
        stop at final value of gain (default=2000).
        
    Returns
    -------
    float
        returns gain upper limit K_upper.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 0])
    >>> stability_gain_range(G)
    """
    
    l_num = len(G.num[0][0])
    l_den = len(G.den[0][0])
    
    poly_num = numpy.copy(G.num[0][0])
    poly_num_total = numpy.copy(G.num[0][0])
    poly_den = numpy.copy(G.den[0][0])
    poly_den_total = numpy.copy(G.den[0][0])
    
    poly_num = poly_num.astype(float)
    poly_num_total = poly_num_total.astype(float)
    poly_den = poly_den.astype(float)
    poly_den_total = poly_den_total.astype(float)

    for K in numpy.arange(initial_gain,final_gain+0.01,0.01):
    
        if l_den >= l_num:
            poly_den_total[-l_num:] = poly_den[-l_num:] + K*poly_num
            r = numpy.roots(poly_den_total).real
        elif l_num > l_den:
            poly_num_total[-l_den:] = poly_num[-l_den:] + K*poly_den
            r = numpy.roots(poly_num_total).real

        if max(r) >= 0:
            break
    if K >= (2000):
        print("System is stable for all values of gain till 2000.")
        
    return round(K,3)




def intersection_point_poles(radial_distance, damp_ratio):
    """Gives complex coordinates for a given point in radial distance on damping ratio line.
    
    Computes complex coordinates (used for poles) from the radial distance r from origin on a damping ratio 
    line on a root locus graph (complex plane).
    
    Parameters
    ----------
    radial_distance : int or float
        radial distance on damping ratio line from origin on complex plane.
        
    Returns
    -------
    complex
        complex coordinates (used for poles) at the radial distance.
        
    Examples
    --------
    >>> intersection_point_poles(2, 0.8)
    """
    r = radial_distance
    theta = math.pi - math.acos(damp_ratio)
    
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    
    z1 = complex(round(x,2), round(y,2))
    z2 = complex(round(x,2), round(-y,2))
    
    return [z1, z2]


def intersection_point_gain(G, point):
    """Computes the value of gain for a pole location represented by a complex number or point.
    
    Computes the gain from the transfer function, for the pole locations (used for poles at intersection 
    points of root locus and damping ratio line). The coordinates for poles are used to determine gain from.
    Takes the first pole if its a list of poles.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package forward-path transfer function object.
    point: complex
        complex coordinates for a pole.
        
    Returns
    -------
    float
        gain of a pole location.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 4])
    >>> intersection_point_gain(G, 5+3j)
    """
    
    if type(point)==list:
        point = point[0]
    magn =abs(G.horner(point))
    
    return round(numpy.ndarray.item(1/magn),2)



def find_rlocus(G, damp_ratio, r_final=0, r_init=0):
    """Finds the intersection points of root locus and damping ratio line'
    
    Computes the intersection points/poles where a root locus intersects the damping ratio line
    and provides the coordinates for poles and the respective gains at those points on the root locus.

    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package forward-path transfer function object.
    
    damp_ratio: int or float
        damping ratio value
    
    r_init: int or float
        starting point on radial line for finding intersection points/poles. Default value is 0.
        
    r_final: int or float
        final point on radial line for finding intersection points/poles. Function estimates value itself,
        if default value is left at 0. Otherwise, input a value to be used greater than 0.
        
    Returns
    -------
    poles: list of complex numbers
        list of complex numbers corresponding to poles.
    gain: list of floats
        list of floats corresponding to gain values at the poles.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 4])
    >>> find_rlocus(G, 0.8)
    >>> find_rlocus(G, 0.8, 20)
    >>> find_rlocus(G, 0.8, 30, 10)
    """
    zeta = damp_ratio
    if order_tf(G) < 2:
        print('Please input transfer function of 2nd order or higher')
        return -1, -1
    
    
    
    r=r_init
    #print(r)
    if r < 10**-5:
        r += 10**-5
    
    k_deg = 180/math.pi
    theta = math.pi - math.acos(zeta)
    #print('theta: ', theta*k_deg)
    # estimate upper limit on r
    
    if r_final == 0:
        x_max = max(abs(G.poles()))
        r_final = abs(x_max/math.cos(theta))
    
    
    poles = G.poles()
    zeros = G.zeros()
    
    n = len(poles)+len(zeros)
    all_poles =[]
    all_gains=[]
    power = -3
    prev = 0
    while r < r_final:
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        sum = 0
        for p in poles:
            p = math.atan(y/(x-p.real))
            if p < 0:
                p = math.pi+p
            #print('poles: ',p*k_deg)
            sum += p
            
        for z in zeros:
            z = math.atan(y/(x-z.real))
            #print('y: ',y)
            #print('x - z.real: ', x-z.real)
            if z < 0:
                z = math.pi+z
            #print('zeros: ',z*k_deg)
            sum -= z
        #print(sum*k_deg)
        #print('r: ',r)
        #print('------------------')
        
        for k in range(0, (n//2)+1):
            if abs(abs(sum*k_deg)- (2*k+1)*180) < 10**(power+1):
                intersect_poles = intersection_point_poles(r, zeta)
                intersect_gain = intersection_point_gain(G, intersect_poles)
                if intersect_poles not in all_poles:
                    all_poles.append(intersect_poles)
                    all_gains.append(intersect_gain)
                            
        r += 10**power
    if len(all_poles) != 0:
        return all_poles, all_gains
    else:
        print('not found')
        return -1, -1


def settling_time(pole):
    """Computes the settling time from a pole from conjugate pair.
    
    Computes the settling time from a single pole of conjugate pair or dominant pole of higher order
    system using second order approximation.
    
    Parameters
    ----------
    pole : complex
        pole value as complex number.
        
    Returns
    -------
    float
        settling time of a second order system/approximation.
        
    Examples
    --------
    >>> settling_time(-2+3j)
    """

    T_s = 4 / abs(pole.real)
    
    return round(T_s,2)



def peak_time(pole):
    """Computes the peak time from the pole value.
    
    Computes the peak time from a single pole of conjugate pair or dominant pole of higher order
    system using second order approximation.
    
    Parameters
    ----------
    pole : complex
        pole value as complex number.
        
    Returns
    -------
    float
        peak time of a second order system/approximation.
        
    Examples
    --------
    >>> peak_time(-2+3j)
    """

    T_p = math.pi / abs(pole.imag)
    
    return round(T_p, 2)



def natural_frequency_from_pole(pole):
    """Computes natural frequency from the pole value.
    
    Computes natural frequency from a single pole of conjugate pair or dominant pole of higher order
    system using second order approximation.
    
    Parameters
    ----------
    pole : complex
        pole value as complex number.
        
    Returns
    -------
    float
        natural frequency of a second order system/approximation.
        
    Examples
    --------
    >>> natural_frequency_from_pole(-2+3j)
    """
    
    w_n = math.sqrt(pole.real**2 + pole.imag**2)
    
    return round(w_n, 2)


def natural_frequency_from_ts(ts, damp_ratio):
    """Computes natural frequency from the settling time.
    
    Computes natural frequency from the settling time of second order or higher order
    system using second order approximation.
    
    Parameters
    ----------
    ts : float
        settling time.
        
    damp_ratio: float
        damping ratio
        
    Returns
    -------
    float
        natural frequency of a second order system/approximation.
        
    Examples
    --------
    >>> natural_frequency_from_ts(1.11, 0.8)
    """
    
    w_n = 4 / (ts * damp_ratio)
    
    return round(w_n, 2)

    
def unity_feedback(G, H=1):
    """Convert forward transfer function to closed loop unity feedback.
    
    Computes natural frequency from a single pole of conjugate pair or dominant pole of higher order
    system using second order approximation.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package transfer function object.
    H:  control.xferfcn.TransferFunction
        control package transfer function object.
    Returns
    -------
    control.xferfcn.TransferFunction object
        control package transfer function object with unity feedback.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 0])
    >>> unity_feedback(G)
    """
    
    T = control.feedback(G, H)
    return T


def compensated_pole_from_ts(new_ts, damp_ratio):
    
    """Get desired pole values from required settling time.
    
    Computes pair of conjugate pole pair from the required settling time values.
    
    Parameters
    ----------
    new_ts : float
        desired settling time.
        
    damp_ratio:  float
        damping ratio.
        
    Returns
    -------
    list of complex numbers
        complex conjugate poles as a list.
        
    Examples
    --------
    >>> compensated_pole_from_ts(1.1, 0.5)
    """
    
    W_n = 4 / (new_ts * damp_ratio)
    
    new_pole1=complex(round(-damp_ratio * W_n,2) , round(W_n * math.sqrt(1-damp_ratio**2),2));
    new_pole2=complex(round(-damp_ratio * W_n,2) , round(-W_n * math.sqrt(1-damp_ratio**2),2));
    
    return [new_pole1, new_pole2]



def velocity_constant(G, gain):
    """Computes the velocity constant and steady state error.
    
    Computes velocity constant from lim s->0 s*G(s) (as t-> inf) and the corresponding steady state error.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package transfer function object.
    gain:  float
        value of gain.
    Returns
    -------
    float, float
        velocity constant and error.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 0])
    >>> velocity_constant(G, 0.8)
    """
    
    sG = s * G
    
    sG = sG.minreal()*gain
    Kv = sG.dcgain()
    error = 1/Kv
    
    return Kv, error


def zero_compensator_tf(desired_poles, G):
    """Computes value of compensating zero for PD controller.
    
    Computes compensating zero from the desired pole value and given transfer function and returns 
    the new numerator s polynomial for a zero.
    
    Parameters
    ----------
    desired_poles: complex
        desired pole as a complex number.
        
    G : control.xferfcn.TransferFunction
        control package transfer function object.
        
    Returns
    -------
    s + zero: control transfer function object one numerator term
        numerator term for transfer function.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 0])
    >>> zero_compensator_tf(-2.2+3.1j, G)
    """
    
    k_deg = 180/math.pi
    
    angle_desired_pole = numpy.angle(G.horner(desired_poles)[0][0][0])*k_deg
    
    angle_PD = 180 - angle_desired_pole
    
    y_zero = desired_poles[0].imag
    theta = angle_PD / k_deg
    x_zero = (y_zero/math.tan(theta)) - desired_poles[0].real
    
    s = control.TransferFunction.s
    
    return s + x_zero

def find_poles_zeros_at_gain(G, gain):
    """Computes values for poles and zeros from transfer function.
    
    Computes poles and zeros from transfer function at particular value of gain.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package transfer function object.
    gain:  float
        value of gain.
    Returns
    -------
    numpy array, numpy array
        numpy arrays for poles and zeros.
        
    Examples
    --------
    >>> find_poles_zeros_at_gain(G, gain)
    """
    
    G_closed = control.feedback(gain*G)
    
    den = G_closed.den
    den_poly = den[0][0]
    
    num = G_closed.num
    num_poly = num[0][0]
    
    poles = numpy.roots(den_poly)
    zeros = numpy.roots(num_poly)
    
    return poles, zeros

def draw_overlay_rlocus(G, damp_ratio, r_final=0):
    """Draws root locus graph, overlays damping ratio lines and, marks and returns intersection poles.
    
    Draws root locus graph and radial damping ratio lines on it. Finds the intersection of lines for 
    root locus and damping ratio lines. Marks the intersection poles on graph and also returns the intersection
    pole values. Default value of radial distance on the damping ratio radial line is zero and allows the program 
    to use its own estimate for final value to search for intersection. If pole not found then a desired 
    r_final value could be used but will increase the computation time.
    
    Parameters
    ----------
    G : control.xferfcn.TransferFunction
        control package transfer function object.
        
    damp_ratio:  float
        damping ratio.
        
    r_final: float
        estimate of final radial distance on damping ratio line (default is 0, 
        do not change unless intersection exists and not found)
        
    Returns
    -------
    poles: list of type complex
        poles as a list of complex numbers.
        
    Examples
    --------
    >>> G = control.tf([1],[1, 10, 24, 0])
    >>> damp_ratio = 0.5
    >>> draw_overlay_rlocus(G, damp_ratio)
    """
    
    if order_tf(G) < 2:
        print('Please input transfer function of 2nd order or higher')
        return -1

    value = control.rlocus(G)
    
    # estimate final value for plotting radial line for damping ratio
    max_val = numpy.absolute(value[0]).max()
    x_max = max(abs(G.poles()))
    final = int((x_max+1) * max_val)
    
    # angle of damping ratio radial line
    theta =  math.pi - math.acos(damp_ratio)

    # get x and y coordinates for damping ratio line
    x = []
    y_pos = []
    y_neg = []
    for r in range(0,final, 1):
    
        x += [r * math.cos(theta)]
        y = r * math.sin(theta)
        y_pos += [y]
        y_neg += [-y]
        
    
    # find intersection poles for rlocus and damping ratio lines
    # where r_final provides estimate for final value of r, can one's own value
    if r_final == 0:
        r_final = abs(x_max/math.cos(theta))
    poles, _ = find_rlocus(G, damp_ratio, r_final)
    
    if poles == -1:
        print("Intersection of damping ratio line with root locus not found.")

    # plot damping ratio lines with x and y coordinates obtained above
    plt.plot(x, y_pos, linestyle='dashed', color='black', alpha=0.6) #marker='o', markerfacecolor='blue'
    plt.plot(x, y_neg, linestyle='dashed', color='black', alpha=0.6)
    
    # iterate though all the pairs and poles if they exist
    if poles != -1:
        for pair in poles:
            for p in pair:
                plt.plot(p.real, p.imag, 'rx', markersize=7,alpha=1) #

    return poles

