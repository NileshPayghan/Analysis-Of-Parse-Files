# Analysis-Of-Files
This class is used to make analysis of xml, dita and ditamap etc. files.
This module is worked on parsing files like xml.

Author: Nilesh Payghan
contact: nileshpayghan7@gmail.com
Linkdin: www.linkedin.com/in/nileshpayghan7


Description: This is simple analysis example for parsing files and identify their behavior of files.
            - This class is used to make analysis of xml like files.
            - Number of attributes contains that element.
            - This gives us output in csv.
            - CSV contains xpath, attribute and their attribute values. If one attribute contains values more than 10 then it will write it as [....] in list.
            - Because it contains different values with that attribute.
            - It shows attribute and their values if the attribute values are not found more than 10 for that particular tag.
            
            
Warning: set set_prefixes key value pair of file namespaces whatever you have.
         otherwise it will work properly
        - If don't have namespaces for files then comment that lines and run as it is.
        - If file is not parsed then it will show an traceback because I don't handle any kind of exception in this module.
        - so provide correct input and don't forget set set_prefixes for your file namespace.
   
        
command to run: python AnalysisOfFiles.py directory_name extension(xml,dita,ditamap)
    directory_name: contains xml like files for parsing.
    extension: give an extension of files that we wanted to analyse.
                ex. if we give an xml as extension it only gets xml files from directory which is provided.
    
                
Conclusion: We can analyse the hundreds and thousands of files within a minute.
            - We don't need to analyse such files manually while data conversion
            - This is helpful for data conversion expertise for analyse files and get what kind tagging structure within it.
 
 Note: This module is created for educational purpose.
