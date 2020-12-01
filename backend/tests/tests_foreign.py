import unittest
from analyzer_foreign import Analyzer_foreign


class TestAnalyzer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text_analyzer = Analyzer_foreign()

    def test_text_1(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Шла Саша по шоссе и сосала сушку.')['sentences'],
            1
        )

    def test_text_2(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Шла Саша по шоссе и сосала сушку.')['words'],
            7
        )

    def test_text_3(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Все рабочие — от доярок до сварщиков, под команды,'
                                    ' доносившиеся из радиоприемника, дружно приседали и бегали'
                                    ' на месте! Производственная гимнастика, как и многое в СССР,'
                                    ' было добровольно-принудительным занятием. Перед обедом или'
                                    ' в конце смены в течение 5-10 минут на каждом предприятии'
                                    ' проводилась гимнастика. Рабочие, не отходя от станка, под'
                                    ' чутким руководством инструктора выполняли физические'
                                    ' упражнения.')['words'],
            54
        )

    def test_text_4(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('384')['text_ok'],
            False
        )

    def test_text_5(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('')['text_ok'],
            False
        )

    def test_text_6(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Шла Саша по шоссе, была хорошая погода. А в тексте'
                                    ' бывает english/vinglish')['words'],
            13
        )

    def test_text_7(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Сестра Криса Фармера Пенни стала журналисткой. Когда брата убили, ей было 17 лет.В 2015 году — '
                                    'через два года после смерти отца — Пенни Фармер '
                                    'решила попытаться найти предполагаемого убийцу '
                                    'брата в фейсбуке. У нее получилось моментально; '
                                    'кроме того, она нашла двух сыновей мужчины и одну '
                                    'из его жен. Она разослала всем им сообщения — и '
                                    'обратилась в полицию Манчестера. Вскоре выяснилось'
                                    ', что в Сакраменто заново открыли дело об исчезно'
                                    'вении третьей жены Бостона.Полиция допросила сынов'
                                    'ей мужчины. Они рассказали, что всегда знали, что '
                                    'Бостон убил их мать (именно его третья жена родила'
                                    'обоих). Кроме того, они рассказали, что находились'
                                    'на лодке, когда Бостон убил Криса Фармера и Пету '
                                    'Фрэмптон.')['text_ok'],
            True
        )

    def test_text_8(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Это моя одноклассница Лена. Она глупая и некрасивая: глаза круглые, уши большие, '
                                             'нос курносый, характер ужасный. Она думает, она самая умная, потому что учится хорошо. '
                                             'А я знаю: она учится хорошо, потому что уроки делает три часа в день! Она не знает, '
                                             'как называются динозавры, какие бывают автомобили. И она не играет в футбол! ')['level_int'],
            2
        )

    def test_text_9(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Это мой друг. Это моя подруга. Это мой дом. Это мое место. Это моя комната. Это моё окно. Это мой город.')['inA1'],
            100
        )

    def test_text_10(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Мария шла домой с работы. Около дома она увидела Андрея. Раньше они часто встречались,гуляли, ходили в кино, им нравилось быть вместе.'
                                             ' Но однажды Мария и Андрей поссорились и вот уже 4 месяца не видели друг друга. '
                                             'Андрей не приходил, не звонил, и Мария подумала, что у него есть другая девушка. Мария жила одна. Дома ее ждала только рыжая '
                                             'собака Бимка. Она всегда была рада, когда Мария приходила домой с работы. Девушка нашла собаку зимой на улице 3 месяца назад. '
                                             'Сначала Бимка ничего не ела, лежала и грустно смотрела на нее. Потом привыкла, начала есть, Мария ей понравилась. Девушка хотела '
                                             'узнать, чья это собака, но никто не мог сказать, кто ее хозяин. Андрей стоял около дома и ждал Марию. Он мечтал встретить ее. '
                                             '- Здравствуй Маша! - Здравствуй, Андрей! Как дела? - Все нормально.- Что ты здесь делаешь? – Мария не понимала, почему Андрей '
                                             'пришел сюда.- Я ищу свою собаку Ладу. 4 месяца назад зимой Лада гуляла одна на улице и не пришла домой. Я ищу ее все это время, '
                                             'но не могу найти. Я подумал, может быть, ты видела ее?- Твоя собака рыжая?- Да, рыжая.- Тогда пойдем ко мне. Я знаю, где твоя '
                                             'собака. Когда Мария и Андрей вошли в квартиру, Бимка побежала не к ней, а к Андрею. Хозяин и собака были очень рады друг другу.-'
                                             ' Я не знала, что у тебя есть собака, что это твоя собака, - сказала Мария.- Я купил ее, потому что мне было плохо, когда мы '
                                             'поссорились, - ответил Андрей.- Наконец, ты нашел свою Ладу, а я звала ее Бимка, - грустно сказала Мария, - теперь вы можете '
                                             'идти домой. Андрей ничего не ответил. Он понял, что пришел к Марии не потому, что искал собаку, а потому, что любит ее. '
                                             'Он не хотел уходить. А Лада-Бимка сидела, смотрела на них и тоже нехотела уходить. Она мечтала, чтобы ее старый хозяин и новая '
                                             'хозяйка были вместе.')['level_int'],
            1
        )

    def test_text_10(self):
        self.assertEqual(
            TestAnalyzer.text_analyzer.start('Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры (арендодателем) другой стороне '
                                             '(арендатору) жилого помещения за определенную плату во владение и пользование с ограниченным сроком по времени и другими '
                                             'условиями. Нотариальное заверение договора аренды не требуется и обязательной нотариальной формы такого договора '
                                             'законодательством не предусмотрено, однако по желанию - стороны вправе предусмотреть его нотариальное удостоверение. '
                                             'Арендодатель подтверждает, что он получил согласие всех совершеннолетних лиц, зарегистрированных по данному адресу, или '
                                             'владеющих совместно с ним данной жилплощадью, на сдачу данной квартиры в аренду. Арендодатель подтверждает, что на момент '
                                             'подписания настоящего Договора аренды данная квартира не продана, не подарена, не является предметом судебного спора, не '
                                             'находится под залогом, арестом, не сдана внаем. Дом на период аренды квартиры не подлежит сносу или капитальному ремонту с '
                                             'отселением. Арендодатель имеет право посещать Арендатора только с предварительным уведомлением. Арендодатель последствия аварий '
                                             'и повреждений, происшедших не по вине Арендатора, устраняет своими силами. Арендодатель оплачивает: эксплуатационные расходы, '
                                             'центральное отопление, коммунальные услуги, телефон (абонентская ежемесячная плата).') ['inB1'],
            48)

    def test_text_11(self):
        with self.assertRaises(KeyError):
            TestAnalyzer.text_analyzer.start(
                'Договор аренды квартиры — документ подтверждающий предоставление собственником квартиры (арендодателем) другой стороне '
                '(арендатору) жилого помещения за определенную плату во владение и пользование с ограниченным сроком по времени и другими '
                'условиями.')['characters']

if __name__ == '__main__':
    unittest.main()
