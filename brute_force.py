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


def read_data(filename):
    data = pd.read_csv(filename)
    return data


def clean_data(data):
    data = data.rename(
        columns={
            "Actions #": "name",
            "Coût par action (en euros)": "cost",
            "Bénéfice (après 2 ans)": "profit",
        }
    )
    data["profit"] = data["profit"].apply(lambda x: float(x.strip("%")) / 100)
    return data


@timeit
def read_and_format_data(filename):
    data = read_data(filename)
    data = clean_data(data)
    return data


# Faire une petite classe pour stocker les données d'une action
class Action:
    def __init__(self, name, cost, profit):
        self.name = name
        self.cost = cost
        self.profit = profit

    def __repr__(self):
        return f"{self.name} (Coût : {self.cost} euros, Bénéfice : {self.profit * 100:.0f}%)"


def convert_dataframe_to_action_list(data):
    actions = []
    for action in data.itertuples():
        actions.append(Action(action.name, action.cost, action.profit))
    return actions


# Fonction pour générer toutes les combinaisons possibles d'actions
@timeit
def generer_combinaisons(actions, budget_max):
    meilleures_combinaisons = []
    nombre_total_combinaisons = 0
    meilleur_profit = 0

    # Boucle pour générer toutes les combinaisons
    for r in range(1, len(actions) + 1):
        for combinaison in it.combinations(actions, r):
            coût_total = sum(action.cost for action in combinaison)
            nombre_total_combinaisons += 1

            # Vérifie si la combinaison respecte les contraintes de budget
            if coût_total <= budget_max:
                profit_combinaison = sum(
                    action.profit * action.cost for action in combinaison
                )
                if profit_combinaison > meilleur_profit:
                    meilleures_combinaisons = [combinaison]
                    meilleur_profit = profit_combinaison
                elif profit_combinaison == meilleur_profit:
                    meilleures_combinaisons.append(combinaison)

    return meilleures_combinaisons, nombre_total_combinaisons, meilleur_profit


# Fonction pour affichage de la meilleure combinaison


def afficher_meilleure_combinaison(meilleures_combinaisons, meilleur_profit):
    if len(meilleures_combinaisons) > 0:
        print("Meilleure combinaison d'actions :")
        for action in meilleures_combinaisons[0]:
            print("*", action)
        print(f"\nProfit total  : {meilleur_profit:.1f} euros")
        # Nombre total d'actions dans la combinaison
        print(
            f"\tNombre total d'actions dans la combinaison : {len(meilleures_combinaisons[0])}"
        )
        # Coût total de la combinaison
        print(
            f"\tCoût total de la combinaison : {sum(action.cost for action in meilleures_combinaisons[0])} euros"
        )
        print("\nNombre total de combinaisons générées :", nombre_total_combinaisons)
    else:
        print("Aucune combinaison possible respectant les contraintes de budget.")


# Lancer le programme

if __name__ == "__main__":
    filename = "dataset.csv"
    budget_max = 500

    data = read_and_format_data(filename)
    actions = convert_dataframe_to_action_list(data)
    (
        meilleures_combinaisons,
        nombre_total_combinaisons,
        meilleur_profit,
    ) = generer_combinaisons(actions, budget_max)
    afficher_meilleure_combinaison(meilleures_combinaisons, meilleur_profit)
