import pickle
import matplotlib.pyplot as plt


if __name__=="__main__":
    with open("imgep_with_homemade_mutation_operator/dict/imgep.pickle","rb") as f:
        imgep = pickle.load(f)
    with open("random_exploration/dict/randomexploration.pickle","rb") as f:
        random_exploration = pickle.load(f)
    N_init = 100
    N = 1000
    plt.figure(figsize=(10,8))
    plt.scatter(imgep["core2_exec_time"],imgep["core1_exec_time"], label="imgep")
    plt.scatter(random_exploration["core2_exec_time"],random_exploration["core1_exec_time"], label="random exploration")
    plt.ylabel("execution time core 1")
    plt.xlabel("execution time core 2")
    plt.title(f"Imgep with experimental budget N={N} and Ninit = {N_init} VS Random exploration with N={N}")
    plt.legend()
    plt.savefig("image/comparaison")
    plt.show()

