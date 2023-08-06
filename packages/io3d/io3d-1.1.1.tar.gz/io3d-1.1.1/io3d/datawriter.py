#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple program for ITK image read/write in Python
# import itk


import numpy as np

import logging
logger = logging.getLogger(__name__)

import os.path

import dicom
import rawN
# from sys import argv


def write(data3d, path, filetype='auto', metadata=None):
    """

    :param data3d: input ndarray
    :param path: output path, if braces are in the name ("dir/file{:04d}.dcm"), image stack is produced
    :param filetype: dcm, png, h5, ... "image_stack"
    :param metadata: metadata f.e. {'voxelsize_mm': [3,2,2]}
    :return:
    """
    dw = DataWriter()
    dw.Write3DData(data3d, path, filetype, metadata)


class DataWriter:

    def Write3DData(self, data3d, path, filetype='auto', metadata=None):
        """
        data3d: input ndarray data
        path: output path
        metadata: {'voxelsize_mm': [1, 1, 1]}
        filetype: dcm, vtk, rawiv, image_stack

        """
        try:
            d3d = data3d.pop('data3d')
            metadata = data3d
            data3d = d3d
        except:
            pass

        if filetype == 'auto':
            startpath, ext = os.path.splitext(path)
            filetype = ext[1:]

        mtd = {'voxelsize_mm': [1, 1, 1]}
        if metadata is not None:
            mtd.update(metadata)

        if path.find('{') >= 0:
            filetype = 'image_stack'
            # one_file_per_slice = True

    #     if one_file_per_slice:
    #         self._one_file_per_slice(self, data3d, path, filetype, metadata)
    #     else:
    #         self._all_in_one_file(self, data3d, path, filetype, metadata)
    #
    # def _all_in_one_file(self, data3d, path, filetype, metadata):

        if filetype in ['vtk', 'tiff', 'tif']:
            self._write_with_sitk(path, data3d, mtd)
        elif filetype in ['dcm', 'DCM', 'dicom']:
            self._write_with_sitk(path, data3d, mtd)
            self._fix_sitk_bug(path, metadata)
        elif filetype in ['rawiv']:
            rawN.write(path, data3d, metadata)
        elif filetype in ['image_stack']:
            self.save_image_stack(data3d, path, metadata)
        elif filetype in ['hdf5', 'hdf', 'h5', 'he5']:
            self.save_hdf5(data3d, path, metadata)
        elif filetype in ['pkl', 'pklz']:
            import misc
            metadata['data3d'] = data3d
            datap = metadata

            misc.obj_to_file(datap, path)

        else:
            logger.error('Unknown filetype: "' + filetype + '"')

            # data = dicom.read_file(onefile)

    def _write_with_sitk(self,path, data3d, metadata):
        import SimpleITK as sitk
        mtd=metadata
        dim = sitk.GetImageFromArray(data3d)
        vsz = mtd['voxelsize_mm']
        dim.SetSpacing([vsz[1], vsz[2], vsz[0]])
        sitk.WriteImage(dim, path)

    def _fix_sitk_bug(self, path, metadata):
        """
        There is a bug in simple ITK for Z axis in 3D images. This is a fix
        :param path:
        :param metadata:
        :return:
        """
        import dicom
        ds = dicom.read_file(path)
        ds.SpacingBetweenSlices = metadata["voxelsize_mm"][0]
        dicom.write_file(path, ds)

    def save_hdf5(self, data3d, path, metadata):
        # TODO this is not implemented in proper way
        import h5py
        f = h5py.File(path, "w")
        f.create_dataset('data3d', data=data3d, compression='gzip')
        met = f.create_group('metadata')
        met.create_dataset('voxelsize_mm', data=metadata['voxelsize_mm'], compression='gzip')
        # f.create_dataset('metadata', data=metadata, compression='gzip')
        f.flush()
        f.close()

    def __write_h5_key(self, grp, dct):
        import h5py
        import numpy as np
        retval = {}
        for key in dct.keys():
            try:
                data = dct[key]
                if type(data) == np.ndarray:
                    if data.dtype == np.dtype('O'):
                        logger.warning("problem with dtype('O')")
                        print "Press 'c' for continue"
                        from PyQt4 import QtCore; QtCore.pyqtRemoveInputHook()
                        import ipdb; ipdb.set_trace()
                    else:
                        grp.create_dataset(key, data=data)
                elif type(data) == list:
                    grp.create_dataset(key, data=data)
                elif type(data) == dict:
                    subgrp = grp.create_group('key')
                    self.__write_h5_key(subgrp, data)
                else:
                    grp[key] = data
            except:
                import traceback
                logger.warning(traceback.format_exc())


        return retval

    def DataCopyWithOverlay(self, dcmfilelist, out_dir, overlays):
        """
        Function make 3D data from dicom file slices

        :dcmfilelist list of sorted .dcm files
        :overlays dictionary of binary overlays. {1:np.array([...]), 3:...}
        :out_dir output directory

        """
        dcmlist = dcmfilelist
        # data3d = []

        for i in range(len(dcmlist)):
            onefile = dcmlist[i]

            logger.info(onefile)
            data = dicom.read_file(onefile)

            for i_overlay in overlays.keys():
                overlay3d = overlays[i_overlay]
                data = self.encode_overlay_slice(data,
                                                 overlay3d[-1 - i, :, :],
                                                 i_overlay)

            # construct output path
            head, tail = os.path.split(os.path.normpath(onefile))
            filename_out = os.path.join(out_dir, tail)

# save
            data.save_as(filename_out)
            # import pdb; pdb.set_trace()

    def add_overlay_to_slice_file(
        self,
        filename,
        overlay,
        i_overlay,
        filename_out=None
    ):
        """ Function adds overlay to existing file.
        """
        if filename_out is None:
            filename_out = filename
        data = dicom.read_file(filename)
        data = self.encode_overlay_slice(data, overlay, i_overlay)
        data.save_as(filename_out)
        pass

    def encode_overlay_slice(self, data, overlay, i_overlay):
        """
        """
        # overlay index
        n_bits = 8

        # On (60xx,3000) are stored ovelays.
        # First is (6000,3000), second (6002,3000), third (6004,3000),
        # and so on.
        dicom_tag1 = 0x6000 + 2 * i_overlay

        #  data (0x6000, 0x3000)
        # WR = 'OW'
        # WM = 1

        # On (60xx,0010) and (60xx,0011) is stored overlay size
        row_el = dicom.dataelem.DataElement(
            (dicom_tag1, 0x0010),
            'US',
            int(overlay.shape[0])
        )
        data[row_el.tag] = row_el

        col_el = dicom.dataelem.DataElement(
            (dicom_tag1, 0x0011),
            'US',
            int(overlay.shape[1])
        )
        data[col_el.tag] = col_el

# arrange values to bit array
        overlay_linear = np.reshape(overlay, np.prod(overlay.shape))

    # allocation of dataspace
        encoded_linear = np.zeros(
            np.prod(overlay.shape) / n_bits,
            dtype=np.uint8
        )

# encoded data
        for i in range(0, len(overlay_linear)):
            if overlay_linear[i] > 0:
                bit = 1
            else:
                bit = 0

            encoded_linear[i / n_bits] |= bit << (i % n_bits)

        overlay_raw = encoded_linear.tostring()

        # Decoding data. Each bit is stored as array element
# TODO neni tady ta jednička blbě?
#        for i in range(1,len(overlay_raw)):
#            for k in range (0,n_bits):
#                byte_as_int = ord(overlay_raw[i])
#                decoded_linear[i*n_bits + k] = (byte_as_int >> k) & 0b1
#
        # overlay = np.array(pol)

        overlay_el = dicom.dataelem.DataElement(
            (dicom_tag1, 0x3000),
            'OW',
            overlay_raw
        )
        data[overlay_el.tag] = overlay_el

        return data

    def save_image_stack(self, data3d, filepattern, metadata=None):
        datadir, dataname = os.path.split(filepattern)

        if not os.path.exists(datadir):
            os.mkdir(datadir)
        databasename, dataext = os.path.splitext(dataname)


        if filepattern.find('{') < 0:
            # filepattern does not contain place for integer
            filepattern = os.path.join(
                datadir,
                databasename + "{:05d}" + dataext)
        # print filepattern

        for i in range(0, data3d.shape[0]):
            newfilename = filepattern.format(i)
            logger.debug(newfilename)
            data2d = data3d[i, :, :]
            import SimpleITK as sitk
            # pixelType = itk.UC
            # imageType = itk.Image[pixelType, 2]
            dim = sitk.GetImageFromArray(data2d)

            if metadata is not None:
                vsz = np.asarray(metadata['voxelsize_mm']).astype('double')
                dim.SetSpacing([vsz[0], vsz[2], vsz[1]])
            # import ipdb; ipdb.set_trace()
            sitk.WriteImage(dim, newfilename)


def saveOverlayToDicomCopy(input_dcmfilelist, output_dicom_dir, overlays,
                           crinfo, orig_shape):
    """ Save overlay to dicom. """
    import datawriter as dwriter
    import qmisc

    if not os.path.exists(output_dicom_dir):
        os.mkdir(output_dicom_dir)

    # uncrop all overlays
    for key in overlays:
        overlays[key] = qmisc.uncrop(overlays[key], crinfo, orig_shape)

    dw = dwriter.DataWriter()
    dw.DataCopyWithOverlay(input_dcmfilelist, output_dicom_dir, overlays)
