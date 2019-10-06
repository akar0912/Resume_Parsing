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
# from pywintypes import com_error
# import win32com.client as win32
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

def resume_filter():
 
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
        all_skills = {'Excel': ["Excel", "Advance Excel", "MS Excel", "Report", "Charts"], "VBA" : ["Visual Basic", "Visual Basic Application", "Macro", "Automation"], "Database": ["MS access", "Access Database", "SQL Server", "SQL", "SSIS"], "Power BI":["Power BI", "Power Query", "Power Pivot"] , "Qlikview":["Qlikview", "Set analysis"], "QlikSense":["QlikSense"], "Analytics":["Machine Learning", "Deep Learning", "AI", "Artificial Intelligence", "ML", "SVM", "SAS", "R programming","Python"], "Sharepoint":["Sharepoint"]} 
        skill_set = list(np.concatenate(list(all_skills.values()), axis=0 ))
        f = []
        for s in skill_set:
            #if re.search(s, text, re.I):
            if s.lower() in text.lower():
                if len(s)>2:
                    f.append(s)
                    #f.append(getKeysByValue(all_skills,s))
        return list(set(f))

    # def extract_skill_set(text):
    #     with open("C:\\Users\\PritamDevadattaJena\\Desktop\\alisha\\skills.txt","r") as skill:
    #         skill_set = skill.read().split("\n")    
    #     f = []
    #     for s in skill_set:
    #         #if re.search(s, text, re.I):
    #         if s in text:
    #             if len(s)>2:
    #                 f.append(s)
       
    #     return f
 
 
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
        nlp_text=nlp(document)
        pattern=[{'POS':'PROPN'},{'POS':'PROPN'}]
        matcher.add('NAME',None,pattern)
        matches=matcher(nlp_text)
        for match_id,start,end in matches:
            span=nlp_text[start:end]
            return span.text
    #------------------------------------------------------------------------------#
    path = "C:\\Users\\LENOVO\\Desktop\\res\\resume\\"
    data = []
    #data = pd.DataFrame(columns = ["FileName","FileContents","Name","Email Address","Contact Number","Experience","rank"])
 
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
            skills = extract_skill_set(res)
            exp= exper(res)
            python_count,excel_count,vba_count,sql_count = count_skills(res)
            data.append({"FileName":filename, "FileContents":res, "Name":name, "Email Address":email,"Skills":skills,"Contact Number":cno,"Experience": exp,"python_count":python_count,"excel_count":excel_count,"vba_count":vba_count,"sql_count":sql_count})
            df = pd.DataFrame(data, columns = ["FileName","FileContents","Name","Email Address","Contact Number","Skills","Experience","python_count","excel_count","vba_count","sql_count"])    
            df.to_csv(path+"resumes_filter10.csv", index=False)
 
def browsefunc():
    path = filedialog.askdirectory()
    path = os.path.abspath(os.path.expanduser(path))
    pathlabel.config(text=path)
 
def CreatePDF():
 
    path = "C:\\Users\\LENOVO\\Desktop\\res\\resume\\"
    list_file=[]
 
    for filename in os.listdir(path):
        if filename in list_file:
            break
        if filename.endswith('.doc') or filename.endswith('.docx'):
            list_file.append(filename)
            print(filename)
            head,sep,tail = filename.partition('.')
            wdFormatPDF = 17
 
            in_file = os.path.abspath(path + filename)
            out_file = os.path.abspath(path + head + ".pdf")
 
            word = comtypes.client.CreateObject("Word.Application")
            doc = word.Documents.Open(in_file)
            doc.SaveAs(out_file,FileFormat = wdFormatPDF)
            doc.Close()
            word.Quit()
 
 
 
class TKGUI:
    def __init__(self):
        self.root= Tk() ##initilise the main window
        self.quit = False ##defaults the quit flag
        self.root.title("Resume Filter")
        self.root.geometry("500x350")
    def clear_root(self):
        children = self.root.winfo_children()
        for child in children:
            child.pack_forget()
            child.destroy()
       
    def save_skills(self, event, v1, v2, v3, v4, v5):
        varstates ="Python: %d,\nR: %d,\nQlikview: %d,\nVBA: %d,\nExcel: %d" % (v1.get(), v2.get(),v3.get(),v4.get(),v5.get())
        with open("C:\\Users\\LENOVO\\Desktop\\res\\resume\\output.txt","w") as f:
            f.write(varstates)
        #with open("C:\\Users\\LENOVO\\Desktop\\res\\resume\\output.txt","r") as f:
            #print(f.read())
       
        d = dict()
        skills = []
        path = "C:\\Users\\LENOVO\\Desktop\\res\\resume\\"
        data = pd.read_csv(path + "resumes_filter10.csv")
        with open(path + "output.txt", 'r') as f:
            for line in f:
                y = line.split()
                z = "".join(y)
                z = z.replace(",","")
                a,b = z.split(":")
                if(b == '1'):
                    skills.append(a)
        data2 = pd.DataFrame(columns= data.columns)
        for s in skills:
            indices = data["Skills"].str.contains(s)
            b = data[indices]
            data2 = data2.append(b)
        data2.drop_duplicates(inplace=True)
        data2.to_csv(path+"shortlisted_resumes.csv",index=False)
        print(path+"shortlisted_resumes.csv")
 
    def skills(self):
        self.clear_root()
       
        self.root.title("Skills")
        self.root.geometry("300x250")
       
        var1 = IntVar()
        check1 = Checkbutton(self.root, text="Python", variable=var1)
        check1.pack() ## useing pack because you are not being fancy and its easier to use.
        var2 = IntVar()
        check2 = Checkbutton(self.root, text="R", variable=var2)
        check2.pack()
        var3 = IntVar()
        check3 = Checkbutton(self.root, text="Qlikview", variable=var3)
        check3.pack()
        var4 = IntVar()
        check4 = Checkbutton(self.root, text="VBA", variable=var4)
        check4.pack()
        var5 = IntVar()
        check5 = Checkbutton(self.root, text="Excel", variable=var5)
        check5.pack()
       
        Button(self.root, text="Save Skills", command=lambda e=Event(), v1=var1, v2=var2, v3=var3, v4=var4, v5=var5: self.save_skills(e, v1 ,v2 ,v3, v4, v5)).pack()
        Button(self.root, text="Back", command=self.main_GUI).pack()
       
    def main_GUI(self):
        self.clear_root()
        self.root.title("Resume Filter")
        self.root.geometry("500x350")
       
       
        top_frame = Frame(self.root) #if you have pack on the same line then it returns "None" and not the widget
        top_frame.pack()
        bottom_frame = Frame(self.root)
        bottom_frame.pack(side = "bottom")
 
        btn1 = Button(top_frame,text = "filelocation", command=browsefunc)
        btn1.pack()
        pathlabel = Label(self.root)
        pathlabel.pack()
 
        Button(top_frame,text = "Convert any file to PDF",command = CreatePDF).pack() # you do not need to assigne a variable to a button unless you want to use it elsewhere
 
        Button(top_frame,text = "Press Enter",command = resume_filter).pack()
 
        Button(top_frame,text = "Enter Skills",command = self.skills).pack()

 
    def run(self): ##main part of the application
        self.root.configure(bg="white") #sets the background to white rather than default gray.
        self.root.protocol("WM_DELETE_WINDOW", self.quitting) ##changes the X (close) Button to run a function instead.
 
       
        self.main_GUI()
       
       
       
        while not self.quit: ##flag to quit the application
            self.root.update_idletasks() #updates the root. same as root.mainloop() but safer and interruptable
            self.root.update() #same as above. This lest you stop the loop or add things to the loop.
            #add extra functions here if you need them to run with the loop#
 
    def quitting(self): ##to set the quit flag
        self.quit = True
           
if __name__ == "__main__":
    app = TKGUI() ##creates instance of GUI class
    try:
        app.run()# starts the application
    except KeyboardInterrupt:
        app.quitting() ##safely quits the application when crtl+C is pressed
    except:
        raise #you can change this to be your own error handler if needed