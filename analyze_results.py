import os
import vizualize


class Smells_summary:
    def __init__(self, version):
        self.version = version
        self.dense_structure = 0
        self.god_component = 0
        self.scattered_functionality = 0
        self.ambigious_interface = 0
        self.feature_concentration = 0
        self.cyclic_dependency = 0
        self.unstable_dependency = 0
        self.loc = 0

    def get_total(self):
        return self.ambigious_interface + self.scattered_functionality + self.cyclic_dependency + \
               self.god_component + self.unstable_dependency + self.feature_concentration + self.dense_structure


class Smell_count:
    def __init__(self):
        self.dense_structure = []
        self.god_component = []
        self.scattered_functionality = []
        self.ambigious_interface = []
        self.feature_concentration = []
        self.cyclic_dependency = []
        self.unstable_dependency = []


def _count_smells(out_path, versions):
    smell_summary_list = []
    for version in versions:
        cur_folder = os.path.join(out_path, version[0])
        if os.path.isfile(cur_folder):
            continue
        cur_file = os.path.join(cur_folder, 'ArchitectureSmells.csv')
        if not os.path.exists(cur_file):
            print("architecture smell file not found in " + version[0])
            continue

        smell_count = Smells_summary(version[0])
        with open(cur_file, 'r', errors='ignore') as file:
            is_header = True
            for line in file.readlines():
                if is_header:
                    is_header = False
                    continue
                # Project Name	Package Name	Architecture Smell	Cause of the Smell
                tokens = line.split(',')
                if len(tokens) > 3:
                    if tokens[2] == 'Dense Structure':
                        smell_count.dense_structure += 1
                    if tokens[2] == 'Feature Concentration':
                        smell_count.feature_concentration += 1
                    if tokens[2] == 'Unstable Dependency':
                        smell_count.unstable_dependency += 1
                    if tokens[2] == 'God Component':
                        smell_count.god_component += 1
                    if tokens[2] == 'Cyclic Dependency':
                        smell_count.cyclic_dependency += 1
                    if tokens[2] == 'Scattered Functionality':
                        smell_count.scattered_functionality += 1
                    if tokens[2] == 'Ambigious Interface':
                        smell_count.ambigious_interface += 1
        smell_summary_list.append(smell_count)
    return smell_summary_list


def _count_loc(out_path, smell_count_list):
    for version in os.listdir(out_path):
        cur_folder = os.path.join(out_path, version)
        if os.path.isfile(cur_folder):
            continue
        cur_file = os.path.join(cur_folder, 'TypeMetrics.csv')
        if not os.path.exists(cur_file):
            print("type metrics file not found in " + version)
            continue

        smell_summary = next((x for x in smell_count_list if x.version == version), None)
        loc = 0
        if smell_summary is not None:
            # Project Name	Package Name	Type Name	NOF	NOPF	NOM	NOPM	LOC	WMC	NC	DIT	LCOM	FANIN	FANOUT
            with open(cur_file, 'r', errors='ignore') as file:
                is_header = True
                for line in file.readlines():
                    if is_header:
                        is_header = False
                        continue
                    tokens = line.split(',')
                    if len(tokens) > 13:
                        loc += int(tokens[7])  # loc
        smell_summary.loc = loc


def _export_summary(smell_count_list, versions, out_path):
    with open(os.path.join(out_path, 'smell_analysis_summary.csv'), 'w') as file:
        file.write("Version,Commit-hash,Date,LOC,Total architecture smells\n")
        i = 1
        for version in versions:
            smell_summary = next((x for x in smell_count_list if x.version == version[0]), None)
            if smell_summary is not None:
                line = "V" + str(i) + "," + version[0] + "," + str(version[1].date()) + "," + str(
                    smell_summary.loc) + "," + \
                       str(smell_summary.get_total()) + "\n"
                file.write(line)
                i += 1


def _export_smell_density(smell_summary_list, out_path):
    x = []
    y = []
    i = 1
    for smell_summary in smell_summary_list:
        x.append('V' + str(i))
        i += 1
        density = (smell_summary.get_total() * 1000) / smell_summary.loc if smell_summary.loc > 0 else 0
        y.append(float("%.2f" % density))
    vizualize.show_line_chart(x, y, "Version", "Smell density", os.path.join(out_path, 'smell_density.png'))


def _export_smell_distribution(smell_summary_list, out_path):
    smell_count = Smell_count()
    with open(os.path.join(out_path, 'smell_distribution.csv'), 'w') as file:
        file.write(
            'Version,Ambigious interface,Cyclic dependency,Dense structure,God component,Feature concentration,Scattered functionality,Unstable dependency\n')
        for smell_summary in smell_summary_list:
            smell_count.ambigious_interface.append(smell_summary.ambigious_interface)
            smell_count.cyclic_dependency.append(smell_summary.cyclic_dependency)
            smell_count.dense_structure.append(smell_summary.dense_structure)
            smell_count.feature_concentration.append(smell_summary.feature_concentration)
            smell_count.god_component.append(smell_summary.god_component)
            smell_count.scattered_functionality.append(smell_summary.scattered_functionality)
            smell_count.unstable_dependency.append(smell_summary.unstable_dependency)
            line = smell_summary.version + "," + str(smell_summary.ambigious_interface) + "," + str(
                smell_summary.cyclic_dependency) + \
                   "," + str(smell_summary.dense_structure) + "," + str(smell_summary.god_component) + "," + str(
                smell_summary.feature_concentration) + \
                   "," + str(smell_summary.scattered_functionality) + "," + str(
                smell_summary.unstable_dependency) + '\n'
            file.write(line)

    vizualize.show_smell_distribution(smell_count, os.path.join(out_path, 'smell_distribution.png'))


def _export_component_structure(out_path, versions):
    i = 0
    for version in versions:
        cur_folder = os.path.join(out_path, version[0])
        if os.path.isfile(cur_folder):
            continue
        cur_file = os.path.join(cur_folder, 'ArchitectureSmells.csv')
        if not os.path.exists(cur_file):
            print("architecture smell file not found in " + version[0])
            continue

        i += 1
        with open(cur_file, 'r', errors='ignore') as file:
            is_header = True
            for line in file.readlines():
                if is_header:
                    is_header = False
                    continue
                # Project Name	Package Name	Architecture Smell	Cause of the Smell
                tokens = line.split(',')
                if len(tokens) > 3:
                    if tokens[2] == 'Dense Structure':
                        cause = tokens[3]
                        index = cause.find('All the dependencies among components:')
                        if index > 0:
                            cause = cause[index:]
                            vizualize.show_component_structure(cause, os.path.join(out_path,
                                                                                   'component_structure_ v' + str(i)))


def summarize(out_path, versions):
    smell_summary_list = _count_smells(out_path, versions)
    _count_loc(out_path, smell_summary_list)
    _export_summary(smell_summary_list, versions, out_path)
    _export_smell_density(smell_summary_list, out_path)
    _export_smell_distribution(smell_summary_list, out_path)
    _export_component_structure(out_path, versions)
