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
import PyPDF2
from pywintypes import com_error
import win32com.client as win32
import io
import docx2txt


from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import spacy

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


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # reading the csv file
    data = pd.read_csv("skills.csv") 
    # extract values
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


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
    if 'years' in h and 'months' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]+ " " +h[h.index('months')-1] + " " +h[h.index('months')]
    #elif 'year' in h:
        #d=h[h.index('year')-1] + " " + h[h.index('year')]
    elif 'years' in h:
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



def count_skills(doc,x):
    x = [i.lower() for i in x]
    a = doc.lower()
    a = re.sub('[^A-Za-z0-9]+', ' ', a)
    a = a.split()
    dic = {}
    dic['sl']= []
    dic['name'] = []
    dic['count'] = []
    for idx,i in enumerate(range(len(x))):
        dic['sl']=idx
        dic['name'].append(x[i])
        dic['count'].append(a.count(x[i]))
    dic= pd.DataFrame(dic)
    dic = pd.pivot_table(dic,values='count',index=['sl'], columns=['name']).reset_index()
    dic['score'] =  dic[dic.columns.difference(['sl'])].sum(axis=1)    
    dic['score'] = dic.sort_values('score',ascending=False)
    dic['rank'] =  list(range(len(dic)))
    dic['rank'] =  dic['rank']+1
    return (dic['rank'].values)

    
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
    nlp_text=nlp(document)
    pattern=[{'POS':'PROPN'},{'POS':'PROPN'}]
    matcher.add('NAME',None,pattern)
    matches=matcher(nlp_text)
    for match_id,start,end in matches:
        span=nlp_text[start:end]
        return span.text
#------------------------------------------------------------------------------#

def full_resume(inp):
    path = "C:\\Users\\PritamDevadattaJena\\Desktop\\alisha\\resumes\\"
    data = []
    data = pd.DataFrame(columns = ["FileName","FileContents","Name","Email Address","Contact Number","Experience","rank"])
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
            email = extract_email_addresses(res)
            cno = extract_mobile_number(res)
                #skills = extract_skill_set(res)
            exp= exper(res)
            count = count_skills(doc=res, x=inp)
            data = data.append({"FileName":filename, "FileContents":res, "Name":name, "Email Address":email,\
                    "Contact Number":cno,"Experience": exp,"rank":count},ignore_index=True)
            
            #df2 = pd.DataFrame(data, columns = ["FileName","FileContents","Name","Email Address","Contact Number","Experience"])    
            #df.to_csv("resumes_filter8.csv", index=False)
    return data

inp ='r,java'
output= full_resume(inp)