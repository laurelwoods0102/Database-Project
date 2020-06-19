import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, Ridge
import matplotlib.pyplot as plt
from query import QueryProcess

from pprint import pprint

class FeatureSelectionModel:
    def __init__(self):
        self.alpha = np.logspace(-3, 1, 5)
        self.max_iter = np.logspace(3, 7, 5)    # As Shrinkage alpha increases, need to increase max_iter to converge coefficients

        self.query_processor = QueryProcess()

        #city_list = ["Songpa-gu"]              # For Test
        #self.category_list = ["Beer"]
        self.city_list = self.query_processor.city_name().values.T.tolist()[0]
        self.category_list = self.query_processor.GS_category().values.T.tolist()[0]

    def plot_feature(self, data, city, category, column):
        plt.figure(figsize=(12, 12))

        plt.semilogx(data)
        plt.xticks(self.alpha, labels=np.log10(self.alpha))
        plt.legend(column, loc='upper right')

        plt.title("Feature Selection")
        plt.savefig("{0}_{1}.png".format(city, category))
        plt.close()

    def select_feature(self, city, category):
        data_2017 = self.query_processor.query_dataset(2017, str(city), str(category))
        data_2018 = self.query_processor.query_dataset(2018, str(city), str(category))
        data = pd.concat([data_2017, data_2018])
        column = data.columns.values[:15]       # Column Index for Plotting

        # Normalization
        dataset = data.values
        data_mean = dataset.mean(axis=0)
        data_std = dataset.std(axis=0)

        dataset = (dataset-data_mean)/data_std

        # Compare Coefficient of different Shrinkage alpha
        result = []
        for i, item in enumerate(zip(self.alpha, self.max_iter)):
            lasso = Lasso(alpha=item[0], max_iter=item[1]).fit(dataset[:, :15], dataset[:, -1])
            result.append(pd.Series(np.hstack([lasso.coef_])))  # Sometimes include lasso.intercept

        df_result = pd.DataFrame(result, index=self.alpha)
        df_result.columns = column      # Add Column Index for Plotting

        self.plot_feature(df_result, city, category, column)
        
        df_result = df_result[::-1].apply(np.absolute)      # To compare distance from 0
        feature_sorted = df_result.loc[self.alpha[0]].to_frame().sort_values(by=[self.alpha[0]], ascending=False)
        #print(feature_sorted.index.tolist())

        with open("{0}_{1}.txt".format(city, category), "w") as f:
            for features in feature_sorted.index.tolist():
                f.write(features)
                f.write("\n")

    # Cartesian Product of all Cities and Categories
    def process_all(self):
        exception = list()
        for city in self.city_list:
            for category in self.category_list:
                try:
                    self.select_feature(city, category)
                except Exception as e:
                    exception.append([city, category, e])
        
        with open("exception.txt", 'w') as f:
            for ex in exception:
                f.write(ex)
                f.write("\n")


if __name__ == "__main__":
    feature_selection_model = FeatureSelectionModel()
    #feature_selection_model.select_feature("Songpa-gu", "Beer")
    feature_selection_model.process_all()