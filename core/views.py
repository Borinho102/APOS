from django.shortcuts import render
import csv
import os


# Create your views here.

def csv_creator(user_id):
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA = os.path.join(BASE, "data")

    path = os.path.join(DATA, "school/" + user_id + ".csv")
    data = ["user_id,school_id,type,date".split(",")]
    try:
        handle = open(path, "r")
    except FileNotFoundError:
        file = open(path, "w")
        with open(path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)

    path = os.path.join(DATA, "branch/" + user_id + ".csv")
    data = ["user_id,branch_id,date".split(",")]
    try:
        handle = open(path, "r")
    except FileNotFoundError:
        file = open(path, "w")
        with open(path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)

    path = os.path.join(DATA, "search/" + user_id + ".csv")
    data = ["user_id,term,date".split(",")]
    try:
        handle = open(path, "r")
    except FileNotFoundError:
        file = open(path, "w")
        with open(path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)

    try:
        handle = open(os.path.join(DATA, "profile/" + user_id + ".csv"), "r")
    except FileNotFoundError:
        file = open(os.path.join(DATA, "profile/" + user_id + ".csv"), "w")