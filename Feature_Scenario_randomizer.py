import random
import os
import subprocess

from behave.parser import parse_feature

# Function provided by ChatGPt to obtain the scenario names from behave.
# As building the randomizer is not part of the project, we have opted to use this generated function.
def get_scenario_names(feature_file_path):
    with open("Features/" + feature_file_path, 'r') as feature_file:
        feature_content = feature_file.read()

    feature = parse_feature(feature_content)

    scenario_names = []
    for scenario in feature.scenarios:
        scenario_names.append(scenario.name)

    return scenario_names

# Get the list of feature files
feature_files = [f for f in os.listdir('features') if f.endswith('.feature')]

# Shuffle the feature files
random.shuffle(feature_files)

# Run behave with the shuffled files
for feature_file in feature_files:
    # Get scenarios and shuffle them
    scenarios_list = get_scenario_names(feature_file)
    random.shuffle(scenarios_list)
    for scenario in scenarios_list:
        subprocess.run(['behave', '-n' + scenario])

