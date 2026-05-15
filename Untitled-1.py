import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)


formula_df: pd.DataFrame = pd.read_csv("dataEngineeringDataset.csv")
formula_df.shape
print("Broj redova i kolona")
print(formula_df.shape)
print("info o datasetu")
print(formula_df.info())
print("null vrijednosti po kolonama", formula_df.isnull().sum())
print("Opis podataka")
print(formula_df.describe())
print(formula_df[formula_df.duplicated()])
for col in formula_df.select_dtypes(include=["object", "string"]).columns:
    print(f"\n--- {col} ---")
    print(formula_df[col].unique())
