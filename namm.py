

try:
    from distutils.command.install_egg_info import safe_name
    import streamlit.components.v1 as components
    import json
    import os
    from io import BytesIO
    from PIL import Image
    import streamlit as st
    import numpy as np
    import base64
    import js2py
    import json
    import os
    from selenium import webdriver

except Exception as e:
    print(e)
# PIL : açık kaynak kodlu grafik işleme kütüphanesidir. Bu kütüphane,
# içinde barındırdığı hazır fonksiyonlar sayesinde programcıya üstün bir grafik işleme imkânı sunar.
# Birçok grafik türünü açıp kaydetme yeteneği ile birlikte çizim, düzenleme,
# filtreleme gibi işlemlerde kullanılabilecek fonksiyonlara sahiptir.
# lsb en önemsiz bit   \\least important bit
##############################################3
# io : Senkron ve asenkron olmak üzere iki tür I/O işlemi bulunmaktadır.
# Senkron I/O işlemlerinde uygulama bloklanmakta yani I/O işlemi tamamlanana kadar beklenilmektedir.
# Asenkron I/O işlemlerinde ise olayın tamamlanması beklenmez,
# uygulama bloklanmaksızın bu süreç boyunca başka işlemler yapılabilir
# buradaki işlevi vewrilen dosyaları türleri ile açmak örnek f= open("myfile.jpg","r",encoding,"utf-8") gibi bir
# planmlama çalıştırma için bu kütüphane kulannıldı

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

astyle = """
display: inline;
width: 200px;
height: 40px;
background: #F63366;
padding: 9px;
margin: 8px;
text-align: center;
vertical-align: center;
border-radius: 5px;
color: white;
line-height: 25px;
text-decoration: none;
"""


# Bazı Faydalı fonksiyonlar ============================
# iki görüntü arasındaki 'Ortalama Kare Hatası', iki görüntü arasındaki kare farkının toplamıdır;
# NOT: iki resim aynı boyuta sahip olmalıdır
# asytpe: veri analizinde kullanılan bir işlemdir asynic kütüphanesinden çekilir.
# shape :bir numphy fonksiyonudur ve eleman ekleme işi yapar
#
tabs = ["Hakkında"]
page = st.sidebar.radio("Sekmeler", tabs)

image1 = Image.open("mona3.png")
image2 = Image.open("heredot.png")
image3 = Image.open("tablet.png")
image4 = Image.open("kalem.png")
image5 = Image.open("kripto.png")
image6 = Image.open("neden blok zinciri.png")
image8 = Image.open("meta.png")
image9 = Image.open("650x344-python-nedir-egitim-dersleri-nereden-alinir-phyton-ile-neler-yapilabilir-tk1-1600422751598.jpg")
image10 = Image.open("download.jpg")
video_file = open('Steganografi Nedir.mp4', 'rb')
video_bytes = video_file.read()

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # MSE'yi döndürün, hata ne kadar düşükse, iki görüntü o kadar "benzer" olur
    return err


# BytesIO: Değişkenlerle yaptığımız gibi, io modülünün Byte IO işlemlerini kullandığımızda
# veriler bir bellek içi arabellekte bayt olarak tutulabilir.
def get_image_download_link(filename, img):
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = '<a href="data:file/png;base64,' + img_str + '" indir=' + filename + ' style="' + astyle + '" target="_blank">Resmi indir</a>'

    return href


#  dump . bir değer döndürmez ama verilen değeri istenilen konuma gönderir
def get_key_download_link(filename, key):
    buffered = BytesIO()
    key.dump(buffered)
    key_str = base64.b64encode(buffered.getvalue()).decode()
    href = '<a href="data:file/pkl;base64,' + key_str + '" download=' + filename + ' style="' + astyle + '" target="_blank">Download Key</a>'
    return href


# Algo 1 =======================================

# Pikseller, 8 bitlik ikili verilere göre değiştirilir ve sonunda döndürülür.
def modPix(pix, data):
    datalist = [format(ord(i), '08b') for i in data]
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Bir seferde 3 piksel çıkarma
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]

        # Piksel değeri 1 için tek yapılmalı ve 0 için bile, pix bir pikselin bir kanalıdır
        for j in range(0, 8):
            if (datalist[i][j] == '0'):
                pix[j] &= ~(1 << 0)

            elif (datalist[i][j] == '1'):
                pix[j] |= (1 << 0)

        # Her kümenin sekizinci pikseli, daha fazla okumayı durdurup durdurmayacağını söyler.
        # 0, okumaya devam et anlamına gelir; 1 mesajın bittiği anlamına gelir.
        if (i == lendata - 1):
            pix[-1] |= (1 << 0)

        else:
            pix[-1] &= ~(1 << 0)

        # yield : iteratyrler ile beraber çalışır aynı mantıkla döngülerde tekrarrı sağlar
        pix = tuple(pix)
        yield pix[0:3]  # pixel 1
        yield pix[3:6]  # pixel 2
        yield pix[6:9]  # pixel 3


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        # Değiştirilmiş pikselleri yeni görüntüye yerleştirme
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Verileri görüntüye kodlayın
def encode(filename, image, bytes):
    global c1, c2

    data = c1.text_area("Kodlanacak veriyi giriniz", max_chars=bytes)

    if (c1.button('Encode', key="1")):
        if (len(data) == 0):
            c1.error("Veri boş")
        else:
            c2.markdown('#')
            result = "Verilen veriler, verilen kapak resminde kodlanmıştır."
            c2.success(result)
            c2.markdown('####')
            c2.markdown("#### Kodlanmış resim")
            c2.markdown('######')

            newimg = image.copy()
            encode_enc(newimg, data)
            c2.image(newimg, channels="BGR")

            filename = 'encoded_' + filename

            image_np = np.array(image)
            newimg_np = np.array(newimg)
            MSE = mse(image_np, newimg_np)
            msg = "MSE: " + str(MSE)
            c2.warning(msg)
            c2.markdown("#")
            c2.markdown(get_image_download_link(filename, newimg), unsafe_allow_html=True)


# Görüntüdeki verilerin kodunu çözün
def decode(image):
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]

        # ikili veri dizisi
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))

        if (pixels[-1] % 2 != 0):
            return data


# sidebar. yazılmak iistenen değer ve fonksiyonları streamlite de yan tarafa yazar ,
# md . de kullanılan href monalisa resmine ulaşır




def main():
    global c1, c2, d1, d2


    if page == "Hakkında":
        st.markdown("<h1 style='text-align:center;'> Geliştirilen Proje</h1>",unsafe_allow_html=True)

        st.write("Geliştirlen bu web arayüzü her hangi bir ticari amaç gütmeksizin tamamı ile ücretsiz ve eğitim amaçlı kurulmuştur.")
        st.video(video_bytes)
        if st.checkbox("Projede Kullanılan Programlama Dili "):
            st.image(image9, caption="Python")
            st.markdown("<a href='https://www.python.org/'>Python</a>", unsafe_allow_html=True)
        elif st.checkbox("Projede Kullanılan Editör"):
            st.image(image10, "Pycharm")
            st.markdown("<a href='https://www.jetbrains.com/pycharm/'>Pycharm</a>", unsafe_allow_html=True)

        elif st.checkbox("Resim Gizleme ve Gizli Resmi Çözme"):
            st.sidebar.title("Dijital Görüntü İşleme Projesi")
            st.sidebar.subheader("lütfen ya metamask hesaabınız ile giriş yapın ya da başka bir yöntem deneyin")
            md = ("")
            st.sidebar.markdown(md, unsafe_allow_html=True)
            info = """
                                # Resim Steganografisi
                                Steganografi, nesnenin içinde saklı hiçbir bilgi yokmuş gibi izleyiciyi aldatacak şekilde nesnelerin içindeki 
                                bilgileri gizleme çalışması ve uygulamasıdır. 
                                Sadece hedeflenen alıcının görebilmesi için bilgileri açık bir şekilde gizler..
                                """
            fileTypes = ["png", "jpg"]
            fileTypes1 = ["pkl"]

            choice = st.radio('Seçim', ["Encode", "Decode"])
            if (choice == "Encode"):
                c1, c2 = st.columns(2)
                file = c1.file_uploader("Kapak Resmini Yükle", type=fileTypes, key="fu1")
                show_file = c1.empty()
                if not file:
                    show_file.info("Lütfen bir dosya türü yükleyin: " + ", ".join(["png", "jpg"]))
                    return

                im = Image.open(BytesIO(file.read()))
                filename = file.name
                w, h = im.size
                bytes = (w * h) // 3
                c1.info("maksimum veri: " + str(bytes) + " Bytes")
                encode(filename, im, bytes)

                content = file.getvalue()
                if isinstance(file, BytesIO):
                    show_file.image(file)

                file.close()

            elif (choice == "Decode"):
                file = st.file_uploader("Kodlanmış Resmi Yükle", type=fileTypes, key="fu2")
                show_file = st.empty()
                if not file:
                    show_file.info("Lütfen bir dosya türü yükleyin: " + ", ".join(["png", "jpg"]))
                    return

                im = Image.open(BytesIO(file.read()))

                data = decode(im)

                if (st.button('Decode', key="4")):
                    st.subheader("kodu çözülmüş metin")
                    st.write(data)

                content = file.getvalue()
                if isinstance(file, BytesIO):
                    show_file.image(file)

                file.close()
        elif st.checkbox("Örnek Çalışmalar"):
            pass






if __name__ == "__main__":
    main()
