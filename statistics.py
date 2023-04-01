"""
TODO:
 1. Sredni czas podrozy wszystkich pojazdow
 2. Nie zapisuj pojazdow z obiektach/zmiennych tylko czytaj z pliku i sumuj
"""
import os
import xml.etree.ElementTree as ET


class Statistics:
    def get_data_by_attr(self, attribute, is_float=True):
        return_list = list()
        for file in self.files:
            tree = ET.parse(file)
            root = tree.getroot()
            for veh in root.findall('tripinfo'):
                if is_float:
                    return_list.append(float(veh.get(attribute)))
                else:
                    return_list.append(veh.get(attribute))

        return return_list

    def get_avg_for_attr(self, attribute='duration'):
        duration_list = self.get_data_by_attr(attribute)
        duration_sum = 0.0
        avg = 0.0

        for d in duration_list:
            duration_sum += d

        avg = duration_sum / len(duration_list)
        print("avg", avg)
        print(duration_list)
        return avg

    def __init__(self, guid: str):
        path = 'results/%s/' % guid

        self.files = []
        for file in os.listdir(path):
            self.files.append(path + file)

        self.statistics = {}


def main():
    stats = Statistics('173433')
    stats.get_avg_for_attr('duration')


if __name__ == "__main__":
    main()
