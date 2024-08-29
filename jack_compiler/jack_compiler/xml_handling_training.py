from xml.etree import ElementTree

root = ElementTree.Element("Class")
sub_element = ElementTree.SubElement(root, "subroutine")
ElementTree.SubElement(sub_element, "keyword").text = "VAR DECLARATION"
ElementTree.SubElement(sub_element, "keyword").text = "VAR DECLARATION_2"
ElementTree.SubElement(sub_element, "keyword").text = "VAR DECLARATION_3"

if __name__ == "__main__":
    tree = ElementTree.ElementTree(root)
    tree.write("test.xml")

