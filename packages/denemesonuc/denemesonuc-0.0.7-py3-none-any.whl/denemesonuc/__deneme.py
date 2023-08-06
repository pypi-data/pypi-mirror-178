from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class DersSonucObject:
    """derslere göre sonuçları saklamak için oluşturulan, pek de bir amacı olmayan sınıf"""

    dogru: int = 0
    yanlis: int = 0
    bos: int = 0
    net: float = 0.0
    soru: int = 0


@dataclass
class DenemeDereceObject:
    """dereceleri tutmak için oluşturulan, pek de bir amacı olmayan sınıf"""

    sinif: int
    kurum: int
    il: int
    genel: int


@dataclass
class Deneme:
    """deneme hakkında bilgileri tutan sınıf"""

    deneme_adi: str = ""
    url: str = "https://bes.karnemiz.com/?pg=ogrgiris"
    genel: Optional[DersSonucObject] = None
    edb: Optional[DersSonucObject] = None
    trh: Optional[DersSonucObject] = None
    cog: Optional[DersSonucObject] = None
    din: Optional[DersSonucObject] = None
    mat: Optional[DersSonucObject] = None
    fiz: Optional[DersSonucObject] = None
    kim: Optional[DersSonucObject] = None
    biy: Optional[DersSonucObject] = None
    fel: Optional[DersSonucObject] = None
    sfl: Optional[DersSonucObject] = None
    drc: Optional[DenemeDereceObject] = None
    sinif: Optional[str] = None
    puan: Optional[float] = None


class Denek:
    """# denemeye giren kişi. denek.

    `fetchDeneme`: verilen denemenin sonuçlarını çeker
    `getDeneme`: çekilen deneme sonucunu döndürür"""

    def __init__(
        self,
        driver: WebDriver,
        ad: str,
        no: int,
        sinif_duzeyi: int,
        sehir: str,
        ilce: str,
        kurum: str,
    ) -> None:
        """### denek bilgileri

        `ad`: ad
        `no`: numara
        `sinif_duzeyi`: sınıf düzeyi
        `sehir`: şehir, tamamı büyük harf olmalı
        `kurum`: okulun adı, siteye yazıldığında listede ilk sonuç olarak görünmeli"""
        self.__driver = driver
        self.ad = ad
        self.no = no
        self.sinif_duzeyi = sinif_duzeyi
        self.sehir = (
            sehir.replace("ı", "I").replace("i", "İ").upper()
        )  # pythonın localeler ile sorunu var
        self.ilce = ilce.replace("ı", "I").replace("i", "İ").upper()
        self.kurum = kurum
        self.__deneme = {}

    def __repr__(self) -> str:
        """can sıkıntısı. denekleri stringe çevirmek için. abracadabra"""
        return f"Denek: {self.no} ({self.ad})"

    def fetchDeneme(self, deneme: Deneme) -> int:
        """### denek ve deneme bilgileriyle deneme sonuçlarını çeker

        return:
        - 0: çekme başarılı
        - 1:
        - 2: denek denemeye girmemiş"""

        d = deepcopy(deneme)

        self.__driver.get(d.url)

        def click_on_list_element(text_equal_to: str, *args, **kwargs):
            ul = self.__driver.find_element(*args, **kwargs)
            li = ul.find_elements("tag name", "li")
            for i in li:
                if i.text == text_equal_to:
                    i.click()
                    return
            raise NoSuchElementException(f"element with text {text_equal_to} not found")

        self.__driver.find_element("id", "select2-gt_ogrencino_sinifcombo-container").click()
        click_on_list_element(
            str(self.sinif_duzeyi) + ".Sınıf", "id", "select2-gt_ogrencino_sinifcombo-results"
        )

        self.__driver.find_element("id", "select2-gt_ogrencino_ilcombo-container").click()
        click_on_list_element(self.sehir, "id", "select2-gt_ogrencino_ilcombo-results")

        self.__driver.find_element("id", "select2-gt_ogrencino_ilcecombo-container").click()
        click_on_list_element(self.ilce, "id", "select2-gt_ogrencino_ilcecombo-results")

        self.__driver.find_element("id", "select2-gt_ogrencino_kurumcombo-container").click()
        click_on_list_element(self.kurum, "id", "select2-gt_ogrencino_kurumcombo-results")

        ogrnoinp = self.__driver.find_element("id", "gt_ogrencino_ogrnoedit")
        ogrnoinp.send_keys(str(self.no))

        # if it exists, type value
        try:
            adinp = self.__driver.find_element("id", "gt_ogrencino_adedit")
            adinp.send_keys(self.ad)
        except NoSuchElementException:
            pass

        self.__driver.find_element("id", "gt_ogrencino_girisbtn").submit()

        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located(("xpath", "/html/body/section/div/div[1]/div/div/h6[2]"))
        )

        root = self.__driver.find_element("xpath", "/html/body/section")
        li = root.find_elements("tag name", "a")
        for i in li:
            if i.text == d.deneme_adi:
                i.click()
                break

        # at data page

        document = "/html/body/section"

        derece_head = f"{document}/div[1]/div[5]/div/div/div/"
        d_sinif = int(
            self.__driver.find_element("xpath", f"{derece_head}/div[2]").text
        )  # /html/body/section/div[1]/div[5]/div/div/div/div[2]
        d_kurum = int(
            self.__driver.find_element("xpath", f"{derece_head}/div[3]").text
        )  # /html/body/section/div[1]/div[5]/div/div/div/div[3]
        d_il = int(self.__driver.find_element("xpath", f"{derece_head}/div[5]").text)
        d_genel = int(
            self.__driver.find_element("xpath", f"{derece_head}/div[6]").text.split("\n")[0]
        )
        d.drc = DenemeDereceObject(d_sinif, d_kurum, d_il, d_genel)

        d.sinif = (
            self.__driver.find_element("xpath", f"{document}/div/div[1]/div/div/h5")
            .text.replace(
                "-", ""  # 9larda "-9A" gibi, diğer sınıflarda "11A" gibi gözüküyor o yüzden
            )
            .split()[0]
        )  # "12C / 987" gibi.

        d.puan = float(
            self.__driver.find_element(
                "xpath", f"/html/body/section/div[1]/div[3]/div/div/div/div[2]"
            ).text.replace(",", ".")
        )

        ul = self.__driver.find_element("xpath", f"{document}/div[1]")
        li = ul.find_elements("tag name", "div")

        i = 23 - 1
        available_heads = {}
        while True:
            i += 1
            try:
                self.__driver.find_element("xpath", f"{document}/div[1]/div[{i}]")
            except NoSuchElementException:
                break

            try:
                b = self.__driver.find_element("xpath", f"{document}/div[1]/div[{i}]/div/div")
                c = self.__driver.find_element(
                    "xpath", f"{document}/div[1]/div[{i+1}]/div[2]/div/div"
                )
            except NoSuchElementException:
                continue

            if c.find_elements("tag name", "h3"):
                h = "3"
            elif c.find_elements("tag name", "h2"):
                h = "2"
            elif c.find_elements("tag name", "h5"):
                h = "5[2]"
            else:
                continue

            available_heads[b.text] = DersSonucObject(
                int(
                    self.__driver.find_element(
                        "xpath", f"{document}/div[1]/div[{i+1}]/div[2]/div/div/h{h}"
                    ).text
                ),
                int(
                    self.__driver.find_element(
                        "xpath", f"{document}/div[1]/div[{i+1}]/div[3]/div/div/h{h}"
                    ).text
                ),
                int(
                    self.__driver.find_element(
                        "xpath", f"{document}/div[1]/div[{i+1}]/div[4]/div/div/h{h}"
                    ).text
                ),
                float(
                    self.__driver.find_element(
                        "xpath", f"{document}/div[1]/div[{i+1}]/div[5]/div/div/h{h}"
                    ).text.replace(",", ".")
                ),
                int(
                    self.__driver.find_element(
                        "xpath", f"{document}/div[1]/div[{i+1}]/div[1]/div/div/h{h}"
                    ).text
                ),
            )

        def getDers(name: str = "") -> DersSonucObject | None:
            """#### dersleri tek tek toplamak yerine yazılmış fonksiyon"""
            return available_heads[name] if name in available_heads else None

        d.genel = getDers("Toplam")
        d.edb = getDers("TYT Türkçe Testi Toplamı")
        d.trh = getDers("Tarih-1")
        d.cog = getDers("Coğrafya-1")
        d.din = getDers("Din Kül. ve Ahl. Bil.")
        d.mat = getDers("TYT Matematik Testi Toplamı")
        d.fiz = getDers("Fizik")
        d.kim = getDers("Kimya")
        d.biy = getDers("Biyoloji")
        d.fel = getDers("Felsefe")
        d.sfl = getDers("Felsefe (Seçmeli)")

        self.__deneme[d.deneme_adi] = d
        return 0

    def getDenemeList(self) -> list[str]:
        """### girilen denemelerin adlarının listesini döndürür"""
        return list(self.__deneme.keys())

    def getDeneme(self, deneme_adi: str) -> Deneme:
        """### çekilmiş deneme sonucunu döndürür

        `deneme_adi`: deneme adı"""
        return self.__deneme[deneme_adi]
