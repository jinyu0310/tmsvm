#!/usr/bin/python
#_*_ coding: utf-8 _*_
#author: 张知临 zhzhl202@163.com
#Filename: tms.py
'''tmsvm系统的入口程序.'''

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),"src"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),"dependence"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),"lsa_src"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),"tools"))
import train_model
import predict_model
import grid_search_param
import tms_svm
import result_analysis

def tms_train(filename,indexes=[1],main_save_path="../",stopword_filename="",svm_param="",config_name="tms.config",dic_name="dic.key",model_name="tms.model",train_name="svm.train",svm_type="libsvm",param_name="svm.param",ratio=0.4,delete=True,str_splitTag="^",tc_splitTag="\t",seg=0,param_select=True,global_fun="one",local_fun="tf"):
    '''训练的自动化程序，分词,先进行特征选择，重新定义词典，根据新的词典，自动选择SVM最优的参数。 然后使用最优的参数进行SVM分类，最后生成训练后的模型。
    需要保存的文件：（需定义一个主保存路径）
    必须参数：
     filename 训练文本所在的文件名
    结果文件：
         模型文件（词典.key+模型.model）和  临时文件（svm分类数据文件.train 和参数选择文件）
   可选参数： 
    indexs需要训练的指标项 ，默认为[1]
    main_save_path 模型保存的路径.默认为"../"
    stopword_filename 停用词的名称以及路径 ;默认不适用停用词
    svm_type :svm类型：libsvm 或liblinear 。默认为"libsvm"
    svm_param  用户自己设定的svm的参数,这个要区分libsvm与liblinear参数的限制。默认" " 
    config_name:模型配置文件的名称，默认为"tms.config"
    dic_name 用户自定义词典名称;默认“dic.key”
    model_name用户自定义模型名称 ;默认"svm.model"
    train_name用户自定义训练样本名称 ；默认“svm.train”
    param_name用户自定义参数文件名称 ；默认"svm.param"
    ratio 特征选择保留词的比例 ；默认 0.4
    delete对于所有特征值为0的样本是否删除,True or False，默认：True
    str_splitTag 分词所用的分割符号 ，默认"^"
    tc_splitTag训练样本中各个字段分割所用的符号 ，默认"\t"
    seg 分词的选择：0为不进行分词；1为使用mmseg分词；2为使用aliws分词，默认为0
    param_select ;是否进行SVM模型参数的搜索。True即为使用SVM模型grid.搜索，False即为不使用参数搜索。默认为True
    local_fun：即对特征向量计算特征权重时需要设定的计算方式:x(i,j) = local(i,j)*global(i).可选的有tf。默认为"tf"
    global_fun :全局权重的计算方式：有"one","idf","rf" ,默认为"one"
    '''
    train_model.ctm_train(filename, indexes, main_save_path, stopword_filename, svm_param, config_name, dic_name, model_name, train_name, svm_type, param_name, ratio, delete, str_splitTag, tc_splitTag, seg, param_select, global_fun, local_fun)

def tms_segment(filename,indexes=[1],out_filename="",str_splitTag="^",tc_splitTag="\t",seg=1):
    '''分词的主程序
        必须参数：
        filename 训练文本所在的文件名，默认情况下，已经分好词。
        可选参数： 
        indexs需要训练的指标项 ，默认为[1]
        out_filename:分词后的结果保存的文件,如果为""，则保存在和输入文件同目录下的"segmented".默认情况下""
        str_splitTag 分词所用的分割符号 ，默认"^"
        tc_splitTag训练样本中各个字段分割所用的符号 ，默认"\t"
        seg 分词的选择：0为不进行分词；1为使用mmseg分词；2为使用aliws分词，默认为0
    '''
    train_model.file_seg(filename, indexes, out_filename, str_splitTag, tc_splitTag, seg)
    
   
def tms_feature_select(filename,indexes=[1],global_fun="one",main_save_path="../",dic_name="dic.key",ratio=0.4,stopword_filename="",str_splitTag="^",tc_splitTag="\t"):
    '''特征选择的主程序，输入指定的文件，会自动生成词典，并根据卡方公式进行特征选择。
    必须参数：
        filename 训练文本所在的文件名，默认情况下，已经分好词。
    结果文件：
        词典。
   可选参数：
    indexs需要训练的指标项 ，默认为[1]
    main_save_path 模型保存的路径.默认为"../"
    stopword_filename 停用词的名称以及路径 ;默认不适用停用词
    dic_name 用户自定义词典名称;默认“dic.key”
    ratio 特征选择保留词的比例 ；默认 0.4
    str_splitTag 分词所用的分割符号 ，默认"^"
    tc_splitTag训练样本中各个字段分割所用的符号 ，默认"\t"
    global_fun :全局权重的计算方式：有"one","idf","rf" ,默认为"one"
    '''
    train_model.ctm_feature_select(filename, indexes, global_fun, main_save_path, dic_name, ratio, stopword_filename, str_splitTag, tc_splitTag)


def cons_train_sample_for_svm(filename,dic_path,sample_save_path="../svm.train",indexs=[1],local_fun="tf",delete=True,str_splitTag="^",tc_splitTag="\t"):
    '''将已经分好词的文件转换为libsvm和liblinear的输入格式。
    必须参数：
        filename 训练文本所在的文件名，默认情况下，已经分好词。
        dic_path 词典所在的目录，将文本转换为向量。
    可选参数：
    sample_save_path 。转换好的文件保存的位置。默认情况下为"../svm.train"
    indexs需要训练的指标项 ，默认为[1]
    local_fun：即对特征向量计算特征权重时需要设定的计算方式:x(i,j) = local(i,j)*global(i).可选的有tf。默认为"tf"
    delete对于所有特征值为0的样本是否删除,True or False，默认：True
    str_splitTag 分词所用的分割符号 ，默认"^"
    tc_splitTag训练样本中各个字段分割所用的符号 ，默认"\t"
    '''
    train_model.cons_train_sample_for_cla(filename, indexs, local_fun, dic_path, sample_save_path, delete, str_splitTag, tc_splitTag)
    
    
def tms_grid_param(problem_path, result_save_path="../svm.param", svm_type="libsvm", coarse_c_range=(-5,7,2), coarse_g_range=(3,-10,-2), fine_c_step=0.5, fine_g_step=0.5):
    '''对SVM的参数进行搜索,如果是libsvm则搜索(c,gamma)，如果是liblinear则搜索(c)。当训练样本的容量大于3000时就会在粗粒度搜索时使用子集，子集的大小为[3000,5000]范围内。
    当
    必须参数：
       problem_path：SVM输入格式文件的路径即名称。 
    可选参数:
       result_save_path:结果文件的保存路径:默认为"../svm.param"
       svm_type :选择的SVM的类型，默认为libsvm
       coarse_c_range ：粗粒度搜索时c搜索的范围，默认情况下为[-5,7],步长为2
       coarse_g_range：粗粒度搜索时g搜索的范围，默认情况下为[3,-10]步长为-2
       fine_c_step ：细粒度搜索时c的步长，默认情况下为0.5
       fine_c_step ：细粒度搜索时c的步长，默认情况下为0.5
    '''
    if svm_type=="liblinear":
       coarse_g_range=(1,1,1)
       fine_g_step=0
    c,g = grid_search_param.grid(problem_path, result_save_path, svm_type, coarse_c_range, coarse_g_range, fine_c_step, fine_g_step)
    print "best c=%s ,g=%s"%(c,g)
    return c,g

def tms_train_model(problem_path,svm_type="libsvm",param="",model_save_path="../svm.model"):
    '''训练模型程序。输入参数，可以训练libsvm与liblinear的模型。
    必须参数:
       problem_path :输入问题的路径即名称：
    可选参数 :
        svm_type :svm类型：libsvm 或liblinear 。默认为"libsvm"
        param  用户自己设定的svm的参数,这个要区分libsvm与liblinear参数的限制。默认" " 
        model_save_path :模型保存的路径,默认情况下路径为"../svm.model"
    '''
    tms_svm.set_svm_type(svm_type)
    train_model.ctm_train_model(problem_path, param, model_save_path)
    
def tms_predict(filename,config_file,result_save_path="../tms.result",indexes=[1],result_indexes=[0],str_splitTag="^",tc_splitTag="\t",seg=0,delete=False,change_decode=False,in_decode="UTF-8",out_encode="GBK"):
    '''模型预测程序.输入需要预测的文件，以及模型的配置文件，既可利用已经训练好的模型对文件进行预测。
    必须参数：
        filename：
    '''
    predict_model.ctm_predict(filename,config_file,indexes,result_save_path,result_indexes,str_splitTag,tc_splitTag,seg,delete=False,change_decode=False,in_decode="UTF-8",out_encode="GBK")

def tms_predict_multi(filename,config_files,indexes_lists,result_save_path="../tms.result",result_indexes=[0],str_splitTag="^",tc_splitTag="\t",seg=0,delete=False,change_decode=False,in_decode="UTF-8",out_encode="GBK"):
    predict_model.ctm_predict_multi(filename, config_files, indexes_lists, result_save_path, result_indexes, str_splitTag, tc_splitTag, seg, delete, change_decode, in_decode, out_encode)

def tms_analysis(filename,output_file="",indexes=[0,1,2],step=1,predicted_label_index=0,predicted_value_index=1,true_label_index=2,threshold=0.0,label=1,min=0,max=1):
    '''function 是值要选择进行分析的函数，其中1为cal_multi_rate（多类别模型的分类准确率）；2为cal_f（）'''
    ""
    "cal_f"
    "cal_f_binary"
    output=False
    if len(output_file)>1:
        output=True
        f = file(output_file,'w')
    min = min*10
    max = max*10
    X = result_analysis.read_result(filename,indexes)
    if step==1:
        rate,micro,macro = result_analysis.cal_rate([y[true_label_index] for y in X ],[y[predicted_label_index] for y in X ])
        if output==False:
            print "micro = %g,macro = %g" %(micro,macro)
            print rate
        else:
            f.write("micro = %g,macro = %g\n" %(micro,macro))
            f.write("各个类别的分类准确率")
            result_analysis.save_result(f,rate)
            
    if step==2:
        rate  = result_analysis.cal_f([y[true_label_index] for y in X ],[y[predicted_label_index] for y in X ])
        if output==False:
            print rate
        else:
            f.write("各个类别的F值、召回率、准确率")
            result_analysis.save_result(f,rate)

    if step==3:
        rate  = result_analysis.cal_f_by_threshold([y[true_label_index] for y in X ],[y[predicted_label_index] for y in X ],[y[predicted_value_index] for y in X],label,threshold)
        if output==False:
            print rate
        else:
            f.write("对特定类别的F值、召回率、准确率")
            result_analysis.save_result(f,rate)
            
    if step==4:
        rate = result_analysis.threshlod_anlysis([y[true_label_index] for y in X ],[y[predicted_label_index] for y in X ],[y[predicted_value_index] for y in X],first_range=[i/10.0 for i in range(min,max)])
        if output==False:
            print rate
        else:
            f.write("所有类别各个阈值下得F值、召回率、准确率")
            result_analysis.save_result(f,rate)
        
    if output ==True:
        f.close()