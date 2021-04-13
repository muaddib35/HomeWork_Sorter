# -*- coding:utf-8 -*-

import glob
import os
import pandas as pd
import shutil

START_DIR = "dosyalar" # zip dosyasının açıldığı klasör
TARGET_DIR = "homeworks" # dosyaların eğiticilere dağıtılacağı ana dizin




ASSIGNMENTS = [
        {'Instructor': 'Murat Çizmecioğlu', 'dirname': 'murat', 'selections': [0,1,2]},
        {'Instructor': 'Güneş Çoban', 'dirname': 'gunes', 'selections': [3,4,5]},
        {'Instructor': 'Özlem Akgül', 'dirname': 'ozlem', 'selections': [6,7]},
        {'Instructor': 'Ayşe Hande Tarıkoğulları', 'dirname': 'ayse', 'selections': [8]},
        {'Instructor': 'Şirin Uysal', 'dirname': 'sirin', 'selections': [9]},
]


def FindInstructor(StudentNumber, InstructorList):
    stringNumber = str(StudentNumber)
    lastdigit = int(stringNumber[-1])
    for instructor in InstructorList:
        try:
            a = instructor['selections'].index(lastdigit)
            return instructor
        except ValueError:
            continue
            
def CopyFileToTarget(targetFile, DestinationFile):
    try:
        shutil.copyfile(targetFile,DestinationFile)
    except shutil.Error as err:
        print(err)
        return False
    except IOError as io_error:
        os.makedirs(os.path.dirname(DestinationFile))
        shutil.copyfile(targetFile,DestinationFile)
    return True

def Prepare_Student_List(classroomfile):
    df = pd.read_excel(os.path.join(classroomfile), engine='openpyxl')
    ogrenci_listesi = []
    for index  in df.index:
        objem = {'adsoyad': df['Adı'][index] + ' '+ df['Soyadı'][index], 'ogrenciNo': df['ID numarası'][index]}
        ogrenci_listesi.append(objem)
    return ogrenci_listesi

def Prepare_Directory_List(Startdir, Liste):
    directory_list = os.listdir(Startdir)
    total_dir_count = len(directory_list)
    for directory_name in directory_list:
        if os.path.isdir(os.path.join(Startdir,directory_name)):
            dir_StudentName = Analyze_Directory_Name(directory_name)
            OgrenciNo = SearchStudent(dir_StudentName, Liste)
            print('{} - {}'.format(OgrenciNo,dir_StudentName))
            files = glob.glob(os.path.join(Startdir,directory_name)+'/*')
            targetFile = os.path.basename(files[0])
            a = FindInstructor(OgrenciNo, ASSIGNMENTS)
            renamedFileName = '{:s}_{:s}_{:s}'.format(str(OgrenciNo),dir_StudentName,targetFile)
            if not CopyFileToTarget(files[0], os.path.join(TARGET_DIR,a['dirname'],renamedFileName)):
                print(targetFile)
                print(os.path.join(TARGET_DIR,a['dirname'],renamedFileName))
            
def SearchStudent(StudentNameSurname, Liste):
    a = filter(lambda item: item['adsoyad']==StudentNameSurname, Liste)
    for i in a:
        return i['ogrenciNo']
            
def Analyze_Directory_Name(DirName):
    StudentName = DirName.split('_')
    return StudentName[0]
    
liste = Prepare_Student_List('Sinif_Listesi.xlsx')
Prepare_Directory_List(START_DIR, liste)
