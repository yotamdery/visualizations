import pandas as pd

## Load data
# Loading the data of the candidates before applying satisfy_constraints method
df_no_constraints = pd.read_csv('data/candidates_perf_login_no_constraints_with_objf.csv')
# Loading the data after applying satisfy_constraints method
df_after_constraints = pd.read_csv('data/candidates_perf_after_constraints_with_objf.csv')
# Loading data for Login limits (the limits are relative)
login_limits = pd.read_csv('data/login_limits.csv')