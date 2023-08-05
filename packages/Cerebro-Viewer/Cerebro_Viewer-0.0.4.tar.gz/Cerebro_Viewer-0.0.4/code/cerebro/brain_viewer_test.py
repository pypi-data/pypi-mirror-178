import matplotlib.pyplot as plt

from . import cerebro_brain_viewer as cbv

my_brain_viewer = cbv.Cerebro_brain_viewer()

surface = 'midthickness_MSMAll'
left_surface_file = f'../data/templates/HCP/surfaces/S1200.L.{surface}.32k_fs_LR.surf.gii'
right_surface_file = f'../data/templates/HCP/surfaces/S1200.R.{surface}.32k_fs_LR.surf.gii'
surface_model = my_brain_viewer.load_GIFTI_cortical_surface_models(left_surface_file, right_surface_file)

cifti_template_file = f'../data/templates/HCP/dscalars/ones.dscalar.nii'
cifti_space = my_brain_viewer.visualize_CIFTI_space(surface_model['object_id'], cifti_template_file)

# stat = 'curvature'
stat = 'sulc'
dscalar_file = f'../data/templates/HCP/dscalars/S1200.{stat}_MSMAll.32k_fs_LR.dscalar.nii'
dscalar_layer = my_brain_viewer.add_CIFTI_dscalar_layer(cifti_space['object_id'], dscalar_file=dscalar_file)

dscalar_layer = my_brain_viewer.add_CIFTI_dscalar_layer(cifti_space['object_id'], dscalar_file=dscalar_file, colormap=plt.cm.jet, vlims=[0, 10])

my_brain_viewer.show()
