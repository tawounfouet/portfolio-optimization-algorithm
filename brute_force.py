import time
import pandas as pd
import itertools as it


# fonction pour calcule le temps d'execution
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print(f"{method.__name__} : {te-ts:.2f} sec")
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


# Faire une petite classe pour stocker les données d'une action
class Action:
    def __init__(self, name, price, profit):
        self.name = name
        self.price = price
        self.profit = profit

    def __repr__(self):
        return (
            f"{self.name} (Price : {self.price} €, Return : {self.profit * 100:.0f}%)"
        )


def convert_dataframe_to_action_list(data):
    actions = []
    for action in data.itertuples():
        actions.append(Action(action.name, action.price, action.profit))
    return actions


# Fonction pour générer toutes les combinaisons possibles d'actions
@timeit
def generer_combinaisons(actions, budget_max):
    best_combinations = []
    total_combinations = 0
    best_gain = 0  # gain = price * profit

    # Boucle pour générer toutes les combinaisons
    for r in range(1, len(actions) + 1):
        for combination in it.combinations(actions, r):
            total_cost_combination = sum(
                action.price for action in combination
            )  # cout total de la combinaison
            total_combinations += 1

            # Vérifie si la combinaison respecte les contraintes de budget
            if (
                total_cost_combination <= budget_max
            ):  # combinaison_gains = sum(action.profit * action.price for action in combinaison)
                all_combinations_gain = sum(
                    action.profit * action.price for action in combination
                )
                if all_combinations_gain > best_gain:
                    best_combinations = [combination]
                    best_gain = all_combinations_gain
                elif all_combinations_gain == best_gain:
                    best_combinations.append(combination)

    return best_combinations, total_combinations, best_gain


# Fonction pour affichage de la meilleure combinaison
def afficher_meilleure_combinaison(best_combinations, total_combinations, best_gain):
    if len(best_combinations) > 0:
        print("Meilleure combinaison d'actions :")
        for action in best_combinations[0]:
            print("*", action)
        print(f"\nGain total de l'investissement  : {best_gain:.1f} euros")
        # Nombre total d'actions dans la combinaison
        print(
            f"\tNombre total d'actions dans la combinaison : {len(best_combinations[0])}"
        )

        # Coût total de la combinaison
        total_cost_combination = sum(action.price for action in best_combinations[0])
        print(
            f"\tCoût total investit dans la combinaison : {total_cost_combination} euros"
        )

        # Rentabilité de la combinaison (Profitabilité)
        profitability = (best_gain / total_cost_combination) * 100
        print(f"\tRentabilité de la combinaison : {profitability:.1f}%")

        print("\nNombre total de combinaisons générées :", total_combinations)
    else:
        print("Aucune combinaison possible respectant les contraintes de budget.")


def main():
    # Chemin du fichier CSV et budget maximal
    filepath = "./data/dataset.csv"
    budget_max = 500

    # Chargement et nettoyage des données
    data = load_and_clean_dataset(filepath)

    # Conversion des données en liste d'actions
    actions = convert_dataframe_to_action_list(data)

    # Génération des combinaisons optimales
    (best_combinations, total_combinations, best_gain) = generer_combinaisons(
        actions, budget_max
    )

    # Affichage de la meilleure combinaison et de ses statistiques
    afficher_meilleure_combinaison(best_combinations, total_combinations, best_gain)


# Lancer le programme
if __name__ == "__main__":
    main()
