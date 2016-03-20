TITLE Hyperpolarization-activated Ih after Spencer 2012

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
}


NEURON {
     SUFFIX hs
     NONSPECIFIC_CURRENT i
     RANGE ghbar, gh, ih
     GLOBAL hinf, htau
 }

PARAMETER {
    celsius (degC)
    treference = 33 (degC) : Spencer says, 33 degC for h-current (as in original  Oertel's code)
    eh = -38 (mV)
    ghbar = 0.0076 (mho/cm2) : For soma. For dends set ghbar_hs = 0.0006
    q10 = 4.5 : Other currents are corrected in temperature with q10 = 3 
}

STATE {
    h
}

ASSIGNED {
    v (mV)
    i (mA/cm2)
    gh (mho/cm2)
    hinf
    htau (ms)
    qt
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    gh = ghbar*h
    i = gh*(v-eh)
}
UNITSOFF
INITIAL {
    setrates(v)
    h = hinf
}

DERIVATIVE states {
    setrates(v)
    
    h' = qt*(hinf - h)/htau
}


PROCEDURE setrates(v) {: computes minf, hinf, mtau, htau at current v
    qt = q10^((celsius - treference)/10.0)
    
    hinf = 1 / ( 1 + exp((v+66)/7))
    htau = 125*exp(10.44*(v+50)/(273.16 + celsius)) / (1 + exp(34.81*(v+50)/(273.1+celsius)))
}
UNITSON