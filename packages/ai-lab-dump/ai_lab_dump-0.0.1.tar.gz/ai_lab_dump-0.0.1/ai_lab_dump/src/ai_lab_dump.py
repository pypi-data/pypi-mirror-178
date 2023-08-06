import requests
base_url = "https://raw.githubusercontent.com/JasbirCodeSpace/AI-Lab-Exercises-Dump/main/"
dirs = ["Missionaries%26Cannibals/bfs.py"
"Missionaries%26Cannibals/state_space_search.py",
"8Puzzle/astar.py",
"8Queens/hill_climbing.py",
"TSP/simulated_annealing.py",
"ZeroSum/alpha_beta_pruning.py",
"IDDFS/iddfs.py",
"WumpusWorld/wumpus_world.py",
"BlocksWorld_GoalStackPlanning/heuristic.py",
"AO_Graph/ao_star.py",
"BayesianClassification/naive_bayes.py",
"SupervisedLearning/decision_tree.py",
"SupervisedLearning/linear_regression.py",
"SupervisedLearning/k_means.py"]


def download_file(url, download_location):
    with open(download_location, 'wb') as out_file:
        content = requests.get(url, stream=True).content
        out_file.write(content)


def start():
    print("Enter download location: ")
    download_location = str(input())


    print("1. Missionaries and Cannibals (using bfs)")
    print("2. Missionaries and Cannibals (using state space search)")
    print("3. 8 Puzzle Problem (using bfs)")
    print("4. 8 Puzzle Problem (using A*)")
    print("5. 8 Queens Problem (using hill climbing)")
    print("6. TSP Problem (using simulated annealing)")
    print("7. Zero Sum Problem (using alpha beta pruning")
    print("8. Iterative Deepening Search (IDS or IDDFS)")
    print("9. Wumpus World Problem")
    print("10. Blocks World Problem (using goal stack planning)")
    print("11. AO* - And Or Graph")
    print("12. Naive Bayes Classification")
    print("13. Decision Tree")
    print("14. Linear Regression")
    print("15. K Means")

    choice = int(input("Enter choice: "))

    download_file(base_url + dirs[choice], download_location)