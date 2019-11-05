# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:25:19 2019

@author: PritamDevadattaJena
"""

#%% Packages
import os
import re
import pandas as pd
import numpy as np
#import nltk
import spacy
from spacy.matcher import Matcher
#from nltk.corpus import stopwords
nlp=spacy.load('en_core_web_sm')
matcher=Matcher(nlp.vocab)
from nltk.corpus import stopwords
import PyPDF2
import io
import docx2txt
from tkinter import *
from tkinter import filedialog
import comtypes.client
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import spacy
STOPWORDS = set(stopwords.words('english'))

print("all packages imported")
#%% FUNCTIONS

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
            
            
def extract_names(document):
    nlp_text=nlp(document)
    pattern=[{'POS':'PROPN'},{'POS':'PROPN'}]
    matcher.add('NAME',None,pattern)
    matches=matcher(nlp_text)
    for match_id,start,end in matches:
        span=nlp_text[start:end]
        return span.text.title()
    

def extract_email(text):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None    
        
def extract_mobile_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{7})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number      
        

def extract_skill_set(text):
    all_skills = {'Excel': ["Excel", "Advance Excel", "MS Excel", "Report", "Charts"], 
                  "VBA" : ["Visual Basic", "Visual Basic Application", "Macro", "Automation"], 
                  "Database": ["MS access", "Access Database", "SQL Server", "SQL", "SSIS"], 
                  "Power BI": ["Power BI", "Power Query", "Power Pivot"] , 
                  "Qlikview": ["Qlikview", "Set analysis","Minitab"], 
                  "QlikSense": ["QlikSense"], 
                  "Analytics": ["Machine Learning", "R"," market mix modelling","forecasting","Deep Learning", "AI", "Artificial Intelligence", "ML", "SVM", "SAS", "R programming","Python", "Decision tree", "Naïve Bayes", "k-NN", "SVM",
                                "logistic regression","linear regression","Recommendation System", "Random Forest" , "XgBoost","Ensemble Methods"],
                  "Sharepoint": ["Sharepoint"],
                  "Language" : ["C","C++"]} 
    
    skill_set = list(np.concatenate(list(all_skills.values()), axis=0 ))
    f = []
    for s in skill_set:
        #if re.search(s, text, re.I):
        if s.lower() in text.lower():
            if len(s)>2:
                f.append(s)
                #f.append(getKeysByValue(all_skills,s))
    return list(set(f))          


DEGREE = ['B.E.','B.E','PGDM', 'MSC', "M.SC","BACHELOR OF TECHNOLOGY",'MASTER OF SCIENCE',
            'BTECH', 'B.TECH','B TECH','BACHELORS IN ECONOMICS','BACHELORS IN ENGINEERING','M.TECH', 'MTECH','MASTERS IN BUSINESS ADMINISTRATION',
            ]

def degree(text):
    f = []
    for s in DEGREE:
        if re.search(r'\b' + s + r'\b', text.upper()):
           f.append(s.title())
    return list(set(f))


def extract_education_year(resume_text):
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
            if tex.upper() in DEGREE and tex not in STOPWORDS:
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
    d=[]
    if 'years' in h and 'months' in h:
        if h[h.index('years')-1].isdigit() ==True:
            d = h[h.index('years')-1] + " " + h[h.index('years')]+ " " +h[h.index('months')-1] + " " +h[h.index('months')]
        else:
            if int(h[h.index('months')-1]) >= 12:
                d = str(int(h[h.index('months')-1])/12) + " " + h[h.index('years')]
    elif 'years' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]
    elif 'months' in h:
        if int(h[h.index('months')-1]) >= 12:
            d = str(int(h[h.index('months')-1])/12) + " " + h[h.index('years')]
            #print('yay!')
        else:
            d = h[h.index('months')-1] + " " + h[h.index('months')]
    #elif 'month' in h:
    #   d=h[h.index('month')-1] + " " + h[h.index('month')]
    elif re.search('no experience',str(h),re.M|re.I) :
        d = 'No Experience'
    else:
        d = generate_ngrams(fullText, 2)
    return d


def location(text):
    l = []
    l.append([line for line in res.split(' ') if "location" in line])
    a= re.match('^.*(?P<zipcode>\d{6}).*$', res).groupdict()['zipcode']
    l.append([line for line in res.split(' ') if a in line])
    l.append([line for line in res.split(' ') if "address" in line])
    l.append([line for line in res.split(' ') if "india" in line])
    l = [item for sublist in l for item in sublist]
    return l
  
#%% Resume parsing
path = "C:\\Users\\PritamDevadattaJena\\Desktop\\Resume\\resume\\"
df = pd.DataFrame()
data = [] 
####IMPORTING PDF ONLY
for filename in os.listdir(path):
    if filename.endswith(('.pdf')):
        print(filename)
        res = []
        for page in extract_text_from_pdf(path, filename):
           
            res +="" +page
            res = ''.join(res)
            res = res.replace('\n', ' ')
            res = res.strip()
           
        name=extract_names(res)
        email = extract_email(res)
        cno = extract_mobile_number(res)
        skills = extract_skill_set(res)
        deg = degree(res)
        edu_year = extract_education_year(res)
        try:
            exp= re.findall(r"[-+]?\d*\.\d+|\d+", exper(res))
        except TypeError:
            pass           
        loc = location(res)
        #        python_count,excel_count,vba_count,sql_count = count_skills(res)
        data.append({"FileName":filename, "Name":name, "Email Address":email,"Contact Number":cno,"skills":skills,"Degree":deg,"Education year":edu_year,"Experience":exp,"Location": loc})
        df = pd.DataFrame(data, columns = ["FileName","Name","Email Address","Contact Number","skills","Degree","Education year","Experience","Location"])    
        #df.to_csv(path+"resumes_parser.csv", index=False)       
        
        



    

    
    


    
    
    


 
 