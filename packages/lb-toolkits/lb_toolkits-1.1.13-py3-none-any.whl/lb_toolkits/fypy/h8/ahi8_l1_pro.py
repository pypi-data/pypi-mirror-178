# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : ahi8_l1_pro.py

@Modify Time :  2022/11/10 14:45

@Author      : Lee

@Version     : 1.0

@Description :

'''

import os
import datetime
import time

import numpy as np
from .ahi8_read_hsd import ahi8_read_hsd
import glob


class ahi8_l1_pro(object):

    def __init__(self, filelist, bandid=None, obstype=None, tmppath=None):

        self.BandID = bandid
        self.ObsType = obstype
        self.tmpfile = []
        outdata = None

        for hsdname in filelist :
            if not os.path.isfile(hsdname):
                continue

            self._unzipped = self.unzip_file(hsdname, tmppath)
            if self._unzipped:
                # But if it is, set the filename to point to unzipped temp file
                self.is_zipped = True
                filename = self._unzipped

                self.tmpfile.append(filename)
            else:
                filename = hsdname

            if filename.endswith('.bz2') :
                print('unzip fail, will continue this file...')
                continue

            print(filename)

            # 根据块号对数据进行拼接
            SegmentNum, data = self.readhsd(filename)
            if outdata is None :
                line, pixel = data.shape
                outdata = np.full(shape=(line*self.SegmentTotal, pixel), fill_value=65535, dtype=np.uint16)

            data[np.isnan(data)] = 655.35
            outdata[(SegmentNum-1)*line:(SegmentNum)*line, :] = np.array(data*100, dtype=np.uint16)

        if outdata is None :
            self.data = None
        else:
            self.data = outdata
    def readhsd(self, filename):
        name = os.path.basename(filename)
        namelist = name.split('_')

        # self.NowTime = datetime.datetime.strptime('%s %s' % (namelist[2], namelist[3]), '%Y%m%d %H%M')
        # self.BandID = int(namelist[4][1:])
        # self.ObsType = namelist[5]
        # self.Resolution = float(namelist[6][1:])/1000.0
        SegmentNum = int(namelist[7][1:3])
        self.SegmentTotal = int(namelist[7][3:5])

        mahi8 = ahi8_read_hsd(filename, SegmentNum, self.SegmentTotal)
        if mahi8.data is None :
            mahi8 = ahi8_read_hsd(filename, SegmentNum, self.SegmentTotal)

        # self.regrow, self.regcol = mahi8.latlon2ij(H8_LAT, H8_LON)


        return SegmentNum, mahi8.data.values

    def unzip_file(self, filename, tmppath=None):
        from subprocess import Popen, PIPE
        from io import BytesIO
        from contextlib import closing
        import shutil
        import bz2

        try:
            from shutil import which
        except ImportError:
            # python 2 - won't be used, but needed for mocking in tests
            which = None

        """Unzip the file if file is bzipped = ending with 'bz2'."""
        # pathin = os.path.dirname(filename)
        # name = os.path.basename(filename)
        if filename.endswith('bz2'):
            # fdn, tmpfilepath = tempfile.mkstemp()
            if tmppath is None :
                tmpfilepath = filename.replace('.bz2','')
            else:
                tmpfilepath = os.path.join(tmppath, os.path.basename(filename).replace('.bz2',''))

            if os.path.isfile(tmpfilepath) :
                return tmpfilepath
            print("Using temp file for BZ2 decompression: %s", tmpfilepath)
            # try pbzip2
            pbzip = which('pbzip2')
            # Run external pbzip2
            if pbzip is not None:
                n_thr = os.environ.get('OMP_NUM_THREADS')
                if n_thr:
                    runner = [pbzip,
                              '-dc',
                              '-p'+str(n_thr),
                              filename]
                else:
                    runner = [pbzip,
                              '-dc',
                              filename]
                p = Popen(runner, stdout=PIPE, stderr=PIPE)
                stdout = BytesIO(p.communicate()[0])
                status = p.returncode
                if status != 0:
                    raise IOError("pbzip2 error '%s', failed, status=%d"
                                  % (filename, status))
                with closing(open(tmpfilepath, 'wb')) as ofpt:
                    try:
                        stdout.seek(0)
                        shutil.copyfileobj(stdout, ofpt)
                    except IOError:
                        import traceback
                        traceback.print_exc()
                        print("Failed to read bzipped file %s",
                              str(filename))
                        os.remove(tmpfilepath)

                return tmpfilepath

            # Otherwise, fall back to the original method
            bz2file = bz2.BZ2File(filename)
            with closing(open(tmpfilepath, 'wb')) as ofpt:
                try:
                    ofpt.write(bz2file.read())
                except IOError:
                    import traceback
                    traceback.print_exc()
                    print("Failed to read bzipped file %s", str(filename))
                    # os.remove(tmpfilepath)
                    return None
            return tmpfilepath

        return None

    def __del__(self):
        for filename in self.tmpfile :
            if os.path.isfile(filename) :
                try:
                    os.remove(filename)
                except BaseException as e :
                    print(e)
                    time.sleep(2)
                    try:
                        os.remove(filename)
                    except BaseException as e :
                        print(e)


def hsd2netcdf(outname, nowdate, hsdpath):
    tmppath = os.path.dirname(outname)
    if not os.path.isdir(tmppath) :
        tmppath = './'

    overwrite = 1
    # if os.path.isfile(outname) :
    #     return None

    # if not os.path.isdir(pathout) :
    #     os.makedirs(pathout)

    for chid in np.arange(1, 17) :

        # filelist=process(nowdate, dstpath='./data/', okpath='./data/', BandID=chid, ObsType='FLDK')
        filelist = glob.glob(os.path.join(hsdpath, nowdate.strftime('%Y%m%d'),
                            r'*HS_H08_%s_B%02d_FLDK_R*_S*.DAT.bz2' %(nowdate.strftime('%Y%m%d_%H%M'),chid)))
        if len(filelist) == 0:
            continue

        mpro = ahi8_l1_pro(filelist, bandid=chid, obstype='FLDK', tmppath=tmppath)
        data = mpro.data

        # writehdf(outname, 'band%02d' %(chid), data, overwrite=overwrite)
        # overwrite = 0
        # continue

        if data is not None:
            sdsinfo = {
                'scale_factor': 0.01,
                'add_offset': 0.0,
                '_fillvalue': 65535,
                'missing_value': 65535,
                'units': 'NUL',
                'standard_name': 'band%02d' %(chid),
                'long_name': 'band%02d' %(chid),
            }

            # if overwrite == 1 :
            #     lat = np.arange(ProjectionMaxLatitude, ProjectionMinLatitude, -ProjectionResolution)
            #     lon = np.arange(ProjectionMinLongitude, ProjectionMaxLongitude, ProjectionResolution)
            #     writenc(outname, 'latitude', lat, overwrite=1)
            #     writenc(outname, 'longitude', lon, overwrite=0)
            #     overwrite=0
            #
            # writenc(outname, 'band%02d' %(chid), data,
            #         dimension=('latitude', 'longitude'),
            #         dictsdsinfo=sdsinfo, overwrite=overwrite)


    # filename = r'D:\DATA\H8\L1\HS_H08_20210401_0000_B01_FLDK_R10_S0110.DAT.bz2'
    # ahi_l1_pro(filename)

if __name__ == '__main__':

    starttime = datetime.datetime.strptime('20190626000000', '%Y%m%d%H%M%S')
    endtime   = datetime.datetime.strptime('20190626040000', '%Y%m%d%H%M%S')

    while starttime <= endtime :

        hsdpath = r'O:\H8L1\hsd/'
        pathout = os.path.join(r'O:\H8L1\netcdf', starttime.strftime('%Y%m%d'))

        outname = os.path.join(pathout, 'HS_H08_%s_FLDK.nc' %(starttime.strftime('%Y%m%d_%H%M')))

        if os.path.isfile(outname) :
            print(outname+' is exist, will continue...')
            starttime += datetime.timedelta(minutes=10)
            continue

        if not os.path.isdir(pathout) :
            os.makedirs(pathout)

        hsd2netcdf(outname, starttime, hsdpath)
        starttime += datetime.timedelta(minutes=10)


# h8l1name = H8_BT_L1_Name.format(YYYY_MM_DD=nowdate.strftime('%Y%m%d'),
#                                 YYYYMMDD = nowdate.strftime('%Y%m%d'),
#                                 HHMM = nowdate.strftime('%H%M'))
#
# if not os.path.isfile(h8l1name) :
#     h8l1path = os.path.dirname(h8l1name)
#     if not os.path.isdir(h8l1path) :
#         os.makedirs(h8l1path)
#
#     hsd2netcdf(h8l1name, nowdate, H8_HSD_L1_Path)

