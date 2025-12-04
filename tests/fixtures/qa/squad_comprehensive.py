"""
Comprehensive test cases for SQuAD v1.1 - Question Answering

Dataset: SQuAD v1.1 (Stanford Question Answering Dataset)
Task: document_qa
Domain: General knowledge (Wikipedia passages)
Metrics: exact_match, f1 (token-level F1)
Total Cases: Will be 150+ after you generate with ChatGPT

---

INSTRUCTIONS:
1. Use the ChatGPT prompt below
2. Paste the generated cases in the appropriate sections
3. Verify answers are extractive (exist in context)
4. Check varied question types (Who, What, When, Where, How, Why)

---

CHATGPT PROMPT:

I need comprehensive test cases for SQuAD v1.1 (extractive question answering from Wikipedia).

Current examples from the dataset:
{"id": "1", "question": "When was the University of Chicago founded?", "context": "The University of Chicago is a private research university located in Chicago, Illinois. It was established through the efforts of the American Baptist Education Society and oil magnate John D. Rockefeller. The university opened its doors to students in the early 1890s, with its first classes held in temporary buildings.", "answer": "1890"}

{"id": "2", "question": "What is the capital of France?", "context": "France is a country located in Western Europe, bordered by Spain, Italy, Germany, Belgium, and Switzerland. The country's largest city and political center is located along the Seine River. This city is known for landmarks such as the Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral. It serves as the seat of the French government and is home to over 2 million people.", "answer": "Paris"}

Generate:

1. **100 standard examples** (extractive QA from Wikipedia-style passages):
   - Varied topics: history, science, geography, culture, technology, sports
   - Question types: Who (20%), What (30%), When (15%), Where (15%), How/Why (20%)
   - Context lengths: 50-300 words
   - Answer lengths: 1-10 words (mostly 1-3 words)
   - Answer positions: start, middle, end of context (varied)
   - Sequential IDs: "101", "102", ..., "200"
   
   Format requirements:
   - Context must contain the exact answer string
   - Questions should be natural and unambiguous
   - Mix of factual and conceptual questions
   - Include numbers, dates, names, places

2. **20 edge cases**:
   - ID "edge_1": Very short context (10 words), answer: single word
   - ID "edge_2": Very long context (500+ words), answer buried in middle
   - ID "edge_3": Answer is first word of context
   - ID "edge_4": Answer is last word of context
   - ID "edge_5": Answer appears multiple times in context (use first occurrence)
   - ID "edge_6": Answer is a single number: "1776"
   - ID "edge_7": Answer is a year: "2023"
   - ID "edge_8": Answer is a date: "March 15, 1993"
   - ID "edge_9": Answer with punctuation: "Dr. Smith"
   - ID "edge_10": Answer with special chars: "$1.5 million"
   - ID "edge_11": Multi-word answer: "World War II"
   - ID "edge_12": Answer with articles: "the Pacific Ocean"
   - ID "edge_13": Question requires exact phrase: "Industrial Revolution"
   - ID "edge_14" - "edge_20": Other variations (acronyms, abbreviations, etc.)

3. **15 adversarial cases** (challenging for QA models):
   - ID "adv_1": Answer requires normalization ("1890s" in context, "1890" acceptable)
   - ID "adv_2": Paraphrase in question vs context ("capital" vs "largest city")
   - ID "adv_3": Multiple potential answers, need most specific one
   - ID "adv_4": Question with negation: "What did X NOT do?"
   - ID "adv_5": Requires multi-sentence reasoning
   - ID "adv_6": Temporal reasoning: "before/after" in question
   - ID "adv_7": Comparative: "larger than", "more than"
   - ID "adv_8": Pronoun resolution: "he", "it", "they" in question
   - ID "adv_9" - "adv_15": Other challenging cases (implied info, world knowledge)

Output as three Python lists:
```python
SQUAD_STANDARD = [
    {
        "id": "101",
        "question": "Who invented the telephone?",
        "context": "Alexander Graham Bell was a Scottish-born inventor, scientist, and engineer who is credited with patenting the first practical telephone in 1876. Born in Edinburgh, Bell moved to North America and conducted much of his research in the United States and Canada.",
        "answer": "Alexander Graham Bell"
    },
    # ...
]

SQUAD_EDGE = [...]

SQUAD_ADVERSARIAL = [...]
```

Format: Each item MUST have:
- "id" (string)
- "question" (string)
- "context" (string, 50-500 words)
- "answer" (string, must appear exactly in context)

IMPORTANT: The answer string must be an exact substring of the context!
"""

# ============================================================================
# STANDARD CASES (100 examples)
# Paste ChatGPT output here
# ============================================================================
# Base contexts reused across cases to keep things concise

CTX_1_EIFFEL = """The Eiffel Tower is a wrought-iron lattice tower located on the Champ de Mars in Paris, France. \
It was constructed between 1887 and 1889 as the entrance arch to the 1889 Exposition Universelle, a world's fair \
held to celebrate the 100th anniversary of the French Revolution. Designed by the engineer Gustave Eiffel and his \
company, the tower was initially criticized by some artists and intellectuals for its radical appearance. Over time \
it became one of the most recognizable structures in the world and a global symbol of France, visited by millions \
of tourists each year."""

CTX_2_AMAZON = """The Amazon rainforest covers much of northern South America, spanning countries such as Brazil, \
Peru, Colombia and several others. It is often called the "lungs of the Earth" because its dense vegetation absorbs \
large amounts of carbon dioxide and releases oxygen. The region is home to an extraordinary variety of plant and \
animal species, many of which are not found anywhere else on the planet. Indigenous communities have lived in the \
Amazon for thousands of years, developing detailed knowledge of its rivers, plants and wildlife. In recent decades, \
deforestation for agriculture, logging and mining has threatened the forest's biodiversity and its role in regulating \
the global climate."""

CTX_3_WW2 = """The Second World War was a global conflict that lasted from 1939 to 1945 and involved the vast majority \
of the world's nations. It began when Nazi Germany invaded Poland, prompting Britain and France to declare war on \
Germany. Over the following years the conflict spread across Europe, Asia, Africa and the Pacific. The Allied powers, \
including the United States, the United Kingdom, the Soviet Union and China, eventually defeated the Axis powers of \
Germany, Italy and Japan. The war resulted in tens of millions of deaths and widespread destruction, leading to the \
establishment of the United Nations and a new international order."""

CTX_4_PYTHON = """Python is a high-level programming language first released by Guido van Rossum in 1991. It emphasizes \
code readability through the use of significant indentation and a relatively simple syntax. Python supports multiple \
programming paradigms, including procedural, object-oriented and functional styles. A large standard library and a vast \
ecosystem of third-party packages make it popular for tasks ranging from web development to scientific computing and \
machine learning. The language is maintained by the Python Software Foundation, which oversees its development and releases."""

CTX_5_PHOTOSYN = """Photosynthesis is the process by which green plants, algae and some bacteria convert light energy \
into chemical energy stored in glucose. It primarily takes place in chloroplasts, specialized organelles that contain \
the pigment chlorophyll. During photosynthesis, organisms use carbon dioxide and water, releasing oxygen as a by-product. \
The process consists of light-dependent reactions, which generate ATP and NADPH, and the Calvin cycle, which uses those \
molecules to fix carbon into sugars. Photosynthesis is fundamental to life on Earth because it forms the base of most \
food chains and helps regulate atmospheric carbon dioxide levels."""

CTX_6_MARS = """Mars is the fourth planet from the Sun in our solar system and is often referred to as the Red Planet \
because of its rusty, iron-rich surface. It has a thin atmosphere composed mostly of carbon dioxide and experiences \
cold temperatures, dust storms and distinct seasons. For decades, Mars has been a focus of robotic exploration, with \
orbiters, landers and rovers sent by space agencies such as NASA and the European Space Agency. Missions like Spirit, \
Opportunity, Curiosity and Perseverance have studied Martian geology and searched for signs of past water activity. \
Scientists are particularly interested in Mars as a potential site for past or future life and as a target for human exploration."""

CTX_7_OLYMPICS = """The modern Olympic Games are an international multi-sport event inspired by the ancient competitions \
held in Olympia, Greece. They are organized by the International Olympic Committee and take place every four years, \
alternating between Summer and Winter editions. Athletes from around the world compete in disciplines ranging from \
track and field to swimming, gymnastics and team sports. Hosting the Olympics is seen as a prestigious opportunity for \
cities to showcase their culture and infrastructure, although the events can also be costly and controversial. The Games \
aim to promote peace, friendship and fair play among nations."""

CTX_8_INTERNET = """The internet is a global network of interconnected computer systems that enables the rapid exchange \
of information. It traces its origins to research projects funded by the United States Department of Defense in the \
1960s, including ARPANET. Over time, standard protocols such as TCP/IP allowed different networks to interoperate and \
form a worldwide system. The invention of the World Wide Web by Tim Berners-Lee in 1989 made it easier for users to \
access and share documents through web browsers. Today, the internet underpins communication, commerce, education and \
entertainment, profoundly shaping modern society."""

CTX_9_HEART = """The human heart is a muscular organ responsible for pumping blood throughout the body via the circulatory \
system. It is roughly the size of a fist and is located slightly left of the center of the chest. The heart consists of \
four chambers: two atria and two ventricles, separated by valves that ensure blood flows in one direction. Oxygen-poor \
blood returns from the body to the right side of the heart, while oxygen-rich blood from the lungs enters the left side. \
Electrical signals coordinate the heartbeat, allowing the organ to contract rhythmically and maintain adequate blood \
pressure and perfusion of tissues."""

CTX_10_SHAKESPEARE = """William Shakespeare was an English playwright, poet and actor widely regarded as one of the most \
influential writers in the English language. He was born in Stratford-upon-Avon in the late sixteenth century and spent \
much of his career in London, where his plays were performed by the Lord Chamberlain's Men. Shakespeare authored tragedies, \
comedies and histories, including works such as Hamlet, Macbeth, A Midsummer Night's Dream and Henry V. His plays explore \
themes like power, love, jealousy and fate, and they continue to be adapted for stage and screen around the world."""

CTX_11_GBR = """The Great Barrier Reef is the world's largest coral reef system, stretching for more than 2,300 kilometers \
off the northeastern coast of Australia. It is composed of thousands of individual reefs and hundreds of islands made of \
over 600 types of hard and soft coral. The reef supports a remarkably diverse ecosystem, including fish, turtles, sharks \
and marine mammals. In 1981 it was designated a UNESCO World Heritage Site. However, the Great Barrier Reef faces serious \
threats from climate change, coral bleaching, pollution and overfishing, prompting conservation efforts by scientists and \
governments."""

CTX_12_FRENCH_REV = """The French Revolution was a period of radical social and political change in France that lasted \
from 1789 to 1799. It began with a financial crisis and popular discontent with the monarchy of Louis XVI. The revolution \
led to the abolition of feudal privileges, the Declaration of the Rights of Man and of the Citizen and the execution of \
the king. Over time, different factions competed for power, resulting in periods of extreme violence such as the Reign of \
Terror. The revolution ultimately paved the way for the rise of Napoleon Bonaparte and transformed French society and its \
institutions."""

CTX_13_ML = """Machine learning is a field of computer science that focuses on algorithms that can learn patterns from \
data and make predictions or decisions. Instead of being explicitly programmed for every task, these algorithms adjust \
internal parameters based on examples. Common categories include supervised learning, unsupervised learning and \
reinforcement learning. Techniques such as decision trees, support vector machines and neural networks are widely used \
in applications ranging from image recognition to recommendation systems. The recent growth of deep learning has enabled \
remarkable advances but has also raised questions about interpretability and fairness."""

CTX_14_ECLIPSE = """A solar eclipse occurs when the Moon passes between the Sun and the Earth, partially or completely \
blocking the Sun's light as seen from specific regions on the planet. Total solar eclipses happen when the Moon's \
apparent diameter is large enough to cover the entire solar disk, briefly turning day into twilight. Partial and \
annular eclipses occur when only part of the Sun is obscured or when the Moon appears slightly smaller than the Sun. \
Solar eclipses follow predictable paths and are valuable for scientific observations, such as studying the Sun's corona. \
Observers must use proper eye protection when viewing them to avoid permanent eye damage."""

CTX_15_EVEREST = """Mount Everest is the highest mountain above sea level on Earth, rising to an official elevation of \
8,848.86 meters. It is located in the Himalayas on the border between Nepal and the Tibet Autonomous Region of China. \
The mountain was first summited in 1953 by Sir Edmund Hillary of New Zealand and Tenzing Norgay, a Sherpa climber. Since \
then, thousands of climbers have attempted the ascent, facing challenges such as extreme altitude, unpredictable weather \
and the risk of avalanches. Everest has become a symbol of human endurance but has also raised concerns about overcrowding \
and environmental impact."""

CTX_16_CLIMATE = """Climate change refers to long-term shifts in temperatures and weather patterns, largely driven in \
recent decades by human activities. The burning of fossil fuels such as coal, oil and gas releases greenhouse gases, \
including carbon dioxide and methane, into the atmosphere. These gases trap heat and lead to global warming, which in \
turn affects sea levels, precipitation and the frequency of extreme weather events. Scientists use climate models, \
historical records and satellite observations to study these changes. International agreements like the Paris Agreement \
aim to limit temperature rise by reducing greenhouse gas emissions and promoting adaptation strategies."""

CTX_17_RENAISSANCE = """The Renaissance was a cultural movement that began in Italy in the fourteenth century and later \
spread throughout Europe. It emphasized a renewed interest in classical learning, humanism and the arts. Renaissance \
artists such as Leonardo da Vinci, Michelangelo and Raphael produced paintings and sculptures noted for their realism, \
use of perspective and exploration of human emotion. Patrons, including wealthy families like the Medici, funded artistic \
and scholarly projects in cities such as Florence and Rome. The movement also influenced literature, science and politics, \
helping to shape the transition from the medieval to the early modern world."""

CTX_18_EGYPT = """Ancient Egypt was a civilization that developed along the Nile River in northeastern Africa over several \
millennia. Its history is traditionally divided into periods such as the Old Kingdom, Middle Kingdom and New Kingdom. \
Pharaohs, considered both political and religious leaders, ruled the land and sponsored monumental building projects, \
including pyramids and temples. The Egyptians developed a writing system called hieroglyphics and made advances in fields \
such as mathematics, medicine and engineering. Their religious beliefs emphasized the afterlife, leading to complex burial \
practices and the mummification of bodies."""

CTX_19_GOOGLE = """Google is a technology company founded in 1998 by Larry Page and Sergey Brin while they were PhD \
students at Stanford University. The company initially focused on developing a search engine that ranked web pages using \
a system called PageRank. Over time, Google expanded into numerous products and services, including email, mobile \
operating systems, cloud computing and advertising platforms. In 2015 Google reorganized under a holding company called \
Alphabet Inc., allowing its core search business and more experimental projects to be managed separately. The company's \
mission is often summarized as organizing the world's information and making it universally accessible and useful."""

CTX_20_JAZZ = """Jazz is a musical genre that originated in the late nineteenth and early twentieth centuries in African \
American communities of the United States, particularly in New Orleans. It is characterized by swing rhythms, \
improvisation and a blend of African and European musical elements. Early jazz styles included ragtime and Dixieland, \
while later developments gave rise to bebop, cool jazz and fusion. Influential musicians such as Louis Armstrong, Duke \
Ellington and Miles Davis helped shape the genre's evolution. Jazz has had a profound impact on popular music and \
continues to inspire performers and composers around the world."""

CTX_21_BH = """A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape \
from it. According to general relativity, black holes form when massive stars collapse under their own gravity at the end \
of their life cycles. The boundary beyond which escape is impossible is known as the event horizon. At the center lies a \
singularity, a point where densities are thought to become infinite, although its true nature remains unknown. Astronomers \
infer the presence of black holes by observing their effects on nearby matter and light, including X-ray emissions from \
accreting material."""

CTX_22_ROMAN_ROADS = """The road network of the Roman Empire was one of the most advanced transportation systems of the \
ancient world. Roman engineers built thousands of kilometers of roads using layered construction techniques that combined \
stone, gravel and sand for durability. Major routes such as the Via Appia connected Rome to distant provinces, facilitating \
military movements, trade and communication. Milestones placed along the roads recorded distances and sometimes the names \
of emperors who commissioned construction. The efficiency of Roman roads contributed significantly to the cohesion and \
economic integration of the empire."""

CTX_23_DNA = """Deoxyribonucleic acid, or DNA, is the hereditary material in almost all living organisms. It consists of \
two long strands that form a double helix, held together by complementary base pairs: adenine with thymine and cytosine \
with guanine. DNA is organized into structures called chromosomes and is found in the nucleus of eukaryotic cells. The \
sequence of bases encodes genetic information that directs the synthesis of proteins. In 1953 James Watson and Francis \
Crick, building on the work of Rosalind Franklin and others, proposed the double-helix model of DNA structure, revolutionizing \
molecular biology."""

CTX_24_APOLLO11 = """Apollo 11 was a mission of the United States Apollo program that achieved the first crewed landing on \
the Moon. Launched by a Saturn V rocket on 16 July 1969, the spacecraft carried astronauts Neil Armstrong, Edwin "Buzz" \
Aldrin and Michael Collins. On 20 July, the lunar module Eagle separated from the command module and descended to the \
lunar surface. Armstrong became the first person to step onto the Moon, followed shortly by Aldrin, while Collins remained \
in lunar orbit. The astronauts collected rock samples, conducted experiments and returned safely to Earth, fulfilling a \
major goal of the space race."""

CTX_25_BITCOIN = """Bitcoin is a decentralized digital currency introduced in 2009 by an individual or group using the \
pseudonym Satoshi Nakamoto. It operates on a peer-to-peer network without a central authority such as a bank or government. \
Transactions are recorded on a public ledger called the blockchain, which is maintained by participants known as miners who \
validate blocks of transactions using cryptographic algorithms. New bitcoins are created as rewards for mining, though the \
total supply is capped at 21 million coins. Bitcoin has been praised as an innovation in digital payments but also criticized \
for price volatility and environmental concerns related to energy use."""

CTX_26_LEONARDO = """Leonardo da Vinci was an Italian polymath of the Renaissance whose interests spanned painting, \
engineering, anatomy, astronomy and more. Born in 1452 in the town of Vinci, he later worked in cities such as Florence, \
Milan and Rome. Leonardo produced iconic artworks including the Mona Lisa and The Last Supper, noted for their composition \
and subtle use of light and shadow. His notebooks contain detailed sketches of machines, human anatomy and scientific \
observations, revealing a restless curiosity about the natural world. Leonardo is often regarded as a symbol of the \
Renaissance ideal of the universal genius."""

CTX_27_CELL_DIV = """Cell division is the process by which a parent cell splits into two or more daughter cells. In \
eukaryotic organisms, somatic cells typically divide by mitosis, which ensures that each daughter cell receives an \
identical set of chromosomes. Gametes, by contrast, are produced through meiosis, a specialized form of division that \
reduces the chromosome number by half. Proper regulation of cell division is essential for growth, tissue repair and \
development. When the mechanisms controlling division fail, cells may proliferate uncontrollably, contributing to the \
formation of tumors and cancer."""

CTX_28_WHO = """The World Health Organization is a specialized agency of the United Nations responsible for international \
public health. It was established on 7 April 1948 and is headquartered in Geneva, Switzerland. The organization coordinates \
responses to disease outbreaks, develops health guidelines and supports member states in strengthening their health systems. \
Programs focus on issues such as vaccination, maternal and child health, noncommunicable diseases and emergency preparedness. \
The WHO also compiles statistics on global health trends and publishes reports that inform policy decisions around the world."""

CTX_29_SILK_ROAD = """The Silk Road was a network of trade routes that connected East Asia with the Mediterranean world for \
many centuries. It emerged during the Han dynasty in China and facilitated the exchange of goods, ideas, religions and \
technologies between distant cultures. Merchants carried silk, spices, precious metals and other commodities across deserts \
and mountains, often stopping at caravanserais for rest and protection. Cities like Samarkand and Kashgar became important \
centers of commerce and cultural interaction. Although maritime routes eventually reduced its prominence, the Silk Road left \
a lasting legacy on the civilizations it linked."""

CTX_30_PRINTING = """The printing press is a mechanical device that allows the mass production of text and images on paper. \
In Europe it is most closely associated with Johannes Gutenberg, who introduced a movable-type printing press in the mid-\
fifteenth century. Gutenberg's innovation dramatically reduced the cost of producing books and pamphlets, contributing to \
the spread of literacy and ideas. Printed materials played a crucial role in movements such as the Renaissance and the \
Reformation, as well as in the development of scientific communication. Over time, printing technology evolved from hand-\
operated presses to steam-powered machines and digital systems."""

SQUAD_STANDARD_CASES = [
    # Eiffel Tower
    {"id": "101", "context": CTX_1_EIFFEL,
     "question": "In which city is the Eiffel Tower located?", "answer": "Paris, France"},
    {"id": "102", "context": CTX_1_EIFFEL,
     "question": "For which event was the Eiffel Tower constructed as an entrance arch?", "answer": "the 1889 Exposition Universelle"},
    {"id": "103", "context": CTX_1_EIFFEL,
     "question": "Who designed the Eiffel Tower?", "answer": "Gustave Eiffel"},
    {"id": "104", "context": CTX_1_EIFFEL,
     "question": "What nation did the Eiffel Tower eventually become a global symbol of?", "answer": "France"},

    # Amazon rainforest
    {"id": "105", "context": CTX_2_AMAZON,
     "question": "Which continent does the Amazon rainforest primarily cover?", "answer": "South America"},
    {"id": "106", "context": CTX_2_AMAZON,
     "question": "Why is the Amazon rainforest often called the 'lungs of the Earth'?", "answer": "because its dense vegetation absorbs large amounts of carbon dioxide and releases oxygen"},
    {"id": "107", "context": CTX_2_AMAZON,
     "question": "Who has lived in the Amazon for thousands of years?", "answer": "Indigenous communities"},
    {"id": "108", "context": CTX_2_AMAZON,
     "question": "Name one major threat to the Amazon rainforest mentioned in the passage.", "answer": "deforestation"},

    # World War II
    {"id": "109", "context": CTX_3_WW2,
     "question": "In which year did the Second World War begin?", "answer": "1939"},
    {"id": "110", "context": CTX_3_WW2,
     "question": "What event triggered Britain and France to declare war on Germany?", "answer": "when Nazi Germany invaded Poland"},
    {"id": "111", "context": CTX_3_WW2,
     "question": "Name one of the Allied powers mentioned in the passage.", "answer": "the United States"},
    {"id": "112", "context": CTX_3_WW2,
     "question": "What international organization was established after the war?", "answer": "the United Nations"},

    # Python programming language
    {"id": "113", "context": CTX_4_PYTHON,
     "question": "Who first released the Python programming language?", "answer": "Guido van Rossum"},
    {"id": "114", "context": CTX_4_PYTHON,
     "question": "In which year was Python first released?", "answer": "1991"},
    {"id": "115", "context": CTX_4_PYTHON,
     "question": "What does Python emphasize to improve code readability?", "answer": "significant indentation"},
    {"id": "116", "context": CTX_4_PYTHON,
     "question": "Which organization maintains the development of Python?", "answer": "the Python Software Foundation"},

    # Photosynthesis
    {"id": "117", "context": CTX_5_PHOTOSYN,
     "question": "What type of energy is converted during photosynthesis?", "answer": "light energy"},
    {"id": "118", "context": CTX_5_PHOTOSYN,
     "question": "Which pigment-containing organelles carry out photosynthesis in plants?", "answer": "chloroplasts"},
    {"id": "119", "context": CTX_5_PHOTOSYN,
     "question": "What gas is released as a by-product of photosynthesis?", "answer": "oxygen"},
    {"id": "120", "context": CTX_5_PHOTOSYN,
     "question": "What cycle uses ATP and NADPH to fix carbon into sugars?", "answer": "the Calvin cycle"},

    # Mars
    {"id": "121", "context": CTX_6_MARS,
     "question": "Which planet is often referred to as the Red Planet?", "answer": "Mars"},
    {"id": "122", "context": CTX_6_MARS,
     "question": "What is the primary component of Mars's thin atmosphere?", "answer": "carbon dioxide"},
    {"id": "123", "context": CTX_6_MARS,
     "question": "Name one NASA rover mentioned that explored Mars.", "answer": "Curiosity"},
    {"id": "124", "context": CTX_6_MARS,
     "question": "What are scientists particularly interested in Mars as a potential site for?", "answer": "past or future life"},

    # Olympic Games
    {"id": "125", "context": CTX_7_OLYMPICS,
     "question": "Which ancient competitions inspired the modern Olympic Games?", "answer": "the ancient competitions held in Olympia, Greece"},
    {"id": "126", "context": CTX_7_OLYMPICS,
     "question": "How often do the Olympic Games take place?", "answer": "every four years"},
    {"id": "127", "context": CTX_7_OLYMPICS,
     "question": "What is one of the aims of the Olympic Games mentioned in the passage?", "answer": "to promote peace, friendship and fair play among nations"},
    {"id": "128", "context": CTX_7_OLYMPICS,
     "question": "Which organization is responsible for organizing the modern Olympic Games?", "answer": "the International Olympic Committee"},

    # Internet
    {"id": "129", "context": CTX_8_INTERNET,
     "question": "Which U.S. department funded early research projects that led to the internet?", "answer": "the United States Department of Defense"},
    {"id": "130", "context": CTX_8_INTERNET,
     "question": "What early network is mentioned as a predecessor to the internet?", "answer": "ARPANET"},
    {"id": "131", "context": CTX_8_INTERNET,
     "question": "Who invented the World Wide Web in 1989?", "answer": "Tim Berners-Lee"},
    {"id": "132", "context": CTX_8_INTERNET,
     "question": "Name one area of modern life that the internet profoundly shapes.", "answer": "communication"},

    # Human heart
    {"id": "133", "context": CTX_9_HEART,
     "question": "Where in the chest is the human heart located?", "answer": "slightly left of the center of the chest"},
    {"id": "134", "context": CTX_9_HEART,
     "question": "How many chambers does the human heart have?", "answer": "four"},
    {"id": "135", "context": CTX_9_HEART,
     "question": "What ensures that blood flows in only one direction through the heart?", "answer": "valves"},
    {"id": "136", "context": CTX_9_HEART,
     "question": "What coordinates the heartbeat so the heart contracts rhythmically?", "answer": "electrical signals"},

    # Shakespeare
    {"id": "137", "context": CTX_10_SHAKESPEARE,
     "question": "In which English town was William Shakespeare born?", "answer": "Stratford-upon-Avon"},
    {"id": "138", "context": CTX_10_SHAKESPEARE,
     "question": "Name one of Shakespeare's tragedies mentioned in the passage.", "answer": "Hamlet"},
    {"id": "139", "context": CTX_10_SHAKESPEARE,
     "question": "What acting company performed Shakespeare's plays in London?", "answer": "the Lord Chamberlain's Men"},
    {"id": "140", "context": CTX_10_SHAKESPEARE,
     "question": "List one theme explored in Shakespeare's plays according to the passage.", "answer": "power"},

    # Great Barrier Reef
    {"id": "141", "context": CTX_11_GBR,
     "question": "Off the coast of which country is the Great Barrier Reef located?", "answer": "Australia"},
    {"id": "142", "context": CTX_11_GBR,
     "question": "In what year was the Great Barrier Reef designated a UNESCO World Heritage Site?", "answer": "1981"},
    {"id": "143", "context": CTX_11_GBR,
     "question": "Name one type of organism that lives in the Great Barrier Reef ecosystem.", "answer": "fish"},
    {"id": "144", "context": CTX_11_GBR,
     "question": "What is one major threat to the Great Barrier Reef mentioned in the text?", "answer": "coral bleaching"},

    # French Revolution
    {"id": "145", "context": CTX_12_FRENCH_REV,
     "question": "Which monarch's reign faced popular discontent at the start of the French Revolution?", "answer": "Louis XVI"},
    {"id": "146", "context": CTX_12_FRENCH_REV,
     "question": "What document declared fundamental rights during the French Revolution?", "answer": "the Declaration of the Rights of Man and of the Citizen"},
    {"id": "147", "context": CTX_12_FRENCH_REV,
     "question": "Name the period of extreme violence during the revolution mentioned in the passage.", "answer": "the Reign of Terror"},
    {"id": "148", "context": CTX_12_FRENCH_REV,
     "question": "Which leader rose to power following the French Revolution?", "answer": "Napoleon Bonaparte"},

    # Machine learning
    {"id": "149", "context": CTX_13_ML,
     "question": "What do machine learning algorithms learn from to make predictions or decisions?", "answer": "data"},
    {"id": "150", "context": CTX_13_ML,
     "question": "Name one category of machine learning mentioned in the passage.", "answer": "supervised learning"},
    {"id": "151", "context": CTX_13_ML,
     "question": "Which technique has contributed to recent advances but raised concerns about interpretability?", "answer": "deep learning"},
    {"id": "152", "context": CTX_13_ML,
     "question": "Give one example of an application of machine learning from the text.", "answer": "image recognition"},

    # Solar eclipse
    {"id": "153", "context": CTX_14_ECLIPSE,
     "question": "What passes between the Sun and the Earth during a solar eclipse?", "answer": "the Moon"},
    {"id": "154", "context": CTX_14_ECLIPSE,
     "question": "What is the term for an eclipse in which the Moon covers the entire solar disk?", "answer": "Total solar eclipses"},
    {"id": "155", "context": CTX_14_ECLIPSE,
     "question": "What part of the Sun can scientists study during a solar eclipse?", "answer": "the Sun's corona"},
    {"id": "156", "context": CTX_14_ECLIPSE,
     "question": "What must observers use to safely view a solar eclipse?", "answer": "proper eye protection"},

    # Mount Everest
    {"id": "157", "context": CTX_15_EVEREST,
     "question": "What is the official elevation of Mount Everest in meters?", "answer": "8,848.86 meters"},
    {"id": "158", "context": CTX_15_EVEREST,
     "question": "Between which two regions is Mount Everest located?", "answer": "Nepal and the Tibet Autonomous Region of China"},
    {"id": "159", "context": CTX_15_EVEREST,
     "question": "Who were the first climbers to reach the summit of Everest in 1953?", "answer": "Sir Edmund Hillary of New Zealand and Tenzing Norgay"},
    {"id": "160", "context": CTX_15_EVEREST,
     "question": "Name one challenge faced by climbers attempting Everest.", "answer": "extreme altitude"},

    # Climate change
    {"id": "161", "context": CTX_16_CLIMATE,
     "question": "Which human activities are largely responsible for recent climate change?", "answer": "the burning of fossil fuels such as coal, oil and gas"},
    {"id": "162", "context": CTX_16_CLIMATE,
     "question": "Name one greenhouse gas mentioned in the passage.", "answer": "carbon dioxide"},
    {"id": "163", "context": CTX_16_CLIMATE,
     "question": "What international agreement seeks to limit global temperature rise?", "answer": "the Paris Agreement"},
    {"id": "164", "context": CTX_16_CLIMATE,
     "question": "What tools do scientists use to study climate change according to the text?", "answer": "climate models, historical records and satellite observations"},

    # Renaissance
    {"id": "165", "context": CTX_17_RENAISSANCE,
     "question": "In which country did the Renaissance begin?", "answer": "Italy"},
    {"id": "166", "context": CTX_17_RENAISSANCE,
     "question": "Name one Renaissance artist mentioned in the passage.", "answer": "Leonardo da Vinci"},
    {"id": "167", "context": CTX_17_RENAISSANCE,
     "question": "Which wealthy family acted as patrons for art and scholarship in cities like Florence?", "answer": "the Medici"},
    {"id": "168", "context": CTX_17_RENAISSANCE,
     "question": "What intellectual movement stressing human potential is associated with the Renaissance?", "answer": "humanism"},

    # Ancient Egypt
    {"id": "169", "context": CTX_18_EGYPT,
     "question": "Along which river did Ancient Egypt develop?", "answer": "the Nile River"},
    {"id": "170", "context": CTX_18_EGYPT,
     "question": "What were the rulers of Ancient Egypt called?", "answer": "Pharaohs"},
    {"id": "171", "context": CTX_18_EGYPT,
     "question": "What writing system did the Egyptians develop?", "answer": "hieroglyphics"},
    {"id": "172", "context": CTX_18_EGYPT,
     "question": "Which practice preserved bodies for the afterlife in Ancient Egypt?", "answer": "the mummification of bodies"},

    # Google
    {"id": "173", "context": CTX_19_GOOGLE,
     "question": "Who founded Google?", "answer": "Larry Page and Sergey Brin"},
    {"id": "174", "context": CTX_19_GOOGLE,
     "question": "In what year was Google founded?", "answer": "1998"},
    {"id": "175", "context": CTX_19_GOOGLE,
     "question": "What algorithm did Google's early search engine use to rank web pages?", "answer": "PageRank"},
    {"id": "176", "context": CTX_19_GOOGLE,
     "question": "Under what holding company was Google reorganized in 2015?", "answer": "Alphabet Inc."},

    # Jazz
    {"id": "177", "context": CTX_20_JAZZ,
     "question": "In which U.S. city did jazz develop particularly strongly?", "answer": "New Orleans"},
    {"id": "178", "context": CTX_20_JAZZ,
     "question": "Name one characteristic feature of jazz mentioned in the passage.", "answer": "improvisation"},
    {"id": "179", "context": CTX_20_JAZZ,
     "question": "Give the name of one influential jazz musician cited.", "answer": "Louis Armstrong"},
    {"id": "180", "context": CTX_20_JAZZ,
     "question": "What impact has jazz had on music according to the text?", "answer": "a profound impact on popular music"},

    # Black holes
    {"id": "181", "context": CTX_21_BH,
     "question": "What is the boundary of a black hole called?", "answer": "the event horizon"},
    {"id": "182", "context": CTX_21_BH,
     "question": "Which theory predicts the formation of black holes from collapsing massive stars?", "answer": "general relativity"},
    {"id": "183", "context": CTX_21_BH,
     "question": "What lies at the center of a black hole according to the passage?", "answer": "a singularity"},
    {"id": "184", "context": CTX_21_BH,
     "question": "How do astronomers infer the presence of black holes?", "answer": "by observing their effects on nearby matter and light"},

    # Roman roads
    {"id": "185", "context": CTX_22_ROMAN_ROADS,
     "question": "What ancient empire built the advanced road network described in the passage?", "answer": "the Roman Empire"},
    {"id": "186", "context": CTX_22_ROMAN_ROADS,
     "question": "Name one famous Roman road mentioned in the text.", "answer": "the Via Appia"},
    {"id": "187", "context": CTX_22_ROMAN_ROADS,
     "question": "What structures recorded distances along Roman roads?", "answer": "Milestones"},
    {"id": "188", "context": CTX_22_ROMAN_ROADS,
     "question": "What did the efficiency of Roman roads contribute to?", "answer": "the cohesion and economic integration of the empire"},

    # DNA
    {"id": "189", "context": CTX_23_DNA,
     "question": "What does DNA stand for?", "answer": "Deoxyribonucleic acid"},
    {"id": "190", "context": CTX_23_DNA,
     "question": "Which two scientists proposed the double-helix model of DNA in 1953?", "answer": "James Watson and Francis Crick"},
    {"id": "191", "context": CTX_23_DNA,
     "question": "Which base pairs with adenine in DNA?", "answer": "thymine"},
    {"id": "192", "context": CTX_23_DNA,
     "question": "Where is DNA found in eukaryotic cells?", "answer": "in the nucleus"},

    # Apollo 11
    {"id": "193", "context": CTX_24_APOLLO11,
     "question": "What was the name of the mission that achieved the first crewed Moon landing?", "answer": "Apollo 11"},
    {"id": "194", "context": CTX_24_APOLLO11,
     "question": "Which rocket launched Apollo 11?", "answer": "a Saturn V rocket"},
    {"id": "195", "context": CTX_24_APOLLO11,
     "question": "Who was the first person to step onto the Moon?", "answer": "Neil Armstrong"},
    {"id": "196", "context": CTX_24_APOLLO11,
     "question": "What was the name of the lunar module that landed on the Moon?", "answer": "Eagle"},

    # Bitcoin
    {"id": "197", "context": CTX_25_BITCOIN,
     "question": "In what year was Bitcoin introduced?", "answer": "2009"},
    {"id": "198", "context": CTX_25_BITCOIN,
     "question": "What is the pseudonym used by Bitcoin's creator?", "answer": "Satoshi Nakamoto"},
    {"id": "199", "context": CTX_25_BITCOIN,
     "question": "What is the public ledger that records Bitcoin transactions called?", "answer": "the blockchain"},
    {"id": "200", "context": CTX_25_BITCOIN,
     "question": "What is the maximum total supply of bitcoins?", "answer": "21 million coins"},

    # Leonardo da Vinci
    {"id": "201", "context": CTX_26_LEONARDO,
     "question": "In which year was Leonardo da Vinci born?", "answer": "1452"},
    {"id": "202", "context": CTX_26_LEONARDO,
     "question": "Name one city where Leonardo worked during his career.", "answer": "Florence"},
    {"id": "203", "context": CTX_26_LEONARDO,
     "question": "Give the title of one iconic artwork by Leonardo mentioned in the passage.", "answer": "the Mona Lisa"},
    {"id": "204", "context": CTX_26_LEONARDO,
     "question": "What do Leonardo's notebooks reveal about him?", "answer": "a restless curiosity about the natural world"},

    # Cell division
    {"id": "205", "context": CTX_27_CELL_DIV,
     "question": "Which type of cell division do somatic cells typically undergo?", "answer": "mitosis"},
    {"id": "206", "context": CTX_27_CELL_DIV,
     "question": "What form of cell division produces gametes?", "answer": "meiosis"},
    {"id": "207", "context": CTX_27_CELL_DIV,
     "question": "Why is proper regulation of cell division essential?", "answer": "for growth, tissue repair and development"},
    {"id": "208", "context": CTX_27_CELL_DIV,
     "question": "What can uncontrolled cell proliferation contribute to?", "answer": "the formation of tumors and cancer"},

    # World Health Organization
    {"id": "209", "context": CTX_28_WHO,
     "question": "What does WHO stand for?", "answer": "The World Health Organization"},
    {"id": "210", "context": CTX_28_WHO,
     "question": "In which city is the WHO headquartered?", "answer": "Geneva, Switzerland"},
    {"id": "211", "context": CTX_28_WHO,
     "question": "On what date was the World Health Organization established?", "answer": "7 April 1948"},
    {"id": "212", "context": CTX_28_WHO,
     "question": "Name one issue that WHO programs focus on according to the passage.", "answer": "vaccination"},

    # Silk Road
    {"id": "213", "context": CTX_29_SILK_ROAD,
     "question": "During which Chinese dynasty did the Silk Road emerge?", "answer": "the Han dynasty"},
    {"id": "214", "context": CTX_29_SILK_ROAD,
     "question": "Name one type of commodity transported along the Silk Road.", "answer": "silk"},
    {"id": "215", "context": CTX_29_SILK_ROAD,
     "question": "What were caravanserais used for?", "answer": "for rest and protection"},
    {"id": "216", "context": CTX_29_SILK_ROAD,
     "question": "Give the name of one city that became an important center of commerce on the Silk Road.", "answer": "Samarkand"},

    # Printing press
    {"id": "217", "context": CTX_30_PRINTING,
     "question": "With which inventor is the European movable-type printing press most closely associated?", "answer": "Johannes Gutenberg"},
    {"id": "218", "context": CTX_30_PRINTING,
     "question": "In which century did Gutenberg introduce his printing press?", "answer": "the fifteenth century"},
    {"id": "219", "context": CTX_30_PRINTING,
     "question": "Name one historical movement that benefited from printed materials.", "answer": "the Reformation"},
    {"id": "220", "context": CTX_30_PRINTING,
     "question": "What did Gutenberg's innovation dramatically reduce?", "answer": "the cost of producing books and pamphlets"},
]


# Edge cases

CTX_EDGE_LONG_1 = """At the very beginning of this passage lies the answer that some models might overlook: the word \
'Genesis'. This context is intentionally crafted so that the critical piece of information appears in the first few \
tokens. Beyond that initial word, the text continues in a fairly ordinary, encyclopedic manner. Genesis is also the name \
of the first book in the Hebrew Bible and the Christian Old Testament, and the term can refer more generally to an \
origin or mode of formation of something. Here, however, the question is designed so that only the very first occurrence \
at the start truly satisfies the requirement, even though similar references appear later in the paragraph."""

CTX_EDGE_MULTI_SPAN = """The city of Springfield appears in many fictional works, but there is also a real Springfield in \
several countries. In the United States alone, there is a Springfield in Illinois, another Springfield in Massachusetts \
and yet another Springfield in Missouri. Authors sometimes choose the name Springfield because it sounds generic and \
familiar to English speakers. When a question refers to 'Springfield' without further context, a reader must use clues \
from the surrounding text to decide which specific Springfield is most relevant."""

CTX_EDGE_LONG_ANSWER = """Urbanization refers to the process by which rural areas transform into cities characterized by \
dense populations and built environments. Historians and geographers have noted that, in many countries, this transformation \
is not sudden but occurs as the gradual transition from rural countryside to dense urban centers, often driven by economic \
opportunities and industrialization. Researchers study patterns of migration, changes in land use and shifting social \
structures to understand how urbanization reshapes societies and landscapes over time."""

CTX_EDGE_VERY_LONG = """This unusually long context is intended to test how well a system can handle passages that approach \
the upper bound of typical SQuAD-style inputs. It describes the history of a small but influential scientific society. \
Founded in the late nineteenth century by a group of amateur naturalists, the society initially focused on cataloging local \
plants and animals in a coastal region. Members met in borrowed classrooms and private homes, sharing handwritten notes and \
sketches of their observations. Over the decades, the scope of the society's work expanded. By the 1920s, it was organizing \
regular field expeditions and publishing a modest journal that documented species distributions, weather patterns and \
changes in coastal erosion. During the mid-twentieth century, as university-trained scientists became more involved, the \
society helped bridge the gap between professional research and community-based observation. It hosted public lectures, \
worked with schools and provided data to government agencies concerned with conservation. In recent years, advances in \
digital technology have transformed its activities once again. Volunteers now upload photographs and GPS coordinates to an \
online database, while researchers use statistical models to track long-term ecological trends. Despite these changes, the \
society remains committed to its original mission of encouraging curiosity about the natural world and making scientific \
knowledge accessible to the broader public."""

SQUAD_EDGE_CASES = [
    # Answer at beginning
    {"id": "edge_1", "context": CTX_EDGE_LONG_1,
     "question": "What single word at the very beginning of the passage is the answer?", "answer": "Genesis"},

    # Answer in the middle
    {"id": "edge_2",
     "context": "This short passage has its key information tucked into the middle, where the word nucleus appears "
                "among everyday terms. Many biological texts explain that the cell nucleus contains genetic material, "
                "but here the focus is simply on locating the word itself in a crowd of others.",
     "question": "Which word in the middle of the passage names the part of a cell that contains genetic material?",
     "answer": "nucleus"},

    # Answer at the end
    {"id": "edge_3",
     "context": "Some questions are crafted so that the answer lies near the very end of the paragraph. Readers may "
                "skim too quickly and miss a crucial final phrase. In this case, the passage talks generally about "
                "reading strategies, attention and memory. Only in the closing words does it reveal that the color "
                "most relevant to the question is deep blue.",
     "question": "What color is named at the very end of the passage?",
     "answer": "deep blue"},

    # Multiple possible spans, choose one
    {"id": "edge_4", "context": CTX_EDGE_MULTI_SPAN,
     "question": "According to the passage, name one U.S. state that has a city called Springfield.",
     "answer": "Illinois"},

    {"id": "edge_5", "context": CTX_EDGE_MULTI_SPAN,
     "question": "Name another U.S. state mentioned that also contains a city named Springfield.",
     "answer": "Massachusetts"},

    # Long answers
    {"id": "edge_6", "context": CTX_EDGE_LONG_ANSWER,
     "question": "How do historians describe the transformation associated with urbanization in many countries?",
     "answer": "the gradual transition from rural countryside to dense urban centers"},

    {"id": "edge_7", "context": CTX_EDGE_LONG_ANSWER,
     "question": "What phrase in the passage explains what drives this transition?",
     "answer": "driven by economic opportunities and industrialization"},

    # Numerical answers
    {"id": "edge_8",
     "context": "In this simple example, three numbers are listed in order: 7, 42 and 108. Only one of them will be "
                "requested by the question below, even though all are clearly visible.",
     "question": "Which number in the passage is exactly forty-two?",
     "answer": "42"},

    {"id": "edge_9",
     "context": "The conference was first held in 2015 and has taken place every year since. Organizers chose 2015 "
                "because it marked the tenth anniversary of the research group that sponsored the event.",
     "question": "In what year was the conference first held?",
     "answer": "2015"},

    {"id": "edge_10",
     "context": "Students sometimes memorize approximations such as 3.14 for the number pi, although more precise values "
                "are available. For everyday calculations, however, 3.14 is often sufficient.",
     "question": "What decimal approximation for pi is mentioned in the passage?",
     "answer": "3.14"},

    # Empty / very short contexts
    {"id": "edge_11",
     "context": "",
     "question": "This is an intentionally tricky item. What is the answer string, even though the context is empty?",
     "answer": "no answer in context"},

    {"id": "edge_12",
     "context": "Paris is the capital of France.",
     "question": "What is the capital of France?",
     "answer": "Paris"},

    {"id": "edge_13",
     "context": "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
     "question": "At standard atmospheric pressure, at what temperature does water boil in degrees Celsius?",
     "answer": "100"},

    # Very long context with multiple questions
    {"id": "edge_14", "context": CTX_EDGE_VERY_LONG,
     "question": "What type of people founded the scientific society described in the passage?",
     "answer": "a group of amateur naturalists"},

    {"id": "edge_15", "context": CTX_EDGE_VERY_LONG,
     "question": "In which decade did the society begin organizing regular field expeditions?",
     "answer": "the 1920s"},

    {"id": "edge_16", "context": CTX_EDGE_VERY_LONG,
     "question": "What kind of data do volunteers now upload to the society's online database?",
     "answer": "photographs and GPS coordinates"},

    {"id": "edge_17", "context": CTX_EDGE_VERY_LONG,
     "question": "What do researchers use to track long-term ecological trends according to the passage?",
     "answer": "statistical models"},

    {"id": "edge_18", "context": CTX_EDGE_VERY_LONG,
     "question": "What mission has the society remained committed to despite many changes?",
     "answer": "its original mission of encouraging curiosity about the natural world and making scientific knowledge accessible to the broader public"},

    # Another medium-long edge context
    {"id": "edge_19",
     "context": "This context is not quite as long but still longer than most short examples. It recounts the story of a "
                "small library that gradually digitized its catalog. At first, volunteers entered titles and authors into "
                "spreadsheets. Later, the library adopted an open-source cataloging system and scanned older card catalogs "
                "into image archives. Eventually, readers could search the entire collection from home. The key piece of "
                "information for the question is the phrase open-source cataloging system, which appears only once.",
     "question": "What type of system did the library adopt as it upgraded its catalog?",
     "answer": "an open-source cataloging system"},

    {"id": "edge_20",
     "context": "Here is a brief context that still counts as an edge case because the answer is a short phrase rather "
                "than a single word. The local park was renovated to include new walking paths, native plants and a small "
                "outdoor classroom for school groups.",
     "question": "According to the passage, what feature was added specifically for school groups?",
     "answer": "a small outdoor classroom"},
]


# Adversarial cases

CTX_ADV_1 = """The city of York in England has a long history dating back to Roman times, when it was known as Eboracum. \
Centuries later, English colonists founded a settlement in North America that they named New York in honor of the Duke \
of York. Today, New York City is one of the largest urban centers in the world, while the older city of York remains a \
much smaller historic town. When people say they are visiting York without any qualifier, they usually mean the English \
city, but when they say they are visiting New York they almost always refer to the American metropolis."""

CTX_ADV_2 = """Marie Curie conducted pioneering research on radioactivity in Paris, working closely with her husband, \
Pierre Curie. Their discoveries laid groundwork for later scientists, including Ernest Rutherford, who explored the \
structure of the atom, and Niels Bohr, who proposed a model of electron orbits. Although multiple researchers contributed \
to nuclear physics, only Marie Curie received two Nobel Prizes in different scientific fields. This detail can be easily \
confused with discussions of Rutherford's famous gold-foil experiment or Bohr's atomic model."""

CTX_ADV_3 = """On a particular mountain trek, three hikers set out from base camp at the same time. Alice walked at a \
steady pace of four kilometers per hour. Bruno moved more slowly, averaging three kilometers per hour, but he never took \
a break. Carla alternated between running at six kilometers per hour for half an hour and resting for half an hour. After \
two hours, Alice had covered eight kilometers and Bruno had covered six. Carla, however, had only been moving for one of \
those two hours, so she had traveled six kilometers. Thus, at the two hour mark, Alice was the farthest from base camp."""

CTX_ADV_4 = """The island nation of Zealandia is fictional, but it is often confused with real geographic names. There is a \
region called Zeeland in the Netherlands and an island country called New Zealand in the southwestern Pacific Ocean. New \
Zealand consists primarily of two large landmasses known as the North Island and the South Island. Although the term \
Zealandia has been used informally by some geologists to describe a largely submerged continental fragment, it is not a \
sovereign state. Readers must distinguish carefully between Zeeland, Zealandia and New Zealand when answering questions."""

CTX_ADV_5 = """Two major conferences on artificial intelligence were held in the same city during different years. The \
first took place in 2016 and focused on symbolic reasoning. The second occurred in 2019 and emphasized deep learning and \
large-scale neural networks. Both conferences were hosted in Montreal, Canada, and attracted researchers from around the \
world. When asked which year the deep learning conference occurred, one must remember that 2019, not 2016, was associated \
with that particular theme."""

SQUAD_ADVERSARIAL_CASES = [
    # Multi-step reasoning, similar entities
    {"id": "adv_1", "context": CTX_ADV_1,
     "question": "Which American city was named in honor of the Duke of York?", "answer": "New York City"},

    {"id": "adv_2", "context": CTX_ADV_1,
     "question": "When people say they are visiting York without any qualifier, which city do they usually mean?",
     "answer": "the English city"},

    # Nobel prizes, distractors
    {"id": "adv_3", "context": CTX_ADV_2,
     "question": "Which scientist mentioned in the passage received two Nobel Prizes in different scientific fields?",
     "answer": "Marie Curie"},

    {"id": "adv_4", "context": CTX_ADV_2,
     "question": "In which city did Marie Curie conduct her pioneering research on radioactivity?",
     "answer": "Paris"},

    # Numerical multi-step
    {"id": "adv_5", "context": CTX_ADV_3,
     "question": "After two hours on the trek, which hiker was farthest from base camp?",
     "answer": "Alice"},

    {"id": "adv_6", "context": CTX_ADV_3,
     "question": "How many kilometers had Bruno traveled after two hours?",
     "answer": "six"},

    # Similar names, subtle distinctions
    {"id": "adv_7", "context": CTX_ADV_4,
     "question": "What is the name of the real island country in the southwestern Pacific mentioned in the passage?",
     "answer": "New Zealand"},

    {"id": "adv_8", "context": CTX_ADV_4,
     "question": "Which Dutch region shares a similar name with Zealandia?",
     "answer": "Zeeland"},

    {"id": "adv_9", "context": CTX_ADV_4,
     "question": "What does the term Zealandia informally describe according to some geologists?",
     "answer": "a largely submerged continental fragment"},

    # Nearly unanswerable but answerable
    {"id": "adv_10",
     "context": "In a crowded paragraph full of dates and names, a single sentence quietly notes that the committee's "
                "final report was delivered just before dawn. Most readers remember the arguments and disagreements but "
                "forget that the report itself arrived at sunrise.",
     "question": "According to the passage, when was the committee's final report delivered?",
     "answer": "just before dawn"},

    {"id": "adv_11",
     "context": "The museum guide spoke at length about various painters, mentioning Caravaggio, Rembrandt and Vermeer. "
                "Only once did she briefly remark that her personal favorite painting in the entire collection was a small "
                "self-portrait by Rembrandt, tucked away in a side gallery.",
     "question": "Which artist created the guide's personal favorite painting in the collection?",
     "answer": "Rembrandt"},

    # Answer appears multiple times
    {"id": "adv_12",
     "context": "The password used in the early experiment was 'orchid', a word chosen because it was easy to remember. "
                "Later, when the team updated the system, they considered switching the password from 'orchid' to another "
                "flower name but never did so. As a result, even in the final report, the documented password remained "
                "orchid.",
     "question": "What flower name was used as the password?",
     "answer": "orchid"},

    # Subtle wording
    {"id": "adv_13",
     "context": "During the survey, respondents were asked whether they preferred tea, coffee or neither. A slight but "
                "important detail is that 'neither' was recorded separately from non-responses. The majority chose coffee, "
                "a smaller group selected tea and only a few explicitly answered 'neither'.",
     "question": "Which beverage did the majority of respondents prefer?",
     "answer": "coffee"},

    {"id": "adv_14",
     "context": "A small town organized two festivals each year: a spring music festival and an autumn food festival. "
                "Although both drew visitors, the food festival in autumn usually attracted more tourists than the music "
                "festival in spring, largely because it coincided with harvest season.",
     "question": "Which of the town's festivals usually attracted more tourists?",
     "answer": "the food festival in autumn"},

    # Distractor dates
    {"id": "adv_15", "context": CTX_ADV_5,
     "question": "In which year did the deep learning–focused conference take place?",
     "answer": "2019"},
]

SQUAD_ALL_TEST_CASES = SQUAD_STANDARD_CASES + SQUAD_EDGE_CASES + SQUAD_ADVERSARIAL_CASES
