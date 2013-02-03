# -*- coding: utf-8 -*-

import io
import os
import unittest
import tempfile
import warnings

from wand.color import Color
from wand.image import ClosedImageError, Image
from wand.version import MAGICK_VERSION_INFO
from wand.exceptions import MissingDelegateError


def asset(filename):
    return os.path.join(os.path.dirname(__file__), 'assets', filename)


def get_sig_version(versions):
    """
    Returns matching signature version value for current
    `ImageMagick` version.

    :param versions: Dict of versions.
    :type versions: :class:`dict`
    :returns: matched sig value
    :rtype: :class:`basestring`

    """
    sorted_versions = reversed(sorted(versions.keys()))
    for v in sorted_versions:
        if v <= MAGICK_VERSION_INFO:
            sig = versions[v]
            break
    else:
        sig = versions[v]
    return sig


class ImageTests(unittest.TestCase):
    def test_empty_image(self):
        with Image() as img:
            self.assertEqual(img.size, (0,0))

    def test_blank_image_01(self):
        with self.assertRaises(TypeError):
            Image(height=0, filename='/test.png')

    def test_blank_image_02(self):
        with self.assertRaises(TypeError):
            Image(width=0, height=0)

    def test_blank_image_03(self):
        transparent = Color('transparent')
        with Image(width=20, height=10) as img:
            self.assertEqual(img[10, 5], transparent)

    def test_blank_image_04(self):
        gray = Color('#ccc')
        with Image(width=20, height=10, background=gray) as img:
            self.assertEqual(img.size, (20, 10))
            self.assertEqual(img[10, 5], gray)

    def test_clear_image_01(self):
        with Image() as img:
            img.read(filename=asset('mona-lisa.jpg'))
            self.assertEqual(img.size, (402,599))

            img.clear()
            self.assertEqual(img.size, (0,0))

            img.read(filename=asset('beach.jpg'))
            self.assertEqual(img.size, (800,600))

    def test_read_from_file_01(self):
        with Image() as img:
            img.read(filename=asset('mona-lisa.jpg'))
            self.assertEqual(img.width, 402)

    def test_read_from_file_02(self):
        with Image() as img:
            with open(asset('mona-lisa.jpg'), 'rb') as f:
                img.read(file=f)
                self.assertEqual(img.width, 402)

    def test_read_from_file_02(self):
        with Image() as img:
            with open(asset('mona-lisa.jpg'), 'rb') as f:
                blob = f.read()
                img.read(blob=blob)
                self.assertEqual(img.width, 402)

    def test_operate_on_closed_image(self):
        with open(asset('mona-lisa.jpg'), 'rb') as f:
            with Image(file=f) as img:
                pass

        with self.assertRaises(ClosedImageError):
            img.wand

    def test_new_from_file_01(self):
        with open(asset('mona-lisa.jpg'), 'rb') as f:
            with Image(file=f) as img:
                self.assertEqual(img.width, 402)

    def test_new_from_file_02(self):
        with open(asset('mona-lisa.jpg'), 'rb') as f:
            strio = io.BytesIO(f.read())

        with Image(file=strio) as img:
            self.assertEqual(img.width, 402)

    def test_access_invalid_file_01(self):
        with self.assertRaises(TypeError):
            Image(file='not file object')

    def test_access_invalid_file_02(self):
        with self.assertRaises(IOError):
            Image(filename=asset('not-exists.jpg'))

    def test_new_image_from_filename(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.width, 402)

    def test_new_image_from_blob(self):
        with open(asset('mona-lisa.jpg'), 'rb') as f:
            blob = f.read()

        with Image(blob=blob) as img:
            self.assertEqual(img.width, 402)

    def test_new_image_with_format(self):
        with open(asset('google.ico'), 'rb') as f:
            blob = f.read()

        with self.assertRaises(Exception):
            Image(blob=blob)

        with Image(blob=blob, format='ico') as img:
            self.assertEqual(img.size, (16, 16))

    def test_clone_image_01(self):
         with Image(filename=asset('mona-lisa.jpg')) as img:
            with Image(image=img) as cloned:
                self.assertNotEqual(img.wand, cloned.wand)
                self.assertEqual(img.size, cloned.size)

    def test_clone_image_02(self):
         with Image(filename=asset('mona-lisa.jpg')) as img:
            with img.clone() as cloned:
                self.assertNotEqual(img.wand, cloned.wand)
                self.assertEqual(img.size, cloned.size)

    def test_save_to_filename(self):
        savefile = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
        with Image(filename=asset('mona-lisa.jpg')) as orig:
            orig.save(filename=savefile)

            with self.assertRaises(IOError):
                orig.save(filename=os.path.join(savefile, 'invalid.jpg'))

            with self.assertRaises(TypeError):
                orig.save(filename=1234)

        self.assertTrue(os.path.isfile(savefile))
        with Image(filename=savefile) as saved:
            self.assertEqual(saved.size, (402, 599))

        os.remove(savefile)

    def test_save_to_file(self):
        buffer = io.BytesIO()
        with tempfile.TemporaryFile() as savefile:
            with Image(filename=asset('mona-lisa.jpg')) as orig:
                orig.save(file=savefile)
                orig.save(file=buffer)

                with self.assertRaises(TypeError):
                    orig.save(file='filename')

                with self.assertRaises(TypeError):
                    orig.save(file=1234)

            savefile.seek(0)
            with Image(file=savefile) as saved:
                self.assertEqual(saved.size, (402, 599))

            buffer.seek(0)
            with Image(file=buffer) as saved:
                self.assertEqual(saved.size, (402, 599))

    def test_save_error(self):
        filename = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
        fileobj = io.BytesIO()

        with Image(filename=asset('mona-lisa.jpg')) as orig:
            with self.assertRaises(TypeError):
                orig.save()

            with self.assertRaises(TypeError):
                orig.save(filename=filename, file=fileobj)

    def test_make_blob(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.format, 'JPEG')

            with Image(blob=img.make_blob('png')) as img2:
                self.assertEqual(img2.size, (402, 599))
                self.assertEqual(img2.format, 'PNG')

            with self.assertRaises(TypeError):
                img.make_blob(123)

    def test_get_size(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.size, (402, 599))
            self.assertEqual(img.width, 402)
            self.assertEqual(img.height, 599)
            self.assertEqual(len(img), 599)

    def test_get_format_01(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.format, 'JPEG')

    def test_get_format_02(self):
        with Image(filename=asset('croptest.png')) as img:
            self.assertEqual(img.format, 'PNG')

    def test_set_format(self):
        buffer = io.BytesIO()

        with Image(filename=asset('mona-lisa.jpg')) as img:
            img.format = 'png'
            self.assertEqual(img.format, 'PNG')
            img.save(file=buffer)

        buffer.seek(0)
        with Image(file=buffer) as pngimage:
            self.assertEqual(pngimage.format, 'PNG')

            with self.assertRaises(ValueError):
                pngimage.format = 'HONG'

            with self.assertRaises(TypeError):
                pngimage.format = 123

    def test_get_image_type(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.type, "truecolor")

            img.alpha_channel = True
            self.assertEqual(img.type, "truecolormatte")

    def test_set_image_type(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            img.type = "grayscale"
            self.assertEqual(img.type, "grayscale")

    def test_get_image_compression(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.compression_quality, 80)

    def test_set_image_compression(self):
        buffer = io.BytesIO()
        with Image(filename=asset('mona-lisa.jpg')) as img:
            img.compression_quality = 50
            self.assertEqual(img.compression_quality, 50)
            img.save(file=buffer)

        buffer.seek(0)
        with Image(file=buffer) as img:
            self.assertEqual(img.compression_quality, 50)

            with self.assertRaises(TypeError):
                img.compression_quality = 'high'

    def test_resolution_01(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.resolution, (72, 72))

    def test_resolution_02(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            img.resolution = (100, 100)
            self.assertEqual(img.resolution, (100, 100))

    def test_resolution_03(self):
        with Image(filename=asset('sample.pdf'), resolution=(100,100)) as img:
            self.assertEqual(img.resolution, (100, 100))

    def test_resolution_04(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            img.resolution = 100
            self.assertEqual(img.resolution, (100, 100))

    def test_resolution_05(self):
        with Image(filename=asset('sample.pdf'), resolution=100) as img:
            self.assertEqual(img.resolution, (100, 100))

    def test_units_01(self):
        with Image(filename=asset('beach.jpg')) as img:
            self.assertEqual(img.units, "pixelsperinch")

    def test_units_02(self):
        with Image(filename=asset('sasha.jpg')) as img:
            self.assertEqual(img.units, "undefined")

    def test_units_03(self):
        with Image(filename=asset('watermark.png')) as img:
            img.units="pixelspercentimeter"
            self.assertEqual(img.units, "pixelspercentimeter")

    def test_depth_01(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.depth, 8)

    def test_depth_02(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            img.depth = 16
            self.assertEqual(img.depth, 16)

    def test_strip(self):
        with Image(filename=asset('beach.jpg')) as img:
            buffer = io.BytesIO()
            img.save(file=buffer)

            len_unstripped = buffer.tell()
            buffer = io.BytesIO()

            img.strip()
            img.save(file=buffer)
            len_stripped = buffer.tell()

            self.assertGreater(len_unstripped, len_stripped)


    def test_trim_01(self):
        with Image(filename=asset('trimtest.png')) as img:
            oldx, oldy = img.size
            img.trim()
            newx, newy = img.size

            self.assertLess(newx, oldx)
            self.assertLess(newy, oldy)

    def test_trim_02(self):
        with Image(filename=asset('trim-color-test.png')) as img:
            self.assertEqual(img.size, (100, 100))
            with Color('blue') as blue:
                img.trim(blue)
                self.assertEqual(img.size, (50, 100))

            with Color('srgb(0,255,0)') as green:
                self.assertTrue(img[0, 0] == img[0, -1] == img[-1, 0] == img[-1, -1] == green)

    def test_get_mimetype_01(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertIn(img.mimetype, ('image/jpeg', 'image/x-jpeg'))

    def test_get_mimetype_02(self):
        with Image(filename=asset('croptest.png')) as img:
            self.assertIn(img.mimetype, ('image/png', 'image/x-png'))

    def test_convert(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            buffer = io.BytesIO()
            with img.convert('png') as converted:
                self.assertEqual(converted.format, 'PNG')
                converted.save(file=buffer)

            buffer.seek(0)
            with Image(file=buffer) as img2:
                self.assertEqual(img2.format, 'PNG')

            with self.assertRaises(ValueError):
                img.convert('HONG')

            with self.assertRaises(TypeError):
                img.convert(123)

    def test_slice_clone(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with img[:,:] as cloned:
                self.assertEqual(img.size, cloned.size)

    def test_invalid_slice(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(TypeError):
                img['12']
            with self.assertRaises(TypeError):
                img[1.23]
            with self.assertRaises(ValueError):
                img[()]
            with self.assertRaises(ValueError):
                img[:, :, :]
            with self.assertRaises(ValueError):
                img[::2, :]
            with self.assertRaises(IndexError):
                img[1:1, :]
            with self.assertRaises(IndexError):
                img[:, 2:2]
            with self.assertRaises(TypeError):
                img[100.0:, 100.0]
            with self.assertRaises(TypeError):
                img['100':, '100']
            with self.assertRaises(IndexError):
                img[500:, 900]
            with self.assertRaises(TypeError):
                img['1', 0]
            with self.assertRaises(TypeError):
                img[1, '0']

        with Image(filename=asset('croptest.png')) as img:
            with self.assertRaises(IndexError):
                img[300, 300]
            with self.assertRaises(IndexError):
                img[-301, -301]

    def test_pixel(self):
        with Image(filename=asset('croptest.png')) as img:
            self.assertEqual(img[0, 0], Color('transparent'))
            self.assertEqual(img[99, 99], Color('transparent'))
            self.assertEqual(img[100, 100], Color('black'))
            self.assertEqual(img[150, 150], Color('black'))
            self.assertEqual(img[-200, -200], Color('black'))
            self.assertEqual(img[-201, -201], Color('transparent'))

    def test_index_row(self):
        with Color('transparent') as transparent:
            with Color('black') as black:
                with Image(filename=asset('croptest.png')) as img:
                    for c in img[0]:
                        self.assertEqual(c, transparent)

                    for c in img[99]:
                        self.assertEqual(c, transparent)

                    for i, c in enumerate(img[100]):
                        if 100 <= i < 200:
                            self.assertEqual(c, black)
                        else:
                            self.assertEqual(c, transparent)

                    for i, c in enumerate(img[150]):
                        if 100 <= i < 200:
                            self.assertEqual(c, black)
                        else:
                            self.assertEqual(c, transparent)

                    for i, c in enumerate(img[-200]):
                        if 100 <= i < 200:
                            self.assertEqual(c, black)
                        else:
                            self.assertEqual(c, transparent)

                    for c in img[-201]:
                        self.assertEqual(c, transparent)


    def test_slice_crop(self):
        with Image(filename=asset('croptest.png')) as img:
            with img[100:200, 100:200] as cropped:
                self.assertEqual(cropped.size, (100, 100))

                with Color('#000') as black:
                    for row in cropped:
                        for col in row:
                            self.assertEqual(col, black)

            with img[150:, :150] as cropped:
                self.assertEqual(cropped.size, (150, 150))

            with img[-200:-100, -200:-100] as cropped:
                self.assertEqual(cropped.size, (100, 100))

            with img[100:200] as cropped:
                self.assertEqual(cropped.size, (300, 100))

            self.assertEqual(img.size, (300, 300))

            with self.assertRaises(IndexError):
                img[:500, :500]

            with self.assertRaises(IndexError):
                img[290:310, 290:310]

    def test_crop_01(self):
        with Image(filename=asset('croptest.png')) as img:
            with img.clone() as cropped:
                self.assertEqual(cropped.size, img.size)
                cropped.crop(100, 100, 200, 200)
                self.assertEqual(cropped.size, (100, 100))

                with Color('#000') as black:
                    for row in cropped:
                        for col in row:
                            self.assertEqual(col, black)

    def test_crop_02(self):
        with Image(filename=asset('croptest.png')) as img:
            with img.clone() as cropped:
                self.assertEqual(cropped.size, img.size)
                cropped.crop(100, 100, width=100, height=100)
                self.assertEqual(cropped.size, (100, 100))

    def test_crop_03(self):
        with Image(filename=asset('croptest.png')) as img:
            with img.clone() as cropped:
                self.assertEqual(cropped.size, img.size)
                cropped.crop(left=150, bottom=150)
                self.assertEqual(cropped.size, (150, 150))

    def test_crop_04(self):
        with Image(filename=asset('croptest.png')) as img:
            with img.clone() as cropped:
                self.assertEqual(cropped.size, img.size)
                cropped.crop(left=150, height=150)
                self.assertEqual(cropped.size, (150, 150))

    def test_crop_05(self):
        with Image(filename=asset('croptest.png')) as img:
            with img.clone() as cropped:
                self.assertEqual(cropped.size, img.size)
                cropped.crop(-200, -200, -100, -100)
                self.assertEqual(cropped.size, (100, 100))

    def test_crop_06(self):
        with Image(filename=asset('croptest.png')) as img:
            with img.clone() as cropped:
                self.assertEqual(cropped.size, img.size)
                cropped.crop(top=100, bottom=200)
                self.assertEqual(cropped.size,(300, 100))

    def test_crop_07(self):
        with Image(filename=asset('croptest.png')) as img:
            with self.assertRaises(ValueError):
                img.crop(0, 0, 500, 500)

    def test_crop_08(self):
        with Image(filename=asset('croptest.png')) as img:
            with self.assertRaises(ValueError):
                img.crop(290, 290, 50, 50)

    def test_crop_09(self):
        with Image(filename=asset('croptest.png')) as img:
            with self.assertRaises(ValueError):
                img.crop(290, 290, width=0, height=0)


    def test_crop_10(self):
        with Image(filename=asset('croptest.png')) as img:
            with self.assertRaises(TypeError):
                img.crop(right=1, width=2)
            with self.assertRaises(TypeError):
                img.crop(bottom=1, height=2)


    def test_resize(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with img.clone() as a:
                self.assertEqual(a.size, (402, 599))
                a.resize(100, 100)
                self.assertEqual(a.size, (100, 100))
            with img.clone() as b:
                self.assertEqual(b.size, (402, 599))
                b.resize(height=100)
                self.assertEqual(b.size, (402, 100))
            with img.clone() as c:
                self.assertEqual(c.size, (402, 599))
                c.resize(width=100)
                self.assertEqual(c.size, (100, 599))

    def resize_errors(self):
        """Resizing errors."""
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(TypeError):
                img.resize(width='100')
            with self.assertRaises(TypeError):
                img.resize(height='100')
            with self.assertRaises(ValueError):
                img.resize(width=0)
            with self.assertRaises(ValueError):
                img.resize(height=0)
            with self.assertRaises(ValueError):
                img.resize(width=-5)
            with self.assertRaises(ValueError):
                img.resize(height=-5)

    def test_transform_01(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as a:
                self.assertEqual(a.size, (800, 600))
                a.transform(resize='200%')
                self.assertEqual(a.size, (1600, 1200))

    def test_transform_02(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as b:
                self.assertEqual(b.size, (800, 600))
                b.transform(resize='200%x100%')
                self.assertEqual(b.size, (1600, 600))

    def test_transform_03(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as c:
                self.assertEqual(c.size, (800, 600))
                c.transform(resize='1200')
                self.assertEqual(c.size, (1200, 900))

    def test_transform_04(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as d:
                self.assertEqual(d.size, (800, 600))
                d.transform(resize='x300')
                self.assertEqual(d.size, (400, 300))

    def test_transform_05(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as e:
                self.assertEqual(e.size, (800, 600))
                e.transform(resize='400x600')
                self.assertEqual(e.size, (400, 300))

    def test_transform_06(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as f:
                self.assertEqual(f.size, (800, 600))
                f.transform(resize='1000x1200^')
                self.assertEqual(f.size, (1600, 1200))

    def test_transform_07(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as g:
                self.assertEqual(g.size, (800, 600))
                g.transform(resize='100x100!')
                self.assertEqual(g.size, (100, 100))

    def test_transform_08(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as h:
                self.assertEqual(h.size, (800, 600))
                h.transform(resize='400x500>')
                self.assertEqual(h.size, (400, 300))

    def test_transform_09(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as i:
                self.assertEqual(i.size, (800, 600))
                i.transform(resize='1200x3000<')
                self.assertEqual(i.size, (1200, 900))

    def test_transform_10(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as j:
                self.assertEqual(j.size, (800, 600))
                j.transform(resize='120000@')
                self.assertEqual(j.size, (400, 300))

    def test_transform_11(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as k:
                self.assertEqual(k.size, (800, 600))
                k.transform(crop='300x300')
                self.assertEqual(k.size, (300, 300))

    def test_transform_12(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as l:
                self.assertEqual(l.size, (800, 600))
                l.transform(crop='300x300+100+100')
                self.assertEqual(l.size, (300, 300))

    def test_transform_13(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as m:
                self.assertEqual(m.size, (800, 600))
                m.transform(crop='300x300-150-150')
                self.assertEqual(m.size, (150, 150))

    def test_transform_14(self):
        with Image(filename=asset('beach.jpg')) as img:
            with img.clone() as n:
                self.assertEqual(n.size, (800, 600))
                n.transform('300x300', '200%')
                self.assertEqual(n.size, (600, 600))

    def test_transform_errors_01(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(TypeError):
                img.transform(crop=500)

    def test_transform_errors_02(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(TypeError):
                img.transform(resize=500)

    def test_transform_errors_03(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(TypeError):
                img.transform(500, 500)

    def test_transform_errors_04(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(ValueError):
                img.transform(crop=u'⚠ ')

    def test_transform_errors_05(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            with self.assertRaises(ValueError):
                img.transform(resize=u'⚠ ')

    def test_signature(self):
        sig = get_sig_version({
            (6, 6, 9, 7):
                '763774301b62cf9ea033b661f5136fbda7e8de96254aec3dd0dff63c05413a1e',
            (6, 7, 7, 6):
                '8c6ef1dcb1bacb6ad8edf307f2f2c6a129b3b7aa262ee288325f9fd334006374'
        })

        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.signature, sig)
            img.format = 'png'
            self.assertEqual(img.signature, sig)

    def test_equal(self):
        with Image(filename=asset('mona-lisa.jpg')) as a:
            with Image(filename=asset('mona-lisa.jpg')) as a2:
                self.assertEqual(a, a2)
                self.assertTrue(not (a != a2))

            with Image(filename=asset('sasha.jpg')) as b:
                self.assertNotEqual(a, b)

            with a.convert('png') as a3:
                self.assertEqual(a, a3)
                self.assertTrue(not (a != a3))

    def test_object_hash(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            a = hash(img)
            img.format = 'png'
            b = hash(img)
            self.assertEqual(a, b)

    def test_get_alpha_channel(self):
        with Image(filename=asset('watermark.png')) as img:
            self.assertEqual(img.alpha_channel, True)
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(img.alpha_channel, False)

    def test_set_alpha_channel(self):
        with Image(filename=asset('watermark.png')) as img:
            self.assertEqual(img.alpha_channel, True)
            img.alpha_channel = False
            self.assertEqual(img.alpha_channel, False)

    def test_get_background_color(self):
        with Image(filename=asset('mona-lisa.jpg')) as img:
            self.assertEqual(Color('white'), img.background_color)

    def test_set_background_color(self):
        with Image(filename=asset('croptest.png')) as img:
            with Color('transparent') as color:
                img.background_color = color
                self.assertEqual(img.background_color, color)

    def test_watermark(self):
        sig = get_sig_version({
            (6, 6, 9, 7):
                '9c4c182e44ee265230761a412e355cb78ea61859658220ecc8cbc1d56f58584e',
            (6, 7, 7, 6):
                'd725d924a9008ddff828f22595237ec6b56fb54057c6ee99584b9fc7ac91092c'
        })

        with Image(filename=asset('beach.jpg')) as img:
            with Image(filename=asset('watermark.png')) as wm:
                img.watermark(wm, 0.3)
                msg = 'img = {0!r}, marked = {1!r}'.format(
                    img.signature, sig)
                self.assertEqual(img.signature, sig)

    def test_reset_coords(self):
        """Reset the coordinate frame so to the upper-left corner of
        the image is (0, 0) again.

        """
        sig = get_sig_version({
            (6, 6, 9, 7):
                '9537655c852cb5a22f29ba016648ea29d1b9a55fd2b4399f4fcbbcd39cce1778',
            (6, 7, 7, 6):
                'e8ea17066378085a60f7213430af62c89ed3f416e98b39f2d434c96c2be82989',
        })
        with Image(filename=asset('sasha.jpg')) as img:
                img.rotate(45, reset_coords=True)
                img.crop(0, 0, 170, 170)
                msg = 'img = {0!r}, control = {1!r}'.format(
                    img.signature, sig)
                self.assertEqual(img.signature, sig)


    def test_metadata(self):
        """Test metadata api"""
        with Image(filename=asset('beach.jpg')) as img:
            self.assertEqual(len(img.metadata), 52)
            self.assertIn('exif:ApertureValue', img.metadata)
            self.assertIn('exif:UnknownValue', img.metadata)
            self.assertNotIn('exif:UnknownValue', img.metadata)

            self.assertEqual(img.metadata['exif:ApertureValue'], '192/32')
            self.assertEqual(img.metadata.get('exif:UnknownValue', "IDK"), "IDK")


    def test_channel_depths(self):
        with Image(filename=asset('beach.jpg')) as i:
            self.assertEqual(dict(i.channel_depths), {
                'blue': 8, 'gray': 8, 'true_alpha': 1, 'opacity': 1,
                'undefined': 1, 'composite_channels': 8, 'index': 1,
                'rgb_channels': 1, 'alpha': 1, 'yellow': 8, 'sync_channels': 1,
                'default_channels': 8, 'black': 1, 'cyan': 8,
                'all_channels': 8, 'green': 8, 'magenta': 8, 'red': 8,
                'gray_channels': 1
            })

        with Image(filename=asset('google.ico')) as i:
            self.assertEqual(dict(i.channel_depths), {
                'blue': 8, 'gray': 8, 'true_alpha': 1, 'opacity': 1,
                'undefined': 1, 'composite_channels': 8, 'index': 1,
                'rgb_channels': 1, 'alpha': 1, 'yellow': 8, 'sync_channels': 1,
                'default_channels': 8, 'black': 1, 'cyan': 8, 'all_channels': 8,
                'green': 8, 'magenta': 8, 'red': 8, 'gray_channels': 1
            })

    def test_channel_images(self):
        with Image(filename=asset('sasha.jpg')) as i:
            actual = dict((c, i.signature) for c, i in i.channel_images.items())
        del actual['rgb_channels']   # FIXME: workaround for Travis CI
        del actual['gray_channels']  # FIXME: workaround for Travis CI
        self.assertEqual(actual, {
            'blue': get_sig_version({
                (6, 5, 7, 8): 'b56f0c0763b49d4b0661d0bf7028d82a'
                              '66d0d15817ff5c6fd68a3c76377bd05a',
                (6, 7, 7, 6): 'b5e59c5bb24379e0f741b8073e19f564'
                              '9a456af4023d2dd3764a5c012989470b',
                (6, 7, 9, 5): 'a372637ff6256ed45c07b7be04617b99'
                              'cea024dbd6dd961492a1906f419d3f84'
            }),
            'gray': get_sig_version({
                (6, 6, 9, 7): 'ee84ed5532ade43e28c1f8baa0d52235'
                              '1aee73ff0265d188797d457f1df2bc82',
                (6, 7, 7, 6): 'd0d2bae86a40e0107f69bb8016800dae'
                              '4ad8178e29ac11649c9c3fa465a5a493',
                (6, 7, 9, 5): 'bac4906578408e0f46b1943f96c8c392'
                              '73997659feb005e581e7ddfa0ba1da41'
            }),
            'true_alpha': get_sig_version({
                (6, 5, 7, 8): '3da06216c40cdb4011339bed11804714'
                              'bf262ac7c20e7eaa5401ed3218e9e59f',
                (6, 7, 9, 5): '3da06216c40cdb4011339bed11804714'
                              'bf262ac7c20e7eaa5401ed3218e9e59f'
            }),
            'opacity': get_sig_version({
                (6, 5, 7, 8): '0e7d4136121208cf6c2e12017ffe9c48'
                              '7e8ada5fca1ad76b06bc41ad8a932de3'
            }),
            'undefined': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'composite_channels': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'index': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'yellow': get_sig_version({
                (6, 6, 9, 7): 'b56f0c0763b49d4b0661d0bf7028d82a'
                              '66d0d15817ff5c6fd68a3c76377bd05a',
                (6, 7, 7, 6): 'b5e59c5bb24379e0f741b8073e19f564'
                              '9a456af4023d2dd3764a5c012989470b',
                (6, 7, 9, 5): 'a372637ff6256ed45c07b7be04617b99'
                              'cea024dbd6dd961492a1906f419d3f84'
            }),
            'black': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'sync_channels': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'default_channels': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'green': get_sig_version({
                (6, 5, 7, 8): 'ee703ad96996a796d47f34f9afdc74b6'
                              '89817320d2b6e6423c4c2f7e4ed076db',
                (6, 7, 7, 6): 'ad770e0977567c12a336b6f3bf07e57e'
                              'c370af40641238b3328699be590b5d16',
                (6, 7, 9, 5): '87139d62ff097e312ab4cc1859ee2db6'
                              '066c9845de006f38163b325d405df782'
            }),
            'cyan': get_sig_version({
                (6, 5, 7, 8): 'ee84ed5532ade43e28c1f8baa0d52235'
                              '1aee73ff0265d188797d457f1df2bc82',
                (6, 7, 7, 6): 'd0d2bae86a40e0107f69bb8016800dae'
                              '4ad8178e29ac11649c9c3fa465a5a493',
                (6, 7, 9, 5): 'bac4906578408e0f46b1943f96c8c392'
                              '73997659feb005e581e7ddfa0ba1da41'
            }),
            'all_channels': get_sig_version({
                (6, 5, 7, 8): 'b68db111c7d6a58301d9d824671ed810'
                              'b790d397429d2988dcdeb7562729bb46',
                (6, 7, 7, 6): 'ae62e71111167c83d9449bcca50dd65f'
                              '565227104fe148aac514d3c2ef0fe9e2',
                (6, 7, 9, 5): 'd659b35502ac753c52cc44d488c78acd'
                              'c0201e65a7e9c5d7715ff79dbb0b24b3'
            }),
            'alpha': get_sig_version({
                (6, 5, 7, 8): '0e7d4136121208cf6c2e12017ffe9c48'
                              '7e8ada5fca1ad76b06bc41ad8a932de3',
                (6, 7, 7, 6): '0e7d4136121208cf6c2e12017ffe9c48'
                              '7e8ada5fca1ad76b06bc41ad8a932de3'
            }),
            'magenta': get_sig_version({
                (6, 5, 7, 8): 'ee703ad96996a796d47f34f9afdc74b6'
                              '89817320d2b6e6423c4c2f7e4ed076db',
                (6, 7, 7, 6): 'ad770e0977567c12a336b6f3bf07e57e'
                              'c370af40641238b3328699be590b5d16',
                (6, 7, 9, 5): '87139d62ff097e312ab4cc1859ee2db6'
                              '066c9845de006f38163b325d405df782'
            }),
            'red': get_sig_version({
                (6, 5, 7, 8): 'ee84ed5532ade43e28c1f8baa0d52235'
                              '1aee73ff0265d188797d457f1df2bc82',
                (6, 7, 7, 6): 'd0d2bae86a40e0107f69bb8016800dae'
                              '4ad8178e29ac11649c9c3fa465a5a493',
                (6, 7, 9, 5): 'bac4906578408e0f46b1943f96c8c392'
                              '73997659feb005e581e7ddfa0ba1da41'
            })
        })

    def test_composite(self):
        with Image(filename=asset('beach.jpg')) as img:
            with Image(filename=asset('watermark.png')) as fg:
                img.composite(fg, 0, 0)
                self.assertEqual(img.signature, get_sig_version({
                    (6, 6, 9, 7): '9c4c182e44ee265230761a412e355cb7'
                                  '8ea61859658220ecc8cbc1d56f58584e',
                    (6, 7, 7, 6): 'd725d924a9008ddff828f22595237ec6'
                                  'b56fb54057c6ee99584b9fc7ac91092c'
                }))

    def test_composite_with_xy(self):
        with Image(filename=asset('beach.jpg')) as img:
            with Image(filename=asset('watermark.png')) as fg:
                img.composite(fg, 5, 10)
                self.assertEqual(img.signature, get_sig_version({
                    (6, 6, 9, 7): 'e2a17a176de6b995b0f0f83e3c523006'
                                  '99190c7536ce1c599e65346d28f74b3b',
                    (6, 7, 7, 6): 'a40133f53093ce92e3e010d99a68fe13'
                                  '55544821cec2f707d5bd426d326921f8'
                }))

    def test_composite_channel(self):
        with Image(filename=asset('beach.jpg')) as img:
            w, h = img.size
            with Color('black') as color:
                with Image(width=w / 2, height=h / 2, background=color) as cimg:
                    img.composite_channel('red', cimg, 'copy_red', w / 4, h / 4)
                    self.assertEqual(img.signature, get_sig_version({
                        (6, 6, 9, 7): 'df4531b9cb50b0b70f0d4d88ac962cc7'
                                      '51133d2772d7ce695d19179804a955ae',
                        (6, 7, 7, 6): '51ebd57f8507ed8ca6355906972af369'
                                      '5797d278ae3ed04dfc1f9b8c517bcfab'
                    }))


    def test_liquid_rescale(self):
        with Image(filename=asset('beach.jpg')) as img:
            try:
                img.liquid_rescale(600, 600)
            except MissingDelegateError:
                warnings.warn('skip liquid_rescale test; has no LQR delegate')
            else:
                self.assertEqual(img.signature, get_sig_version({
                    (6, 6, 9, 7): '459337dce62ada2a2e6a3c69b6819447'
                                  '38a71389efcbde0ee72b2147957e25eb'
                }))


    def test_border(self):
        with Image(filename=asset('sasha.jpg')) as img:
            left_top = img[0, 0]
            left_bottom = img[0, -1]
            right_top = img[-1, 0]
            right_bottom = img[-1, -1]

            with Color('red') as color:
                img.border(color, 2, 5)

                self.assertEqual(img[0, 0], img[0, -1])
                self.assertEqual(img[0, 0], img[-1, 0])
                self.assertEqual(img[0, 0], img[-1, -1])
                self.assertEqual(img[0, 0], img[1, 4])
                self.assertEqual(img[0, 0], img[1, -5])
                self.assertEqual(img[0, 0], img[-2, 4])
                self.assertEqual(img[0, 0], img[-2, -5])

                self.assertEqual(img[2, 5], left_top)
                self.assertEqual(img[2, -6], left_bottom)
                self.assertEqual(img[-3, 5], right_top)
                self.assertEqual(img[-3, -6], right_bottom)


class ImageSlowTests(unittest.TestCase):
    def test_iterate(self):
        with Color('#000') as black:
            with Color('transparent') as transparent:
                with Image(filename=asset('croptest.png')) as img:
                    for i, row in enumerate(img):
                        self.assertEqual(len(row), 300)

                        if i % 3:
                            continue

                        if 100 <= i < 200:
                            for x, color in enumerate(row):
                                if x % 3:
                                    continue # avoid slowness
                                if 100 <= x < 200:
                                    self.assertEqual(color, black)
                                else:
                                    self.assertEqual(color, transparent)
                        else:
                            for color in row:
                                self.assertEqual(color, transparent)

                    self.assertEqual(i, 299)

    def test_rotate(self):
        with Image(filename=asset('rotatetest.gif')) as img:
            self.assertEqual(150, img.width)
            self.assertEqual(100, img.height)
            with img.clone() as cloned:
                cloned.rotate(360)
                self.assertEqual(img.size, cloned.size)
                with Color('black') as black:
                    self.assertEqual(black, cloned[0, 50])
                    self.assertEqual(black, cloned[74, 50])
                    self.assertEqual(black, cloned[0, 99])
                    self.assertEqual(black, cloned[74, 99])

                with Color('white') as white:
                    self.assertEqual(white, cloned[75, 50])
                    self.assertEqual(white, cloned[75, 99])

            with img.clone() as cloned:
                cloned.rotate(90)
                self.assertEqual(100, cloned.width)
                self.assertEqual(150, cloned.height)
                with Color('black') as black:
                    with Color('white') as white:
                        for y, row in enumerate(cloned):
                            for x, col in enumerate(row):
                                if y < 75 and x < 50:
                                    self.assertEqual(col, black)
                                else:
                                    self.assertEqual(col, white)
            with Color('red') as bg:
                with img.clone() as cloned:
                    cloned.rotate(45, bg)

                    self.assertLessEqual(176, cloned.width)
                    self.assertLessEqual(cloned.height, 178)

                    self.assertEqual(bg, cloned[0, 0])
                    self.assertEqual(bg, cloned[0, -1])

                    self.assertEqual(bg, cloned[-1, 0])
                    self.assertEqual(bg, cloned[-1, -1])

                    with Color('black') as black:
                        self.assertEqual(black, cloned[2, 70])
                        self.assertEqual(black, cloned[35, 37])
                        self.assertEqual(black, cloned[85, 88])
                        self.assertEqual(black, cloned[52, 120])
