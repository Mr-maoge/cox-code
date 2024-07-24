import time
import numpy as np

from Hyperparameter.v0_hyperparameter_selection import grid_search_hyperparameters_v0
from Hyperparameter.v1_hyperparameter_selection import grid_search_hyperparameters_v1
from comparison_method.no_tree_model import no_tree_model
from data_generation import generate_simulated_data
from evaluation_indicators import evaluate_coef_test
from main_ADMM import ADMM_optimize

'''
proposed method vs no tree
'''


# def run_admm():
start_time = time.time()
''' ==========   参数修改区   ============ '''
G = 11    # 类别数
tree_structure = "G11"
p = 100  # 变量维度
rho = 1
eta = 0.2

B_type = 1
Correlation_type = "Band1"      # X 的协方差形式

N_train = np.array([200]*G)
N_test = np.array([500]*G)
'''  ======================================  '''
results = {}
key = (B_type, Correlation_type)
results[key] = {}

train_data, test_data, B = generate_simulated_data(p, N_train, N_test,
                                                   B_type=B_type, Correlation_type=Correlation_type, seed=0)
X, Y, delta = train_data['X'], train_data['Y'], train_data['delta']

if False:
    parameter_ranges = {'lambda1': np.linspace(0.05, 0.3, 3),
                        'lambda2': np.linspace(0.05, 0.4, 4)}
    # 执行网格搜索
    lambda1_proposed, lambda2_proposed, B_proposed = grid_search_hyperparameters_v1(parameter_ranges, X, Y, delta,
                                                                                    tree_structure=tree_structure,
                                                                                    rho=rho, eta=eta,
                                                                                    method='proposed')
    lambda1_notree, B_notree = grid_search_hyperparameters_v0(parameter_ranges, X, Y, delta, rho=rho, eta=eta,
                                                              method='no_tree')
else:
    lambda1_proposed, lambda2_proposed = 0.3, 0.28
    lambda1_notree = 0.17
    B_notree = no_tree_model(X, Y, delta, lambda1=lambda1_notree, rho=rho, eta=eta)
    B_proposed = ADMM_optimize(X, Y, delta, lambda1=lambda1_proposed, lambda2=lambda2_proposed, rho=rho, eta=eta,
                               B_init=B_notree, tree_structure=tree_structure)

# Proposed method
results[key]['proposed'] = evaluate_coef_test(B_proposed, B, test_data)
# NO tree method
results[key]['notree'] = evaluate_coef_test(B_notree, B, test_data)

print(results)

# 计算运行时间
running_time = time.time() - start_time
print(f"running time: {running_time / 60:.2f} minutes ")


# if __name__ == "__main__":      # 并行计算
#     run_admm()


