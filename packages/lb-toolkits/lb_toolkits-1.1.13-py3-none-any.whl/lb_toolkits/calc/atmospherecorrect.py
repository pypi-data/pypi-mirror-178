from pyspectral.rayleigh import Rayleigh


def refldata(saz, saa, soz, soa, bandname):
    """
根据太阳天顶角，卫星天顶角，相对方位角，计算得到校正系数
    :param saz: 卫星天顶角
    :param saa: 卫星方位角
    :param soz: 太阳天顶角
    :param soa: 太阳方位角
    :param bandname: 波段名称
    :return:
    """
    # 计算相对方位角
    ssadiff = np.abs(saa - soa)
    ssadiff[ssadiff > 180] = 360 - ssadiff[ssadiff > 180]

    mersi = Rayleigh('FY-3D', 'mersi-2')
    refl_cor = mersi.get_reflectance(soz, saz, ssadiff, bandname)

    # 修正
    refl_cor_revise = refl_cor * np.cos(soz * np.pi / 180)
    refl_cor_revise[soz > 90] = 0
    return refl_cor_revise
    
    
    # 调用大气校正
    accor_blue = refldata(saz, saa, soz, soa, 'ch1')
    
    # # 利用大气校正系数进行大气校正
    blueBand_refl = blueBand - accor_blue / 100.0


#! usr/bin/env python
# -*- coding:utf-8 -*-
# AtmosphericCorrection for Landsat8

import glob
import os
import sys
import tarfile
import re

from osgeo import gdal, gdalconst, osr, ogr

import numpy as np
from Py6S import *
from osgeo import gdal
import pdb
import shutil
import argparse
# from .base import MeanDEM

def MeanDEM(pointUL, pointDR):
    '''
    计算影像所在区域的平均高程.
    '''
    script_path = os.path.split(os.path.realpath(__file__))[0]
    dem_path = os.path.join(script_path, "GMTED2km.tif")

    try:
        DEMIDataSet = gdal.Open(dem_path)
    except Exception as e:
        raise e

    DEMBand = DEMIDataSet.GetRasterBand(1)
    geotransform = DEMIDataSet.GetGeoTransform()
    # DEM分辨率
    pixelWidth = geotransform[1]
    pixelHight = geotransform[5]

    # DEM起始点：左上角，X：经度，Y：纬度
    originX = geotransform[0]
    originY = geotransform[3]

    # 研究区左上角在DEM矩阵中的位置
    yoffset1 = int((originY - pointUL['lat']) / pixelWidth)
    xoffset1 = int((pointUL['lon'] - originX) / (-pixelHight))

    # 研究区右下角在DEM矩阵中的位置
    yoffset2 = int((originY - pointDR['lat']) / pixelWidth)
    xoffset2 = int((pointDR['lon'] - originX) / (-pixelHight))

    # 研究区矩阵行列数
    xx = xoffset2 - xoffset1
    yy = yoffset2 - yoffset1
    # 读取研究区内的数据，并计算高程
    DEMRasterData = DEMBand.ReadAsArray(xoffset1, yoffset1, xx, yy)

    MeanAltitude = np.mean(DEMRasterData)
    return MeanAltitude

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--Input_dir',type=str,help='Input dir',default=None)
    parser.add_argument('--Output_dir',type=str,help='Output dir',default=None)

    return parser.parse_args(argv)

# 逐波段辐射定标
def RadiometricCalibration(BandId):
    # LandSat8 TM辐射定标参数
    global data2,ImgRasterData
    parameter_OLI = np.zeros((9,2))

    #计算辐射亮度参数
    parameter_OLI[0,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_1.+',data2)[0]).split("=")[1])
    parameter_OLI[1,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_2.+',data2)).split("=")[1])
    parameter_OLI[2,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_3.+',data2)).split("=")[1])
    parameter_OLI[3,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_4.+',data2)).split("=")[1])
    parameter_OLI[4,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_5.+',data2)).split("=")[1])
    parameter_OLI[5,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_6.+',data2)).split("=")[1])
    parameter_OLI[6,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_7.+',data2)).split("=")[1])
    parameter_OLI[7,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_8.+',data2)).split("=")[1])
    parameter_OLI[8,0] = float(''.join(re.findall('RADIANCE_MULT_BAND_9.+',data2)).split("=")[1])

    parameter_OLI[0,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_1.+',data2)[0]).split("=")[1])
    parameter_OLI[1,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_2.+',data2)).split("=")[1])
    parameter_OLI[2,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_3.+',data2)).split("=")[1])
    parameter_OLI[3,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_4.+',data2)).split("=")[1])
    parameter_OLI[4,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_5.+',data2)).split("=")[1])
    parameter_OLI[5,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_6.+',data2)).split("=")[1])
    parameter_OLI[6,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_7.+',data2)).split("=")[1])
    parameter_OLI[7,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_8.+',data2)).split("=")[1])
    parameter_OLI[8,1] = float(''.join(re.findall('RADIANCE_ADD_BAND_9.+',data2)).split("=")[1])

    Gain = parameter_OLI[int(BandId) - 1,0]
    Bias = parameter_OLI[int(BandId) - 1,1]

    RaCal = np.where(ImgRasterData>0 ,Gain * ImgRasterData + Bias,-9999)
    return (RaCal)

# 6s大气校正
def AtmosphericCorrection(BandId):
    global data
    # 6S模型
    s = SixS()

    s.geometry = Geometry.User()
    s.geometry.solar_z = 90-float(''.join(re.findall('SUN_ELEVATION.+',data2)).split("=")[1])
    s.geometry.solar_a = float(''.join(re.findall('SUN_AZIMUTH.+',data2)).split("=")[1])
    s.geometry.view_z = 0
    s.geometry.view_a = 0


    # 日期
    Dateparm = ''.join(re.findall('DATE_ACQUIRED.+',data2)).split("=")
    Date = Dateparm[1].split('-')

    s.geometry.month = int(Date[1])
    s.geometry.day = int(Date[2])

    # 中心经纬度
    point1lat = float(''.join(re.findall('CORNER_UL_LAT_PRODUCT.+',data2)).split("=")[1])
    point1lon = float(''.join(re.findall('CORNER_UL_LON_PRODUCT.+',data2)).split("=")[1])
    point2lat = float(''.join(re.findall('CORNER_UR_LAT_PRODUCT.+',data2)).split("=")[1])
    point2lon = float(''.join(re.findall('CORNER_UR_LON_PRODUCT.+',data2)).split("=")[1])
    point3lat = float(''.join(re.findall('CORNER_LL_LAT_PRODUCT.+',data2)).split("=")[1])
    point3lon = float(''.join(re.findall('CORNER_LL_LON_PRODUCT.+',data2)).split("=")[1])
    point4lat = float(''.join(re.findall('CORNER_LR_LAT_PRODUCT.+',data2)).split("=")[1])
    point4lon = float(''.join(re.findall('CORNER_LR_LON_PRODUCT.+',data2)).split("=")[1])

    sLongitude = (point1lon + point2lon + point3lon + point4lon) / 4
    sLatitude = (point1lat + point2lat + point3lat + point4lat) / 4

    # 大气模式类型
    if sLatitude > -15 and sLatitude <= 15:
        s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.Tropical)

    if sLatitude > 15 and sLatitude <= 45:
        if s.geometry.month > 4 and s.geometry.month <= 9:
            s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeSummer)
        else:
            s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.MidlatitudeWinter)

    if sLatitude > 45 and sLatitude <= 60:
        if s.geometry.month > 4 and s.geometry.month <= 9:
            s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.SubarcticSummer)
        else:
            s.atmos_profile = AtmosProfile.PredefinedType(AtmosProfile.SubarcticWinter)

    # 气溶胶类型大陆
    s.aero_profile = AtmosProfile.PredefinedType(AeroProfile.Continental)

    # 目标地物？？？？？？
    s.ground_reflectance = GroundReflectance.HomogeneousLambertian(0.36)

    # 550nm气溶胶光学厚度,根据日期从MODIS处获取。
    #s.visibility=40.0
    s.aot550 = 0.14497

    # 通过研究去区的范围去求DEM高度。
    pointUL = dict()
    pointDR = dict()
    pointUL["lat"] = point1lat
    pointUL["lon"] = point1lon
    pointDR["lat"] = point4lat
    pointDR["lon"] = point2lon
    meanDEM = (MeanDEM(pointUL, pointDR)) * 0.001

    # 研究区海拔、卫星传感器轨道高度
    s.altitudes = Altitudes()
    s.altitudes.set_target_custom_altitude(meanDEM)
    s.altitudes.set_sensor_satellite_level()

    # 校正波段（根据波段名称）
    if BandId == '1':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B1)

    elif BandId == '2':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B2)

    elif BandId == '3':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B3)

    elif BandId == '4':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B4)

    elif BandId == '5':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B5)

    elif BandId == '6':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B6)

    elif BandId == '7':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B7)

    elif BandId == '8':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B8)

    elif BandId == '9':
        s.wavelength = Wavelength(PredefinedWavelengths.LANDSAT_OLI_B9)

    # 下垫面非均一、朗伯体
    s.atmos_corr = AtmosCorr.AtmosCorrLambertianFromReflectance(-0.1)

    # 运行6s大气模型
    s.run()

    xa = s.outputs.coef_xa
    xb = s.outputs.coef_xb
    xc = s.outputs.coef_xc
    x = s.outputs.values
    return (xa, xb, xc)

if __name__ == '__main__':

    #输入数据路径
    # RootInputPath = parse_arguments(sys.argv[1:]).Input_dir
    # RootOutName = parse_arguments(sys.argv[2:]).Output_dir

    RootInputPath = r'D:\DATA\LC08_L1TP_143030_20200831_20200906_01_T1'
    RootOutName = r'./'
    #创建日志文件
    LogFile = open(os.path.join(RootOutName,'log.txt'),'w')

    for root,dirs,RSFiles in os.walk(RootInputPath):

        #判断是否进入最底层
        if len(dirs)==0:
            #根据输入输出路径建立生成新文件的路径
            RootInputPathList = RootInputPath.split(os.path.sep)
            RootList = root.split(os.path.sep)
            StartList = len(RootInputPathList)
            EndList = len(RootList)
            outname = RootOutName
            for i in range(StartList,EndList):
                if os.path.exists(os.path.join(outname,RootList[i]))==False:
                    os.makedirs(os.path.join(outname,RootList[i]))
                    outname=os.path.join(outname,RootList[i])
                else:
                    outname=os.path.join(outname,RootList[i])

            MeteDatas = glob.glob(os.path.join(root,'*MTL.txt'))

            for MeteData in MeteDatas:
                pass

            f = open(MeteData)
            data = f.readlines()
            data2 =' '.join(data)

            shutil.copyfile(MeteData,os.path.join(outname,os.path.basename(MeteData)))

            if len(os.path.basename(MeteData))<10:

                RSbands = glob.glob(os.path.join(root,"B0[1-8].tiff"))
            else:
                RSbands = glob.glob(os.path.join(root,"*B[1-8].TIF"))
            print('影像'+root+'开始大气校正')
            print(RSbands)
            for tifFile in RSbands:

                BandId = (os.path.basename(tifFile).split('.')[0])[-1]

                #捕捉打开数据出错异常
                try:
                    IDataSet = gdal.Open(tifFile)
                except Exception as e:
                    print("文件%S打开失败" % tifFile)
                    LogFile.write('\n'+tifFile+'数据打开失败')

                if IDataSet == None:
                    LogFile.write('\n'+tifFile+'数据集读取为空')
                    continue
                else:
                    #获取行列号
                    cols = IDataSet.RasterXSize
                    rows = IDataSet.RasterYSize
                    ImgBand = IDataSet.GetRasterBand(1)
                    ImgRasterData = ImgBand.ReadAsArray(0, 0, cols, rows)

                    if ImgRasterData is None:
                        LogFile.write('\n'+tifFile+'栅格数据为空')
                        continue
                    else:
                        #设置输出文件路径
                        outFilename=os.path.join(outname,os.path.basename(tifFile))

                        #如果文件存在就跳过，进行下一波段操作
                        if os.path.isfile(outFilename):
                            print("%s已经完成" % outFilename)
                            continue
                        else:
                            # #辐射校正
                            RaCalRaster = RadiometricCalibration(BandId)
                            #大气校正
                            a, b, c = AtmosphericCorrection(BandId)
                            y = np.where(RaCalRaster!=-9999,a * RaCalRaster - b,-9999)
                            atc = np.where(y!=-9999,(y / (1 + y * c))*10000,-9999)

                            driver = IDataSet.GetDriver()
                            #输出栅格数据集
                            outDataset = driver.Create(outFilename, cols, rows, 1, gdal.GDT_Int16)

                            # 设置投影信息，与原数据一样
                            geoTransform = IDataSet.GetGeoTransform()
                            outDataset.SetGeoTransform(geoTransform)
                            proj = IDataSet.GetProjection()
                            outDataset.SetProjection(proj)

                            outband = outDataset.GetRasterBand(1)
                            outband.SetNoDataValue(-9999)
                            outband.WriteArray(atc, 0, 0)
                print('第%s波段计算完成'%BandId)
            # print(root+'计算完成')
            print('\n')
    #关闭日志文件
    LogFile.close()

