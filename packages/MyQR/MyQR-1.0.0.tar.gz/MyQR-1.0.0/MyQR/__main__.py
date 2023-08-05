#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from MyQR.mylibs import theqrmodule
from PIL import Image

# Alignment Pattern Locations
alig_location = [
    (6, 18), (6, 22), (6, 26), (6, 30), (6, 34), (6, 22, 38), (6, 24, 42), (6, 26, 46), (6, 28, 50), (6, 30, 54), (6, 32, 58), (6, 34, 62), (6, 26, 46, 66), (6, 26, 48, 70), (6, 26, 50, 74), (6, 30, 54, 78), (6, 30, 56, 82), (6, 30, 58, 86), (6, 34, 62, 90), (6, 28, 50, 72, 94), (6, 26, 50, 74, 98), (6, 30, 54, 78, 102), (6, 28, 54, 80, 106), (6, 32, 58, 84, 110), (6, 30, 58, 86, 114), (6, 34, 62, 90, 118), (6, 26, 50, 74, 98, 122), (6, 30, 54, 78, 102, 126), (6, 26, 52, 78, 104, 130), (6, 30, 56, 82, 108, 134), (6, 34, 60, 86, 112, 138), (6, 30, 58, 86, 114, 142), (6, 34, 62, 90, 118, 146), (6, 30, 54, 78, 102, 126, 150), (6, 24, 50, 76, 102, 128, 154), (6, 28, 54, 80, 106, 132, 158), (6, 32, 58, 84, 110, 136, 162), (6, 26, 54, 82, 110, 138, 166), (6, 30, 58, 86, 114, 142, 170)
    ]

def combine(ver, qr_name, bg_name, colorized, contrast, brightness, save_place):
    from PIL import ImageEnhance, ImageFilter
    
    qr = Image.open(qr_name)
    qr = qr.convert('RGBA') if colorized else qr
    
    bg0 = Image.open(bg_name).convert('RGBA')
    con = contrast if contrast else 1.0
    bg0 = ImageEnhance.Contrast(bg0).enhance(con)
    bri = brightness if brightness else 1.0
    bg0 = ImageEnhance.Brightness(bg0).enhance(bri)

    if bg0.size[0] < bg0.size[1]:
        bg0 = bg0.resize((qr.size[0]-24, (qr.size[0]-24)*int(bg0.size[1]/bg0.size[0])))
    else:
        bg0 = bg0.resize(((qr.size[1]-24)*int(bg0.size[0]/bg0.size[1]), qr.size[1]-24))    
        
    bg = bg0 if colorized else bg0.convert('1')
    
    aligs = []
    if ver > 1:
        aloc = alig_location[ver-2]
        for a in range(len(aloc)):
            for b in range(len(aloc)):
                if not ((a==b==0) or (a==len(aloc)-1 and b==0) or (a==0 and b==len(aloc)-1)):
                    for i in range(3*(aloc[a]-2), 3*(aloc[a]+3)):
                        for j in range(3*(aloc[b]-2), 3*(aloc[b]+3)):
                            aligs.append((i,j))

    for i in range(qr.size[0]-24):
        for j in range(qr.size[1]-24):
            if not ((i in (18,19,20)) or (j in (18,19,20)) or (i<24 and j<24) or (i<24 and j>qr.size[1]-49) or (i>qr.size[0]-49 and j<24) or ((i,j) in aligs) or (i%3==1 and j%3==1) or (bg0.getpixel((i,j))[3]==0)):
                qr.putpixel((i+12,j+12), bg.getpixel((i,j)))
    
    qr_name = os.path.join(save_place, os.path.splitext(os.path.basename(bg_name))[0] + '_qrcode.png')
    qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
    return qr_name

def run():
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('WORDs', help = 'The words to produce you QR-code picture, like a URL or a sentence. Please read the README file for the supported characters.')
    argparser.add_argument('-v', '--version', type = int, choices = range(1,41), help = 'The version means the length of a side of the QR-Code picture. From little size to large is 1 to 40.')
    argparser.add_argument('-l', '--level', choices = list('LMQH'), help = 'Use this argument to choose an Error-Correction-Level: L(Low), M(Medium) or Q(Quartile), H(High). Otherwise, just use the default one: H')
    argparser.add_argument('-p', '--picture', help = 'the picture  e.g. example_pic.jpg')
    argparser.add_argument('-c', '--colorized', action = 'store_true', help = "Produce a colorized QR-Code with your picture. Just works when there is a correct '-p' or '--picture'.")
    argparser.add_argument('-con', '--contrast', type = float, help = 'A floating point value controlling the enhancement of contrast. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more. There are no restrictions on this value. Default: 1.0')
    argparser.add_argument('-bri', '--brightness', type = float, help = 'A floating point value controlling the enhancement of brightness. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more. There are no restrictions on this value. Default: 1.0')
    args = argparser.parse_args()

    tempdir = os.path.join(os.path.expanduser('~'), '.myqr')
    
    try:
        # the default version depends on WORDs and level
        # init as 0
        ver = args.version if args.version else 0
        # the default level is Q
        ecl = args.level if args.level else 'H'
        
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        
        try:
            ver, qr_name = theqrmodule.get_qrcode(ver, ecl, args.WORDs, tempdir)
        except TypeError:
            qr_name = args.picture = None

        if args.picture and args.picture[-4:]=='.gif':
            print('it takes a while, please wait for minutes...')

            import imageio
             
            im = Image.open(args.picture)
            im.save(os.path.join(tempdir, '0.png'))
            while True:
                try:
                    seq = im.tell()
                    im.seek(seq + 1)
                    im.save(os.path.join(tempdir, '%s.png' %(seq+1)))
                except EOFError:
                    break
            
            imsname = []
            for s in range(seq+1):
                bg_name = os.path.join(tempdir, '%s.png' % s)
                imsname.append(combine(ver, qr_name, bg_name, args.colorized, args.contrast, args.brightness, tempdir))
            
            ims = [imageio.imread(pic) for pic in imsname]
            qr_name = os.path.splitext(os.path.basename(args.picture))[0] + '_qrcode.gif'
            imageio.mimsave(qr_name, ims)
        elif args.picture:
            qr_name = combine(ver, qr_name, args.picture, args.colorized, args.contrast, args.brightness, os.getcwd())
        elif qr_name:
            qr = Image.open(qr_name)
            qr_name = os.path.basename(qr_name)
            qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
          
        if qr_name:
            print('Succeed! \nCheck out your ' +str(ver) + '-' + str(ecl) + ' QR-code at', os.path.abspath(qr_name))
    except:
        raise
    finally:
        import shutil
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir) 
#            
if __name__ == '__main__':
    run()