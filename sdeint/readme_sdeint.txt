To correctly use the sdeint package together with pycascades, it necessary to replace the file "wiener.py" from sdeint
by the "wiener.py" file in this folder. 

The only changes can be found in lines 52 and 53 for the inclusion of Lévy noise or Cauchy noise. To use Lévy noise, 
it is necessary to comment gaussian noise out and Lévy noise in. Accrodingly for Cauchy noise.


N.B.: Of course the SDEINT package must be installed (https://pypi.org/project/sdeint/)