import xml.etree.cElementTree as ET
from lxml import etree
from os.path import join as joinpath
from os import listdir
from datetime import datetime

filename = "Input\\gtr_ftp.xml"
output_folder = "Output"



def split_xml_to_chunks(xml_file, output_folder):
    line = ""
    sline = ""
    count = 0
    lines = []
    start = False
    end = False
    print("StartTime: " + str(datetime.now()))
    with open(file=xml_file, mode="r", encoding="utf-8") as source:
        # for i in range(5):
        #     line = source.readline().strip()
        #     print(line)
        while sline != "</GTRPublicData>":
            line = source.readline().replace("\n", "")
            sline = line.strip()
            if sline == "<GTRLabData>":
                start = True
                end = False
            if sline == "</GTRLabData>":
                end = True
                start = False
            if start:
                lines.append(line + "\n")
                pass
            if end:
                lines.append(line + "\n")
                print("Median " + str(count) + " : " + str(datetime.now()))
                with open(joinpath(output_folder, str(count) + ".xml"), mode="w", encoding="utf-8") as temp:
                    temp.writelines(lines)
                lines = []
                count += 1
            
        print(line)
    print("EndTime: " + str(datetime.now()))

def read_data_from_chunks(folder_path):
    for filename in listdir(folder_path):
        print(filename)
        with open(joinpath(folder_path, filename), mode="r", encoding="utf-8") as source:
            # parser = etree.iterparse(source)
            tree = etree.parse(source)
            print(tree.root())

# split_xml_to_chunks(filename, output_folder)
read_data_from_chunks(output_folder)
