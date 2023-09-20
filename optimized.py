import time
import pandas as pd
import itertools as it


# fonction pour calcule le temps d'execution
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print(f"{method.__name__} : {te-ts:.3f} sec")
        return result

    return timed

# Function to read and rename columns
def read_data(filepath):
    data = pd.read_csv(filepath)
    data = data.rename(
        columns={
            "Actions #": "name",
            "Coût par action (en euros)": "price",
            "Bénéfice (après 2 ans)": "profit",
        }
    )
    return data

# Function to format profit
def format_profit(x):
    if isinstance(x, str):
        return x.replace("%", "")
    return x

# Function to clean the dataset
def clean_dataset(data):
    # Clean the 'profit' column
    data["profit"] = data["profit"].apply(format_profit)
    data["profit"] = data["profit"].apply(lambda x: float(x) / 100)

    # Clean the 'price' column
    data["price"] = data["price"].apply(lambda x: float(x))

    # Filter rows with positive prices
    data = data[data["price"] > 0]

    return data


@timeit
def load_and_clean_dataset(filepath):
    data = read_data(filepath)
    data = clean_dataset(data)
    return data


# Classe pour représenter une action
class Action:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = price
        self.profit = profit

    def __lt__(self, other_action):
        return self.profit < other_action.profit

    def __repr__(self):
        return f"{self.name} (Price: {self.price}€, Return: {self.profit * 100:.2f}%)"


def convert_dataframe_to_action_list(data):
    actions = []
    for action in data.itertuples():
        actions.append(Action(action.name, action.price, action.profit))
    return actions


# Fonction pour résoudre le problème en utilisant une approche gloutonne
@timeit
def solve_greedy(actions, budget_max):
    # Triez les actions en fonction du ROI décroissant
    # actions.sort(key=calculate_roi, reverse=True)
    actions.sort(reverse=True)

    selected_actions = []
    total_cost = 0
    total_profit = 0

    for action in actions:
        if total_cost + action.price <= budget_max:
            selected_actions.append(action)
            total_cost += action.price
            total_profit += action.profit * action.price

    return selected_actions, total_profit


# Fonction pour afficher les actions sélectionnées et le profit total
def display_selected_actions(selected_actions, total_profit):
    if len(selected_actions) > 0:
        print("\nActions sélectionnées :")
        for action in selected_actions:
            print("*", action)
        
        print(f"\nNombre d'actions sélectionnées : {len(selected_actions)}")
        print(f"\tGain total  : {total_profit:.1f} euros")
        selection_total_cost = sum(action.price for action in selected_actions)
        print(f"\tCoût total de la sélection : {selection_total_cost :.1f} euros")

        print(f"\tROI total de la sélection : {(total_profit / selection_total_cost) * 100 :.2f}%")
    else:
        print("Aucune action sélectionnée. Le budget est trop faible.")


# Programme principal

def main():
    filename = "./data/dataset1.csv"  # Le chemin vers le fichier de données
    budget_max = 500  # Le budget maximum disponible

    # Charger et nettoyer le jeu de données à partir du fichier CSV
    data = load_and_clean_dataset(filename)

    # Convertir le DataFrame en une liste d'objets Action
    actions = convert_dataframe_to_action_list(data)

    # Résoudre le problème de sélection d'actions en utilisant  l'approche gloutonne
    selected_actions, total_profit = solve_greedy(actions, budget_max)

    # Affichage des actions sélectionnées et le profit total
    display_selected_actions(selected_actions, total_profit)


# Appel de la fonction principale
if __name__ == "__main__":
    main()


