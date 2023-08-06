from nudisxs import _nudisxs as xs
import numpy as np
import logging
log = logging.getLogger('disxs')
logformat='[%(name)20s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)
log.setLevel(logging.getLevelName("INFO"))
#logging.root.setLevel(logging.getLevelName("INFO")) # set global logging level

class disxs(object):
    def __init__(self):
        # init common block with default values. Can be changed explicitly
        #self.old_pdf_settings()
        log.info('initializing')
        self.init_masses()
        self.init_bend_factor()
        self.init_q2_min()
        self.init_abc()
        self.init_neutrino()
        self.init_pdf()
        self.init_target()
        self.init_structure_functions()
        self.init_r_function()
        self.init_final_hadron_mass()
        self.init_fl_function()
        self.init_qc()

    def init_masses(self):
        GeV = 1.0
        MeV = 1e-3*GeV
        self.m_e   = 0.51099892*MeV
        self.m_mu  = 105.658369*MeV
        self.m_tau = 1.77699*GeV
        self.m_n   = 0.93956536*GeV
        self.m_p   = 0.93827203*GeV

    def init_pdf(self,name='CT10nlo.LHgrid'):
        xs.initpdf(name)
        log.info(f'init_pdf with {name}')

    def init_neutrino(self,pdg=14):
        xs.n_nt.n_nt = np.sign(pdg)
        if np.abs(pdg) == 12:
            xs.m_lep.m_lep = self.m_e
        elif np.abs(pdg) == 14:
            xs.m_lep.m_lep = self.m_mu
        elif np.abs(pdg) == 16:
            xs.m_lep.m_lep = self.m_tau
        else:
            log.error('unknown pdg',pdg)
        xs.m_lep.mm_lep = xs.m_lep.m_lep**2
        log.info(f'init_neutrino with pdg={pdg}')

    def init_target(self,target='proton'):
        if target == 'proton':
            xs.n_tt.n_tt = 1
            xs.m_ini.m_ini = self.m_p
            xs.m_ini.mm_ini = self.m_p**2
        elif target == 'neutron':
            xs.n_tt.n_tt = 2
            xs.m_ini.m_ini = self.m_n
            xs.m_ini.mm_ini = self.m_n**2
        else:
            log.error(f'init_target. Unknown target={target}')
        log.info(f'init_target {target}')

    def init_structure_functions(self,model=1):
         xs.n_ag_dis.n_ag_dis = model
         log.info(f'init_structure_functions model={model}')

    def init_r_function(self,model=2,modification=1):
        xs.n_rt_dis.n_rt_dis = model
        xs.n_rc_dis.n_rc_dis = modification
        log.info(f'init_r_function model={model}, modification={modification}')

    def init_final_hadron_mass(self,m=1.2):
        xs.m_fin.m_fin = m
        xs.m_fin.mm_fin = xs.m_fin.m_fin**2
        log.info(f'init_final_hadron_mass={m} GeV')

    def init_fl_function(self,model=2):
        xs.n_fl_dis.n_fl_dis = model
        log.info(f'init_fl_function model={model}')

    def init_qc(self,model=0):
        xs.n_qc_dis.n_qc_dis = model
        log.info(f'init_qc model={model}')

    def init_bend_factor(self, f=1.0):
        xs.n_bf_dis.n_bf_dis = f
        log.info(f'init_bend_factor={f:6.3E}')

    def init_q2_min(self,q2_min=1.):
        xs.q2_dis.q2_dis = q2_min
        log.info(f'init_q2_min={q2_min:6.3E}')

    def init_abc(self,a=0.0,b=0.0,c=0.0):
        xs.a0_dis.a0_dis =  a
        xs.b0_dis.b0_dis =  b
        xs.c0_dis.c0_dis =  c
        log.info(f'init_abc parameters=({a:6.3E},{b:6.3E},{c:6.3E})')

    def xs_cc(self,Enu,x,y):
        return xs.d2sdiscc_dxdy(Enu,x,y)

    def xs_cc_as_array(self,enu,x,y):
        results = np.zeros(shape=(enu.shape[0],y.shape[0],x.shape[0]),dtype=float)
        for ie, ee in enumerate(enu):
            for iy, yy in enumerate(y):
                for ix, xx in enumerate(x):
                    results[ie,iy,ix] = xs.d2sdiscc_dxdy(ee,xx,yy)
        return results
