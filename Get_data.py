import xml.etree.ElementTree as ET

print("Entre o caminho do arquivo:")
xml=input()


tree = ET.parse(xml)
root = tree.getroot()

print("BRAM")
print(root[3][0][0].text)
print("LUT")
print(root[3][0][3].text)
print("FlipFLops")
print(root[3][0][2].text)
print("DSP")
print(root[3][0][1].text)
print("Latencia")
print(root[2][2][2].text)
