import pandas as pd

stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

spell_errors =['ks','tiway','s', 'm','t', 'ts', 'h', 'bajan', 'misfieldsl', 'fafa' ,'midiwicket','yaara','hiiiiiiiigh','questioneverybody','ufff','anorher', 'noetheless','slipgoogly', 'slipslammed', 'fuil', 'shamsuddin', 'prasidhs', 'smith-like', 'decisionsmith', 'md-on', 'xis', 'neednt', 'rethin', 'snea', 'offpulled', 'helmethe', 'leggies', 'hanfcuffs', 'bushnoi', 'cumminss', 'juuuust', 'thing:', 'qide', 'showins', 'fingerspin', 'hoemcoming', 'rcba', 'natmeg', 'dcs', 'finethis', 'mis-timing', 'guntur', 'zampas', 'prayas', 'hnds', 'b-l-u-d-g-e-o-n', 'tewatis', 'ashwins', 'plessus', 'jb', 'boundarys', 'crackalicious', 'batsmans', 'yorrker', 'quinnys', 'binnsta', 'roomgayle', 'mid-om', 'barbadian', 'yoroker', 'slip/', 'snadeep', 'gowatham', 'swins', 'yuuuge', 'shami-like', 'humongouuuuuus', 'that:', 'dowhose', 'shot:', 'bowledim', 'under-edging', 'dags', 'ovcerpitched', 'baaaang', 'ayyappa', 'mucles', 'rasikh', 'cuurrrrrruch', 'huuuuuuuge', 'toards', 'deepmidwicket', 'goees', 'thakurs', 'half-dived', 'runbs', 'piack-up', 'ts', 'nutmegs', 'perfctly', 'yorkrs', 'sahas', 'mishy', 'midwcket', 'stanlakes', 'kn', 'tiway', 'nudger', 'all-karnataka', 'entirelyfluent', 'banjaxed', 'no-one', 'tip-and-run', 'back-pedalling', 'bouner', 'backpeddling', 'yassss', 'hismelf', 'stoinies', 'uae', 'ct', 'plukcs', 'thereve', 'theremight', 'naik', 'celebrappeal', 'fiyah', 'yokrer', 'nahhhhh', 'legbrea', 'back-flic', 'dhoni-like', 'hetmer', 'td', 'nowhwere', 'bardue', 'it>', 'wankhede', 'edege', 'axars', 'deliverys', 'nd', 'russ-type', '#weird', 'bhajjis', 'bishno', 'pc', 'mid-ridd', 'result:', 'hiiiiiigh', 'p-i-s-s-e-d', 'mdiwicket', 'gaule', 'swkwardly', 'yjb', 'fulishl', 'ovepitched', 'gayle-y', 'revrse', 'stumpgets', 'st', 'operation:', 'ingrams', 'insult:', 'elft', 'place:', 'noooooooooo', 'bowler:', 'gpsing', 'chahah', 'short-of-a-lenght', 'padikka', 'n', 'remonstrates', 'itoffers', 'overmidwicket', 'waaaaay', 'hjes', '---', 'aorund', 'cresae', 'squeareleg', 'showes', 'ngdi', 'crunnnnnnches', 'itdips', 'happenin', 'ohhh', 'fiedler', 'attac', 'eaaaaasssy', 'jubbly', 'finee', 'staright', 'bould', 'mvp', 'onfield', 'nurdling', 'wided', 'k', 'dilscoops', 'dooper', 'spanged', 'paranthas', 'gaffaneys', 'half-ducking-half-pulling', 'chirs', 'mars-kisser', 'ooooof', 'buttler-like', 'pt', 'year:', 'again:', 'wanst', 'legspiner', 'plumblest', 'pad-boot', 'immeidately', '-run', 'kathik', 'anorher', 'long--on', 'footthat', 'snt', 'chest-hunting', 'mankaded', 'kadhav', 'wayyyyyyyyy', 'over:', '-year', 'otuside', 'inwinger', 'huuuge', 'special:', 'juuuuuust', 'saha:', 'kablammo', '#magic', 'enoogh', 'p', 'kxp', 'forwardwilliamson', 'hiiiiiiiigh', 'sycthes', 'pitchside', 'finewarner', 'maraius', '-year-old', 'flattie', 'ewin', 'keps', 'oh-so-often', 'sweeeper', 'body-weight', 'stic', 'samson-smith', 'twenty-two', 'camerman', 'crrrrrraaack', 'it:', 'outsdie', 'is:', 'goooooood', 'ontp', 'khanw', 'u-', 'vstart', 'lerbreak', 'nrr', 'prasidth', 'yesssss', 'tramlines', 'patel:', 'triphti', 'rahid', 'hammed', 'tooeven', 'huuge', 'sighters', 'certianly', 'fifty-four', 'lovelry', 'splice-jarring', 'backtrac', 'whoooosh', 'steely-eyed', 'magix', 'biosecure', 'wiiiild', 'area:', 'bluffmaster', 'arsh', 'mogans', 'spiner', 'seam/cut', 'free-for-all', 'biiiig', 'covershailesh:', 'under-s', 'over-done', 'ength', 'twenty-three', 'dreruss', 'karn', 'straight-ish', '\[pad', 'linethat', 'natmegs', 'singleits', 'raucaous', 'equation:', 'absoiutely', 'goes:', 'shkhar', 'gorunded', 'deliveyr', 'moosed', 'tuc', 'wrner', 'absent-mindedly', 'nagarkotis', 'bruteforces', 'ngidi', '-for--in-pp', 'drop-kic', 'nurdled', 'sarafraz', 'infoeld', 'good:', 'larruped', 'loooopy', 'pauls', 'skiddiness', 'dhawn', '-plus', 'wrongun', 'new-ball', 'aliiive', 'yoekr', 'apeeal', 'deepo', 'legbreaak', 'stand-and-delivered', 'frustratedly', 'offutter', 'auckland', 'jadeje', 'insideout', 'side-ish', 'crase', 'completey', 'supernly', 'less-than-%', 'eventualy', 'uthapps', 'indrifter', 'someoiw', 'full-blown', 'hiiiiigh', 'lenngth', 'backpedalled', 'mujumdar', 'piyush', 'underarmed', 'trods', 'slowish', 'test-like', 'pullconnects', '-on', 'appealer', 'legspinners', 'last:', 'cricle', 'whatre', 'scambling', 'lg', 'hoodwin', 'p\[itched', 'toooo', '-meter', 'hurredly', 'hurrier', 'mdiwickets', 'frm', 'gwhip', 'chalwa', 'under-arming', 'premeditating', 'leg-stumpish', 'billins', 'padnya', 'deepish', 'back:', 'hoic', 'clooooose', 'h', 'lbowl', 'boshes', 'toknock', 'reaasuring', 'clic', 'suryalkumar', 'lttile', 'ff', 'galllps', 'blatted', 's', 'fact:', 'froward', 'easily-walked', 'premeditatedly', 'percection', 'eaisly', 'manageds', 'warriers', 'vis-a-vis', 'bhuvis', 'gargs', 'againgood', 'mid-onby', 'footsh', 'slightly-more', 'occasionbut', 'booo', 'dhaka', 'mdwicket', 'dj', 'late=cut', 'endge', '-ball', 'buh-rilliant', 'neeshams', 'sweeet', 'boomrah', 'pantastic', 'long-n', 'swiftish', 'shot/', 'egde', 'mdidle', 'news:', 'binny:', 'slin', 'inisde', 'swivelled', 'comepletes', 'midhun:', 'line:', 'miwicket', 'sixiest', 'sixah', 'whippage', 'j', 'bajan', 'mripl', 'plesssis', 'thickish', 'gaikwads', 'landmar', 'on-ace', 'ounches', 'yessss', 'maneouvres', 'half-duc', '-over', 'two-paced', 'whatstanlake', 'best-laid', 'wide-run', 'sighscreen', 'rosogullas', 'poit', 'leggie:', 'straightish', 'slowwww', 'v', 'voer', 'llong', 'ominuous', 'jadha', 'depostis', 'blootered', 'swervy', 'keeperes', 'toiwards', 'midwicet', 'wheee', 'goswamu', 'rellly', 'ultraedge', 'oncethe', 'awalefty', 'overpithced', 'the-end', 'bhvuneshwar', 'nahiiiii', 'non-archer', 'griund', 'abover', 'gorund', 'plon', 'katthik', 'ghali', 'overcoo', 'lpng-off', 'ashwings', 'whooosh', 'midiwcket', 'buttoc', 'kishna', 'go-to', 'bengaluru', 'zoin', 'juuust', 'nitish', 'flashbac', 'bacide', 'manged', 'stroke-making', 'pp', 'hball', 'tight-line', 'outdside', 'villierss', 'colelcting', 'readjusts', 'summins', 'waaayy', 'rwason', 'nochalantly', 'th', 'truing', 'plan:', 'himbairstow', 'balewadi', 'mstimed', 'same:', 'gottim', 'hiiiiiiigh', 'juciy', 'legsidish', 'naths', 'yeegads', 'rebowl', 'nutmegging', 'mid-odff', 'suyakumar', 'though:', 'bat-first-or-pad', 'twenty-seven', 'russellmania', 'colecting', 'ribsa', 'c', 'lebgreak', 'cpr', 'addendum:', 'reallllly', 'outfoxes', 'rech', 'pressure-relieving', 'kohliab', 'kxi', 'shortess', 'aargh', 'cdgs', 'strokeplay', 'balltm', 'baistow', 'next:', 'quicklt', 'msicues', 'keeepers', 'steepling', '#irony', 'lemgth', 'maaaasive', 'piggybac', 'sandep', 'goodun', 'yes-no-yes-no', 'kuckle', 'lbws', 'qucikly', 'three-four', 'lenth', 'permament', 'smashem', 'chepaul', 'fity', 'ogets', 'squarelegs', 'noetheless', 'fifty-three', 'sprins', 'super-sub', 'nosireebob', 'adventurousness', 'also:', 'agawar', 'simple:', 'umpired', 'paddle-scooped', 'uffff', 'mis-hitting', 'knoc', 'timinbg', 'tv', 'gpotaway', 'florgin', 'dreep', 'maneouvre', 'viljoen', 'over-run', 'inducker', 'uncofrtable', 'fullishoutside', 'akram-esque', 'quic', '-yard', 'fayahhh', 'dribbes', 'o-u-c-h', 'loooong', 'hooning', 'susses', 'sudbued', 'driveattempted', 'fhund', 'high-ish', 'himeself', 'batspeed', 'welllll', 'deshpnade', 'whac', 'wideeeee', 'slic-ey', 'upper-cut', 'lught', 'aaaaaand', 'too:', 'mightve', 'momentums', 'ekes', 'nurdles', 'oerpitched', 'acrass', 'thaaat', 'sline', 'bounday', 'legnth', 'full-ish', 'byt', 'waayy', 'jordan-like', 'bouls', 'munchs', 'footwho', 'laves', 'bwoelr', 're-set', 'doenst', 'morring', 'gehardus', 'twenty-one', 'midwicketone', 'dot-ball-out', 'check-driving', '--', 'kocks', 'croid', 'front-of-the', 'straigthened', 'febbly', 'kuleep', 'himtucked', 'devil-may', 'fallows', 'well:', 'bowledem', 'minus-three', 'booom', 'yrker', 'kxis', 'batsmens', 'fullie', 'seventy-seven', 'agarwal', 'forward-diving', 'shicker', 'nadu', 'huuuuuuuuge', 'shortoh', 'spannered', 'chinna', 'under-', 'straigther', 'stojnis', 'nipbacker', 'questioneverybody', 'staats', 'hardikll', 'marais', 'hhim', 'offbrea', 'cover:', 'josephs', 'undhoni-like', 'kohli-esque', 'qickly', 'spinnning', 'straught', 'yorekr', 'white-ball', 'nataraja', 'straght', 'varu', 'fnes', 'bundary-less', 'blin', 'mishy-bhai', 'nmidwicket', 'ius', 'raina-like', 'ufff', 'thigh-five', 'sweeeet', 'aaaand', 'wide-ish', 'oooooover', 'gavaskar', 'wrongu', '#lynnsanity', 'midwicke', 'four-over', 'bowling:', 'lamicchane', 'lamichhanes', 'shamsuddins', 'mis-time', 'sride', 'frontfoot', 'bhajji', 'offstump', 'moradabad', 'acoss', 'convinced:', 'looseners', 'bosie', 'bodytimed', 'poiwerfully', 'sahmi', 'singlethree', 'halfways-in', 'barde', 'mumbai-dd', 'woooohooo', 'through/over', 'thime', 'muralitharan', 'striaghtforward', 'legth', 'eays', 'trhough', 'ahdeep', 'awya', 'msifield', 'gaekwad', 'md-off', '-pkus', 'blal', 'missesthe', 'two-three', 'tuns', 'cue-ended', 'wayyyyy', 'furhter', 'signal:', 'shoudler', 'hthe', 'ingield', 'lalit', 'garner-like', 'itno', 'one-and-a-bit', 'sightboard', 'scrambing', 'bhajj', 'ology', 'carresses', 'huuuuuuge', 'dala', 'contact:', 'smir', 'halfvolley', 'slces', 'coulter-nuile', 'dinto', 'singke', 'dugout:', 'gullyfields', 'sidewilliamson', 'rt', 'sk', 'sweeeeeet', 'hoicking', 'ssequence', 'smarly', 'sacrifical', 'whip-pulled', 'broings', 'bandaru', 'sweet-sounding', 'converntional', 'one:', 'ninety-seven', 'shubam', 'fafa', 'strking', 'trues', 'b>spanked', 'kic', 'edgeyes', 'twenty-five', 'huuuuge', 'smac', 'bowlerdoesnt', 'half-apologises', 'sfrom', 'b-e-a-uty', 'flci', 'uppishy', 'buh-rilllllllliant', 'squarelg', 'overtuned', 'balland', 'misfieldsl', 'ball:', 'thigh-high', 'second-ish', 'deliverie', 'thwac', 'amazing:', 'defelction', 'indrifting', 'massssive', 'kncukle', 'cskll', 'jirdan', 'zealander', 'b', 'm', 'yarra', 'disimisses', 'sauare', 'ra-hul', 'rundworld', 'ouchy', 'timbahhh', 'uppushly', 'attemps', 'wristily', 'tenderised', 'nicley', 'guague', 'mustafizur-like', 'fearliesslly', 'huuuuuge', 'gueeses', 'iyer:', 'tolong-on', 'glove/top', 'apeal', 'tyes', 'jadhav-like', 'limtied-overs', 'koc', 'southee', 'season:', 'sweeeeet', 'helioptered', 'natraja', 'tp', 'thye', 'sidethrough', 'slowr', 't', 'holkar', 'suffles', 'followthrough', 'gowswami', 'lengt', 'samson-like', 'sr', 'offisde', 'sireebob', 'mcclengaghan', 'brabourne', 'evdience', 'blindsighted', 'straigthens', 'aroind', 'barvo', 'plesis', 'aaand', 'r', 'mawell', 'boundarythis', 'mumbaikar', 'min-on', 'depe', 'cdg', 'consigns', 'midqicket', 'wheeee', 'ck', 'attempte', 'shakib', 'bi-play', 'stikers', 'wayyyyyy', 'chuc', 'cms', 'inpushes', 'd', 'tickes', 'refleciton', 'betweem', 'umpire:', 'gabbars', 'kmh', 'aaarrrgghh', 'hooped', 'keeper-', 'unplayeable', 'widish', 'mr', 'to-niiiiight', 'kotla', 'ananthapadmanabhan', 'w-o-w', 'maxwell:', 'reigon', 'bmidwicket', 'wiiide', 'bff', 'wood:', 'hs', 'misitimed', 'half-tacker', 'coevr', 'fastish', 'ballooons', 'makkan', 'hiiiigh', 'bacwing', 'faaaya', 'swining', 'chg', 'againhe', 'lovoly', 'misitmed', 'delighful', 'defeneded', 'underedge', 'fullnearly', 'counts:', 'fiedlers', 'rassshiiiid', 'parthiv', 'slow-mo', 'lovly', 'gloving', 'paraga', 'umps', 'curface', 'suqare', 'himelf', '-metre', 'lancashire', 'of-long-off', 'non-strkers', 'slowie', 'sweper', 'uupishly', 'wayyyy', 'pullable', 'innings:', 'realllyyyyy', 'maaaaaassive', 'badrinath-esque', 'mid-ooff', 'squre', 'mid-s', 'poiint', 'pinnadi', 'steepler', 'offuctter', 'bairstown', 'sliddy', 'competely', 'hiolders', 'leb-bye', 'playsa', 'pluc', 'leiws', 'driveable', 'waston', 'looooovely', 'stunmp', 'midiwicket', 'chec', 'sharoer', 'lovley', 'biundary', 'airy-fairy', 'mis-iht', 'nurdle', 'shoritsh', 'shamshuddin', 'bleepin', 'tcaught', 'outisde', 'rippah', 'frmm', 'boundarues', 'wallajah', 'non-malinga', 'pick-flick', 'wegiht', 'plessiss', 'oh-so-slightly', 'pulverises', 'dagar', 'lung-busting', 'not-enoughs-of', 'ohhhhh']

modify_dict = {'Rashid Khan' : 'Rashid-Khan',
'du Plessis' : 'du-Plessis',
'de Kock' : 'de-Kock',
'Rohit Sharma' : 'Rohit',
'Axar Patel' : 'Axar',
'Avesh Khan' : 'Avesh-khan',
'Shivam Mavi' : 'Shivam-Mavi',
'Sam Curran' : 'Sam-Curran',
'Tom Curran' : 'Tom-Curran',
'JPR Scantlebury-Searles' : 'Searles',
'M Nabi' : 'Nabi',
'Barinder Sran' : 'Barinder-Sran',
'Monu Kumar' : 'Monu-Kumar',
'Shahbaz Ahmed' : 'Shabaz-Ahmed',
'Kartik Tyagi' : 'Karthik-Tyagi',
'S Dhawan' : 'Dhawan',
'Arshdeep Singh' : 'Arshdeep-Singh',
'Abdul Samad' : 'Samad',
'Harpreet Brar' : 'Harpreet-Brar',
'Ravi Bishnoi' : 'Ravi-Bishnoi',
'Chennai Super Kings': 'csk',
'Mumbai Indians':'mi',
'Kolkata Knight Riders':'kkr',
'Delhi Capitals':'dc',
'Kings XI Punjab':'kxip',
'Rajastan Royals':'rr',
'Sunrisers Hyderabad':'srh',
'Royal Challengers Banglore':'rcb',
'Rinku Singh': 'Rinku-Singh',
'1 run':'single',
'no run':'dot-ball',
'2 runs':'two-runs',
'3 runs':'three-runs',
'4 runs': 'four',
'FOUR runs': 'four',
'5 runs':'five-run',
'6 runs': 'six',
'SIX runs': 'six',
'no ball':'no-ball',
'1 wide':'1-wide',
'leg bye':'leg-bye',
'direct hit': 'direct-hit',
' off stump ':' off-stump ',
' leg stump ':' leg-stump ',
' off side ':' off-side ',
' leg side ':' leg-side ',
'run out':'run-out',
' silly mid on':' silly-mid-on',
' silly mid off':' silly-mid-off',
' silly point':' silly-point',
' leg slip':' leg-slip',
' deep midwicket':' deep-midwicket',
' deep backward point':' deep-backward-point',
' deep cover':' deep-cover',
' deep square leg':' deep-square-leg',
' deep point':' deep-point',
' deep fine leg':' deep-fine-leg',
' deep extra cover':' deep-extra-cover',
' short square leg':' short-square-leg',
' short fine leg':' short-fine-leg',
' short midwicket':' short-midwicket',
' short third man':' short-third-man',
' backward point':' backward-point',
' square leg':' square-leg',
' extra cover':' extra-cover',
' fine leg':' fine-leg',
' long off':' long-off',
' long on':' long-on',
' mid on':' mid-on',
' mid off':' mid-off',
' third man':' third-man',
' cover point':' cover-point',
' short leg':' short-leg',
' long leg':' long-leg',
' leg gully':' leg-gully',
' leg slip': ' leg-slip',
' hard length ':' hard-length ',
' short ball ':' short-ball ',
' in the slot ':' in-the-slot ',
' low full toss ':' low-full-toss ',
' full toss ':' full-toss ',
' good length ':' good-length ',
' run out ':' run-out ',
' down leg ':' down-leg ',
' slower ball ':' slower-ball ',
' slog swept ':' slog-swept ',
' outside off ':' outside-off ',
' knuckle ball ':' knuckle-ball ',
' knuckleball ':' knuckle-ball ',
' yorker length ':' yorker ',
}

def joinData():
    ipl2020 = pd.read_csv(r'C:\Users\mheme\Desktop\IPL2020 - Commentary Data.csv')
    ipl2019 = pd.read_csv(r'C:\Users\mheme\Desktop\IPL2019 - Commentary Data.csv')
    ipl2018 = pd.read_csv(r'C:\Users\mheme\Desktop\IPL2018 - Commentary Data.csv')

    txtInput = pd.concat([ipl2018, ipl2019, ipl2020])

    txtInput['short_text'] = txtInput['short_text'].str.replace(",", "")
    txtInput['long_text'] = txtInput['long_text'].fillna("")

    for special_char in ['kph','kmph', 'km/h', '\.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        txtInput['long_text'] = txtInput['long_text'].str.replace(special_char, "")

    txtInput['commentary'] = txtInput['over'].astype(str) + " " + txtInput['short_text'] + " " + txtInput['long_text']

    txtInput = txtInput.drop(["over", "short_text", "long_text"], axis=1)

    for special_char in [';', '\'', ',', '?', '!', '"', ')', '(', '\'s ', '\'ll' ]:
        txtInput['commentary'] = txtInput['commentary'].str.replace(special_char, "")

    for word in modify_dict.keys():
        txtInput['commentary'] = txtInput['commentary'].str.replace(word, modify_dict[word])

    txtInput['commentary'] = txtInput['commentary'].str.lower().replace("  ", " ")

    for word in stopwords:
        token = " " + word + " "
        txtInput['commentary'] = txtInput['commentary'].str.replace(token, " ")

    for word in spell_errors:
        token = " " + word + " "
        txtInput['commentary'] = txtInput['commentary'].str.replace(token, " ")

    txtInput['commentary'] = txtInput['commentary'].str.replace("  ", " ")
    txtInput['commentary'] = txtInput['commentary'].str.replace("  ", " ")
    txtInput['commentary'] = txtInput['commentary'].str.replace("  ", " ")
    txtInput['commentary'] = txtInput['commentary'].str.replace("  ", " ")

    """input_array = []
    for sentence in txtInput['commentary']:
        sentenceArray = []
        for word in sentence.split(" "):
            sentenceArray.append(word)
        input_array.append(sentenceArray)
    #Finding total unique words
    all_words = set()
    for array in input_array:
        for word in array:
            all_words.add(word)
    print(len(all_words))"""
    #return input_array

    txtInput.to_csv(r'C:\Users\mheme\Desktop\combined.csv', index=False)


def generate_glove(input):
    # importing the glove library
    from glove import Corpus, Glove
    # creating a corpus object
    corpus = Corpus()
    # training the corpus to generate the co occurence matrix which is used in GloVe
    corpus.fit(input, window=10)
    # creating a Glove object which will use the matrix created in the above lines to create embeddings
    # We can set the learning rate as it uses Gradient Descent and number of components
    glove = Glove(no_components=50, learning_rate=0.03)

    glove.fit(corpus.matrix, epochs=1, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    glove.save('glove.model')
    return glove

def load_glove():
    from glove import Glove
    glv = Glove()
    glv.load("D:\Downloads\glove.model")

if __name__ =='__main__':
    #load_glove()
    inputArray = joinData()
    """glove = generate_glove(inputArray)

    glove_dict = glove.dictionary
    glove_vecs = glove.word_vectors
    word_vecs = []
    for item in glove_dict:
        word_vec = []
        word_vec.append(item)
        word_vec.extend(glove_vecs[glove_dict[item]])
        word_vecs.append(word_vec)

    np_array = np.array(word_vecs)  # .reshape(-1, 51)
    np.savetxt('file.txt', np_array, fmt='%s')"""