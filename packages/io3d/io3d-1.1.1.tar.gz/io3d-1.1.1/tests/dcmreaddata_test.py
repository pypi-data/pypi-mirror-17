#! /usr/bin/python
# -*- coding: utf-8 -*-


# import funkcí z jiného adresáře
# import sys
import os.path
# import copy

import unittest
from nose.plugins.attrib import attr
path_to_script = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.join(path_to_script, "../extern/pyseg_base/src/"))
# sys.path.append(os.path.join(path_to_script, "../extern/py3DSeedEditor/"))
# sys.path.append(os.path.join(path_to_script, "../src/"))

# from PyQt4.QtGui import QFileDialog, QApplication, QMainWindow

import numpy as np

import dicom
dicom.debug(False)

#
import io3d
import io3d.dcmreaddata as dcmr


class DicomReaderTest(unittest.TestCase):
    interactivetTest = False
#    def setUp(self):
#        self.dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
# self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
#        reader = dcmr.DicomReader(self.dcmdir)
#        self.data3d = reader.get_3Ddata()
#        self.metadata = reader.get_metaData()

    def test_dicomread_read(self):
        dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
        #dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        #self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        data3d, metadata = io3d.datareader.read(dcmdir)
#slice size is 512x512
        self.assertEqual(data3d.shape[2],512)
# voxelsize depth = 5 mm
        self.assertEqual(metadata['voxelsize_mm'][0],5)

    def test_dicomread_read_corrupted_dcmdir_file(self):
        dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
        pth_dicomdir = os.path.join(
                path_to_script, '../sample_data/jatra_5mm/dicomdir.pkl')
        pth_dicomdir_bck = os.path.join(
                path_to_script, '../sample_data/jatra_5mm/dicomdir.pkl.bck')
        import shutil
# Backup file
        shutil.copy2(pth_dicomdir, pth_dicomdir_bck)
# create corrupted file

        f = open(pth_dicomdir, 'w')
        f.write('asdfasdfas')
        f.close()

        #dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        #self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        data3d, metadata = io3d.datareader.read(dcmdir)
#slice size is 512x512
        self.assertEqual(data3d.shape[2],512)
# voxelsize depth = 5 mm
        self.assertEqual(metadata['voxelsize_mm'][0], 5)
        shutil.copy2(pth_dicomdir_bck, pth_dicomdir)

    def test_DicomReader_overlay(self):
        # import matplotlib.pyplot as plt

        dcmdir = os.path.join(path_to_script, '../sample_data/volumetrie/')
        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        reader = dcmr.DicomReader(dcmdir)
        overlay = reader.get_overlay()
        # import pdb; pdb.set_trace()
        # plt.imshow(overlay[1][:,:,0])
        # plt.show()

        self. assertEqual(overlay[1][0, 200, 200], 1)
        self. assertEqual(overlay[1][0, 100, 100], 0)

    def test_read_volumetry_overlay_with_dicom_module(self):
        """
        pydicom module is used for load dicom data. Dicom overlay
        is saved on (60xx,3000) bit after bit. Data are decoded and
        each bit is stored as array element.
        """
        import dicom
        # import py3DSeedEditor
        # import matplotlib.pyplot as plt
        dcmfile = os.path.join(
            path_to_script, '../sample_data/volumetrie/volumetry_slice.DCM')
        data = dicom.read_file(dcmfile)

        # overlay index
        i_overlay = 1
        n_bits = 8

        # On (60xx,3000) are stored ovelays.
        # First is (6000,3000), second (6002,3000), third (6004,3000),
        # and so on.
        dicom_tag1 = 0x6000 + 2 * i_overlay

        overlay_raw = data[dicom_tag1, 0x3000].value

        # On (60xx,0010) and (60xx,0011) is stored overlay size
        rows = data[dicom_tag1, 0x0010].value  # rows = 512
        cols = data[dicom_tag1, 0x0011].value  # cols = 512

        decoded_linear = np.zeros(len(overlay_raw) * n_bits)

        # Decoding data. Each bit is stored as array element
        for i in range(1, len(overlay_raw)):
            for k in range(0, n_bits):
                byte_as_int = ord(overlay_raw[i])
                decoded_linear[i * n_bits + k] = (byte_as_int >> k) & 0b1

        # overlay = np.array(pol)

        overlay = np.reshape(decoded_linear, [rows, cols])

        # plt.imshow(overlay)
        # plt.show()

        self. assertEqual(overlay[200, 200], 1)
        self. assertEqual(overlay[100, 100], 0)
        # pyed = py3DSeedEditor.py3DSeedEditor(overlay)
        # pyed.show()
        # import pdb; pdb.set_trace()

    def test_dcmread(self):

        dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        reader = dcmr.DicomReader(dcmdir)
        data3d = reader.get_3Ddata()
        metadata = reader.get_metaData()
        stats = reader.dcmdirstats()
        info_str = reader.print_series_info(stats, minimal_series_number=0)

# slice size is 512x512
        self.assertEqual(data3d.shape[2], 512)
# voxelsize depth = 5 mm
        self.assertEqual(metadata['voxelsize_mm'][0], 5)
        # test stats
        self.assertEqual(stats[7]['Modality'], 'CT')
        self.assertTrue(info_str,
                        '7 (93, CT, DE_Abdom_1F  5.0  B30f M_0.3, )\n')

    def test_dcmread_series_number(self):

        dcmdir = os.path.join(path_to_script, '../sample_data/jatra_5mm')
        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
# spravne cislo serie je 7
        reader = dcmr.DicomReader(dcmdir, series_number=7)
        data3d = reader.get_3Ddata()
        metadata = reader.get_metaData()
        self.assertEqual(data3d.shape[2], 512)
        self.assertEqual(metadata['voxelsize_mm'][0], 5)

    @unittest.skipIf(not interactivetTest, 'interactiveTest')
    def test_dcmread_select_series(self):

        # dirpath = dcmr.get_dcmdir_qt()
        dirpath = '/home/mjirik/data/medical/data_orig/46328096/'
        # dirpath = dcmr.get_dcmdir_qt()
        # app = QMainWindow()
        reader = dcmr.DicomReader(
            dirpath, series_number=55555)  # , #qt_app =app)
        # app.exit()
        self.data3d = reader.get_3Ddata()
        self.metadata = reader.get_metaData()

    # @unittest.skipIf(not interactivetTest, 'interactiveTest')
    @unittest.skip('skip')
    def test_dcmread_get_dcmdir_qt(self):

        dirpath = dcmr.get_dcmdir_qt()
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        reader = dcmr.DicomReader(dirpath)
        self.data3d = reader.get_3Ddata()
        self.metadata = reader.get_metaData()

        # sss.visualization()
        # import pdb; pdb.set_trace()

    # @attr('actual')
    def test_is_dicomdir(self):
        """
        files in vincentka_sample have no extension
        """
        dcmdir = 'sample_data/vincentka_sample/'
        self.assertTrue(dcmr.is_dicom_dir(dcmdir))

    @attr('actual')
    def test_compare_dcmread_and_dataread(self):

        # dcmdir = os.path.join(path_to_script, '../vincentka_2013_06mm/')
        dcmdir = 'sample_data/vincentka_sample/'
        # dcmdir = '/home/mjirik/data/medical/data_orig/jatra-kma/jatra_5mm/'
        # self.data3d, self.metadata = dcmr.dcm_read_from_dir(self.dcmdir)
        reader = dcmr.DicomReader(dcmdir)
        data3d = reader.get_3Ddata()
        # metadata = reader.get_metaData()
        # import sed3
        # ed = sed3.sed3(data3d)
        # ed.show()

        import io3d
        dr = io3d.datareader.DataReader()
        datap = dr.Get3DData(dcmdir, dataplus_format=True)
        ddata3d = datap['data3d']
        # import sed3
        # ed = sed3.sed3(ddata3d)
        # ed.show()
        self.assertEqual(
            0,
            np.sum(np.abs(ddata3d - data3d))
        )

# slice size is 512x512
        # self.assertEqual(data3d.shape[2], 512)
# voxelsize depth = 5 mm
        # self.assertEqual(metadata['voxelsize_mm'][0], 5)

    def test_jpeg_series(self):
        # import io3d
        # import ipdb
        # ipdb.set_trace()  # noqa BREAKPOINT

        pass

#    def test_synthetic_data_lesions_automatic_localization(self):
#        """
#        Function uses lesions  automatic localization in synthetic data.
#        """
# dcmdir =
# os.path.join(path_to_script,'./../sample_data/matlab/examples/sample_data/DICOM/digest_article/') # noqa
#
# data
#        slab = {'none':0, 'liver':1, 'porta':2, 'lesions':6}
#        voxelsize_mm = np.array([1.0,1.0,1.2])
#
#        segm = np.zeros([256,256,80], dtype=np.int16)
#
# liver
#        segm[70:190,40:220,30:60] = slab['liver']
# port
#        segm[120:130,70:220,40:45] = slab['porta']
#        segm[80:130,100:110,40:45] = slab['porta']
#        segm[120:170,130:135,40:44] = slab['porta']
#
# vytvoření kopie segmentace - před určením lézí
#        segm_pre = copy.copy(segm)
#
#        segm[150:180,70:105,42:55] = slab['lesions']
#
#
#        data3d = np.zeros(segm.shape)
#        data3d[segm== slab['none']] = 680
#        data3d[segm== slab['liver']] = 1180
#        data3d[segm== slab['porta']] = 1230
#        data3d[segm== slab['lesions']] = 1110
# noise = (np.random.rand(segm.shape[0], segm.shape[1], segm.shape[2])*30).astype(np.int16) # noqa
# noise = (np.random.normal(0,30,segm.shape))#.astype(np.int16)
#        data3d = (data3d + noise  ).astype(np.int16)
#
#
#        data={'data3d':data3d,
#                'slab':slab,
#                'voxelsize_mm':voxelsize_mm,
#                'segmentation':segm_pre
#                }
#
# @TODO je tam bug, prohlížeč neumí korektně pracovat s doubly
# app = QApplication(sys.argv)
# pyed = QTSeedEditor(noise )
# pyed = QTSeedEditor(data3d)
# pyed.exec_()
# img3d = np.zeros([256,256,80], dtype=np.int16)
#
# pyed = py3DSeedEditor.py3DSeedEditor(data3d)
# pyed.show()
#
#        tumory = lesions.Lesions()
#
#        tumory.import_data(data)
#        tumory.automatic_localization()
# tumory.visualization()
#
#
#
# ověření výsledku
# pyed = py3DSeedEditor.py3DSeedEditor(outputTmp, contour=segm==slab['porta'])
# pyed.show()
#
#        errim = np.abs(
#                (tumory.segmentation == slab['lesions']).astype(np.int) -
#                (segm == slab['lesions']).astype(np.int))
#
# ověření výsledku
# pyed = py3DSeedEditor.py3DSeedEditor(errim, contour=segm==slab['porta'])
# pyed.show()
# evaluation
#        sum_of_wrong_voxels = np.sum(errim)
#        sum_of_voxels = np.prod(segm.shape)
#
# print "wrong ", sum_of_wrong_voxels
# print "voxels", sum_of_voxels
#
#        errorrate = sum_of_wrong_voxels/sum_of_voxels
#
#
#        self.assertLess(errorrate,0.1)
#        self.assertLess(errorrate,0.1)
#
#
#

    def test_idx_data(self):
        io3d.read("/home/mjirik/data/medical/orig/cvd-matrm3/microscopy_data/MM358-001-uint8.idx")


if __name__ == "__main__":
    unittest.main()
