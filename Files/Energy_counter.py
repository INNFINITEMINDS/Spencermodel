# TODO: во все компартменты добавить *все* токи, только ненужные токи "выключить",
#       выставив gbar=0


# Посчитатель энергии в равновесии: (а) Способом Moujahid et al., 2011,
#(б) Способом подсчета ионов Attwell & Laughlin 2001

# (а)

def net_section_currendenrg(section):
    "Sum up specific currents within section and return in nA"
    net_i = defaultdict(lambda: 0)
    "e_acc holds resting energies"
    e_acc = defaultdict(lambda: 0)
    Erevs = {'ina':h.initial.ena,
             'ik':h.soma.ek,
             'ih':h.soma.eh_hcno,
             'leak': h.soma.erev_leak
            }
    for seg in section:
        a = seg.area()*1e-8*1e6 # конвертируем площадь в см^2 и ток в nA заодно
        
        try: 
            net_i['ik'] += seg.ik*a # все К токи: Iklt, Ikht. nA
            e_acc['ik'] += seg.ik*a*(seg.v-Erevs['ik']) # nA*mV = pW = 1e-12*W = 1e-12*J/s
        except NameError: 
            print "Skipping iK"
    
        try: 
            net_i['ina'] += seg.ina*a 
            e_acc['ina'] += seg.ina*a*(seg.v-Erevs['ina'])
        except NameError: 
            print "Skipping iNa"
            
        try: 
            net_i['ih'] += seg.hcno.i*a 
            e_acc['ih'] += seg.hcno.i*a*(seg.v-Erevs['ih'])
        except NameError: 
            print "Skipping ih"
            
        try: 
            net_i['leak'] += seg.leak.i*a 
            e_acc['leak'] += seg.leak.i*a*(seg.v-Erevs['leak'])
        except NameError: 
            print "Skipping leak"  
    return net_i, e_acc

# (б)

def net_section_AtLau_enrg(section) :
    "Counts total resting energy consumption in ATP_moles/s (CHECK THIS in AL&Lau2001)"
    
    F = 96450 # Кл/млоь
    Rin = 6e9 # значение Rin из литературы (для крысы), Ом
    Fatp = 50*1e15 # энергия гидролиза АТФ в пДж/моль, по Moujahid et al., 2014 (п. 2.3)
    
#     Что делать с входным сопротивлением? По авторам формулы, Rin = 1/(gna+gk). 
#     Можно посчитать Rin в модели, но будет ли оно соответствовать формуле
#     Или: Какие брать значения gna, gk?
#     Вот, попробовал 6 МОм
  
    Erevs = {'ina':h.initial.ena,
             'ik':h.soma.ek,
             'ih':h.soma.eh_hcno,
             'leak': h.soma.erev_leak
            }
    for seg in section:
        J = ((Erevs['ina']-seg.v)*(seg.v-Erevs['ik']))/(F*Rin*(seg.v+2*Erevs['ina']-3*Erevs['ik']))
        # J в моль_АТФ/с
        
#     print  ("ATP_mol/s at rest --> %.3e" % (J))
#     print  ("ATPs/s at rest --> %.3e" % (J*6.02*1e23))
    return  ( "Energy in pJ/s %.6g" % (J*Fatp))