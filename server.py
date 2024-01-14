from flask import Flask, render_template, send_file, g
from markupsafe import Markup
from werkzeug.utils import secure_filename

import os
import json

"""
    A quick helper script that makes it easier to add content to the website.
"""

app = Flask(__name__)
URL = "https://soontobesmits.github.io/"

CONTENT = {
    'NAV_OUR_STORY': {'en': "Our Story", 'nl': "Ons Verhaal"},
    'NAV_ACCOMODATION': {'en': "Accomodation", 'nl': "Accomodatie"},
    'NAV_TRANSPORT': {'en': "Transport", 'nl': "Vervoer"},
    'NAV_TODO': {'en': "To-Do", 'nl': "Te-Doen"},
    'NAV_FAQ': {'en': "FAQ", 'nl': "FAQ"},
    'NAV_RSVP': {'en': "RSVP", 'nl': "RSVP"},

    'PREVIOUS': {'en': "Previous", 'nl': "Vorige"},
    'NEXT': {'en': "Next", 'nl': "volgende"},

    # Countdown Section
    'DAYS': {'en': "Days", 'nl': "Dagen"},
    'HOURS': {'en': "Hours", 'nl': "Uren"},
    'MINUTES': {'en': "Minutes", 'nl': "Minuten"},
    'SECONDS': {'en': "Seconds", 'nl': "Seconden"},

    # Our Story Section
    'OUR_STORY': {'en': "Our Story", 'nl': "Ons Verhaal"},
    'WITH_LOVE': {'en': "WITH LOVE", 'nl': "MET LIEFDE"},
    'HOW_WE_MET': {'en': "How We Met", 'nl': "Hoe We Ontmoete"},
    'HOW_WE_MET_DESC': {
        'en': """
            Ruben went shopping for lunch and decided to buy a single banana. He took a picture for a 
            friend, who passed it on to another, before reaching Olivia. Spotting a sad face in the banana's 
            marks, she digitally drew on a little face, and sent it back to her friend. This was passed back 
            to Ruben, and a group chat (as well as our journey) was started -all thanks to a single banana
        """, 
        'nl': """
            Ruben deed boodschappen doen voor zijn lunch en besloot een losse banaan te kopen. Hij maakte een 
            foto voor een vriend, die deze aan een ander doorgaf, voordat deze Olivia bereikte. Ze zag een 
            verdrietig gezicht in de vlekken van de banaan, tekende digitaal een klein gezichtje en stuurde 
            het terug naar haar vriend. Dit werd teruggestuurd naar Ruben, en een groepschat (evenals onze reis) 
            werd gestart - allemaal dankzij een enkele banaan  
        """
    },
    'HOW_WE_MET_DATE': {'en': "20 Oct. 2017", 'nl': "20 okt. 2017"},
    'STARTED_DATING': {'en': "Started Dating", 'nl': "Begonnen Met Daten"},
    'STARTED_DATING_DESC': {
        'en': """
            Ruben flew over to England and joined Olivia and her family on a trip to Cornwall. One
            morning they decided to wake up early to watch the sunrise. Ruben then asked Olivia to
            be his girlfriend on the roof of the house, overlooking the sea. After Olivia said yes, 
            Ruben then got attacked by a massive fly 
            <span class="fw-light">(it hit me right in the back of the head!)</span> and we quickly 
            ran inside.
        """, 
        'nl': """
            Ruben vloog naar Engeland en vergezelde Olivia en haar familie op een reis naar Cornwall. 
            Op een ochtend besloten ze vroeg op te staan om naar de zonsopgang te kijken. Ruben vroeg 
            Olivia toen om zijn vriendin te worden op het dak van het huis, met uitzicht op de zee. 
            Nadat Olivia ja had gezegd, werd Ruben aangevallen door een enorme vlieg 
            <span class="fw-light">(hij raakte me recht op mijn achterhoofd!)</span> en we renden snel naar binnen.
        """
    },
    'STARTED_DATING_DATE': {'en': "26 Jun. 2018", 'nl': "26 jun. 2018"},
    'FINALLY_TOGETHER': {'en': "Finally Together", 'nl': "Eindelijk Samen"},
    'FINALLY_TOGETHER_DESC': {
        'en': """
            Ruben came over in March 2020 to visit Olivia for the weekend, as he did every month. 
            Before he could fly back home, the UK went into lockdown due to Covid and his diabetic 
            team back in the Netherlands advised him to stay there and not to fly due to the virus, 
            until they knew more. Since then, Ruben hasn't left and we moved in together in April 2022
        """, 
        'nl': """
            Ruben kwam in maart 2020 een weekend naar Olivia, zoals hij elke maand deed. Voordat hij 
            terug naar huis kon vliegen, werd het Verenigd Koninkrijk afgesloten vanwege Covid en zijn 
            diabetesteam in Nederland adviseerde hem om daar te blijven en niet te vliegen vanwege het 
            virus, totdat ze meer wisten. Sindsdien is Ruben niet meer weggegaan en in april 2022 kochten 
            we onze eerste woning.
        """
    },
    'FINALLY_TOGETHER_DATE': {'en': "13 Mar. 2020", 'nl': "13 mrt. 2020"},
    'HE_PROPOSED': {'en': "He Proposed", 'nl': "Het Aanzoek"},
    'HE_PROPOSED_DESC': {
        'en': """
            Ruben and Olivia went to Southport with her family to celebrate her parents' anniversay. During a 
            walk on the beach during sunset one evening, they discscused their relationship, with all of its 
            many highs. Ruben got down on one knee and asked Olivia to marry him. Olivia, overwhelmed with joy, 
            said yes, and they've been happily planning the wedding ever since!
        """, 
        'nl': """
            Ruben en Olivia gingen met haar familie naar Southport om het jubileum van haar ouders te vieren. 
            Tijdens een wandeling op het strand tijdens zonsondergang op een avond, bespraken ze hun relatie, 
            met al zijn vele hoogtepunten. Ruben ging op één knie zitten en vroeg Olivia ten huwelijk. Olivia, 
            overweldigd door vreugde, zei ja, en sindsdien zijn ze opgetogen bezig met het plannen van de bruiloft!
        """
    },
    'HE_PROPOSED_DATE': {'en': "29 Aug. 2021", 'nl': "29 aug. 2021"},
    'OUR_WEDDING_DAY': {'en': "Our Wedding Day", 'nl': "Onze Trouwdag"},
    'OUR_WEDDING_DAY_DESC': {
        'en': """
            Olivia and Ruben have booked their wedding for Friday the 13th of September, 2024 at the Foxtail Barns, Consall, England. This is only the start of our journey, and we can't find to find out what wonders life has in store for us. It would be wonderful to share this beautiful moment with you; we hope to see you there! 
        """, 
        'nl': """
            Olivia en Ruben hebben hun bruiloft geboekt voor vrijdag 13 september 2024 in de Foxtail Barns in Consall, Engeland. Dit is nog maar het begin van onze reis en we kunnen niet wachten om te ontdekken welke wonderen het leven voor ons in petto heeft. Het zou geweldig zijn om dit mooie moment met jullie te delen; we hopen jullie daar te zien!
        """
    },
    'OUR_WEDDING_DAY_DATE': {'en': "13 Sep. 2024", 'nl': "13 sep. 2024"},

    # Accomodation section
    'WHERE_TO_STAY': {'en': "WHERE TO STAY", 'nl': "WAAR TE BLIJVEN"},
    'ACCOMODATION': {'en': "Accomodation", 'nl': "Accomodatie"},
    'accomodations': [     
        {
            'name': "Woodland Pods",
            'img_url': f"{URL}img/Foxtail-Barns-pods.jpg",
            'description': {
                'en': """
                    These nature-inspired Pods are on premise, and are nestled in the woodland of the
                    fabulous estate. They come in different sizes and configurations with varying check in
                    times, and the price starts at £110 for a double room, and £150 for a family room.<br>

                    <b>Please keep in mind that these pods are very limited, can only be booked through us,
                    and are for one night only!</b> If you're interested in hiring one, please contact Ruben
                    or Olivia
                """,
                'nl': """
                """,
            },
            'costs': "£££",
            'phone': "",
            'url': "https://foxtailbarns-venue.co.uk/woodland-guest-lodges/",
            'display_url': "foxtailbarns-venue.co.uk"
        },
        {
            'name': "The Tawny",
            'img_url': f"{URL}img/The Tawny.jpg",
            'description': {
                'en': """
                    On-site but very expensive
                """,
                'nl': """
                """,
            },
            'costs': "£££££",
            'phone': "+44 (0)1538 787664",
            'url': "https://thetawny.co.uk/",
            'display_url': "thetawny.co.uk"
        }, 
        {
            'name': "Premier Inn - Leek",
            'img_url': f"{URL}img/Premier Inn - Leek.jpg",
            'description': {
                'en': """
                    15 minutes from Foxtail Barns. Call ‘Leek Link Taxis’ on +44 (0)1538 399999 for the best
                    taxi rates back to the Leek Premier Inn at the end of the night. Chargeable on-site
                    parking is available at this hotel at £5 per night
                """,
                'nl': """
                """,
            },
            'costs': "££",
            'phone': "+44 (0)333 321 9252",
            'url': "https://www.premierinn.com/gb/en/hotels/england/staffordshire/leek/leek-town-centre.html",
            'display_url': "premierinn.com"
        },   
        {
            'name': "Premier Inn - Hanley",
            'img_url': f"{URL}img/Premier Inn - Hanley.jpg",
            'description': {
                'en': """
                    9 miles from Foxtail Barns, free parking. Just a ten-minute walk to the shops and cafés
                    of Hanley town centre plus the cute pottery outlets. Two types of rooms, standard and
                    plus. Theres also two types of room rates, flexible where you can pay cancel up to 1pm
                    on the same day and you can pay on arrive, or advanced where you pay now and free
                    cancellation up to 28 days before. Either king or twin rooms.
                """,
                'nl': """
                """,
            },
            'costs': "",
            'phone': "",
            'url': "",
            'display_url': ""
        }, 
        {
            'name': "Hilton Garden Inn - Hanley",
            'img_url': f"{URL}img/Hilton Garden Inn - Hanley.jpg",
            'description': {
                'en': """
                    9 miles from Foxtail Barns. Within half a mile of the cultural quarter, near to the
                    Regent Theatre, Potteries Museum, Art Gallery and Potteries Shopping Centre. Multiple
                    rooms from twin rooms, king rooms and family rooms.
                """,
                'nl': """
                """,
            },
            'costs': "££££",
            'phone': "+44 (0)1782 486960",
            'url': "https://www.hilton.com/en/hotels/manstgi-hilton-garden-inn-stoke-on-trent/",
            'display_url': "www.hilton.com"
        }, 
        {
            'name': "DoubleTree by Hilton - Etruria",
            'img_url': f"{URL}img/DoubleTree by Hilton - Etruria.jpg",
            'description': {
                'en': """
                    25 minutes drive away from Foxtail Barn, Can do group bookings for more than 10 rooms.
                    Do a multiple of rooms, from twins, to king, to suites. Located on Festival Retail park,
                    near the Stoke Ski Centre and waterworld. The hotel has a full-service spa, pool,
                    resturants. Have a multitude of rooms, from Queen twin rooms, to king beds to suites.
                """,
                'nl': """
                """,
            },
            'costs': "£££",
            'phone': "",
            'url': "https://www.hilton.com/en/hotels/manstgi-hilton-garden-inn-stoke-on-trent/",
            'display_url': "www.hilton.com"
        }, 
        {
            'name': "Peak Weavers - Leek",
            'img_url': f"{URL}img/Peak Weavers - Leek.jpg",
            'description': {
                'en': """
                    The house has 3 bedrooms and sleeps 6 plus cot(s). All bedrooms feature handmade,
                    wrought iron beds, 2 of them kingsize and the 3rd a twin room with 2 singles. Self
                    Catering leek, weekly price £595. Also have B&B 6 non-smoking bedrooms, £72. Well
                    equipped kitchen. two pubs within 10 minute walk, one canalside.
                """,
                'nl': """
                """,
            },
            'costs': "£",
            'phone': "",
            'url': "",
            'display_url': ""
        },   
        {
            'name': "White Hart Tea Room",
            'img_url': f"{URL}img/White Hart Tea Room.jpg",
            'description': {
                'en': """
                    15 minutes drive from Foxtail Barns. Accommodation features eight individual en-suite
                    bedrooms. Due to the historic building, all rooms are accessed via stairs. In the heart
                    of leek, the Grace II listed building is opposite the historic Market Place. As well as
                    a B&B its also a traditional tea room and sandwich bar.
                """,
                'nl': """
                """,
            },
            'costs': "£",
            'phone': "",
            'url': "",
            'display_url': ""
        },   
        {
            'name': "Middle Cottage",
            'img_url': f"{URL}img/Middle Cottage.jpg",
            'description': {
                'en': """
                    7 miles from Foxtail Barns, 1 double Bedroom property. Built in the 1700s, and situated
                    in the picturesque village of Endon, next to the village well dating back to 1845. Two
                    village pubs are only a few minutes walk. Fully fitted kitchen included. Option of a
                    guest bed and travel cot if required. Unsure of price, please enquire
                """,
                'nl': """
                """,
            },
            'costs': "Unknown",
            'phone': "+44 (0)1538 787664",
            'url': "https://www.middlecottageholidays.co.uk/",
            'display_url': "www.middlecottageholidays.co.uk"
        },   
        {
            'name': "Allmore Cottage - Gratton Village",
            'img_url': f"{URL}img/Allmore Cottage - Gratton Village.jpg",
            'description': {
                'en': """
                    8 miles from Foxtail Barns. Allmore Cottage is a 1 kingsize bedroom property for 2
                    people. Prices range from £460 - £600 per week. Was originally a neglected farm building
                    turn into a cottage. Fully fitted kitchen and a conservatory at the rear of the cottage,
                    ideal for relaxing and enjoying the views of the surrounding countryside
                """,
                'nl': """
                """,
            },
            'costs': "£££",
            'phone': "01782 505535",
            'url': "http://www.allmorecottageholidays.co.uk",
            'display_url': "www.allmorecottageholidays.co.uk"
        },   
        {
            'name': "Rose Cottages - Endon",
            'img_url': f"{URL}img/Rose Cottages - Endon.jpg",
            'description': {
                'en': """
                    7 miles from Foxtail Barns. Two Cottages with 3 Bedrooms Each, can sleep up to 8 Adult
                    guests and 1 Infant each with excellent parking and gardens. Hot Tub hire available.
                    prices from £325 per night (2 night stay) or £1075 per week (for up to 6 guests). Each
                    property features a fully equipped kitchen, comfortable living room with log burner,
                    dining area for 6-8 people and fully enclosed rear garden.
                """,
                'nl': """
                """,
            },
            'costs': "£££",
            'phone': "",
            'url': "https://rosecottagesendon.co.uk/",
            'display_url': "rosecottagesendon.co.uk"
        },   
        {
            'name': "Spring Cottage",
            'img_url': f"{URL}img/Spring Cottage.jpg",
            'description': {
                'en': """
                    17 minutes from Foxtail Barns. Sleeps 6. 3 bedrooms, one king size, one double one with
                    twin beds. The kitchen has been newly fitted with all mod cons making this a lovely
                    space to prepare delightful meals. The grounds outside Spring Cottage offer guests a
                    place to relax and do some alfresco dining in the warmer months. Two livingrooms fitted
                    with log burners. Unsure of price, please enquire
                """,
                'nl': """
                """,
            },
            'costs': "Unknown",
            'phone': "",
            'url': "https://springcottageholidaylet.co.uk/",
            'display_url': "springcottageholidaylet.co.uk"
        }
    ],

    # Transport section
    'HOW_TO_GET_THERE': {'en': "HOW TO GET THERE", 'nl': "HOE DAAR TE KOMEN"},
    'TRANSPORT': {'en': "Transport", 'nl': "Vervoer"},
    'FLIGHTS': {'en': "Flights", 'nl': "Vluchten"},
    'FLIGHTS_DESC': {
        'en': """
            The best airport to land in is Manchester which is a 40-50 minute drive
            to Stoke-On-Trent. If you're flying from the Netherlands the best airlines we can recommened are
            Easyjet (https://www.easyjet.com) and KLM (https://www.klm.com). Easyjet is usually the
            cheapest option and usually relable, whereas KLM is more luxurious and offers a snack
            half way through the flight. The flight is usually around 50 minutes long, and remember
            you need to be at the airport 2 hours before your flight time! We do not recommend
            Ryanair, we have had negative experience of randomly cancelled flights.
        """, 
        'nl': """
        """
    },
    'PUBLIC_TRANSPORT': {'en': "Public Transport", 'nl': "Openbaar Vervoer"},
    'PUBLIC_TRANSPORT_DESC': {
        'en': """
            There are two modes of public transport in the UK. These are train and
            bus. If you're getting a train from the airport to stoke, or because stoke is in the
            centre of the UK and you want to explore the major cities, using the train will be
            vital. Unlike the Netherlands and other european countries, you need to buy train
            tickets per journey, you can do this at the train station or more relably be using the
            trainline website/app (https://www.thetrainline.com). If you're planning on travelling
            we recommened downloading the app. All you need to do it put your current location and
            where you're travelling too and it will tell you the different times and prices, we
            advise you to avoid peak times. If you're looking at travelling by bus around stoke on
            trent, the most reliable bus service, is the First bus (https://www.firstbus.co.uk), on
            their website you can plan your journey or see when the next bus will be!
        """, 
        'nl': """
        """
    },
    'HIRED_TRANSPORT': {'en': "Hired Transport", 'nl': "Gehuurd Vervoer"},
    'HIRED_TRANSPORT_DESC': {
        'en': """
            There are lots of local taxi and mini-bus services. If there is a large
            group of travellers on the same flight and looking at hiring a mini-bus to travel
            towards Stoke on Trent, we are happy to help accommodate this and pass along some
            mini-bus numbers along. There are a lot of taxi services in Stoke on Trent, these
            include Intercity (<a href="tel:+441782855855">+44 (0)1782 855855</a>), those staying in
            Leek can use Leek Link Taxis' (<a href="tel:+441538399999">+44 (0)1538 399999</a>),
            Lucky Seven (<a href="tel:+441782333333">+44 (0)1782 333333</a>), City Cabs (<a
            href="tel:+441782888888">+44 (0)1782 888888</a>), Magnum Private Hire (<a
            href="tel:+441782819819">+44 (0)1782 819819</a>). Alternatively you can use an app
            called "Take me", which is an app that allows you to book a vechicle in seconds, you can
            view your driver and track his progress or you can use Uber, whichever is easiest for
            you!
        """, 
        'nl': """
        """
    },
    
    # Activities Section
    'WHAT_TO_DO': {'en': "WHAT TO DO", 'nl': "WAT TE DOEN"},
    'THINGS_TO_DO': {'en': "Things to do in Staffordshire", 'nl': "Dingen om te doen in Staffordshire"},

   'activities': [     
        {
            'name': "Alton Towers",
            'img_url': f"{URL}img/Alton Towers.jpg",
            'description': {
                'en': """
                    Alton Towers Resort is a theme park and resort complex in Staffordshire, England, 
                    near the village of Alton. Alton Towers Resort is home to over 40 rides and attractions, 
                    for guests of all ages. The 10 main rollercoasters are the stars of the show, each with 
                    record-breaking elements designed to thrill and delight anyone brave enough to ride. With 
                    20 attractions aimed at young children and families, Alton Towers is the only place in the 
                    UK where you can meet some of CBeebies best loved characters.
                """,
                'nl': """
                    Alton Towers Resort is een themapark en resortcomplex in Staffordshire, Engeland, vlakbij het dorp Alton. Alton Towers Resort heeft meer dan 40 attracties voor gasten van alle leeftijden. De 10 belangrijkste achtbanen zijn de sterren van de show, elk met recordbrekende elementen ontworpen om iedereen die dapper genoeg is om te rijden te laten huiveren en genieten. Met 20 attracties gericht op jonge kinderen en gezinnen is Alton Towers de enige plek in het Verenigd Koninkrijk waar je een aantal van CBeebies' meest geliefde personages kunt ontmoeten.
                """,
            },
            'costs': "3+ £39",
            'address': "Farley Ln, Alton, Stoke-on-Trent ST10 4DB",
            'url': "https://www.altontowers.com",
            'display_url': "www.altontowers.com"
        },
        {
            'name': "Trentham Monkey Forest",
            'img_url': f"{URL}img/Trentham Monkey Forest.jpg",
            'description': {
                'en': """
                    If you are looking for a fun day out with a difference, look no further. Trentham Monkey 
                    Forest is a sanctuary for endangered Barbary monkeys. The natural behaviours of the monkeys 
                    can be seen right in front of your very eyes, making it one of the most fascinating and special 
                    attractions in the UK. Guests walk along the 3/4 of a mile pathway, amongst the monkeys, and see 
                    exactly how they live and behave in the wild.
                """,
                'nl': """Als je op zoek bent naar een leuk dagje uit met een verschil, zoek dan niet verder. Trentham Monkey Forest is een toevluchtsoord voor bedreigde berberapen. De natuurlijke gedragingen van de apen zijn recht voor je ogen te zien, waardoor het een van de meest fascinerende en bijzondere attracties in het Verenigd Koninkrijk is. Gasten lopen over een pad van 3,5 km tussen de apen door en zien precies hoe ze in het wild leven en zich gedrage
                """,
            },
            'costs': "Adult: £12.00 Children: £9.50",
            'address': "Stone Road Trentham Estate, Stoke-on-Trent ST4 8AY England",
            'url': "https://monkey-forest.com",
            'display_url': "monkey-forest.com"
        },
        {
            'name': "Trentham Gardens",
            'img_url': f"{URL}img/Trentham Gardens.jpg",
            'description': {
                'en': """
                    The Trentham Estate is home to the award-winning Trentham Gardens featuring The Italian Garden 
                    by Tom Stuart-Smith, and the Floral Labyrinth and Rivers of Grass by Piet Oudolf and vast 
                    wildflower and woodland meadow plantings by Nigel Dunnett. A fascinating wire fairy sculpture 
                    trail, fab childrens adventure playground with the UK's first barefoot walk, a family-friendly maze, 
                    mile-long Capability Brown lake with seasonal boat and train trips. Trentham Monkey Forest, Trentham 
                    Treetop Adventure and Trentham Shopping Village with 50 shops and 14 cafes and restaurants can also 
                    be found at The Trentham Estate. You'll find something for everyone here.
                """,
                'nl': """Het Trentham Estate is de thuisbasis van de bekroonde Trentham Gardens met The Italian Garden van Tom Stuart-Smith, het Floral Labyrinth en Rivers of Grass van Piet Oudolf en uitgestrekte wilde bloemen- en bosweidebeplantingen van Nigel Dunnett. Een fascinerend sprookjesachtig sculpturenpad, een fantastische kinderspeeltuin met de eerste blotevoetenwandeling in het Verenigd Koninkrijk, een gezinsvriendelijk doolhof, een kilometerslang Capability Brown-meer met seizoensgebonden boot- en treinuitstapjes. Trentham Monkey Forest, Trentham Treetop Adventure en Trentham Shopping Village met 50 winkels en 14 cafés en restaurants zijn ook te vinden op The Trentham Estate. Hier vind je voor elk wat wils.
                """,
            },
            'costs': "£13 Children: £9.50",
            'address': "Trentham Gardens Stone Road Trentham Estate, Trentham, Stoke-on-Trent ST4 8JG England",
            'url': "https://trentham.co.uk",
            'display_url': "trentham.co.uk"
        },
        {
            'name': "Waterworld",
            'img_url': f"{URL}img/Waterworld.jpg",
            'description': {
                'en': """
                    The UK's No.1 tropical indoor aqua park is located at the Waterworld Leisure Resort, in the heart of 
                    the Midlands, Stoke-on-Trent! Open all year round, Waterworld Aqua Park is an epic adventure for the 
                    whole family to enjoy, with over 30 different rides and attractions including Thunderbolt, the UK's 
                    first trap door drop waterslide! There's also the outdoor pool for those looking to enjoy some sunshine 
                    in the summer months! The Waterworld Leisure Resort is also home to Adventure Mini Golf with two 18-hole, 
                    tiki-themed mini golf courses, and the new M Club Spa and Fitness facility, so there has never been more 
                    choice for the best leisure experiences in Staffordshire!            
                """,
                'nl': """Het nummer 1 tropische overdekte aquapark in het Verenigd Koninkrijk ligt in het Waterworld Leisure Resort, in het hart van de Midlands, Stoke-on-Trent! Waterworld Aqua Park is het hele jaar door geopend en is een episch avontuur voor het hele gezin, met meer dan 30 verschillende attracties waaronder Thunderbolt, de eerste valdeurwaterglijbaan in het Verenigd Koninkrijk! Er is ook een buitenzwembad voor wie in de zomermaanden van de zon wil genieten! Het Waterworld Leisure Resort is ook de thuisbasis van Adventure Mini Golf met twee 18-holes minigolfbanen met een tiki-thema, en de nieuwe M Club Spa en fitnessruimte, dus er is nog nooit zoveel keuze geweest voor de beste vrijetijdsbelevenissen in Staffordshire!
                """,
            },
            'costs': "Adult: £22 Children: £20",
            'address': "Waterworld Festival Way Hanley, Stoke-on-Trent ST1 5PU England",
            'url': "https://www.waterworld.co.uk",
            'display_url': "www.waterworld.co.uk"
        },
        {
            'name': "Stoke Ski Resort",
            'img_url': f"{URL}img/Stoke Ski Resort.jpg",
            'description': {
                'en': """
                    Stoke Ski Centre is one of the UK's leading dry slopes offering a wide variety of activities to suit all 
                    ages. From top-quality ski and board coaching and lessons, amazing tubing party packages for children aged 
                    2 years and above, an all new terrain park with a big kicker and quarter pipe combination as well as a 140m 
                    main race slope.<br>
                    Their facility is specifically designed to imitate the mountains and help you train or just to have fun. 
                    With constant work going into improving their slope surface, they are proud to claim it as one of the best in 
                    the country.            
                """,
                'nl': """Stoke Ski Centre is een van de toonaangevende droge pistes in het Verenigd Koninkrijk en biedt een breed scala aan activiteiten voor alle leeftijden. Van ski- en boardcoaching en lessen van topkwaliteit, geweldige tubingpartypakketten voor kinderen vanaf 2 jaar, een gloednieuw terreinpark met een combinatie van een big kicker en een quarterpipe, tot een 140 meter lange wedstrijdpiste.
    Hun faciliteit is speciaal ontworpen om de bergen na te bootsen en je te helpen trainen of gewoon om plezier te hebben. Er wordt constant gewerkt aan het verbeteren van het oppervlak van de piste en ze zijn er trots op dat ze kunnen zeggen dat het een van de beste in het land is.
                """,
            },
            'costs': "Adult £32 Children: £22",
            'address': "Festival Park Festival Way, Stoke-on-Trent ST1 5PU England",
            'url': "https://stokeskicentre.com",
            'display_url': "stokeskicentre.com"
        },
        {
            'name': "World of Wedgwood",
            'img_url': f"{URL}img/World of Wedgwood.jpg",
            'description': {
                'en': """
                    Nestled in acres of stunning Staffordshire countryside is the perfect antidote to the stress of the modern day. 
                    In an age of automation and mass production, the skills of true craftsmanship form real beauty that stand the 
                    test of time. Here, you can visit the Wedgwood Factory, the only place in the world where jasper - the most 
                    famous of Josiah's inventions - is still made today. You can unwind at the potter's wheel or explore the 
                    galleries of the V&A Wedgwood Collection, but make sure you save time for the signature Wedgwood Afternoon Tea. 
                    So come for the plates and stay for the cake, take family walks through our 240 acre estate
                """,
                'nl': """ Genesteld in hectaren adembenemend landschap van Staffordshire ligt het perfecte tegengif voor de stress van de moderne tijd. In een tijdperk van automatisering en massaproductie vormen de vaardigheden van echt vakmanschap echte schoonheid die de tand des tijds doorstaat. Hier kun je de Wedgwood-fabriek bezoeken, de enige plek ter wereld waar jaspis - de beroemdste uitvinding van Josiah - nog steeds wordt gemaakt. Je kunt tot rust komen bij de pottenbakkersschijf of de galerieën van de V&A Wedgwood Collection verkennen, maar zorg ervoor dat je tijd overhoudt voor de kenmerkende Wedgwood Afternoon Tea. Dus kom voor de borden en blijf voor de taart, maak wandelingen met het hele gezin over ons landgoed van 240 hectare.

                """,
            },
            'costs': "Free to enter",
            'address': "Wedgwood Drive, Stoke-on-Trent ST12 9ER England",
            'url': " https://www.worldofwedgwood.com/",
            'display_url': "www.worldofwedgwood.com"
        },
        {
            'name': "Biddulph Grange Garden",
            'img_url': f"{URL}img/Biddulph Grange Garden.jpg",
            'description': {
                'en': """
                    This amazing Victorian garden was created by James Bateman for his collection of plants from around the world. 
                    A visit takes you on a global journey from Italy to the pyramids of Egypt, a Victorian vision of China and a 
                    re-creation of a Himalayan glen.<br>
                    The garden features collections of rhododendrons, summer bedding displays, a stunning Dahlia Walk and the oldest 
                    surviving golden larch in Britain, brought from China in the 1850s.The Geological Gallery shows how Bateman's 
                    interests went beyond botany. Opened in 1862 the unique hallway is a Victorian attempt to reconcile geology and 
                    theology. There are narrow gravel paths and over 400 steps throughout the garden.            
                """,
                'nl': """ Deze verbazingwekkende Victoriaanse tuin werd aangelegd door James Bateman voor zijn verzameling planten uit de hele wereld. Een bezoek neemt je mee op een wereldwijde reis van Italië naar de piramides van Egypte, een Victoriaanse visie op China en een herschepping van een Himalayagloof.
    In de tuin vindt u collecties rododendrons, zomerperken, een prachtige Dahlia Walk en de oudste nog bestaande gouden lariks in Groot-Brittannië, in de jaren 1850 uit China meegenomen. De unieke hal werd geopend in 1862 en is een Victoriaanse poging om geologie en theologie met elkaar te verzoenen.
    Door de hele tuin lopen smalle grindpaden en meer dan 400 treden.
                """,
            },
            'costs': "Adult: £12 Child: £6 ",
            'address': "Grange Road, Biddulph, Staffordshire, ST8 7SD ",
            'url': " https://www.nationaltrust.org.uk/visit/shropshire-staffordshire/biddulph-grange-garden",
            'display_url': "www.nationaltrust.org.uk/visit/shropshire-staffordshire/biddulph-grange-garden"
        },
        {
            'name': "Regent Theatre",
            'img_url': f"{URL}img/Regent Theatre.jpg",
            'description': {
                'en': """
                    The Regent Theatre is a theatre in Stoke-on-Trent, England. Constructed in 1929 as a cinema, it is one of several  
                    theatres in the city centre and one of two operated by the Ambassador Theatre Group on behalf of Stoke-on-Trent 
                    City Council. The Regent Theatre, Stoke-on-Trent is a number one touring venue. Since re-opening, following a 
                    £23 million development of the city centre, it has played host to War Horse, Mamma Mia! and Jersey Boys.            
                """,
                'nl': """ Het Regent Theatre is een theater in Stoke-on-Trent, Engeland. Het werd in 1929 gebouwd als bioscoop en is een van de vele theaters in het stadscentrum en een van de twee die worden uitgebaat door de Ambassador Theatre Group namens de gemeenteraad van Stoke-on-Trent. Het Regent Theatre in Stoke-on-Trent is een van de grootste rondreizende theaters. Sinds de heropening, na een ontwikkeling van het stadscentrum van £23 miljoen, heeft het onderdak geboden aan War Horse, Mamma Mia! en Jersey Boys.
                """,
            },
            'costs': "Price depends on the show",
            'address': "Piccadilly, Stoke-on-Trent, Staffordshire, ST1 1AP",
            'url': " https://www.atgtickets.com/venues/regent-theatre/",
            'display_url': "www.atgtickets.com/venues/regent-theatre/"
        },
    ],

    # FAQ Section
    'EVERYTHING_TO_KNOW': {'en': "EVERYTHING YOU WANT TO KNOW", 'nl': "ALLES WAT JE WIL WETEN"},
    'FAQ_LONG': {'en': "Frequently Asked Questions", 'nl': "Veel Gestelde Vragen"},
    'rsvp_questions': [     
        {
            'name': {'en': "How Do I RSVP?", 'nl': "Hoe kan ik RSVP'en?"},
            'description': {
                'en': """
                    We invite you to RSVP at the bottom of this page or by mailing in the RSVP card sent with the invitation
                """,
                'nl': """
                    Gelieve de RSVP op de bodem van deze webpagina te gebruiken, of door de RSVP-kaart in te sturen die bij de uitnodiging is toegegevoegd
                """,
            }
        },
        {
            'name': {'en': "What date should I RSVP by?", 'nl': "Voor wanneer moet ik RSVP'en?"},
            'description': {
                'en': """
                    Please RSVP by the 13th of June
                """,
                'nl': """
                    RSVP a.u.b. vóór 13 juni
                """,
            }
        },
        {
            'name': {'en': "What is the dress code?", 'nl': "Wat is de dresscode?"},
            'description': {
                'en': """
                    The dress code for our wedding is semi-formal/cocktail attire. Think cocktail dresses or a suit and tie
                """,
                'nl': """
                    De dresscode voor onze bruiloft is semi-formeel/cocktailkleding. Denk aan cocktailjurken of een pak en stropdas
                """,
            }
        },
        {
            'name': {'en': "What is the addresses for the wedding ceremony and reception venue?", 'nl': "Wat zijn de adressen van de trouwceremonie en receptielocatie?"},
            'description': {
                'en': """
                    Foxtail Barns Wedding Venue<br>
                    Consall Hall Gardens Estate<br>
                    Consall<br>
                    Staffordshire<br>
                    ST9 0AG
                """,
                'nl': """
                    Foxtail Barns Wedding Venue<br>
                    Consall Hall Gardens Estate<br>
                    Consall<br>
                    Staffordshire<br>
                    ST9 0AG<br>
                    Engeland
                """,
            }
        },
        {
            'name': {'en': "What time should I arrive?", 'nl': "Hoe laat wordt ik verwacht?"},
            'description': {
                'en': """
                    Help us get the party started as scheduled! We recommend that you arrive at 1 PM, which is an 
                    hour before the start of the ceremony, to make sure everyone is seated on time""",
                'nl': """
                    Help ons het feest op tijd in gang te krijgen! We raden je aan om om 13.00 uur aanwezig te zijn, 
                    wat een uur voor aanvang van de ceremonie is, om er zeker van te zijn dat iedereen op tijd zit
                """,
            }
        },
        {
            'name': {'en': "Is there available parking?", 'nl': "Is er parkeergelegenheid?"},
            'description': {
                'en': """
                    Yes, free parking is available at the venue
                """,
                'nl': """
                    Ja, er is gratis parkeergelegenheid bij de locatie
                """,
            }
        },
        {
            'name': {'en': "What should I do if I have dietary requirements?", 'nl': "Wat moet ik doen als ik dieetwensen of -beperkingen heb?"},
            'description': {
                'en': """
                    Please let us know of any dietary requirements on your RSVP
                """,
                'nl': """
                    Geef eventuele dieetwensen of -beperkingen aan ons door via de RSVP, a.u.b.
                """,
            }
        },
        {
            'name': {'en': "Where are you going on your honeymoon?", 'nl': "Waar gaan jullie heen op huwelijksreis?"},
            'description': {
                'en': """
                    We will be spending two weeks exploring Tokyo, Japan!
                """,
                'nl': """
                    We gaan twee weken lang Tokio, Japan verkennen!
                """,
            }
        },
        {
            'name': {'en': "What can we bring you as a gift?", 'nl': "Wat kunnen we jullie cadeau doen?"},
            'description': {
                'en': """
                    Your presence at our wedding is the greatest gift of all. However, if you wish to honour us with a gift, 
                    a cash gift for our honeymoon would be very welcome. Preferably in GBP(£) or Japanese Yen(¥).
                """,
                'nl': """
                    Jouw aanwezigheid op onze bruiloft is het grootste geschenk van allemaal. Maar, mocht je alsnog een 
                    cadeau willen geven, dan wordt een envelopje met contact geld voor onze huwelijksreis erg op preis gesteld. 
                    Bij voorkeur in Engelse Ponden (£) of Japanse Yen(¥). 
                """,
            }
        },
        {
            'name': {'en': "Can we take photos at the ceremony?", 'nl': "Kunnen we foto's maken tijdens de ceremonie?"},
            'description': {
                'en': """
                    We've hired a photographer and we'd love to have photos with no phones or devices in them. 
                    Please put away your cameras and phones during our wedding ceremony! Please feel free to take as many 
                    photos afterwards to remember our special day!

                """,
                'nl': """
                    We hebben een fotograaf ingehuurd en we willen graag foto's hebben zonder telefoons of camera's in beeld. 
                    Berg uw camera's en telefoons op tijdens onze huwelijksceremonie! Maak gerust achteraf een foto om onze speciale dag te herinneren!
                """,
            }
        },
        {
            'name': {'en': "Can I bring a plus one?", 'nl': "Mag ik iemand meenemen?"},
            'description': {
                'en': """
                    Due to the size of our guest list, we cannot accommodate extra people at the wedding. 
                    We only have spaces for the guests listed on your invitation.
                """,
                'nl': """
                    Vanwege de omvang van onze gastenlijst kunnen wij geen extra personen op de bruiloft ontvangen. 
                    Wij hebben alleen plekken voor de gasten die op de uitnodiging staan vermeld.
                """,
            }
        },
        {
            'name': {'en': "Are children allowed?", 'nl': "Zijn kinderen welkom?"},
            'description': {
                'en': """
                    Yes, however, due to venue limitations, only people listed on the invitation can attend our wedding.
                """,
                'nl': """
                    Ja, maar vanwege locatiebeperkingen kunnen alleen de mensen die op de uitnodiging staan vermeld onze bruiloft bijwonen. 
                """,
            }
        },
        {
            'name': {'en': "We want to stay for a few days, will you be there?", 'nl': "Wij willen een paar dagen blijven, zijn jullie beschikbaar?"},
            'description': {
                'en': """
                    That's great! Due to many guests travelling afar, we've decided to wait for a week before going on honeymoon. 
                    Even though we have to work, we're available for any support, or to meet up (when available)
                """,
                'nl': """
                    Wat leuk! Omdat sommige gasten ver reizen hebben we besloten om een week te wachten voordat we op onze huwelijksreis gaan.
                    Alhouwel we naar werk moeten zijn we beschikkbaar voor steun/advies, en om af te spreken (zolang we beschikbaar zijn)
                """,
            }
        },
        {
            'name': {'en': "Can I do a speech?", 'nl': "Kan ik een toespraak houden?"},
            'description': {
                'en': """
                    Only the Father of the bride, the Groom, and the Bestman will be doing a speech. We'd appreciate if anyone else wants to say a few 
                    words on our special day, to share them with us privately after the wedding breakfast, for a more intimate conversation
                """,
                'nl': """
                   Alleen de vader van de bruid, de bruidegom, en de "best man" zullen een toespraak houden. We zouden het op prijs stellen als iemand 
                   anders een paar woorden wil delen op onze speciale dag, om deze na het huwelijksontbijt privé met ons te delen, voor een intiemer gesprek
                """,
            }
        }
    ],

    # RSVP Section
    'PLEASE_LET_US_KNOW': {'en': "PLEASE LET US KNOW", 'nl': "LAAT HET ONS WETEN"},
    'R.S.V.P.': {'en': "R.S.V.P.", 'nl': "R.S.V.P."},
    'FIRST_NAME': {'en': "First Name", 'nl': "Voornaam"},
    'LAST_NAME': {'en': "Last Name", 'nl': "Achternaam"},
    'EMAIL': {'en': "Email", 'nl': "Email"},
    'PHONE_NUMBER': {'en': "Phone Number", 'nl': "Telefoonnummer"},
    'PLEASE_SELECT': {'en': "Please select", 'nl': "Maak een keuze"},
    'NONE': {'en': "None", 'nl': "Geen"},
    'ONE': {'en': "One", 'nl': "Een"},
    'TWO': {'en': "Two", 'nl': "Twee"},
    'THREE': {'en': "Three", 'nl': "Drie"},
    'FOUR': {'en': "Four", 'nl': "Vier"},
    'FIVE': {'en': "Five", 'nl': "Vijf"},
    'HOW_MANY_INVITE': {'en': "How many people are on your invite?", 'nl': "Hoeveel personen staan op je uitnodiging?"},
    'HOW_MANY_ATTEND': {'en': "How many people of these will attend?", 'nl': "Hoeveel van deze personen komen?"},
    'PROVIDE_NAMES': {'en': "Please provide their names below", 'nl': "Vul hier a.u.b. hun namen in"},
    'DIETARY_REQUIREMENTS': {'en': "Does anyone have any dietary requirements? Please list these", 'nl': "Heeft iemand dieetwensen? Gelieve deze hier te vermelden"},
    'SUBMIT_RSVP': {'en': "Submit RSVP", 'nl': "Verstuur RSVP"},
}

@app.template_filter('translate')
def translate_filter(translation_key):
    val = CONTENT.get(translation_key, {})
    return Markup(f"""<span lang="en">{val.get('en', "Unknown")}</span><span class="hidden" lang="nl">{val.get('nl', "Unknown")}</span>""")

@app.template_filter('translate_val')
def translate_val_filter(val):
    return Markup(f"""<span lang="en">{val.get('en', "Unknown")}</span><span class="hidden" lang="nl">{val.get('nl', "Unknown")}</span>""")

@app.template_filter('translate_select')
def translate_select_filter(translation_key, options):
    val = CONTENT.get(translation_key, {})
    return Markup(f"""
    <option {options} lang="en">{val.get('en', "Unknown")}</option>
    <option {options} lang="nl" class="hidden">{val.get('nl', "Unknown")}</option>
    """)

@app.after_request
def save_index_page(response):
    if hasattr(g, 'template'):
        with open("index.html", "w") as f:
            f.write(response.data.decode())
    return response

@app.route('/', methods=['GET', 'POST'])
def index_page():
    g.template = True
    return render_template("index.html", content=CONTENT, url=URL)

@app.route('/<path:filename>')
def send_media(filename):
    return send_file(filename)

if __name__ == "__main__":
    app.debug = True
    app.run()