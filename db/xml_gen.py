import os
from xml.dom import minidom
import uuid


class XML_Parser:
  def __init__(self, xml_file):
    if os.path.isfile(xml_file) and os.access(xml_file, os.R_OK):
      print ("File exists and is readable")
    else:
      print ("Either file is missing or is not readable, creating file...")
      root = minidom.Document()
      xml = root.createElement('root')
      root.appendChild(xml)
      xml_str = root.toprettyxml()
      with open(xml_file, "w") as f:
        f.write(xml_str)
    self.path = xml_file
    self.xmldoc = minidom.parse(xml_file)

  def change_node(self, node_name, node_id):
    self.xmldoc = minidom.parse(self.path)
    node = self.get_node(node_id)
    node.setAttribute('name', node_name)
    self.pretty_xml()

  def remove_node(self, node_id):
    self.xmldoc = minidom.parse(self.path)
    node = self.get_node(node_id)
    parent_node = node.parentNode;
    parent_node.removeChild(node)
    self.pretty_xml()

  def move_node(self, target_node_iid, node_iid):
    print(f'target {target_node_iid}')
    self.xmldoc = minidom.parse(self.path)
    parent_node = self.get_node(target_node_iid)
    child_node = self.get_node(node_iid)
    parent_node.appendChild(child_node)
    self.pretty_xml()

  def get_node(self, id):
    if id:
      nodes = self.xmldoc.getElementsByTagName('group')
    else:
      node = self.xmldoc.getElementsByTagName('root')[0]
      return node
    for node in nodes:
      if  node.getAttribute('id') == id:
        return node

  def get_nodes(self, treeview):
    if self.xmldoc.hasChildNodes():
      for ch in self.xmldoc.childNodes:
        if ch and ch.nodeType == minidom.Node.ELEMENT_NODE:
          ch_id = ch.getAttribute('id')
          ch_name = ch.getAttribute('name')
          if ch_id and ch_name:
            iid = ch.parentNode.getAttribute('id')
            treeview.insert(iid, 'end', ch_id, text = ch_name)
          self.xmldoc = ch
          self.get_nodes(treeview)

  def add_node(self, parent_id, tag_name):
    self.xmldoc = minidom.parse(self.path)
    if parent_id == '':
      parent = 'root'
    else:
      parent = 'group'
    group_id = uuid.uuid4()
    child = self.xmldoc.createElement('group')
    child.setAttribute('name',tag_name)
    child.setAttribute('id', str(group_id))
    parent_element = self.xmldoc.getElementsByTagName(parent)
    if parent == 'root':
      parent_element[0].appendChild(child)
    else:
      for ele in parent_element:
        if ele.getAttribute('id') == parent_id:
          ele.appendChild(child)
    self.pretty_xml()



  def pretty_xml(self):
    xml_str = self.xmldoc.toprettyxml()
    with open(self.path, "w") as f:
      f.write(xml_str)
    with open(self.path) as xmlfile:
      lines = [line for line in xmlfile if line.strip() != ""]
    with open(self.path, "w") as xmlfile:
      xmlfile.writelines(lines)

