import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score,StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline

data = pd.DataFrame({
    "age": [22, 35, 45, 28, 52, 41, 30, 60, 25, 48, 33, 55],
    "monthly_spend": [
        2000, 4500, 6000, 2500,
        8000, 5500, 3000, 9000,
        2200, 7000, 3500, 7500
    ],
    "tenure": [
        2, 24, 36, 5,
        48, 30, 12, 60,
        3, 42, 18, 50
    ],
    "gender": [
        "Male", "Female", "Male", "Female",
        "Male", "Female", "Male", "Female",
        "Male", "Female", "Male", "Female"
    ],
    "plan": [
        "Basic", "Premium", "Premium", "Basic",
        "Premium", "Standard", "Basic", "Premium",
        "Basic", "Premium", "Standard", "Premium"
    ],
    "churn": [
        1, 0, 0, 1,
        0, 0, 1, 0,
        1, 0, 0, 0
    ]
})
x = data.drop("churn",axis = 1)
y = data["churn"]
x_test,x_train,y_test,y_train = train_test_split(x,y,test_size = 0.2,random_state = 42)
numeric_features = ['age','monthly_spend','tenure']
categorical_features = ['gender','plan']
preprocessor = ColumnTransformer([('numeric',StandardScaler(),numeric_features),('categorical',OneHotEncoder(),categorical_features)])
model_pipeline = Pipeline([('preprocessor',preprocessor),('model',LogisticRegression())])
model_pipeline.fit(x_train,y_train)
y_pred = model_pipeline.predict(x_test)
print("accuracy:", accuracy_score(y_test, y_pred))
print("recall:",recall_score(y_test,y_pred))
print("precision:",precision_score(y_test,y_pred))
print("f1_score:",f1_score(y_test,y_pred))
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model_pipeline,x,y,cv = skf,scoring='accuracy')
print("cross-validation scores :",scores)
print("avg cv score:", scores.mean())