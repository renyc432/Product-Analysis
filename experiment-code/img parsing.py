# These codes read images from url
# These urls do not seem to require headers or proxies
from PIL import Image
from io import BytesIO

img_links = ['https://m.media-amazon.com/images/I/81+pOdurwpL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81etehQ8nqL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/61UXzixYkuL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81ERJyaiSuL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81HrfTqoaqL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/91aiZs3HDbL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/71PYFiUWJTL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81sqVLnXWDL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/513klQX5zdL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81NSfScVP4L._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81+pOdurwpL._AC_UL320_.jpg',
             'https://m.media-amazon.com/images/I/81etehQ8nqL._AC_UL320_.jpg',]

imgs = []
for img_link in img_links:
    response = requests.get(img_link, headers=headers)
    imgs.append(Image.open(BytesIO(response.content)))
