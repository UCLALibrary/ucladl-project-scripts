import pytest
import os
from PIL import Image
from PIL import UnidentifiedImageError
from badimagefinder import *

script_dir = os.path.dirname(__file__)

#Tests for get file size: zero and nonzero
def test_file_zero():
    output = getFileSizeMB(os.path.join(script_dir, 'Test Material',
                                        'zeroLenImg.tif'))
    assert output == 0

def test_file_nonzero():
    output = getFileSizeMB(os.path.join(script_dir, 'Test Material',
                                        'nonZeroImg.tif'))
    assert output == 0.00273

#tests for isCorrupt
def test_corrupt_zero():
    corrupt, reason, img = isCorrupt(os.path.join(script_dir,
                                                  'Test Material',
                                                  'zeroLenImg.tif'))        
    returned_vals = [corrupt, reason, img]
    assert returned_vals == [True, "Zero file size", None]


def test_corrupt_invalid_mime():
    corrupt, reason, img = isCorrupt(os.path.join(script_dir,
                                                  'Test Material',
                                                  'invalidMime.tif'))        
    returned_vals = [corrupt, reason, img]
    #need to think more about this one - how to deal with imgs?    
    assert returned_vals == [True, "Non-TIFF MIME type for .tif file", img]

def test_corrupt_bad_mode():
    #write this one
    return True
    
def test_corrupt_verify_fail():
    #write
    return True

def test_corrupt_UIE():
    #write
    return True

def test_valid_file():
    corrupt, reason, img = isCorrupt(os.path.join(script_dir,
                                                  'Test Material',
                                                  'validImage.tif'))
    returned_vals = [corrupt, reason, img]
    #need to think more about this one - how to deal with imgs?    
    assert returned_vals == [False, "", img]
