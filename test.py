import sys
from html.parser import HTMLParser
from urllib.request import urlopen,Request
from urllib import parse
import json
import mysql.connector as mysql

db = mysql.connect(
   host = "localhost",
   user = "root",
   passwd = "Danu21510",
   database = "researchnew"
)
cursor = db.cursor()

class LinkParser(HTMLParser):
    res=[]
    word=""
    links = []

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="https://www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # https://www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # https://www.netinstructions.com/somepage.html
                    if(value.lower().find(LinkParser.word)>-1):
                        newUrl = parse.urljoin(self.baseUrl, value)
                        self.links = self.links + [newUrl]
                    # And add it to our colection of links:

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url,word):
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        client = Request(url, headers={"User-Agent" : "Mozilla/5.0"})
        response = urlopen(client)
        #response = requests.get(url)
        #print(response,flush=True)
        #print(response.getheader('Content-Type'))
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        if response.getheader('Content-Type').find('text/html')>-1:
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            #print(htmlString)
            if(htmlString.lower().find(word)>-1):
                #print(url)
                return True, self.links
            else:
                return False, []
        else:
            return False, []

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):
    Colombo=["colombo","moratuwa","nugegoda","dehiwala","homagama","kaduwela","kesbewa","kolonnawa","kotte","maharagama","padukka"]
    Colombo=Colombo+["ratmalana","seethawaka","thimbirigasyaya","peliyagoda","avissawella","navinna","wijerama"]
    Colombo=Colombo+["nugegoda","Kalubovila","kirulapone","mount-lavinia","jayawardenapura","dematagoda","borella","boralesgamuwa"]
    Colombo=Colombo+["rajagiriya","malabe","delkanda","pamankada","kurunduwatta","maradana"]
    Gampaha=["gampaha","ragama","attanagalla","biyagama","divulapitiya","dompe","ja-ela","katana","kelaniya"]
    Gampaha=Gampaha+["mahara","minuwangoda","mirigama","negombo","wattala","Kadawatha"]
    kaluthara=["kaluthara","kalutara","agalawatta","bandaragama","beruwala","bulathsinhala","dodangoda","horana","ingiriya"]
    kaluthara=kaluthara+["madurawela","mathugama","millaniya","palindanuwara","panadura","walallavita"]
    Matale=["matale","ambanganga-korale","dambulla","galewela","laggala-pallegama","naula","pallepola","rattota"]
    Matale=Matale+["ukuwela","wilgamuwa","yatawatta"]
    Kandy=["kandy","akurana","delthota","doluwa","ganga-ihala","harispattuwa","hatharaliyadda","kundasale"]
    Kandy=Kandy+["medadumbara","minipe","panvila","pasbage","pathadumbara","pathahewaheta","poojapitiya","thumpane"]
    Kandy=Kandy+["udadumbara","udapalatha","udunuwara","yatinuwara"]
    Nuwaraeliya=["nuwaraeliya","ambagamuwa","hanguranketha","kothmale","walapane"]
    Ampara=["ampara","addalachchenai","akkaraipattu","alayadiwembu","damana","dehiattakandiya"]
    Ampara=Ampara+["eragama","kalmunai","karaitivu","lahugala","mahaoya","navithanveli","ninthavur","padiyathalawa"]
    Ampara=Ampara+["pothuvil","sainthamarathu","samanthurai","thirukkovil","uhana"]
    Batticaloa=["batticaloa","eravur","kattankudy","koralai","manmunai","porativu"]
    Trincomalee=["trincomalee","gomarankadawala","kantalai","kinniya","kuchchaveli","morawewa","muttur"]
    Trincomalee=Trincomalee+["padavi-sri-pura","seruvila","thambalagamuwa","verugal"]
    Anuradhapura=["anuradhapura","galnewa","galenbindunuwewa","horowpothana","ipalogama","kahatagasdigiliya"]
    Anuradhapura=Anuradhapura+["kebithigollewa","kekirawa","mahavilachchiya","medawachchiya","mihinthale","nachchadoowa"]
    Anuradhapura=Anuradhapura+["nochchiyagama","nuwaragam-palatha","padaviya","palagala","palugaswewa","rajanganaya"]
    Anuradhapura=Anuradhapura+["rambewa","thalawa","thambuttegama","thirappane"]
    Polonnaruwa=["polonnaruwa","dimbulagala","elahera","hingurakgoda","lankapura","medirigiriya"]
    Polonnaruwa=Polonnaruwa+["thamankaduwa","welikanda"]
    Jaffna=["jaffna","delft","karainagar","nallur","thenmaradchi","vadamaradchi","valikamam"]
    Kilinochchi=["kilinochchi","kandavalai","karachchi","pachchilaipalli","poonakary"]
    Mannar=["mannar","madhu","manthai","musalai","nanaddan"]
    Mullaitivu=["mullaitivu","maritimepattu","oddusuddan","puthukudiyiruppu","thunukkai","welioya"]
    Vavuniya=["vavuniya","vengalacheddikulam"]
    Kurunegala=["kurunegala","alawwa","ambanpola","bamunakotuwa","bingiriya","ehetuwewa","galgamuwa",]
    Kurunegala=Kurunegala+["ganewatta","giribawa","ibbagamuwa","katupotha","kobeigane","kotavehera","kuliyapitiya"]
    Kurunegala=Kurunegala+["mahawa","mallawapitiya","maspotha","mawathagama","narammala","nikaweratiya","panduwasnuwara"]
    Kurunegala=Kurunegala+["pannala","polgahawela","polpithigama","rasnayakapura","rideegama","udubaddawa"]
    Kurunegala=Kurunegala+["wariyapola","weerambugedara"]
    Puttalam=["puttalam","anamaduwa","arachchikattuwa","chilaw","dankotuwa","kalpitiya","karuwalagaswewa"]
    Puttalam=Puttalam+["madampe","mahakumbukkadawala","mahawewa","mundalama","nattandiya","nawagattegama"]
    Puttalam=Puttalam+["pallama","vanathavilluwa","wennappuwa"]
    Kegalle=["kegalle","aranayaka","bulathkohupitiya","dehiovita","deraniyagala","galigamuwa","mawanella"]
    Kegalle=Kegalle+["rambukkana","ruwanwella","warakapola","yatiyanthota"]
    Ratnapura=["ratnapura","ayagama","balangoda","eheliyagoda","elapattha","embilipitiya","godakawela"]
    Ratnapura=Ratnapura+["imbulpe","kahawatta","kalawana","kiriella","kolonna","kuruvita","nivithigala","opanayaka"]
    Ratnapura=Ratnapura+["pelmadulla","weligepola"]
    Galle=["galle","akmeemana","ambalangoda","baddegama","balapitiya","benthota","bope-poddala","elpitiya"]
    Galle=Galle+["gonapinuwala","habaraduwa","hikkaduwa","imaduwa","karandeniya","nagoda","neluwa","niyagama"]
    Galle=Galle+["thawalama","welivitiya","divithura","yakkalamulla"]
    Hambantota=["hambantota","ambalantota","angunakolapelessa","beliatta","katuwana","lunugamvehera"]
    Hambantota=Hambantota+["okewela","sooriyawewa","tangalle","thissamaharama","walasmulla","weeraketiya"]
    Matara=["matara","akuressa","athuraliya","devinuwara","dickwella","hakmana","kamburupitiya","kirinda"]
    Matara=Matara+["puhulwella","kotapola","malimbada","mulatiyana","pasgoda","pitabeddara","thihagoda","weligama"]
    Matara=Matara+["welipitiya"]
    Badulla=["badulla","bandarawela","ella","haldummulla","hali-ela","haputale","kandaketiya","lunugala"]
    Badulla=Badulla+["mahiyanganaya","meegahakivula","passara","rideemaliyadda","soranathota","uva-paranagama"]
    Badulla=Badulla+["welimada"]
    Moneragala=["moneragala","monaragala","badalkumbura","bibile","buttala","katharagama","madulla","medagama"]
    Moneragala=Moneragala+["sevanagala","siyambalanduwa","thanamalvila","wellawaya"]
    LinkParser.word=word
    originalurl=url
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited=numberVisited+1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            #print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            foundWord, link = parser.getLinks(url,word)
            location="colombo"
            if foundWord:
                LinkParser.links=LinkParser.links+list(set(link))
                for i in link: 
                    try:
                        location="colombo" if(sum(1 for _ in filter(lambda x: x in i.lower(), Colombo))) > 0 else location
                        location="kalutara" if(sum(1 for _ in filter(lambda x: x in i.lower(), kaluthara))) > 0 else location
                        location="gampaha" if(sum(1 for _ in filter(lambda x: x in i.lower(), Gampaha))) > 0 else location
                        location="matale" if(sum(1 for _ in filter(lambda x: x in i.lower(), Matale))) > 0 else location
                        location="kandy" if(sum(1 for _ in filter(lambda x: x in i.lower(), Kandy))) > 0 else location
                        location="nuwaraeliya" if(sum(1 for _ in filter(lambda x: x in i.lower(), Nuwaraeliya))) > 0 else location
                        location="ampara" if(sum(1 for _ in filter(lambda x: x in i.lower(), Ampara))) > 0 else location
                        location="batticaloa" if(sum(1 for _ in filter(lambda x: x in i.lower(), Batticaloa))) > 0 else location
                        location="trincomalee" if(sum(1 for _ in filter(lambda x: x in i.lower(), Trincomalee))) > 0 else location
                        location="anuradhapura" if(sum(1 for _ in filter(lambda x: x in i.lower(), Anuradhapura))) > 0 else location
                        location="polonnaruwa" if(sum(1 for _ in filter(lambda x: x in i.lower(), Polonnaruwa))) > 0 else location
                        location="jaffna" if(sum(1 for _ in filter(lambda x: x in i.lower(), Jaffna))) > 0 else location
                        location="kilinochchi" if(sum(1 for _ in filter(lambda x: x in i.lower(), Kilinochchi))) > 0 else location
                        location="mannar" if(sum(1 for _ in filter(lambda x: x in i.lower(), Mannar))) > 0 else location
                        location="mullaitivu" if(sum(1 for _ in filter(lambda x: x in i.lower(), Mullaitivu))) > 0 else location
                        location="vavuniya" if(sum(1 for _ in filter(lambda x: x in i.lower(), Vavuniya))) > 0 else location
                        location="kurunegala" if(sum(1 for _ in filter(lambda x: x in i.lower(), Kurunegala))) > 0 else location
                        location="puttalam" if(sum(1 for _ in filter(lambda x: x in i.lower(), Puttalam))) > 0 else location
                        location="kegalle" if(sum(1 for _ in filter(lambda x: x in i.lower(), Kegalle))) > 0 else location
                        location="ratnapura" if(sum(1 for _ in filter(lambda x: x in i.lower(), Ratnapura))) > 0 else location
                        location="galle" if(sum(1 for _ in filter(lambda x: x in i.lower(), Galle))) > 0 else location
                        location="hambantota" if(sum(1 for _ in filter(lambda x: x in i.lower(), Hambantota))) > 0 else location
                        location="matara" if(sum(1 for _ in filter(lambda x: x in i.lower(), Matara))) > 0 else location
                        location="badulla" if(sum(1 for _ in filter(lambda x: x in i.lower(), Badulla))) > 0 else location
                        location="moneragala" if(sum(1 for _ in filter(lambda x: x in i.lower(), Moneragala))) > 0 else location
                    except Exception as e:
                        print(e)
                    query = "INSERT INTO links (website, url,location) VALUES (%s, %s, %s)"
                    print(i," ",location)
                    values = (url,i,location)
                    cursor.execute(query, values)
                    db.commit()
                continue
        except:
            continue
    return LinkParser.links

def item():
    websites=["https://riyasewana.com","https://www.carmudi.lk","http://www.riyapola.com","https://www.ikman.lk","https://www.autolanka.com"]
    websites=websites+["https://www.hitadd.lk","https://www.patpat.lk","https://www.automart.lk","https://www.isharatraders.com","https://www.automachan.lk","https://www.ikmanata.lk"]
    websites=websites+["https://www.saleme.lk","https://www.siyalla.lk","https://www.classifieds.lk","https://www.admart.lk","https://www.ape.lk","https://www.soyanna.com","https://www.lkads.lk","https://www.automachan.lk"]
    websites=websites+["https://www.myoffers.lk","https://www.usee.lk","https://www.wahana.lk","https://www.ranads.lk","https://www.ceylonads.lk","https://www.hanika.lk"]
    for url in websites:
        spider(url,sys.argv[1],50)

def main():
    item()

if __name__== "__main__":
      main()
