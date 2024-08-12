# from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import arff

def convert_weka_data(file_path: str):
  """Carrega um arquivo ARFF e retorna as features (X) e labels (y)."""
  data = arff.load(open(file_path, 'r'))
  attributes = [attribute[0] for attribute in data['attributes']]
  data_list = data['data']
  X = [[float(row[i]) for i in range(len(attributes) - 1)] for row in data_list]
  y = [row[-1] for row in data_list]
  return X, y

def train_and_test_svm(label_quantity: int, train_data: list, test_data: list):

  X_train, y_train = convert_weka_data(f'/home/yuri/www/manuscritus/backend/src/svm/treino-{label_quantity}.arff')
  X_test, y_test = convert_weka_data(f'/home/yuri/www/manuscritus/backend/src/svm/teste-{label_quantity}.arff')
  
  X_train.append(train_data[0])
  X_train.append(train_data[1])
  y_train.append('a0')
  y_train.append('a0')
  X_test.append(test_data[0])
  y_test.append('a0')

  clf = SVC(kernel='poly', C=2) 

  clf.fit(X_train, y_train)

  y_pred = clf.predict(X_test)

  accuracy = accuracy_score(y_test, y_pred)
  print(f"Acurácia: {accuracy:.2f}")

  confusion_matrix_to_print = confusion_matrix(y_test, y_pred)
  print("\nMatriz de Confusão:")
  print(confusion_matrix_to_print)

  print("\nPredição para cada manuscrito:")
  for i, prediction in enumerate(y_pred):
      print(f"Manuscrito {i+1}: Autor {prediction}")
      
  return accuracy
