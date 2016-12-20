from sklearn.cluster import KMeans
import sklearn.metrics as sm

def build_model(n_clusters):
	model = KMeans(n_clusters)

	return model
