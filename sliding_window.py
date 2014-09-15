import sys
import PIL
from PIL import Image

def start_point(rect_width,rect_height):
  return (0,0,rect_width,rect_height)

def left2right(image,window_start,x_stepping,count):
  (x1,y1,x2,y2)=window_start
  while(x2<image.size[0]):
      img=image.crop((x1,y1,x2,y2))
      img.save(str(count)+'.jpg')
      x1+=x_stepping
      x2+=x_stepping
      count+=1
  x1=image.size[0]-(x2-x1)
  x2=image.size[0]
  img=image.crop((x1,y1,x2,y2))
  img.save(str(count)+'.jpg')
  count+=1
  return count

def up2bottom(window_start,height,y_stepping):
  (x1,y1,x2,y2)=window_start
  if (y2+y_stepping<=height):
    y1+=y_stepping
    y2+=y_stepping
  else:
    y1=height-(y2-y1)
    y2=height
  return (x1,y1,x2,y2)

def sliding(image,start_window,stepping,count):
  while(start_window[3]<image.size[1]):
    count=left2right(image,start_window,stepping[0],count)
    start_window=up2bottom(start_window,image.size[1],stepping[1])
    if(start_window[3]==image.size[1]):
      count=left2right(image,start_window,stepping[0],count)

if __name__=='__main__':
  if len(sys.argv)!=2:
    print 'Usage:%s image.jpg' % sys.argv[0]
  else:
    im=sys.argv[1]
    img=Image.open(im)
    start_window=start_point(32,32)
    sliding(img,start_window,(5,5),1)
  
    
