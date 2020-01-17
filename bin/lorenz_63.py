import numpy as np
import sys
from ens_assim.measure.measure import Measure
from ens_assim.assimilate.assimilate import SREnKF
from ens_assim.model.model import Model, ODE, rk4
from ens_assim import perturb, calc_stats
import matplotlib.pyplot as plt

RHO = 28
BETA = 8/3
SIGMA = 10

data_std = np.array([1]) 
obs_dim = [1]
data_dim = len(obs_dim)
H = lambda x: x[obs_dim,:]
data_covariance = np.diag(data_std)@np.diag(data_std)

rhs = lambda t,x: np.array([SIGMA*(x[1,:]-x[0,:]),x[0,:]*(RHO-x[2,:]),x[0,:]*x[1,:]-BETA*x[2,:]])
x0 = np.array([[1.1],[1],[1]])
x_dim = len(x0)

initial_model_std = np.array([3,3,3])
model_std = np.array([1,1,1])

solver = rk4
solver_dict = {'h':.01}

num_steps = 1000
ens_num = 10
t0 = 0

model = ODE(x0)
measurement = Measure(covariance=data_covariance, operator=H)
assim_al = SREnKF()

model.set_solver(solver)
model.set_solver_dict(solver_dict)
model.set_num_steps(num_steps)
model.set_rhs(rhs)
model.set_t0(t0)

truth = np.squeeze(model.advance())
data = H(truth)

x_prior = np.tile(x0,(1,ens_num))
x_prior = perturb.absolute_uncorr_perturb(x_prior,initial_model_std)

x_assim = np.zeros((x_dim,ens_num,num_steps+1))
x_assim[:,:,0] = x_prior

x_mean = np.zeros((x_dim,num_steps+1))
x_std = np.zeros((x_dim,num_steps+1))

x_mean[:,0] = x0.flatten()
x_std[:,0] = initial_model_std

model.set_num_steps(1)

for steps in range(num_steps):
    print("step: ", steps)
    meas = perturb.absolute_uncorr_perturb(np.expand_dims(data[:,steps], axis=1),data_std)
    measurement.set_measurement(meas)
    x_post = assim_al.analyze(x_prior, measurement)
    x_assim[:,:,steps+1] = x_post
    model.set_initial_conditions(x_post)
    x_mean[:,steps+1] = calc_stats.get_mean(x_post).squeeze()
    x_std[:,steps+1] = calc_stats.get_std(x_post).squeeze()
    x_prior = model.advance().squeeze()
    x_prior = perturb.absolute_uncorr_perturb(x_prior,model_std)

#Plotting the results
t = np.array([t0 + solver_dict['h']*time for time in range(num_steps+1)])
x = x_mean[0,:]
y = x_mean[1,:]
z = x_mean[2,:]

x_err = x_std[0,:]
y_err = x_std[1,:]
z_err = x_std[2,:]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.suptitle('Plot of analyzed solution / truth with +/- 1 std error bar')
ax1.fill_between(t, x-x_err, x+x_err,facecolor='r',alpha=0.5)
ax1.plot(t, x, label='x_assim')
ax1.plot(t[1:], truth[0,:], label='x_truth')
ax1.legend()
ax1.set_title('t vs x')
ax2.fill_between(t, y-y_err, y+y_err,facecolor='r',alpha=0.5)
ax2.plot(t, y, label='y_assim')
ax2.plot(t[1:], truth[1,:], label='y_truth')
ax2.legend()
ax2.set_title('t vs y')
ax3.fill_between(t, z-z_err, z+z_err,facecolor='r',alpha=0.5)
ax3.plot(t, z, label='z_assim')
ax3.plot(t[1:], truth[2,:], label='z_truth')
ax3.set_title('t vs z')
ax3.legend()

plt.show()