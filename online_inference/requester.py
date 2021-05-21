import argparse
import csv
from urllib import parse

import requests


def get_prediction(host: str, port: int, api_url: str, data: dict) -> dict:
    req_url = parse.urlunparse(["http", f"{host}:{port}", api_url, "", "", ""])

    responce = requests.post(req_url, json={"features": [data]})
    responce.raise_for_status()

    return responce.json()


def main(args):
    with open(args.test_csv, "r", encoding="utf-8", newline="") as raw_file:
        header = raw_file.readline().strip().split(",")
        csv_readers = csv.DictReader(raw_file, fieldnames=header)

        for i, row in enumerate(csv_readers, 1):
            if args.num_examples is not None and i > args.num_examples:
                break

            for col_name in row:
                try:
                    row[col_name] = int(row[col_name])
                except ValueError:
                    row[col_name] = float(row[col_name])

            true_label = row.pop(args.target)
            predicted_label = get_prediction(args.host, args.port, args.url, row)[
                0]["heart_disease"]
            print(f"Row: {i} Actual label: {true_label} Predicted label: {predicted_label}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost", help="A host of server")
    parser.add_argument("--port", type=int, required=True, help="A port of server")
    parser.add_argument("--test_csv", type=str, default="./test_data/test.csv", help="A path to csv with test data")
    parser.add_argument("--num_examples", type=int, default=None,
                        help="A number of lines to test from csv")
    parser.add_argument("--url", type=str, default="/predict",
                        help="An URL of API")
    parser.add_argument("--target", type=str, default="target")

    args = parser.parse_args()

    main(args)
