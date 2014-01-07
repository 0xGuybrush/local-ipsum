# -*- coding: utf-8 -*-

import web
import urllib
import urllib2
import contextlib
import string
import sys
import lipsum
import contextlib
from bs4 import BeautifulSoup, Comment, Tag

urls = (
	'/([a-z]{2})/(.*)', 'index'
)

class index:

	def GET(self, lang, sitename):
		rightToLeftLanguages = ["ar", "iw"]
		
		dom = getPageContents(sitename)
		dom = makeEverythingAbsolute(dom, sitename)
		#Don't change content if English is passed as the language
		if lang == "en":
			return dom.prettify()
		
		#Make Arabic or Hebrew pages RTL
		if lang in rightToLeftLanguages:
			dom.html['dir'] = "rtl"
		
		return replaceContent(dom, lang)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()

def replaceContent(dom, lang):
		#arabicSample = "التزامنا بالمساهمة المباشرة وغير المباشر.ة في حل مجموعة من. القضايا الملحة. ونحن على قناعة بأننا قادرون على إحداث فرق سواء في. المملكة العربية السعودية أو في المناطق الت.ي نعمل بها، وذلك من خلال الاستثمار في الابتكار وتثمين روح المبادرة، وتوفير الفرص التعليمية، ودعم التقدم الاقتصادي، وزيادة ا.وعي البيئي، وإقامة شراكات لتحقيق الاستدامة في مجا"
		koreanSample = "국제화와 현지화는 동일 문화권이 아닌 환경(특히 다른 국가나 문화)에서 만들어진 출판물이나 하드웨어 또는 소프트웨어를 특정 환경에 맞춰 적용하는 것을 의미한다. 두 낱말은 비슷한 주제를 다루지만 약간의 차이가 있는데, 국제화가 앞으로 가능성 있는 다른 환경을 지원할 수 있도록 하는 것이라면 현지화는 이미 존재하는 환경에 맞춘 기능을 지원하는 것이다."
		af = ["Waar", "teks", "in", "die", "dokument", "sigbaar", "is", "is", "mense", "geneig", "om", "hul", "aandag", "op", "die", "inhoud", "van", "die", "teks", "te", "vestig", "eerder", "as", "op", "die", "oorhoofse", "aanbieding", "en", "daarom", "gebruik", "uitgewers", "wanneer", "hulle", "lettertipe", "of", "ontwerpe", "voorstel", "om", "die", "aandag", "eerder", "op", "die", "aanbieding", "te", "vestig"]
		ar = ["هنالك", "العديد", "من", "الآراء", "في", "أصل", "العربية", "لدى", "قدامى", "اللغويين", "العرب", "فيذهب", "البعض", "إلى", "أن", "يعرب", "كان", "أول", "من", "أعرب", "في", "لسانه", "وتكلم", "بهذا", "اللسان", "العربي", "فسميت", "اللغة", "باسمه،", "وورد", "في", "الحديث", "النبوي", "أن", "نبي", "الله", "إسماعيل", "بن", "إبراهيم", "أول", "من", "فُتق"]
		bg = ["Текстът", "е", "безсмислен", "но", "визуално", "много", "прилича", "на", "истински", "заради", "разпределението", "и", "честотата", "на", "срещане", "на", "по-къси", "средни", "и", "дълги", "думи", "разпределението", "на", "интервалите", "и", "препинателните", "знаци", "както", "и", "дължината", "на", "изреченията"]
		ca = ["Encara", "que", "", "pugui", "suscitar", "curiositat", "per", "la", "seva", "semblança", "amb", "el", "llatí", "clàssic", "la", "intenció", "és", "que", "el", "text", "no", "tingui", "significat", "Quan", "un", "text", "és", "comprensible", "la", "gent", "sol", "centrar-se", "en", "el", "contingut", "textual", "més", "que", "en", "l'efecte", "visual", "Per", "això", "els", "editors", "i", "els", "dissenyadors", "fan", "servir", "aquest", "text", "sense", "significat", "perquè", "l'atenció", "se", "centri", "en", "l'estil", "i", "la", "presentació"]
		zh = ["艭蠸", "圛嬖嬨", "螭蟅謕", "鷃黫鼱", "葮", "溛滁", "肵苂苃", "梴棆棎", "媝寔嵒", "劁", "韕顊", "蜭蜸覟", "涬淠淉", "撱", "轖轕", "蹢鎒鎛", "姛帡恦", "螒螝螜", "緷", "杺枙", "鄜酳銪", "笓粊紒", "獌", "蹢鎒鎛", "珝砯砨", "澂", "螾褾", "榃", "皾籈", "鄨鎷闒", "蒠蓔蜳", "鬋鯫鯚", "輗鋱", "燚璒瘭", "僄塓塕", "絼", "幋", "榃痯痻", "碞碠粻", "黰戄", "餤駰鬳", "醳鏻鐆", "躨钀钁", "銈", "馞鮂", "斠", "拻敁柧", "瞗穇縍", "韰頯餩", "襆贂", "槏殟殠", "茇茺苶", "熩熝犚", "甂睮", "榎"]
		cs = ["Pokud", "by", "se", "pro", "stejný", "účel", "použil", "smysluplný", "text", "bylo", "by", "těžké", "hodnotit", "pouze", "vzhled", "aniž", "by", "se", "pozorovatel", "nechal", "svést", "ke", "čtení", "obsahu", "Pokud", "by", "byl", "naopak", "použit", "nesmyslný", "ale", "pravidelný", "text", "oko", "by", "při", "posuzování", "vzhledu", "bylo", "vyrušováno", "pravidelnou", "strukturou", "textu", "která", "se", "od", "běžného", "textu", "liší"]
		da = ["Teksten", "bruges", "som", "fyldtekst", "for", "at", "ordene", "ikke", "skal", "forstyrre", "det", "grafiske", "udtryk", "under", "selve", "layout-processen", "Fyldteksten", "kan", "genereres", "automatisk", "i", "flere", "moderne", "dtp-programmer", "som", "benytter", "også", "automatisk", "tekste"]
		fr = ["Li", "Europan", "lingues", "es", "membres", "del", "sam", "familie", "Lor", "separat", "existentie", "es", "un", "myth", "Por", "scientie,", "musica,", "sport", "etc,", "litot", "Europa", "usa", "li", "sam", "vocabular", "Li", "lingues", "differe", "solmen", "in", "li", "grammatica,", "li", "pronunciation", "e", "li", "plu", "commun", "vocabules", "Omnicos", "directe", "al", "desirabilite", "de", "un", "nov", "lingua", "franca:", "On", "refusa", "continuar", "payar", "custosi", "traductores", "At", "solmen", "va", "esser", "necessi", "far", "uniform", "grammatica,", "pronunciation", "e", "plu", "sommun", "paroles", "Ma", "quande", "lingues", "coalesce,", "li", "grammatica", "del", "resultant", "lingue", "es", "plu", "simplic", "e", "regulari", "quam", "ti", "del", "coalescent", "lingues", "Li", "nov", "lingua", "franca", "va", "esser", "plu", "simplic", "e", "regulari", "quam", "li", "existent", "Europan", "lingues", "It", "va", "esser", "tam", "simplic", "quam", "Occidental", "in", "fact,", "it", "va", "esser", "Occidental", "A", "un", "Angleso", "it", "va", "semblar", "un", "simplificat", "Angles,", "quam", "un", "skeptic", "Cambridge", "amico", "dit", "me", "que", "Occidental", "es", "Li", "Europan", "lingues", "es", "membres", "del", "sam", "familie", "Lor", "separat", "existentie", "es", "un", "myth", "Por", "scientie,", "musica,", "sport", "etc,", "litot", "Europa", "usa", "li", "sam", "vocabular", "Li", "lingues", "differe", "solmen", "in", "li", "grammatica,", "li", "pronunciation", "e", "li", "plu", "commun", "vocabules", "Omnicos", "directe", "al", "desirabilite", "de", "un", "nov", "lingua", "franca:", "On", "refusa", "continuar", "payar", "custosi", "traductores", "At", "solmen", "va", "esser", "necessi", "far", "uniform", "grammatica,", "pronunciation", "e", "plu", "sommun", "paroles"]
		hi = ["दस्तावेज", "वास्तविक", "परिभाषित", "देने", "सुचना", "विश्व", "प्रमान", "समस्याओ", "जानकारी", "थातक", "अधिक", "संस्था", "विनिमय", "चुनने", "औषधिक", "कैसे", "परस्पर", "हमेहो।", "कार्यलय", "सुचनाचलचित्र", "बारे", "उन्हे", "पहेला", "कलइस", "सहायता", "संपुर्ण", "पुर्व", "उशकी", "केन्द्रित", "स्वतंत्रता", "विशेष", "रिती", "उद्योग", "एकत्रित", "गोपनीयता"]
		ko = ["로렘", "입숨은", "전통", "라틴어와", "닮은", "점", "때문에", "종종", "호기심을", "유발하기도", "하지만", "그", "이상의", "의미를", "담지는", "않는다.", "문서에서", "텍스트가", "보이면", "사람들은", "전체적인", "프레젠테이션보다는", "텍스트에", "담긴", "뜻에", "집중하는", "경향이", "있어서", "출판사들은", "서체나", "디자인을", "보일", "때는", "프레젠테이션", "자체에", "초점을", "맞추기", "위해", "로렘", "입숨을", "사용한다.", "로렘", "입숨은", "영어에서", "사용하는", "문자들의", "전형적인", "분포에", "근접하다고도", "하는데", "이", "점"]
		ru = ["Вэре", "омныз", "дикунт", "квюо", "йн", "вим", "ты", "дёко", "дикырыт", "ныглэгэнтур", "Ку", "рыбюм", "янжольэнж", "витюпырата", "про", "Эжт", "ку", "дикунт", "омйттам", "пробатуж", "зыд", "омнеж", "позтюлант", "интэллэгат", "нэ", "Нибх", "прима", "ты", "вим", "нык", "но", "емпыдит", "щуавятатэ", "Ан", "прё", "тота", "анкилльаы", "ед", "дуо", "дикунт", "бландит", "конкльюдатюрквюэ", "йн", "лэгыры", "квюоджё", "кончэтытюр", "векж"]
		el = ["Φιξ", "πωσιθ", "σεθερος", "περτιναξ", "αδ", "εξπετενδα", "αδωλεσενς", "ηις", "ιν", "εως", "ιδ", "γραεσε", "επισυρει", "Στετ", "υνυμ", "νες", "νο", "ιυσθο", "ασυμσαν", "νε", "ναμ", "ατ", "ιγνωθα", "τασιμαθες", "πρω", "Μινιμ", "αλβυσιυς", "κυι", "ιδ", "ηις", "υλλυμ", "φερθερεμ", "ατ", "ομνες", "σανστυς", "μωλεστιαε", "νο", "μει", "Εσε", "δεσερυντ", "μωλεστιαε", "φιμ", "υθ", "υσυ", "νε", "ορατιο", "μυνερε", "Ναμ", "νο", "ρεβυμ", "φασιλισις", "τεμποριβυς", "Υθ", "ιυς", "ευισμοδ", "φευγαιθ", "νοσθερ", "αλβυσιυς", "περσεσυτι", "ιν", "εως", "Εα", "σεα", "φισι", "λαβορες", "ευ", "μει", "νισλ", "δελεσθυς", "παρτιενδω"]
		iw = ["אל", "זכר", "עיצוב", "מדינות", "וכמקובל", "שער", "גם", "צילום", "רומנית", "מיתולוגיה", "את", "רביעי", "לאחרונה", "כלל", "בה", "מתן", "נפלו", "ביוני", "סדר", "ב", "זקוק", "פיסול", "אדריכלות", "היא", "רביעי", "מועמדים", "של", "כדי", "של", "כניסה", "הנדסת", "תחבורה", "צעד", "אם", "ביולי", "ופיתוחה", "על", "כיצד", "אתנולוגיה", "עזה", "בה", "כתב", "צרפתית", "הקהילה", "ביוטכנולוגיה", "עזרה", "למנוע", "בהשחתה", "ארץ", "גם"]
		ja = ["すしょシ", "る訊栤襃詞", "㫣諤鄤綩奟", "べチ滩䦌や", "姚ー", "ネ姚ー", "媥ちゅ", "襧ごドヂャ䋯", "䛨襞䥞儦ろ", "栣と駺", "夯団", "簣ぬ䤤曣ひ", "み鎌ね誧䄦", "滩䦌", "勤詩びゃ毚堨", "げ䥚ぐ媤に", "觚驩きょえ穞", "ごドヂャ", "りゅ栣", "润揧馨", "勤詩びゃ毚堨", "姟ギャ驚ぴゅ祌", "訦しゃ尦ヤ姥", "ガう䰯鏨尥", "りゃそにゃヂュ觧", "鰣夦の", "奚氩", "ひゃ鋨じぜ饜", "ぽ壃すしょシ", "觚驩きょえ穞", "ぽ壃", "レぞ婃", "杯ス樚", "ク仯", "騧りへ㤣䩨", "ぽ壃すしょシ", "テ	て氯きゃデュ", "勣㣌ぶ禯ゑ", "嫯勯じゅク仯", "ベ䤦くぢゃ極", "穥み", "ポ驨夯", "お谨窣期ゆ", "ぽ壃すしょシ", "べチ滩䦌や", "ひゅ椥キョ", "窯ビ", "ごドヂャ", "くぢゃ", "姟ギャ驚ぴゅ祌", "䨯䥦ㄨ稪い", "れ焨もキュぷ", "げ䥚ぐ媤に", "裟ち㧦ギェゲ", "嫯勯じゅ", "ビャ覟", "饜ぼしゅ", "䤥ブらゐちゃ", "ぴょちょぢゅ鍯騟", "訦しゃ尦ヤ姥", "姟ギャ"]
		
		#korean = (koreanSample, koreanSample.split(" "))
		attributes = ["value", "option", "title", "alt"]
		cjk = ["zh", "ja", "ko"]


		lipsumGen = lipsum.Generator()
		
		if lang in locals():
			lipsumGen.dictionary = locals()[lang]
		for attribute in attributes:
			for element in dom.find_all(attrs={locals()["attribute"]: True}):
				if element[attribute] != "":
					textLength = int(len(element[attribute]) * 1.3)
					newText = unicode(lipsumGen.generate_paragraph(), 'utf-8')
					if len(newText) > textLength:
						newText = newText[:textLength]
					element[attribute] = newText
		
		newLines = dom.find(text="\n")
		if newLines is not None:
			newLines.replaceWith("")
			
		for text in	dom.findAll(text=True):
			if (text.parent.name != "script" and text.parent.name != "style") and not isinstance(text, Comment) and text.string != "\n" and text.string != " " and not "html" in text.string:
					if lang in cjk:
						words = text.string.split(" ")
						textLength = int(len(words) * 1.8)
					else:
						textLength = int(len(text.string) * 1.3) # Setting a max size of current text length + 33%
					newText = unicode(lipsumGen.generate_paragraph(), 'utf-8')
					if len(newText) > textLength:
						newText = newText[:textLength]
					text.string.replace_with(newText)
					
		metaTag = dom.new_tag("meta")
		metaTag['http-equiv'] = "Content-Type"
		metaTag['content'] = "text/html; charset=utf-8"
		dom.head.insert(1, metaTag)
		return dom.prettify()
		
def getPageContents(sitename):
					
	if not sitename.startswith("http:"):
		sitename = "http://" + sitename
		
	request = urllib2.Request(sitename, headers={'User-Agent' : 'Mozilla/5.0'})
	with contextlib.closing(urllib2.urlopen(request)) as response:
		thePage = response.read()
	return BeautifulSoup(thePage)

def makeEverythingAbsolute(dom, sitename):
	domain = "http://www."
	if "/" in sitename:
		domain += sitename.split("/")[0]
	else: 
		domain += sitename
	for el in dom.find_all(href=True):
		if el['href'].startswith('/'):
			el['href'] = domain + el['href']
		if not el['href'].startswith("http") and not el['href'].startswith("#"):
			el['href'] = domain + "/" + el['href']
	for el in dom.find_all(src=True):
		if el['src'].startswith('/'):
			el['src'] = domain + el['src']
		if not el['src'].startswith("http"):
			el['src'] = domain + "/" + el['src']
	return dom
