# Takes the name of the file with a current values in all 20 segments and time. Returns the total 
# number of unit charges that cross the membrane
def func( str ):
    global f
    q=0
    f = np.loadtxt(str, skiprows=2)
    print " f is the file", "*", str, "*", "now!"
    
    # Plot the most distal and proximal currents
    fig = plt.figure(figsize=(10,6))
    fig.suptitle('extra currents during dendritic activation', fontweight = 'bold', fontsize=14)
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top = 0.85)   

    ax.set_title(str)
    ax.set_xlabel('time, ms')
    ax.set_ylabel('current, mA/cm2')
    
    # Define graph max and min lims: max is calculated from the most distal segment 
    # (i.e. from 20th column), min -- from the most proximal (i.e. 1st column)   
    mi = np.amin(f[12000:18000,1])
    ma = np.amax(f[12000:18000,20])

    print ('***\n Plot y-axis lims are\n min       max\n %.3e %.3e' % (mi, ma))
    
    ax.axis([290, 500, mi, ma])

    ax.plot(f[:,0], f[:,1], 'g-', f[:,0], f[:,20], 'r--')
    ax.legend(('$Proximal$', '$Distal$'))
    
    # Now integrate currents in all segments. 
    for i in range(1, 21):
        
        # So q is sum of the total charges per unit area:       
        q += np.trapz(f[12000:18000,i], f[12000:18000,0])
        
    # S is single segment lateral area in cm2
    S = np.pi*3*(280/20)*1e-8
    print ('***\n Single segment lateral surface area (cm^2)*\n ---> %.3e' % S)
    e = 1.602e-19
    
    # qabs is the number of unit charges per dend_surface_area, S, per 4 dends 
    
    qabs = 4*q*1e-3*S/e
    print ('***\n The total number of extra unit_charges \n resulting from dendritic activation is*\n ---> %.3e' % (qabs))