import argparse
import data

def run():
    my_parser = argparse.ArgumentParser(description='analysis the json file')
    my_parser.add_argument('-i', '--init', help='json file path')
    my_parser.add_argument('-u', '--user', help='username')
    my_parser.add_argument('-r', '--repo', help='repository name')
    my_parser.add_argument('-e', '--event', help='type of event')
    args = my_parser.parse_args()