import os
import png
import math

empty_row = []

def expand_imgs( img, maxwidth, maxheight ):
  height = len(img)
  width = len(img[0])/4

  height_diff = (maxheight - height)/2
  width_diff = (maxwidth - width)/2

  rst = []
  for i in xrange(height_diff):
    rst.append( empty_row[:maxwidth*4] )

  for i in xrange( height ):
    lst = empty_row[:width_diff*4] + img[i] + empty_row[:width_diff*4]
    while len(lst) < maxwidth*4:
      lst += [0, 0, 0, 0]

    rst.append(lst)

  for i in xrange(height_diff):
    rst.append( empty_row[:maxwidth*4] )

  return rst 

if __name__ == '__main__':
  import sys
  argv = sys.argv

  if len(argv) != 3:
    print 'python AtlasMaker.py [rootpath] [result size]'
    sys.exit()

  finalheight = finalwidth = int(argv[2])

  rootpath = argv[1]
  if not os.path.isabs(rootpath):
    rootpath = os.path.abspath(rootpath)

  dirs = filter( lambda x:os.path.isdir(rootpath+'/'+x), os.listdir(rootpath) )

  for dirnode in dirs:
    path=str(rootpath) + '/' + str(dirnode)
    files = filter( lambda x:x[-3:].lower()=='png', os.listdir(path) )
    totalfiles = len(files)

    maxwidth = 0
    maxheight = 0

    imglist = []
    empty_row = []

    # Do I need to sort files ?

    if totalfiles == 0:
      print 'There is no png files in', path
      continue

    for strpngfile in files:
      print 'In ', path, ', ', strpngfile, 'is loading...'
      pngfile = png.Reader(path+'/'+strpngfile)
      width, height, pixels, data = pngfile.asRGBA()

      array_list = list( pixels )
      pixels = map ( lambda x:x.tolist(), array_list )
      # returned format : [ [ first row ], [ second row ] ... ]
      # for each row [ r, g, b, a, r, g, b, a ... ]

      maxwidth = width if maxwidth < width else maxwidth
      maxheight = height if maxheight < height else maxheight

      imglist.append(pixels)

    colsize = finalwidth / maxwidth
    rowsize = finalheight / maxheight
    filesize = totalfiles / (colsize *rowsize)

    if totalfiles%(colsize*rowsize) != 0:
      filesize += 1

    for i in xrange(finalwidth*4):
      empty_row.append(0)

    expand_list = map( lambda x:expand_imgs(x, maxwidth, maxheight), imglist )

    def extract_files( fileidx, expand_data ):
      """
      result : by row unit
      rowsize : calculated row size
      colsize : calculated column size
      """

      result = []
      for i in xrange(rowsize):
        startidx = i*colsize
        endidx = min( (i+1)*colsize, len(expand_data) )
        diffwidth = ((i+1)*colsize - endidx )*maxwidth

        if startidx < endidx:
          semiresult = []
          for row in zip(*expand_data[startidx:endidx]):
            semiresult.append( reduce( lambda x, y:x+y, row ) )

          for row in semiresult:
            result.append(row + empty_row[:(finalwidth - maxwidth*colsize + diffwidth)*4])

        else:
          for i in xrange( maxheight ):
            result.append(empty_row)

      while finalheight > len(result):
        result.append(empty_row)

      if data.has_key('size'):
        del data['size']

      print 'In ', path, ', ', str(fileidx)+'.png is written'

      w = png.Writer(width=finalwidth, height=finalheight, **data)
      outfile = open(path + '/' + str(fileidx) + '.png', 'wb')
      w.write( outfile, result )
      outfile.close()

    for i in xrange(filesize):
      start_index = i*rowsize*colsize
      end_index = min( start_index + rowsize*colsize, len(expand_list) )
      extract_files(i, expand_list[start_index:end_index] )

