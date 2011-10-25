import png

if __name__ == '__main__':
  import sys
  argv = sys.argv

  if len(argv) != 2:
    print 'python PngReader.py [filename]'
    sys.exit()

  filname = argv[1]
  empty_row = []

  pngfile = png.Reader('./'+filename)
  width, height, pixels, data = pngfile.asDirect()

  array_list = list( pixels )
  pixels = map ( lambda x:x.tolist(), array_list )

  for row in pixels:
    cnt = 0
    for value in row:
      cnt += 1
      if cnt%4 == 0 && value != 0:
        print 'Alpha :', value

