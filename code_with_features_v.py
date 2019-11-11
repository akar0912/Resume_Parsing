import os
import re
import pandas as pd
import numpy as np
#import nltk
import spacy
from spacy.matcher import Matcher
from nltk.corpus import stopwords
nlp=spacy.load('en_core_web_sm')
matcher=Matcher(nlp.vocab)
import PyPDF2
#from pywintypes import com_error
#import win32com.client as win32
import io
import docx2txt
STOPWORDS = set(stopwords.words('english'))


from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
#import spacy

import sys
import os
import numpy as np
#import comtypes.client




def extract_email_addresses(text):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(text)

def extract_mobile_number(text):
    #mno = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,15}[0-9]', text)
    mno = re.findall(r'[\+\(]?[1-9][0-9 \-\(\)]{8,15}[0-9]', text)
    mono = []
    for i in range(len(mno)):
        digit = 0
        for j in mno[i]:
            if j.isnumeric():
                digit+=1
        if digit > 9 and digit < 15:
            mono.append(mno[i])         
    return mono

def getKeysByValue(dictionary, value):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    for x in range(len(values)):
        for y in values[x]:
            if y == value:
                return keys[x]



def extract_skill_set(text):
    # with open("C:\\Users\\PritamDevadattaJena\\Desktop\\alisha\\skills.txt","r") as skill:
    #     skill_set = skill.read().split("\n")
    all_skills = {'Excel': ["Excel", "Advance Excel", "MS Excel", "Report", "Charts"], "VBA" : ["Visual Basic", "Visual Basic Application", "Macro", "Automation"], "Database": ["MS access", "Access Database", "SQL Server", "SQL", "SSIS"], "Power BI":["Power BI", "Power Query", "Power Pivot"] , "Qlikview":["Qlikview", "Set analysis"], "QlikSense":["QlikSense"], "Analytics":["Analytics", "Machine Learning", "Deep Learning", "AI", "Artificial Intelligence", "ML", "SVM", "SAS", "R"], "Sharepoint":["Sharepoint"]} 
    skill_set = list(np.concatenate(list(all_skills.values()), axis=0 ))
    f = []
    for s in skill_set:
        #if re.search(s, text, re.I):
        if s in text:
            if len(s)>2:
            	f.append(s)
                #f.append(getKeysByValue(all_skills,s))
    
    return list(set(f))


def generate_ngrams(filename, n):
    words = filename.split()
    output = []  
    for i in range(len(words)-n+1):
        output.append(words[i:i+n])
    f=[]            
    for i in output:
        if 'years' in i:
            f.append(output[output.index(i)])
            if len(f)==1:
                n=f[0][0]
                n=n + " " + "years"
                break
    
    if len(f)<1:
        n='Not specified'
    return n


def exper(fullText):
    mi=fullText.lower()
    #print(mi)
    h=mi.replace("_"," ")
    h=h.replace("-"," ")
    h=h.replace(","," ")
    h=h.replace("("," ")
    h=h.replace(")"," ")
    h=h.replace(".docx"," ")
    h=h.replace(".pdf"," ")
    h=h.split()              #look at h only years get it
    #if 'years' in h and 'months' in h:
    #    d=h[h.index('years')-1] + " " + h[h.index('years')]+ " " +h[h.index('months')-1] + " " +h[h.index('months')]
    #elif 'year' in h:
        #d=h[h.index('year')-1] + " " + h[h.index('year')]
    if 'years' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]
    elif 'months' in h:
        d=h[h.index('months')-1] + " " + h[h.index('months')]
    #elif 'month' in h:
     #   d=h[h.index('month')-1] + " " + h[h.index('month')]
    elif re.search('no experience',str(h),re.M|re.I) :
        d='No Experience'
    else:
        d=generate_ngrams(fullText, 2)  
    return d    



def count_skills(doc):
    
    a = doc.lower()
    a = re.sub('[^A-Za-z0-9]+', ' ', a)
    a = a.split()
    return a.count('python'),a.count('excel'),a.count('vba'),a.count('sql')

def extract_text_from_pdf(path, filename):
    with open(path+filename, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )


            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )


            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text


            # close open handles
            converter.close()
            fake_file_handle.close()


def extract_text_from_doc(path,filename):
    temp = docx2txt.process(path+filename)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return text


def extract_names(document):
    #nlp=spacy.load('en_core_web_sm')
    #matcher=Matcher(nlp.vocab)
    document.replace("CURRICULUM VITAE","")
    nlp_text=nlp(document)
    pattern=[{'POS':'PROPN'},{'POS':'PROPN'}]
    matcher.add('NAME',None,pattern)
    matches=matcher(nlp_text)
    for match_id,start,end in matches:
        span=nlp_text[start:end]
        return span.text
    
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MSC', "M.SC",
            'BTECH', 'B.TECH', 'BACHELOR','BACHELORS','MASTER', 'MASTERS','M.TECH', 'MTECH'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)
    #print(nlp_text)
    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            #print(tex.upper(),"\n\n")
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                #print("Yes")
                edu[tex] = text + nlp_text[index + 1]
    #print(edu)
    # Extract year
    education = []
    #degree_year = 'Not specified'
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
            degree_year = ''.join(year[0])
            return degree_year
        #else:
            #education.append(key)
    #return education

DEGREE = [
            'B.E.', 
            'M.E', 'M.E.', 'MSC', "M.SC","BACHELOR OF TECHNOLOGY", "MASTER OF TECHNOLOGY",
            'BTECH', 'B.TECH','BACHELORS IN ENGINEERING','M.TECH', 'MTECH', "MASTERS",'BACHELOR OF SCIENCE','MASTERS'
        ]
def Degree(text):
    f = []
    for s in DEGREE:
        if s in text.upper():
            f.append(s.title())
    return list(set(f))
#------------------------------------------------------------------------------#
path = "/Users/praagraw/Downloads/Alisha/"
data = []
#data = pd.DataFrame(columns = ["FileName","FileContents","Name","Email Address","Contact Number","Experience","rank"])


k=0
####IMPORTING PDF ONLY
for filename in os.listdir(path):
    if filename.endswith(('.pdf')):
        #if filename != "1544684526313_Resume_Akshay_P.pdf":
            #continue
        print(filename)
        res = []
        res1 = []
        for page in extract_text_from_pdf(path, filename):
            
            res +="" +page
            res = ''.join(res)
            res = res.replace('\n', ' ')
            res = res.strip()
        for page in extract_text_from_pdf(path, filename):
            
            res1 +="" +page
            res1 = ''.join(res1)
            
            
        #print(res1)

        
        name= extract_names(res)
        #d = dict()
        #name = getName(res1,d)
        education = extract_education(res)
        #break
        email = extract_email_addresses(res)
        cno = extract_mobile_number(res)
        skills = extract_skill_set(res)
        exp= exper(res)
        degree = Degree(res)
        #print(exp)
        python_count,excel_count,vba_count,sql_count = count_skills(res)
        data.append({"FileName":filename, "FileContents":res, "Name":name, "Email Address":email, "Degree":degree, "Year of Graduation":education, "Skills":skills,"Contact Number":cno,"Experience": exp,"python_count":python_count,"excel_count":excel_count,"vba_count":vba_count,"sql_count":sql_count})
        df = pd.DataFrame(data, columns = ["FileName","FileContents","Name","Email Address","Degree","Year of Graduation","Contact Number","Skills","Experience","python_count","excel_count","vba_count","sql_count"])    
        df['Role1'] = df["Experience"].str.replace(r'[^\d.]+', '')
        df["Role1"] = pd.to_numeric(df["Role1"])
        df.loc[df['Role1'] >= 4 , 'Role'] = "Associate"
        df.loc[df['Role1'].isnull() , 'Role'] = "Not specified"
        df.loc[df['Role1'] < 4, 'Role'] = "Analyst"
        df = df.drop(['Role1'], axis=1)
        df.to_csv("resumes_filter12.csv", index=False)
    