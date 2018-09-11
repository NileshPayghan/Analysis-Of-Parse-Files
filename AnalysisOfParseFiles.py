
///////////////////////////////////////////////////////////////////////////////////////////////////////
//Name:
//Modified:2018
//Author: Nilesh Payghan
//Input:
//output:
//Description: show in README.md
////////////////////////////////////////////////////////////////////////////////////////////////////////

import os
import csv
import sys
import xml.etree.ElementTree as et
import xml.dom as dom
import xml.dom.minidom as minidom



class AnalysisOfFiles:
    def __init__(self,directory,extension='xml'):
        self.directory = directory
        self.extension = extension
        self.xpathTagList = []
        self.tagList = []
        self.filelist = self.getFileList(directory,self.extension) #first take file list 
        self.getEveryTagName()
        self.getXpath()
        self.writeToCsv()

    #used to get any kind of file list by giving it's extensions
    def getFileList(self,directory,extension):
        filelist = []
        for root,dir,files in os.walk(directory):
            for file in files:
                filename = os.path.join(root,file)
                if filename.lower().endswith(extension) and filename not in filelist:
                    filelist.append(filename)
        return filelist

    def findxpath(self,child,root,parentMap):
        '''
              This function is used to find xpath of child tag and return xpath of child
        '''
        temp_element=child
        xpath=""
        while temp_element != root:
            temp_element=parentMap[temp_element]
            tag_name=""
            if temp_element.tag.find(':') > -1:
                tag_name=temp_element.tag.split(':')[1]
            else:
                tag_name=temp_element.tag
            xpath=xpath+'/'+tag_name#temp_element.tag.split(':')[1]
        xpath_list=xpath.split('/')
        xpath_list.reverse()
        xpath='/'.join(xpath_list)
        tag_name=""
        if child.tag.find(':') > -1:
            tag_name=child.tag.split(':')[1]
        else:
            tag_name=child.tag
        xpath=xpath+tag_name#child.tag.split(':')[1]
        return xpath
    
    def getXpath(self):
        for file in self.filelist:
            tree = et.parse(file)
            root = tree.getroot()
            parentMap = dict((c, p) for p in tree.getiterator() for c in p)
            self.set_prefixes(tree, dict(key="namespaces")) # set the namespaces values with their name as dictionary key value pair
            for node in root.iter():
                childrens = node.getchildren()
                xpath = ""
                if childrens:
                    for child in childrens:
                        xpath = self.findxpath(child,root,parentMap)
                        if xpath not in self.xpathTagList:
                            self.xpathTagList.append(xpath)
    
    def writeToCsv(self):
        if self.xpathTagList:
            filename = str(self.extension.capitalize())+'Xpath.csv'
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([str(self.extension.capitalize())+'Xpath List'] + ["TagName"] + ["Number Of Attributes"] + ["Attribute List of Tag"] )
                for path in self.xpathTagList:
                    attrslist = self.checkAttributes(path.split('/')[-1])
                    csvwriter.writerow([path] + [path.split('/')[-1]] + [len(attrslist)] + [attrslist])


    def getEveryTagName(self):
        for file in self.filelist:
            tree = et.parse(file)
            root = tree.getroot()
            self.set_prefixes(tree, dict(key="namespaces")) # set the namespaces values with their name as dictionary key value pair
            for node in root.iter():
                tag = node.tag
                if tag not in self.tagList:
                    if '}' in tag:
                        tag = tag.split('}')[-1]
                    self.tagList.append(tag)
        return self.tagList

    def checkAttributes(self,tag):
            attrslist = {}
            print '\ntag : ' + str(tag)
            flag = True
            for pfile in self.filelist:
                root = minidom.parse(pfile)
                pnorm_tags = root.getElementsByTagName(tag)
                for pnorm_tag in pnorm_tags:
                    if pnorm_tag.hasAttributes():
                        
                        for attr in pnorm_tag.attributes.keys():
                            if attr not in attrslist:

                                attrslist[attr] = [pnorm_tag.getAttribute(attr)]
                            else:
                                if pnorm_tag.getAttribute(attr) not in attrslist[attr] and len(attrslist[attr]) < 10 and flag:
                                    attrslist[attr].append(pnorm_tag.getAttribute(attr))
                                elif len(attrslist[attr]) >= 10 and len(attrslist[attr]) < 11:
                                    flag = False
                                    attrslist[attr] = ['...........']
                                    
            return attrslist

    def set_prefixes(self,elem, prefix_map):

        # check if this is a tree wrapper
        if not et.iselement(elem):
            elem = elem.getroot()

        # build uri map and add to root element
        uri_map = {}
        for prefix, uri in prefix_map.items():
            uri_map[uri] = prefix
            elem.set("xmlns:" + prefix, uri)

        # fixup all elements in the tree
        memo = {}
        for elem in elem.getiterator():
            self.fixup_element_prefixes(elem, uri_map, memo)



    def fixup_element_prefixes(self,elem, uri_map, memo):
        def fixup(name):
            '''The fixup_element_prefixes function follows. This checks all universal names against the URI map, for both element and attribute names.'''
            try:
                return memo[name]
            except KeyError:
                if name[0] != "{":
                    return
                uri, tag = name[1:].split("}")
                if uri in uri_map:
                    new_name = uri_map[uri] + ":" + tag
                    memo[name] = new_name
                    return new_name
        # fix element name
        name = fixup(elem.tag)
        if name:
            elem.tag = name
        # fix attribute names
        for key, value in elem.items():
            name = fixup(key)
            if name:
                elem.set(name, value)
                del elem.attrib[key]


'''
param: python AnalysisOfFiles.py directory extension(xml,dita,ditamap)
'''
if __name__ == '__main__':
    if len(sys.argv) >= 1:
        AnalysisOfFiles(sys.argv[1],sys.argv[2])
            
    
