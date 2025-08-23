from sklearn import ensemble
from sklearn.model_selection import cross_val_score
from predictor.estimators.estimator import Estimator
from predictor.preprocessing.preProcessor import PreProcessor
from domain.solution import Solution

from sklearn.metrics import make_scorer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import r2_score

import numpy as np

class RandomForestEstimator(Estimator):
    
    def __init__(self,directivesFile):
        self.rfRegressor=ensemble.RandomForestRegressor(n_estimators=100)
        self.features = []
        self.results = []
        self.processor = PreProcessor(directivesFile)
        self.isFit = False
    def isTrained(self):
        return self.isFit
    def trainModel(self,dataset):
        """
        fit a whole new forest of trees from the dataset.
        Parameters
        ----------
        dataset : List of Solution objects
        """
        features, results = self.processor.process(dataset)
        self.features = features
        self.results = results
        self.rfRegressor.fit(features,results) #train
        self.isFit = True

    def trainModelPerMetric(self,metric):
        #TODO
        self.rfRegressor.fit(self.features,self.results) #train

   
    def retrain(self,dataset):
        """
        reuse the solution of the previous call to fit 
        and add more estimators to the ensemble.
        Parameters
        ----------
        dataset : List of Solution objects
        """
        features, results = self.processor.process(dataset)
        self.features.extend(features)
        self.results.extend(results)
        self.rfRegressor.fit(self.features,self.results) #train
        self.isFit = True

    def estimateSynthesis(self, dataset):
        #TODO talvez futuramente retornar lista de solutions
        """
        Estimate the output of synthesis from the dataset.

        Parameters
        ----------
        dataset: List of Solution objects

        Returns
        -------
        List : List of the output([FF,DSP,LUT,BRAM,resources,latency],[...],...)
                estimated for these features
        """
        processedFeatures, processedResults =  self.processor.process(dataset)

        return self.rfRegressor.predict(processedFeatures)

    
    def score(self,dataset):
        processedFeatures, processedResults =  self.processor.process(dataset)
        return self.rfRegressor.score(processedFeatures,processedResults)



    def cross_val(self, dataset, cv=5,scorer="r2"):
        """
        Perform cross-validation on the dataset.

        Parameters
        ----------
        dataset : List of Solution objects
        cv : int, default=5
            Number of folds in cross-validation.

        Returns
        -------
        List : List of scores for each fold.
        """
        def cosine_similarity_score(y_true, y_pred):
            # Ensure 2D arrays
            y_true = np.array(y_true)
            y_pred = np.array(y_pred)

            # Average cosine similarity over all rows
            similarities = []
            for i in range(len(y_true)):
                sim = cosine_similarity(y_true[i][-2:].reshape(1, -1), y_pred[i][-2:].reshape(1, -1))[0][0]
                similarities.append(sim)
                    
            return np.mean(similarities) 
        
        def r2_score_last_two(y_true, y_pred):
            y_true = np.array(y_true)
            y_pred = np.array(y_pred)
            
            # Extract only the last two columns
            y_true_last2 = y_true[:, -2:]
            y_pred_last2 = y_pred[:, -2:]
            
            # Compute R² score for each column separately
            r2_values = []
            for i in range(2):  # last two elements
                r2 = r2_score(y_true_last2[:, i], y_pred_last2[:, i])
                r2_values.append(r2)
            
            # Optionally return the average, or both separately
            return np.mean(r2_values)  
        
        def hybrid_similarity_score(y_true, y_pred, alpha=1.0):
            scores = []
            for yt, yp in zip(y_true, y_pred):
                # Ensure arrays
                yt = np.array(yt).reshape(1, -1)
                yp = np.array(yp).reshape(1, -1)
                
                cos_sim = cosine_similarity(yt, yp)[0][0]
                mag_error = abs(np.linalg.norm(yp) - np.linalg.norm(yt)) / (np.linalg.norm(yt) + 1e-8)
                
                score = cos_sim * np.exp(-alpha * mag_error)
                scores.append(score)
                
            return np.mean(scores)

        def r2_score_all_but_last(y_true, y_pred):
            y_true = np.array(y_true)
            y_pred = np.array(y_pred)
            
            # Exclude the last column
            y_true_excl_last = y_true[:, :-1]
            y_pred_excl_last = y_pred[:, :-1]
            
            # Compute R² score for each column separately
            r2_values = []
            for i in range(y_true_excl_last.shape[1]):
                r2 = r2_score(y_true_excl_last[:, i], y_pred_excl_last[:, i])
                r2_values.append(r2)
            
            # Return the average R² over the selected features
            return np.mean(r2_values)
        if scorer=="cosine_sim":
            scorer = make_scorer(hybrid_similarity_score, greater_is_better=True)
        features, results = self.processor.process(dataset)
        scores = cross_val_score(self.rfRegressor, features, results, scoring=scorer , cv=cv)
        return scores

#usar scikit learn pra decisions tree
#testar treino com multi-outputs (prever todas metricas) e testar com varios modelos (um pra cada metrica)
#Titulos dos features de cada coluna vao ser sobre o label e o tipo de diretiva. Ex: 
#             unroll sha_update_label4                         |               pipeline sha_update_label4             |                   array_partition main                                   | Saída(em LUTS por exemplo)
# set_directive_unroll -factor 8 "sha_update/sha_update_label4"| set_directive_pipeline "sha_update/sha_update_label4"|set_directive_array_partition -type block -factor 100 -dim 0 "main" indata|         45

# o dicionário será tipo: dicionario[pipeline] = ['',pipe 1, pipe2], então posso ao invés de colocar '' ou pipe1 ou pipe2 na tabela, posso colocar 0,1,2. EX:

# unroll sha_update_label4 | pipeline sha_update_label4 | array_partition main  | Saída(em LUTS por exemplo)
#          1               |            1               |          2            |            45

#O problema disso é que são categorical variables, portanto devo ajeitar isso com one hot encoding
#Normalizar