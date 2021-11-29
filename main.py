from joblib import dump
from os import getenv

from pandas.core.frame import DataFrame

import boto3
import botocore
import pandas as pd

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
)

from sklearn.ensemble import RandomForestClassifier

BUCKET_NAME = "kueski-ml-system"
FEATURES_KEY = "feature_store/2021/11/28/train_model_pyspark.parquet.gzip"
FEATURES = "train_model_pyspark.parquet.gzip"
MODEL_KEY = "models/2021/11/28/model_risk.joblib"
MODEL = "model_risk.joblib"
DEV: bool = True if getenv("STAGE", None) == "dev" else False


def download_file(bucket_name: str, file_key: str, file_local: str):
    print(f"Downloading file from S3 {bucket_name}/{file_key}")
    s3 = boto3.resource("s3")
    try:
        s3.Bucket(bucket_name).download_file(file_key, file_local)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("The object does not exist.")
        else:
            raise


def upload_file(bucket_name: str, file_key: str, file_local: str):
    print(f"Uploading file to S3 {bucket_name}/{file_key}")
    s3 = boto3.client("s3")
    try:
        s3.upload_file(file_local, bucket_name, file_key)
    except botocore.exceptions.ClientError as e:
        print(f"Error: {e}")
        raise


def train_model(cust_df: DataFrame):
    Y = cust_df["status"]
    cust_df.drop(["status"], axis=1, inplace=True)
    X = cust_df

    # Using Synthetic Minority Over-Sampling Technique(SMOTE) to overcome sample imbalance problem.
    Y = Y.astype("int")
    X_balance, Y_balance = SMOTE().fit_resample(X, Y)
    X_balance = pd.DataFrame(X_balance, columns=X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X_balance, Y_balance, stratify=Y_balance, test_size=0.3, random_state=123
    )

    print(f"Training RandomForestClassifier")
    model = RandomForestClassifier(n_estimators=5)

    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    print("Accuracy Score is {:.5}".format(accuracy_score(y_test, y_predict)))
    print("Precision Score is {:.5}".format(precision_score(y_test, y_predict)))
    print("Recall Score is {:.5}".format(recall_score(y_test, y_predict)))

    return model


if __name__ == "__main__":
    if not DEV:
        download_file(BUCKET_NAME, FEATURES_KEY, FEATURES)
    print(f"Opening feature parquet {FEATURES}")
    df = pd.read_parquet(FEATURES)

    print(f"Filling null values with 0")
    cust_df = df.copy()
    cust_df.fillna(0, inplace=True)

    model = train_model(cust_df)

    print(f"Dumping model to {MODEL}")
    dump(model, MODEL)

    if not DEV:
        upload_file(BUCKET_NAME, MODEL_KEY, MODEL)
