import numpy as np

class KMeans():
    def __init__(self, num_clusters, dist):
        self.k = num_clusters
        self.dist = dist          # (n, f) * (k, f) -> (n, k)
        self.labels = np.array([])
        self.centers = np.array([])
    
    def fit(self, X, max_iter = 1000):
        num_items, num_features = X.shape
        
        idx = np.random.randint(0, num_items, (self.k,))
        self.centers = X[idx]
        
        for i in range(max_iter):            
            self.labels = self.dist(X, self.centers).argmin(axis = 1)
            old_centers = self.centers.copy()
            for j in range(self.k):
                if np.sum(self.labels == j) <= 0:
                    continue
                self.centers[j] = X[self.labels == j].mean(axis = 0)
            if np.square(old_centers - self.centers).sum() <= 1e-5:
                break
                
def EuclidianDistance(X, y):
    assert X.shape[1] == y.shape[1]
    X_2 = np.square(X).sum(axis = 1, keepdims = True)
    y_2 = np.square(y).sum(axis = 1, keepdims = True).T
    Xy = X @ y.T
    return np.sqrt(-2 * Xy + X_2 + y_2)

def CosineDistance(X, y, ep = 1.e-10):
    assert X.shape[1] == y.shape[1]
    Xy = X @ y.T
    X_norm = np.sqrt(np.square(X).sum(axis = 1, keepdims = True) + ep)
    y_norm = np.sqrt(np.square(y).sum(axis = 1, keepdims = True) + ep)
    return 1 - Xy / (X_norm @ y_norm.T)