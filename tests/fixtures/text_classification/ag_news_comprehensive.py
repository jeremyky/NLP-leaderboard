"""
Comprehensive test cases for AG News - Text Classification

Dataset: AG News
Task: text_classification
Classes: world, sports, business, sci/tech
Total Cases: Will be 150+ after you generate with ChatGPT

---

INSTRUCTIONS:
1. Use the ChatGPT prompt from docs/TEST_EXPANSION_GUIDE.md
2. Paste the generated cases below
3. Organize into STANDARD_CASES, EDGE_CASES, ADVERSARIAL_CASES
4. Update ALL_TEST_CASES at the bottom
"""

# ============================================================================
# STANDARD CASES (100-200 examples)
# Paste ChatGPT output here
# ============================================================================
AG_NEWS_STANDARD_CASES = [
    # 101–250 (150 items), cycling labels: world, sports, business, sci/tech
    {"id": "101", "question": "UN Summit Opens in Geneva to Address Rising Global Food Insecurity", "answer": "world"},
    {"id": "102", "question": "City FC Clinches League Title in Dramatic Final-Day Comeback", "answer": "sports"},
    {"id": "103", "question": "Global Markets Rally as Inflation Cools and Fed Signals Rate Pause", "answer": "business"},
    {"id": "104", "question": "Researchers Develop New Quantum Chip That Could Power Next-Gen Encryption", "answer": "sci/tech"},

    {"id": "105", "question": "Peace Talks Resume Between Rival Factions After Months of Border Clashes", "answer": "world"},
    {"id": "106", "question": "Olympic Committee Confirms New Events for 2028 Games, Including Flag Football", "answer": "sports"},
    {"id": "107", "question": "Major Retailer Files for Bankruptcy Amid Shift to Online Shopping", "answer": "business"},
    {"id": "108", "question": "SpaceX Launches 60 More Satellites in Latest Starlink Mission", "answer": "sci/tech"},

    {"id": "109", "question": "Flooding Displaces Thousands as Heavy Rains Batter Southeast Asia", "answer": "world"},
    {"id": "110", "question": "Top Seed Upset in Straight Sets at Australian Open", "answer": "sports"},
    {"id": "111", "question": "Oil Prices Dip as OPEC+ Signals Possible Output Increase", "answer": "business"},
    {"id": "112", "question": "AI Start-Up Unveils Tool That Can Generate Realistic Human Voices from Text", "answer": "sci/tech"},

    {"id": "113", "question": "European Union Approves New Sanctions Package Over Cyberattacks", "answer": "world"},
    {"id": "114", "question": "Rookie Quarterback Leads Team to First Playoff Win in Two Decades", "answer": "sports"},
    {"id": "115", "question": "Fintech Firm Announces Zero-Fee Trading to Attract Young Investors", "answer": "business"},
    {"id": "116", "question": "Scientists Discover Potential Earth-Like Exoplanet in Nearby Star System", "answer": "sci/tech"},

    {"id": "117", "question": "Violent Protests Erupt After Contested Election Results in Capital City", "answer": "world"},
    {"id": "118", "question": "Star Striker Signs Two-Year Extension with Hometown Club", "answer": "sports"},
    {"id": "119", "question": "Electric Vehicle Sales Hit Record High Despite Supply Chain Challenges", "answer": "business"},
    {"id": "120", "question": "New Smartphone Chip Promises Faster Gaming and Improved Battery Life", "answer": "sci/tech"},

    {"id": "121", "question": "Global Leaders Condemn Missile Test, Call for Immediate De-Escalation", "answer": "world"},
    {"id": "122", "question": "National Basketball Team Books Spot in World Cup After Overtime Thriller", "answer": "sports"},
    {"id": "123", "question": "Bank Reports Record Profits on Surge in Credit Card Spending", "answer": "business"},
    {"id": "124", "question": "Open-Source Community Launches New Framework for Privacy-Preserving AI", "answer": "sci/tech"},

    {"id": "125", "question": "Humanitarian Aid Convoys Reach War-Torn Region After Cease-Fire Agreement", "answer": "world"},
    {"id": "126", "question": "Veteran Pitcher Throws No-Hitter in First Start Since Injury", "answer": "sports"},
    {"id": "127", "question": "Housing Market Cools as Mortgage Rates Climb to Five-Year High", "answer": "business"},
    {"id": "128", "question": "Cybersecurity Breach Exposes Data of Millions of Social Media Users", "answer": "sci/tech"},

    {"id": "129", "question": "Regional Bloc Expels Member State Over Repeated Democratic Backsliding", "answer": "world"},
    {"id": "130", "question": "New Study Links Youth Sports Participation to Improved Mental Health", "answer": "sports"},
    {"id": "131", "question": "Start-Up Raises $200 Million to Build Sustainable Packaging Factories", "answer": "business"},
    {"id": "132", "question": "Robotics Company Reveals Humanoid Assistant Aimed at Warehouse Automation", "answer": "sci/tech"},

    {"id": "133", "question": "Wildfires Spread Across Mediterranean Coastline, Forcing Mass Evacuations", "answer": "world"},
    {"id": "134", "question": "Marathon World Record Shattered by Kenyan Runner in Berlin", "answer": "sports"},
    {"id": "135", "question": "Cryptocurrency Exchange Faces Investigation Over Alleged Market Manipulation", "answer": "business"},
    {"id": "136", "question": "Biotech Firm Reports Breakthrough in Gene Therapy for Rare Disorder", "answer": "sci/tech"},

    {"id": "137", "question": "Government Declares State of Emergency After 7.2 Magnitude Earthquake", "answer": "world"},
    {"id": "138", "question": "Women’s National Team Secures Equal Pay Deal in New Labor Agreement", "answer": "sports"},
    {"id": "139", "question": "Tech Giant Misses Earnings Expectations as Ad Revenue Slumps", "answer": "business"},
    {"id": "140", "question": "NASA Confirms Successful Test of Next-Generation Lunar Lander", "answer": "sci/tech"},

    {"id": "141", "question": "Border Tensions Ease as Neighboring Countries Agree to Joint Patrols", "answer": "world"},
    {"id": "142", "question": "High School Phenom Breaks National Record in 100-Meter Dash", "answer": "sports"},
    {"id": "143", "question": "Consumer Confidence Rebounds After Months of Steady Decline", "answer": "business"},
    {"id": "144", "question": "New Battery Technology Promises to Cut Electric Car Charging Time in Half", "answer": "sci/tech"},

    {"id": "145", "question": "WHO Issues Alert Over Resurgence of Measles in Several Regions", "answer": "world"},
    {"id": "146", "question": "League Suspends Star Player Two Games for On-Court Altercation", "answer": "sports"},
    {"id": "147", "question": "Mergers and Acquisitions Slow Amid Regulatory Scrutiny in Europe", "answer": "business"},
    {"id": "148", "question": "Cloud Provider Experiences Outage, Disrupting Services Worldwide", "answer": "sci/tech"},

    {"id": "149", "question": "Referendum Results Show Narrow Support for Constitutional Reform", "answer": "world"},
    {"id": "150", "question": "Underdog Team Advances to Champions League Knockout Stage", "answer": "sports"},
    {"id": "151", "question": "Small Businesses Push Back Against Proposed Tax Increases", "answer": "business"},
    {"id": "152", "question": "Researchers Use Machine Learning to Predict Earthquake Aftershocks", "answer": "sci/tech"},

    {"id": "153", "question": "President Signs Landmark Climate Bill Aimed at Cutting Emissions by 2035", "answer": "world"},
    {"id": "154", "question": "New Rules Introduced to Reduce Concussions in Youth Football Leagues", "answer": "sports"},
    {"id": "155", "question": "Global Airline Alliance Announces Plan to Reach Net-Zero Emissions", "answer": "business"},
    {"id": "156", "question": "Study Finds Social Media Algorithms Can Shape Political Beliefs Over Time", "answer": "sci/tech"},

    {"id": "157", "question": "Cease-Fire Holds as Monitor Group Reports Sharp Drop in Violence", "answer": "world"},
    {"id": "158", "question": "NBA Legend Announces Retirement After 21 Seasons", "answer": "sports"},
    {"id": "159", "question": "E-Commerce Giant Faces Antitrust Lawsuit Over Alleged Predatory Pricing", "answer": "business"},
    {"id": "160", "question": "Scientists Map Human Brain Connections with Unprecedented Detail", "answer": "sci/tech"},

    {"id": "161", "question": "International Court Orders Immediate Halt to Construction of Controversial Dam", "answer": "world"},
    {"id": "162", "question": "Esports Viewership Surges as Global Tournament Breaks Streaming Records", "answer": "sports"},
    {"id": "163", "question": "Real Estate Investors Pivot to Suburban Offices Amid Remote Work Trends", "answer": "business"},
    {"id": "164", "question": "New Encryption Standard Approved to Protect Data from Quantum Attacks", "answer": "sci/tech"},

    {"id": "165", "question": "Human Rights Watchdog Accuses Regime of Systematic Abuses", "answer": "world"},
    {"id": "166", "question": "Fans Return to Stadiums as League Lifts Pandemic Attendance Limits", "answer": "sports"},
    {"id": "167", "question": "Credit Rating Agency Downgrades Country’s Debt After Political Turmoil", "answer": "business"},
    {"id": "168", "question": "Startup Launches App to Help Visually Impaired Users Navigate Cities", "answer": "sci/tech"},

    {"id": "169", "question": "EU and UK Reach Post-Brexit Deal on Northern Ireland Trade Rules", "answer": "world"},
    {"id": "170", "question": "Tennis Star Makes Triumphant Comeback After Year-Long Injury Layoff", "answer": "sports"},
    {"id": "171", "question": "Global Chip Shortage Eases as New Manufacturing Plants Come Online", "answer": "business"},
    {"id": "172", "question": "Deepfake Detection Tools Race to Keep Up with Rapidly Improving AI", "answer": "sci/tech"},

    {"id": "173", "question": "Massive Pro-Democracy Rally Draws Hundreds of Thousands to City Center", "answer": "world"},
    {"id": "174", "question": "Local Club Wins First National Title in Its 75-Year History", "answer": "sports"},
    {"id": "175", "question": "Investors Flock to Green Bonds as Demand for ESG Assets Grows", "answer": "business"},
    {"id": "176", "question": "Researchers Reveal New Method to Recycle Hard-to-Process Plastics", "answer": "sci/tech"},

    {"id": "177", "question": "Refugee Numbers Hit Record High, UN Calls for Global Solidarity", "answer": "world"},
    {"id": "178", "question": "Coach Fired After Disappointing Season, Replacement Named Within Hours", "answer": "sports"},
    {"id": "179", "question": "Major Bank Announces Layoffs as It Shifts to Digital-First Strategy", "answer": "business"},
    {"id": "180", "question": "Engineers Test Self-Driving Buses on Public Streets in Scandinavian City", "answer": "sci/tech"},

    {"id": "181", "question": "Latin American Leaders Meet to Discuss Regional Trade and Migration", "answer": "world"},
    {"id": "182", "question": "Nation’s Top College Basketball Prospect Commits to In-State University", "answer": "sports"},
    {"id": "183", "question": "Inflation Hits Households as Food and Energy Prices Continue to Rise", "answer": "business"},
    {"id": "184", "question": "New Health App Uses Wearable Data to Warn Users of Potential Illness", "answer": "sci/tech"},

    {"id": "185", "question": "Election Observers Report Isolated Irregularities but Call Vote Largely Fair", "answer": "world"},
    {"id": "186", "question": "Star Sprinter Suspended After Positive Test for Banned Substance", "answer": "sports"},
    {"id": "187", "question": "Tech IPO Surges 80% on First Day of Trading, Valuing Firm at $40 Billion", "answer": "business"},
    {"id": "188", "question": "Researchers Use CRISPR to Correct Genetic Mutation in Lab-Grown Organs", "answer": "sci/tech"},

    {"id": "189", "question": "Regional Peacekeeping Force Deployed After Clashes Along Disputed Border", "answer": "world"},
    {"id": "190", "question": "New Analytics Deal Gives Team Access to Real-Time Player Tracking Data", "answer": "sports"},
    {"id": "191", "question": "Small-Cap Stocks Outperform Blue Chips as Investors Seek Higher Returns", "answer": "business"},
    {"id": "192", "question": "Tech Conference Highlights Surge in Generative AI Tools for Creators", "answer": "sci/tech"},

    {"id": "193", "question": "Historic Drought Threatens Crops Across Southern Africa, Aid Groups Warn", "answer": "world"},
    {"id": "194", "question": "National Hockey League Expands to New City After Unanimous Owner Vote", "answer": "sports"},
    {"id": "195", "question": "Regulators Approve Mega-Merger Creating One of World’s Largest Telecoms", "answer": "business"},
    {"id": "196", "question": "Engineers Build Prototype Fusion Reactor Reaching Record Plasma Temperature", "answer": "sci/tech"},

    {"id": "197", "question": "Cease-Fire Breaks Down as Artillery Fire Resumes Overnight", "answer": "world"},
    {"id": "198", "question": "Rising Star Wins First Major Golf Championship in Playoff Finish", "answer": "sports"},
    {"id": "199", "question": "Central Bank Hints at Future Rate Cuts to Support Slowing Economy", "answer": "business"},
    {"id": "200", "question": "New Study Shows Link Between Screen Time and Sleep Quality in Teens", "answer": "sci/tech"},

    {"id": "201", "question": "Global Agreement Reached to Phase Down Coal Use at Climate Conference", "answer": "world"},
    {"id": "202", "question": "National Team Stuns Defending Champions in World Cup Opener", "answer": "sports"},
    {"id": "203", "question": "Online Payment Platform Launches Microloan Service for Gig Workers", "answer": "business"},
    {"id": "204", "question": "Scientists Deploy Underwater Drones to Monitor Melting Glaciers", "answer": "sci/tech"},

    {"id": "205", "question": "New Immigration Rules Spark Debate as Government Tightens Border Controls", "answer": "world"},
    {"id": "206", "question": "Historic Rivalry Game Draws Record TV Audience on Streaming Platforms", "answer": "sports"},
    {"id": "207", "question": "Corporate Profits Slide as Strong Dollar Weighs on Overseas Sales", "answer": "business"},
    {"id": "208", "question": "VR Headset Maker Introduces Affordable Model Aimed at Classrooms", "answer": "sci/tech"},

    {"id": "209", "question": "China and Russia Announce Joint Military Exercises in Pacific Region", "answer": "world"},
    {"id": "210", "question": "New Safety Protocols Introduced After Fan Injured by Foul Ball", "answer": "sports"},
    {"id": "211", "question": "Investors Wary as Meme Stocks See Another Sudden Price Surge", "answer": "business"},
    {"id": "212", "question": "Researchers Train AI to Detect Early Signs of Parkinson’s from Voice Recordings", "answer": "sci/tech"},

    {"id": "213", "question": "Central American Nations Coordinate Response to Powerful Hurricane", "answer": "world"},
    {"id": "214", "question": "Women’s Soccer League Announces Expansion Team Led by Celebrity Ownership Group", "answer": "sports"},
    {"id": "215", "question": "Insurance Companies Brace for Higher Payouts After Series of Natural Disasters", "answer": "business"},
    {"id": "216", "question": "Electric Aircraft Prototype Completes First Successful Test Flight", "answer": "sci/tech"},

    {"id": "217", "question": "Voters in Latin America Elect First Green Party President", "answer": "world"},
    {"id": "218", "question": "Boxing Match Ends in Controversial Split Decision, Rematch Demanded", "answer": "sports"},
    {"id": "219", "question": "Luxury Brand Reports Surge in Online Sales Driven by Gen Z Shoppers", "answer": "business"},
    {"id": "220", "question": "Scientists Use 3D Printing to Create Customized Implants for Surgery", "answer": "sci/tech"},

    {"id": "221", "question": "International Sanctions Eased After Country Complies with Nuclear Inspectors", "answer": "world"},
    {"id": "222", "question": "Cricket World Cup Match Delayed by Heavy Rain, Resumes After Inspection", "answer": "sports"},
    {"id": "223", "question": "Tech Firm Announces Stock Buyback Plan to Boost Shareholder Value", "answer": "business"},
    {"id": "224", "question": "Researchers Demonstrate Wi-Fi Standard That Doubles Current Speeds", "answer": "sci/tech"},

    {"id": "225", "question": "Disputed Maritime Border Settlement Opens New Fishing Grounds", "answer": "world"},
    {"id": "226", "question": "Gymnast Wins All-Around Title with Near-Perfect Performance", "answer": "sports"},
    {"id": "227", "question": "Food Delivery Apps Face New Rules on Worker Classification", "answer": "business"},
    {"id": "228", "question": "Privacy Advocates Criticize Expansion of Facial Recognition in Public Spaces", "answer": "sci/tech"},

    {"id": "229", "question": "International Observers Praise Peaceful Transfer of Power After Election", "answer": "world"},
    {"id": "230", "question": "Baseball League Introduces Pitch Clock to Speed Up Games", "answer": "sports"},
    {"id": "231", "question": "Venture Capital Funding Slows as Investors Turn Cautious on Late-Stage Startups", "answer": "business"},
    {"id": "232", "question": "Company Launches Satellite Constellation to Provide Global Broadband Coverage", "answer": "sci/tech"},

    {"id": "233", "question": "Thousands March in European Capitals to Protest War in Middle East", "answer": "world"},
    {"id": "234", "question": "National Swimming Championships See Multiple Records Fall in One Night", "answer": "sports"},
    {"id": "235", "question": "Airline Shares Drop After Fuel Costs Rise and Travel Demand Softens", "answer": "business"},
    {"id": "236", "question": "New Open-Source Tool Helps Journalists Verify Authenticity of Online Images", "answer": "sci/tech"},

    {"id": "237", "question": "African Union Welcomes New Member State After Years of Diplomatic Effort", "answer": "world"},
    {"id": "238", "question": "Rugby World Cup Organizers Introduce Stricter Head-Injury Protocols", "answer": "sports"},
    {"id": "239", "question": "Gold Prices Hit Record High as Investors Seek Safe Haven Assets", "answer": "business"},
    {"id": "240", "question": "Scientists Deploy Swarm of Cheap Sensors to Track Urban Air Pollution", "answer": "sci/tech"},

    {"id": "241", "question": "Global Aid Conference Raises Billions for Earthquake Recovery Efforts", "answer": "world"},
    {"id": "242", "question": "Formula One Team Unveils Car for New Season with Radical Aerodynamic Design", "answer": "sports"},
    {"id": "243", "question": "Consumer Watchdog Warns of Rising Household Debt Levels", "answer": "business"},
    {"id": "244", "question": "Researchers Use VR Therapy to Help Patients Overcome Phobias", "answer": "sci/tech"},

    {"id": "245", "question": "Middle East Peace Talks Stalled as Parties Disagree on Key Terms", "answer": "world"},
    {"id": "246", "question": "National League Announces Plan to Host Outdoor Hockey Game in City Park", "answer": "sports"},
    {"id": "247", "question": "Automaker Recalls 1.2 Million Vehicles Over Brake Defect", "answer": "business"},
    {"id": "248", "question": "Scientists Develop Wearable Patch That Monitors Blood Sugar Without Needles", "answer": "sci/tech"},

    {"id": "249", "question": "Regional Bloc Launches Joint Currency to Boost Intra-African Trade", "answer": "world"},
    {"id": "250", "question": "Star Forward Transfers to Rival Club in Record-Breaking Deal", "answer": "sports"},
]


AG_NEWS_EDGE_CASES = [
    # Empty / minimal / odd formatting
    {"id": "edge_1", "question": "", "answer": "world"},
    {"id": "edge_2", "question": " ", "answer": "business"},
    {"id": "edge_3", "question": "???", "answer": "sci/tech"},
    {"id": "edge_4", "question": "123456", "answer": "sports"},

    # Very short but clear
    {"id": "edge_5", "question": "Oil climbs", "answer": "business"},
    {"id": "edge_6", "question": "Championship tonight", "answer": "sports"},
    {"id": "edge_7", "question": "Peace talks", "answer": "world"},
    {"id": "edge_8", "question": "New chipset", "answer": "sci/tech"},

    # Ambiguous headline (could be multiple, but we force a label)
    {"id": "edge_9", "question": "Giants crush profits expectations", "answer": "business"},
    {"id": "edge_10", "question": "Amazon storms Europe", "answer": "business"},

    # Near-duplicates with different labels
    {"id": "edge_11", "question": "City wins big after record sponsorship deal", "answer": "business"},
    {"id": "edge_12", "question": "City wins big after record comeback on home field", "answer": "sports"},

    # Special characters / unicode
    {"id": "edge_13", "question": "€ surges as ECB hints at rate hike", "answer": "business"},
    {"id": "edge_14", "question": "“Breakthrough” in climate talks, officials say", "answer": "world"},
    {"id": "edge_15", "question": "New AI model beats humans in Go — again", "answer": "sci/tech"},

    # Very long inputs (short news blurbs, 150–250 words)
    {
        "id": "edge_16",
        "question": (
            "Government leaders from more than 40 countries gathered in Brussels on Monday for an emergency summit "
            "focused on rising energy prices and the ongoing war’s impact on Europe’s gas supply. Over the past year, "
            "households across the continent have faced soaring utility bills as sanctions, supply disruptions, and "
            "decades-low reserves left many nations scrambling to secure alternative sources of fuel. The draft "
            "agreement being circulated proposes a temporary cap on wholesale gas prices, a coordinated effort to "
            "purchase liquefied natural gas from multiple suppliers, and new investments in cross-border infrastructure. "
            "Several member states, however, remain skeptical of price caps, warning that they could drive suppliers to "
            "other regions. Humanitarian organizations have urged leaders to prioritize vulnerable families and public "
            "services such as hospitals and schools, which are struggling to pay for heat and electricity as winter "
            "approaches. Officials say a final deal could be reached later this week."
        ),
        "answer": "world",
    },
    {
        "id": "edge_17",
        "question": (
            "In a move that could reshape the streaming landscape, SportsHub+, a major subscription service dedicated "
            "to live sports, unveiled plans on Thursday to offer a single pass granting fans access to every game across "
            "four top professional leagues. Under the proposal, viewers would pay a flat monthly fee to watch regular-"
            "season and playoff contests in football, basketball, baseball, and hockey without local blackouts. The "
            "announcement comes as younger audiences increasingly abandon cable bundles in favor of on-demand platforms "
            "and as leagues search for new ways to grow international viewership. Industry analysts say the deal, if "
            "approved by team owners and regulators, could dramatically change how fans follow their favorite clubs and "
            "players, while also raising questions about revenue sharing, regional broadcasters, and the long-term value "
            "of traditional TV rights packages."
        ),
        "answer": "sports",
    },
    {
        "id": "edge_18",
        "question": (
            "Shares of consumer electronics manufacturer Novatek fell more than 11% in afternoon trading after the "
            "company reported quarterly earnings that missed Wall Street estimates and issued a cautious outlook for "
            "2026. Executives cited weaker-than-expected demand for tablets and mid-range smartphones, as well as higher "
            "component costs due to lingering supply chain disruptions. To offset the slowdown, Novatek plans to cut "
            "operating expenses, streamline its product portfolio, and accelerate investments in smart-home devices and "
            "wearable health sensors, where margins remain strong. Despite the disappointing results, several analysts "
            "noted that the company’s balance sheet is healthy and that its long-term strategy to focus on premium "
            "devices could pay off if inflation eases and consumer confidence improves in the second half of the year."
        ),
        "answer": "business",
    },
    {
        "id": "edge_19",
        "question": (
            "A team of scientists at the European Molecular Computing Lab has demonstrated what they describe as a major "
            "advance in neuromorphic hardware, unveiling a prototype chip that mimics the way biological neurons fire in "
            "response to electrical signals. Unlike traditional processors, which execute instructions sequentially, the "
            "new device uses thousands of tiny, energy-efficient cores that operate in parallel, potentially allowing it "
            "to run complex artificial intelligence models at a fraction of the power required by current GPUs. During "
            "tests, the chip successfully recognized spoken digits and classified images from a standard benchmark "
            "dataset while consuming less energy than a typical smartphone. The researchers say future generations of "
            "the technology could be embedded in autonomous drones, medical implants, or edge devices that need to "
            "analyze data in real time without constant access to the cloud."
        ),
        "answer": "sci/tech",
    },

    # Boundary style: headline that looks like list / meta
    {"id": "edge_20", "question": "Top 10 things to know about today’s global markets", "answer": "business"},
]


AG_NEWS_ADVERSARIAL_CASES = [
    # Misleading keywords / mixed topics
    {
        "id": "adv_1",
        "question": "Tech stocks rally as championship parade boosts downtown spending",
        "answer": "business",
    },
    {
        "id": "adv_2",
        "question": "Government slams social media giant after soccer final streaming outage",
        "answer": "world",
    },
    {
        "id": "adv_3",
        "question": "Star striker’s NFT collection sells out in minutes, raising $5 million",
        "answer": "business",
    },

    # Subtle negations / reversals
    {
        "id": "adv_4",
        "question": "Study finds no evidence that new vaccine technology increases heart risk",
        "answer": "sci/tech",
    },
    {
        "id": "adv_5",
        "question": "League will not cancel season despite ongoing player contract dispute",
        "answer": "sports",
    },
    {
        "id": "adv_6",
        "question": "Sanctions will not be lifted as leaders say cease-fire terms were violated",
        "answer": "world",
    },

    # Mixed-topic headlines (sport + finance, tech + politics)
    {
        "id": "adv_7",
        "question": "City’s Olympic bid hinges on $3 billion private financing package",
        "answer": "business",
    },
    {
        "id": "adv_8",
        "question": "Artificial intelligence center becomes focal point of diplomatic spat with neighboring country",
        "answer": "world",
    },
    {
        "id": "adv_9",
        "question": "Streaming platform signs massive deal for global football rights as it tests new 8K streaming tech",
        "answer": "sports",
    },
    {
        "id": "adv_10",
        "question": "Crypto-backed soccer league promises to decentralize team ownership using blockchain tools",
        "answer": "sci/tech",
    },

    # Context-dependent, require real understanding
    {
        "id": "adv_11",
        "question": "Central bank tests digital currency in limited pilot with three major commercial lenders",
        "answer": "business",
    },
    {
        "id": "adv_12",
        "question": "Scientists warn that AI-generated war footage could further inflame regional tensions",
        "answer": "world",
    },
    {
        "id": "adv_13",
        "question": "Coach credits data-driven training algorithms for team’s surprise playoff run",
        "answer": "sports",
    },
    {
        "id": "adv_14",
        "question": "Chipmaker faces export controls as new rules target advanced semiconductor tools",
        "answer": "sci/tech",
    },

    # Near-duplicate framing with different possible labels (we fix one)
    {
        "id": "adv_15",
        "question": "Fans protest outside stadium over ticket price hikes ahead of new season",
        "answer": "sports",
    },
]


AG_NEWS_ALL_TEST_CASES = AG_NEWS_STANDARD_CASES + AG_NEWS_EDGE_CASES + AG_NEWS_ADVERSARIAL_CASES


# ============================================================================
# COMBINED (DO NOT MODIFY THIS MANUALLY)
# ============================================================================


