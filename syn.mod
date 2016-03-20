TITLE Synaptic conductance for octopus neurons following Sperncer 2012's model

COMMENT

Note, gmax in micromho

ENDCOMMENT

NEURON {
    POINT_PROCESS syn
    RANGE gmax, e_rev, i, onset, taur, taud
    NONSPECIFIC_CURRENT i
}

UNITS {
    (mV) = (millivolt)
    (nA) = (nanoamp)
    (uS) = (micromho)
}

PARAMETER {
    taur = 0.07 (ms)
    taud = 0.34 (ms)
    
    gmax = 0.002 (uS)
    e_rev = 0.0 (mV)
    
    onset (ms) : must be def in hoc
    delay (ms) : must be def in hoc
}

ASSIGNED {
    i (nA)
    g (uS)
    v (mV)
}

BREAKPOINT {
    if (t > onset) {
	g = cond(t)
	i = g*(v - e_rev)
    }
}

FUNCTION cond(t (ms) ) (uS) {
   : LOCAL tmax, norm
    
    :tmax = (taud*taur/(taud - taur))*log(taud/taur)
    :norm = (exp((-(0.13931-onset))/taud) - exp((-(0.13931-onset))/taur))
    
    cond = gmax*(1/0.5272)*(exp((-(t-onset))/taud) - exp((-(t-onset))/taur))
    : 0.5272 is the max cond(t) (or cond(tmax))
    :cond = gmax*(1/norm)*(exp((-(t-onset))/taud) - exp((-(t-onset))/taur))
}

