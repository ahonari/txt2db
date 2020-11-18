# txt2db
This tool can be used to extract information from news articles downloaded from NexisUni in text format and structure and save it to a database.

## About
* This tool is created as a part of the research project 'Applying machine learning techniques to the study of polarization' which is financially supported by *the focus area Applied Data Science* at Utrecht University. 
* In this research project researchers employed the tool to analyze all articles about immigration issues that were published in 20-year period (January 1999 to January 2019) in two mainstream Dutch newspapers *right-leaning* De Telegraaf and *left-leaning* De Volkskrant.
* The ultimate goal of the project is investigating media discourses on immigration in the Netherlands.
* The researchers have also used machine learning classifier to identify immigration related articles. 
* The extended version of the tool will be available when the project is finalized.
* *Researchers*: Frank van Tubergen and Ali Honari

## Requirements
Python 3
<br>Db browser SQLITE

## Getting started
1. Download your articles from NexisUni in MsWord (.docx) format and in Full Document format.
<br>*important note*: In Tab Formatting Options *uncheck* all options can be included in the delivered document
2. Combine all downloaded files into a single .txt file.
<br>*important note*: While combining/converting downloaded files select the following settings:
<br>2.1. Text encoding: Other encodings --> Unicode (UTF-08)
<br>2.2. Insert line breaks
<br>*Note*: As an example see the file <B>ExampleTXTfile.txt</B>.
3. Place the python script file (TXT2DB1.0.py) and the text file in one single folder.
<br>*note*: Before running the script, open the script in an editor like ATOM and change the name of the output (SQLITE file) in line 15, in case you want to store the data in a different database. Otherwise the data add into the existing database.

## Process
1.  Once the python script is run, you will be asked to enter: 
<br>1.1. the text file name (<B>include</B> .txt)
<br>1.2. the source name (the name should be written exactly as it is in NexisUni)
2.  You can find the Sqlite file in the same folder and open the file by using DB Browser (Sqlite).
3.  In the database, you can find two relational tables:
<br>3.1. Article (meta data) includes:
<br><table style="width:100%">
  <tr>
    <th>id</th>
    <th>Title</th>
    <th>Newspaper</th>
    <th>DataPublished</th>
    <th>WeekdayPublished</th>
    <th>Section</th>
    <th>Length</th>
    <th>Byline</th>
    <th>Subject</th>
    <th>Geographic</th>		
  </tr>
</table>
<br>3.2. Body
<br><table style="width:100%">
  <tr>
    <th>Body</th>
    <th>Articles_id</th>
  </tr>
</table>
