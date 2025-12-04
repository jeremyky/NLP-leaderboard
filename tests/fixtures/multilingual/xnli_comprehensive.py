"""
Comprehensive test cases for XNLI - Cross-Lingual Natural Language Inference

Dataset: XNLI
Task: text_classification
Classes: entailment, contradiction, neutral
Domain: Multilingual NLI
Languages: en, es, fr, de, zh, ar, ru, hi, vi, th (10 languages)
Total Cases: Will be 300+ after you generate with ChatGPT (30+ per language)

---

INSTRUCTIONS:
1. Use the ChatGPT prompt below
2. Paste the generated cases organized by language
3. Verify each language has all 3 classes represented
4. Ensure culturally appropriate examples per language

---

CHATGPT PROMPT:

I need comprehensive test cases for XNLI (cross-lingual natural language inference: entailment, contradiction, neutral).

Current examples from the dataset:
{"id": "en_1", "question": "Premise: A man is playing a guitar. Hypothesis: A person is making music.", "answer": "entailment", "language": "en"}
{"id": "en_2", "question": "Premise: Two children are playing in a park. Hypothesis: The park is empty.", "answer": "contradiction", "language": "en"}
{"id": "es_1", "question": "Premisa: Un hombre está tocando una guitarra. Hipótesis: Una persona está haciendo música.", "answer": "entailment", "language": "es"}

Generate:

1. **300 standard examples** (30 per language, 10 of each class per language):
   - Languages: en, es, fr, de, zh, ar, ru, hi, vi, th
   - Each language gets: 10 entailment, 10 contradiction, 10 neutral
   - Culturally appropriate examples for each language
   - Varied complexity: simple (1 clause) to complex (3+ clauses)
   - Mix of topics: daily life, nature, work, culture, abstract concepts
   - IDs: "en_101", "en_102", ..., "es_101", "es_102", ..., "zh_101", etc.

2. **20 edge cases** (2 per language, distributed across 10 languages):
   - Empty premise/hypothesis
   - Single-word premise/hypothesis
   - Very long premise (100+ words)
   - Identical premise and hypothesis (should be entailment)
   - Premise: "X", Hypothesis: "not X" (should be contradiction)
   - IDs: "edge_en_1", "edge_es_1", "edge_fr_1", etc.

3. **15 adversarial cases** (tricky NLI examples across languages):
   - Subtle contradictions (one word difference)
   - Lexical overlap but different meanings
   - Negation: "nobody came" vs "someone came"
   - Quantifiers: "all" vs "some"
   - Temporal: "always" vs "sometimes"
   - IDs: "adv_en_1", "adv_es_1", "adv_fr_1", etc.

Output format:
```python
XNLI_STANDARD = [
    # English
    {"id": "en_101", "question": "Premise: ... Hypothesis: ...", "answer": "entailment", "language": "en"},
    # ... 29 more English
    
    # Spanish
    {"id": "es_101", "question": "Premisa: ... Hipótesis: ...", "answer": "entailment", "language": "es"},
    # ... 29 more Spanish
    
    # French
    {"id": "fr_101", "question": "Prémisse: ... Hypothèse: ...", "answer": "entailment", "language": "fr"},
    # ... continue for all 10 languages
]

XNLI_EDGE = [...]
XNLI_ADVERSARIAL = [...]
```

Requirements:
- Include language tag in ID prefix
- Include "language" field in each item
- For non-English: translate premise/hypothesis fully, keep structure
- Answer must be one of: "entailment", "contradiction", "neutral"
"""

# ============================================================================
# STANDARD CASES (300 examples, 30 per language)
# Paste ChatGPT output here
# ============================================================================
XNLI_STANDARD_CASES = [
    # English (en) -----------------------------------------------------------
    {"id": "en_101", "premise": "The conference starts at 9 a.m. tomorrow at the city hall.", "hypothesis": "The conference will be held at city hall.", "answer": "entailment", "language": "en"},
    {"id": "en_102", "premise": "Maria has never visited Japan in her life.", "hypothesis": "Maria travels to Japan every summer.", "answer": "contradiction", "language": "en"},
    {"id": "en_103", "premise": "The movie received mixed reviews from critics.", "hypothesis": "The movie was a huge box office success.", "answer": "neutral", "language": "en"},
    {"id": "en_104", "premise": "I left my keys on the kitchen table before going to work.", "hypothesis": "I left my keys in the kitchen.", "answer": "entailment", "language": "en"},
    {"id": "en_105", "premise": "The restaurant closes at 10 p.m. every night.", "hypothesis": "The restaurant stays open 24 hours a day.", "answer": "contradiction", "language": "en"},
    {"id": "en_106", "premise": "Lena bought a new laptop for her design work.", "hypothesis": "Lena's new laptop is made by Apple.", "answer": "neutral", "language": "en"},
    {"id": "en_107", "premise": "After months of training, he finally ran a marathon last Sunday.", "hypothesis": "He completed a marathon.", "answer": "entailment", "language": "en"},
    {"id": "en_108", "premise": "There was not a single cloud in the sky during the picnic.", "hypothesis": "Dark storm clouds covered the sky during the picnic.", "answer": "contradiction", "language": "en"},
    {"id": "en_109", "premise": "The teacher canceled class because of the snowstorm.", "hypothesis": "The students used the free time to study at home.", "answer": "neutral", "language": "en"},
    {"id": "en_110", "premise": "The bookstore is located next to the university library.", "hypothesis": "The bookstore is near the university.", "answer": "entailment", "language": "en"},
    {"id": "en_111", "premise": "No one in the team knew how to play the piano.", "hypothesis": "Several team members were skilled pianists.", "answer": "contradiction", "language": "en"},
    {"id": "en_112", "premise": "The company announced a new smartphone model today.", "hypothesis": "The new smartphone will be too expensive for most people.", "answer": "neutral", "language": "en"},
    {"id": "en_113", "premise": "She speaks both English and Spanish fluently.", "hypothesis": "She can speak Spanish.", "answer": "entailment", "language": "en"},
    {"id": "en_114", "premise": "The museum is open only on weekends.", "hypothesis": "The museum is closed on weekends.", "answer": "contradiction", "language": "en"},
    {"id": "en_115", "premise": "Tom cooked dinner for his friends last night.", "hypothesis": "Tom cooked pasta for his friends.", "answer": "neutral", "language": "en"},

    # Spanish (es) ----------------------------------------------------------
    {"id": "es_101", "premise": "Ayer por la tarde empezó a llover muy fuerte en la ciudad.", "hypothesis": "Ayer llovió en la ciudad por la tarde.", "answer": "entailment", "language": "es"},
    {"id": "es_102", "premise": "Ningún estudiante entregó la tarea a tiempo.", "hypothesis": "Todos los estudiantes entregaron la tarea a tiempo.", "answer": "contradiction", "language": "es"},
    {"id": "es_103", "premise": "Ana trabaja en una oficina cerca del centro.", "hypothesis": "Ana gana un salario muy alto.", "answer": "neutral", "language": "es"},
    {"id": "es_104", "premise": "El tren llegó a la estación con diez minutos de retraso.", "hypothesis": "El tren no llegó a tiempo.", "answer": "entailment", "language": "es"},
    {"id": "es_105", "premise": "Mi hermano es alérgico a los gatos.", "hypothesis": "Mi hermano tiene tres gatos en su casa.", "answer": "contradiction", "language": "es"},
    {"id": "es_106", "premise": "El supermercado abre todos los días a las ocho de la mañana.", "hypothesis": "El supermercado vende comida orgánica.", "answer": "neutral", "language": "es"},
    {"id": "es_107", "premise": "Después del examen, los estudiantes salieron a celebrar.", "hypothesis": "Los estudiantes celebraron después del examen.", "answer": "entailment", "language": "es"},
    {"id": "es_108", "premise": "La conferencia fue cancelada por falta de asistentes.", "hypothesis": "La conferencia tuvo una gran asistencia.", "answer": "contradiction", "language": "es"},
    {"id": "es_109", "premise": "Compré un libro nuevo sobre historia de América Latina.", "hypothesis": "El libro fue escrito por un autor chileno.", "answer": "neutral", "language": "es"},
    {"id": "es_110", "premise": "El restaurante está al lado del cine.", "hypothesis": "El restaurante está cerca del cine.", "answer": "entailment", "language": "es"},
    {"id": "es_111", "premise": "Nunca he estado en España.", "hypothesis": "Conozco muy bien las ciudades españolas porque las he visitado muchas veces.", "answer": "contradiction", "language": "es"},
    {"id": "es_112", "premise": "Laura se mudó a otra ciudad por trabajo.", "hypothesis": "Laura se mudó porque quería estar más cerca de su familia.", "answer": "neutral", "language": "es"},
    {"id": "es_113", "premise": "El niño se quedó dormido mientras veía la película.", "hypothesis": "El niño se durmió durante la película.", "answer": "entailment", "language": "es"},
    {"id": "es_114", "premise": "El banco solo abre de lunes a viernes.", "hypothesis": "El banco abre los domingos.", "answer": "contradiction", "language": "es"},
    {"id": "es_115", "premise": "Javier compró una bicicleta nueva.", "hypothesis": "Javier usa la bicicleta para ir al trabajo todos los días.", "answer": "neutral", "language": "es"},

    # French (fr) -----------------------------------------------------------
    {"id": "fr_101", "premise": "Ce matin, le métro était en retard à cause d'une panne.", "hypothesis": "Le métro n'est pas arrivé à l'heure ce matin.", "answer": "entailment", "language": "fr"},
    {"id": "fr_102", "premise": "Personne n'a posé de questions à la fin de la présentation.", "hypothesis": "Beaucoup de personnes ont posé des questions à la fin de la présentation.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_103", "premise": "Julie habite dans un petit appartement en centre-ville.", "hypothesis": "Julie vit avec trois colocataires.", "answer": "neutral", "language": "fr"},
    {"id": "fr_104", "premise": "Le musée est fermé le lundi.", "hypothesis": "On ne peut pas visiter le musée le lundi.", "answer": "entailment", "language": "fr"},
    {"id": "fr_105", "premise": "Paul ne boit jamais de café.", "hypothesis": "Paul commence chaque journée avec un grand café.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_106", "premise": "Ils ont acheté une voiture électrique la semaine dernière.", "hypothesis": "Ils ont reçu une réduction importante sur la voiture.", "answer": "neutral", "language": "fr"},
    {"id": "fr_107", "premise": "Il fait très froid dehors, il neige depuis ce matin.", "hypothesis": "La température extérieure est basse.", "answer": "entailment", "language": "fr"},
    {"id": "fr_108", "premise": "Le restaurant n'accepte que les paiements en espèces.", "hypothesis": "On peut payer par carte bancaire dans ce restaurant.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_109", "premise": "Sophie a terminé son travail plus tôt que prévu.", "hypothesis": "Sophie est la meilleure employée de son entreprise.", "answer": "neutral", "language": "fr"},
    {"id": "fr_110", "premise": "Le train pour Lyon part à 18 h 30.", "hypothesis": "Le train pour Lyon part en fin d'après-midi.", "answer": "entailment", "language": "fr"},
    {"id": "fr_111", "premise": "Tous les billets pour le concert ont été vendus.", "hypothesis": "Il reste encore beaucoup de billets pour le concert.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_112", "premise": "Marc étudie l'informatique à l'université.", "hypothesis": "Marc veut devenir professeur de mathématiques.", "answer": "neutral", "language": "fr"},
    {"id": "fr_113", "premise": "Elle a oublié son portefeuille à la maison.", "hypothesis": "Elle est sortie sans son portefeuille.", "answer": "entailment", "language": "fr"},
    {"id": "fr_114", "premise": "Le film dure moins d'une heure.", "hypothesis": "Le film dure plus de trois heures.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_115", "premise": "Ils ont déménagé dans une nouvelle maison à la campagne.", "hypothesis": "Leur nouvelle maison a une grande piscine.", "answer": "neutral", "language": "fr"},

    # German (de) -----------------------------------------------------------
    {"id": "de_101", "premise": "Heute Morgen gab es einen langen Stau auf der Autobahn.", "hypothesis": "Der Verkehr auf der Autobahn war heute Morgen stark beeinträchtigt.", "answer": "entailment", "language": "de"},
    {"id": "de_102", "premise": "Keiner der Gäste kam pünktlich zur Party.", "hypothesis": "Alle Gäste kamen rechtzeitig zur Party.", "answer": "contradiction", "language": "de"},
    {"id": "de_103", "premise": "Lisa arbeitet seit zwei Jahren in einer Bäckerei.", "hypothesis": "Lisa plant, bald nach Australien zu ziehen.", "answer": "neutral", "language": "de"},
    {"id": "de_104", "premise": "Der Supermarkt schließt immer um 22 Uhr.", "hypothesis": "Nach 22 Uhr hat der Supermarkt nicht mehr geöffnet.", "answer": "entailment", "language": "de"},
    {"id": "de_105", "premise": "Max ist Vegetarier und isst kein Fleisch.", "hypothesis": "Max isst jeden Tag ein Steak.", "answer": "contradiction", "language": "de"},
    {"id": "de_106", "premise": "Gestern hat es den ganzen Tag geregnet.", "hypothesis": "Heute wird es auch den ganzen Tag regnen.", "answer": "neutral", "language": "de"},
    {"id": "de_107", "premise": "Die Vorlesung findet jeden Dienstag im großen Hörsaal statt.", "hypothesis": "Die Vorlesung wird dienstags im großen Hörsaal gehalten.", "answer": "entailment", "language": "de"},
    {"id": "de_108", "premise": "Das Handy hat keinen Akku mehr.", "hypothesis": "Das Handy ist vollständig aufgeladen.", "answer": "contradiction", "language": "de"},
    {"id": "de_109", "premise": "Im Park spielen viele Kinder nach der Schule.", "hypothesis": "Im Park gibt es auch einen kleinen Teich.", "answer": "neutral", "language": "de"},
    {"id": "de_110", "premise": "Der Bahnhof liegt direkt neben dem Einkaufszentrum.", "hypothesis": "Das Einkaufszentrum ist in der Nähe des Bahnhofs.", "answer": "entailment", "language": "de"},
    {"id": "de_111", "premise": "Die Bibliothek ist heute geschlossen.", "hypothesis": "Man kann heute in der Bibliothek Bücher ausleihen.", "answer": "contradiction", "language": "de"},
    {"id": "de_112", "premise": "Jonas hat gestern ein neues Fahrrad gekauft.", "hypothesis": "Jonas hat sein altes Fahrrad an seinen Bruder verschenkt.", "answer": "neutral", "language": "de"},
    {"id": "de_113", "premise": "Sie hat die Prüfung im zweiten Versuch bestanden.", "hypothesis": "Sie hat die Prüfung nicht beim ersten Versuch bestanden.", "answer": "entailment", "language": "de"},
    {"id": "de_114", "premise": "Im Klassenzimmer war es völlig still.", "hypothesis": "Die Schüler machten die ganze Zeit Lärm.", "answer": "contradiction", "language": "de"},
    {"id": "de_115", "premise": "Die Firma eröffnet eine neue Filiale in Berlin.", "hypothesis": "Die neue Filiale wird besonders viele junge Kunden anziehen.", "answer": "neutral", "language": "de"},

    # Chinese (zh) ----------------------------------------------------------
    {"id": "zh_101", "premise": "昨天晚上下了一整夜的雨。", "hypothesis": "昨天晚上一直在下雨。", "answer": "entailment", "language": "zh"},
    {"id": "zh_102", "premise": "他从来没有坐过飞机。", "hypothesis": "他每个月都要坐飞机出差。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_103", "premise": "她在一家互联网公司上班。", "hypothesis": "她在公司负责市场部门。", "answer": "neutral", "language": "zh"},
    {"id": "zh_104", "premise": "图书馆星期天不开门。", "hypothesis": "星期天不能去图书馆借书。", "answer": "entailment", "language": "zh"},
    {"id": "zh_105", "premise": "今天的考试非常简单，几乎没有人不及格。", "hypothesis": "今天大部分学生都没通过考试。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_106", "premise": "我昨天买了一部新手机。", "hypothesis": "这部手机是打折的时候买的。", "answer": "neutral", "language": "zh"},
    {"id": "zh_107", "premise": "会议推迟到了下午三点开始。", "hypothesis": "会议不会在上午开始。", "answer": "entailment", "language": "zh"},
    {"id": "zh_108", "premise": "这家餐厅只卖素食，不提供肉类。", "hypothesis": "这家餐厅以牛排最有名。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_109", "premise": "他每天早上六点起床。", "hypothesis": "他每天早上都会去跑步。", "answer": "neutral", "language": "zh"},
    {"id": "zh_110", "premise": "火车站就在学校旁边，走路五分钟就到。", "hypothesis": "从学校走路很快就能到火车站。", "answer": "entailment", "language": "zh"},
    {"id": "zh_111", "premise": "这个房间里一个人也没有。", "hypothesis": "房间里坐满了人。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_112", "premise": "他们打算下个月去旅游。", "hypothesis": "他们要去日本旅游。", "answer": "neutral", "language": "zh"},
    {"id": "zh_113", "premise": "她已经在北京住了十年。", "hypothesis": "她在北京生活了很长时间。", "answer": "entailment", "language": "zh"},
    {"id": "zh_114", "premise": "今天是周一，我们刚开始上班。", "hypothesis": "今天是周末，大家都在家休息。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_115", "premise": "我在网上订了一张演唱会的票。", "hypothesis": "那场演唱会是在周五晚上举行的。", "answer": "neutral", "language": "zh"},

    # Arabic (ar) -----------------------------------------------------------
    {"id": "ar_101", "premise": "هطلت الأمطار طوال الليل في المدينة.", "hypothesis": "كان الجو ماطرًا في المدينة ليلًا.", "answer": "entailment", "language": "ar"},
    {"id": "ar_102", "premise": "لم يحضر أي طالب إلى المحاضرة اليوم.", "hypothesis": "حضر جميع الطلاب إلى المحاضرة اليوم.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_103", "premise": "تعمل سارة في بنك قريب من بيتها.", "hypothesis": "سارة مديرة الفرع الرئيسي للبنك.", "answer": "neutral", "language": "ar"},
    {"id": "ar_104", "premise": "تغلق المكتبة أبوابها عند الساعة الثامنة مساءً.", "hypothesis": "بعد الثامنة مساءً تكون المكتبة مغلقة.", "answer": "entailment", "language": "ar"},
    {"id": "ar_105", "premise": "أحمد لا يجيد التحدث بالإنجليزية.", "hypothesis": "أحمد يتحدث الإنجليزية بطلاقة.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_106", "premise": "انتقلوا إلى شقة جديدة الأسبوع الماضي.", "hypothesis": "الشقة الجديدة تقع في الطابق العاشر.", "answer": "neutral", "language": "ar"},
    {"id": "ar_107", "premise": "تعمل الحافلات كل عشر دقائق في الصباح.", "hypothesis": "في الصباح تكون الحافلات متكررة.", "answer": "entailment", "language": "ar"},
    {"id": "ar_108", "premise": "المطعم لا يقدّم أي أطباق حارة.", "hypothesis": "جميع أطباق المطعم حارة جدًا.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_109", "premise": "يقرأ خالد كثيرًا عن التاريخ الإسلامي.", "hypothesis": "خالد يخطط لكتابة كتاب عن التاريخ.", "answer": "neutral", "language": "ar"},
    {"id": "ar_110", "premise": "يقع الفندق بجانب محطة القطار مباشرةً.", "hypothesis": "الفندق قريب من محطة القطار.", "answer": "entailment", "language": "ar"},
    {"id": "ar_111", "premise": "الرحلة أُلغيت بسبب سوء الأحوال الجوية.", "hypothesis": "الرحلة أقلعت في الوقت المحدد دون أي مشاكل.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_112", "premise": "درست هندسة الحاسوب في الجامعة.", "hypothesis": "تعمل الآن في شركة برمجة كبيرة.", "answer": "neutral", "language": "ar"},
    {"id": "ar_113", "premise": "وصلت الرسالة إلى بريدك الإلكتروني صباح اليوم.", "hypothesis": "استلمت رسالة إلكترونية هذا الصباح.", "answer": "entailment", "language": "ar"},
    {"id": "ar_114", "premise": "لم يفُز الفريق بأي مباراة هذا الموسم.", "hypothesis": "حقق الفريق عدة انتصارات هذا الموسم.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_115", "premise": "اشترى والدي سيارة جديدة الأسبوع الماضي.", "hypothesis": "السيارة الجديدة من نوع ياباني.", "answer": "neutral", "language": "ar"},

    # Russian (ru) ----------------------------------------------------------
    {"id": "ru_101", "premise": "Вчера весь день шёл сильный дождь.", "hypothesis": "Вчера погода была дождливой.", "answer": "entailment", "language": "ru"},
    {"id": "ru_102", "premise": "Ни один сотрудник не пришёл вовремя.", "hypothesis": "Все сотрудники пришли на работу вовремя.", "answer": "contradiction", "language": "ru"},
    {"id": "ru_103", "premise": "Ольга работает врачом в городской больнице.", "hypothesis": "Ольга собирается уехать работать за границу.", "answer": "neutral", "language": "ru"},
    {"id": "ru_104", "premise": "Магазин закрывается в десять часов вечера.", "hypothesis": "После десяти вечера магазин не работает.", "answer": "entailment", "language": "ru"},
    {"id": "ru_105", "premise": "У Андрея нет детей.", "hypothesis": "У Андрея трое маленьких детей.", "answer": "contradiction", "language": "ru"},
    {"id": "ru_106", "premise": "Мы заказали пиццу на ужин.", "hypothesis": "Мы съели всю пиццу за десять минут.", "answer": "neutral", "language": "ru"},
    {"id": "ru_107", "premise": "Поезд прибыл на станцию раньше расписания.", "hypothesis": "Поезд приехал раньше, чем ожидалось.", "answer": "entailment", "language": "ru"},
    {"id": "ru_108", "premise": "В комнате было совершенно тихо.", "hypothesis": "В комнате стоял громкий шум.", "answer": "contradiction", "language": "ru"},
    {"id": "ru_109", "premise": "Он читает много книг по философии.", "hypothesis": "Он пишет диссертацию по философии.", "answer": "neutral", "language": "ru"},
    {"id": "ru_110", "premise": "Кафе находится напротив университета.", "hypothesis": "Кафе рядом с университетом.", "answer": "entailment", "language": "ru"},
    {"id": "ru_111", "premise": "Сегодня пятница, и завтра нам на работу.", "hypothesis": "Сегодня воскресенье, и завтра выходной.", "answer": "contradiction", "language": "ru"},
    {"id": "ru_112", "premise": "Она купила новый телефон вчера.", "hypothesis": "Она купила телефон со скидкой в двадцать процентов.", "answer": "neutral", "language": "ru"},
    {"id": "ru_113", "premise": "Иван свободно говорит по-английски и по-немецки.", "hypothesis": "Иван умеет говорить по-немецки.", "answer": "entailment", "language": "ru"},
    {"id": "ru_114", "premise": "На полке не осталось ни одной книги.", "hypothesis": "Полка полностью заставлена книгами.", "answer": "contradiction", "language": "ru"},
    {"id": "ru_115", "premise": "Мы переехали в другой район города.", "hypothesis": "В новом районе есть большой парк.", "answer": "neutral", "language": "ru"},

    # Hindi (hi) ------------------------------------------------------------
    {"id": "hi_101", "premise": "कल रात पूरे शहर में तेज बारिश हुई।", "hypothesis": "कल रात शहर में बहुत बारिश हुई थी।", "answer": "entailment", "language": "hi"},
    {"id": "hi_102", "premise": "किसी भी छात्र ने परीक्षा पास नहीं की।", "hypothesis": "सभी छात्रों ने परीक्षा आसानी से पास कर ली।", "answer": "contradiction", "language": "hi"},
    {"id": "hi_103", "premise": "रीना एक निजी कंपनी में काम करती है।", "hypothesis": "रीना कंपनी की मालिक है।", "answer": "neutral", "language": "hi"},
    {"id": "hi_104", "premise": "दुकान रोज़ाना शाम नौ बजे बंद हो जाती है।", "hypothesis": "रात नौ बजे के बाद दुकान खुली नहीं रहती।", "answer": "entailment", "language": "hi"},
    {"id": "hi_105", "premise": "मुझे दूध से एलर्जी है।", "hypothesis": "मैं रोज़ सुबह दूध का बड़ा गिलास पीता हूँ।", "answer": "contradiction", "language": "hi"},
    {"id": "hi_106", "premise": "हम पिछले महीने नए घर में शिफ्ट हुए।", "hypothesis": "नया घर तीसरी मंज़िल पर है।", "answer": "neutral", "language": "hi"},
    {"id": "hi_107", "premise": "ट्रेन अपने निर्धारित समय से बीस मिनट देर से पहुँची।", "hypothesis": "ट्रेन समय पर नहीं पहुँची।", "answer": "entailment", "language": "hi"},
    {"id": "hi_108", "premise": "कक्षा में बिलकुल शांति थी।", "hypothesis": "कक्षा में बच्चे ज़ोर-ज़ोर से बातें कर रहे थे।", "answer": "contradiction", "language": "hi"},
    {"id": "hi_109", "premise": "वह रोज़ सुबह सैर पर जाता है।", "hypothesis": "वह सुबह सैर के बाद चाय पीता है।", "answer": "neutral", "language": "hi"},
    {"id": "hi_110", "premise": "कॉलेज के सामने वाली सड़क पर एक बड़ा अस्पताल है।", "hypothesis": "अस्पताल कॉलेज के पास स्थित है।", "answer": "entailment", "language": "hi"},
    {"id": "hi_111", "premise": "आज मेरा कोई भी दोस्त स्कूल नहीं आया।", "hypothesis": "आज मेरे सारे दोस्त स्कूल आए थे।", "answer": "contradiction", "language": "hi"},
    {"id": "hi_112", "premise": "कल रात हमने एक नई फ़िल्म देखी।", "hypothesis": "फ़िल्म को कई पुरस्कार मिले हैं।", "answer": "neutral", "language": "hi"},
    {"id": "hi_113", "premise": "उसने दो साल पहले गिटार सीखना शुरू किया था।", "hypothesis": "वह दो साल से गिटार सीख रहा है।", "answer": "entailment", "language": "hi"},
    {"id": "hi_114", "premise": "यह बस सीधे रेलवे स्टेशन जाती है।", "hypothesis": "यह बस बिल्कुल भी स्टेशन नहीं जाती।", "answer": "contradiction", "language": "hi"},
    {"id": "hi_115", "premise": "मैंने बाज़ार से कुछ सब्ज़ियाँ खरीदीं।", "hypothesis": "मैंने आज बाज़ार से फल नहीं खरीदे।", "answer": "neutral", "language": "hi"},

    # Vietnamese (vi) -------------------------------------------------------
    {"id": "vi_101", "premise": "Tối qua trời mưa rất to ở Hà Nội.", "hypothesis": "Tối qua Hà Nội có mưa lớn.", "answer": "entailment", "language": "vi"},
    {"id": "vi_102", "premise": "Không có sinh viên nào làm bài tập về nhà.", "hypothesis": "Tất cả sinh viên đều nộp bài tập đầy đủ.", "answer": "contradiction", "language": "vi"},
    {"id": "vi_103", "premise": "Lan làm việc tại một công ty phần mềm.", "hypothesis": "Lan là giám đốc của công ty đó.", "answer": "neutral", "language": "vi"},
    {"id": "vi_104", "premise": "Siêu thị mở cửa từ 8 giờ sáng đến 10 giờ tối.", "hypothesis": "Sau 10 giờ tối siêu thị đóng cửa.", "answer": "entailment", "language": "vi"},
    {"id": "vi_105", "premise": "Anh ấy không biết lái xe ô tô.", "hypothesis": "Anh ấy lái ô tô đi làm mỗi ngày.", "answer": "contradiction", "language": "vi"},
    {"id": "vi_106", "premise": "Tuần trước tôi mua một chiếc điện thoại mới.", "hypothesis": "Chiếc điện thoại đó được sản xuất ở Hàn Quốc.", "answer": "neutral", "language": "vi"},
    {"id": "vi_107", "premise": "Buổi họp được dời sang chiều mai.", "hypothesis": "Buổi họp sẽ không diễn ra vào sáng mai.", "answer": "entailment", "language": "vi"},
    {"id": "vi_108", "premise": "Quán cà phê này lúc nào cũng rất yên tĩnh.", "hypothesis": "Quán cà phê này lúc nào cũng đông và ồn ào.", "answer": "contradiction", "language": "vi"},
    {"id": "vi_109", "premise": "Nam thường chạy bộ vào buổi sáng.", "hypothesis": "Nam thường chạy bộ cùng em trai.", "answer": "neutral", "language": "vi"},
    {"id": "vi_110", "premise": "Trường học nằm ngay cạnh bưu điện.", "hypothesis": "Trường học ở gần bưu điện.", "answer": "entailment", "language": "vi"},
    {"id": "vi_111", "premise": "Hôm nay là chủ nhật nên chúng tôi không phải đi làm.", "hypothesis": "Hôm nay là ngày làm việc bình thường.", "answer": "contradiction", "language": "vi"},
    {"id": "vi_112", "premise": "Tối qua cả gia đình ăn cơm ở nhà.", "hypothesis": "Bữa tối có món cá kho.", "answer": "neutral", "language": "vi"},
    {"id": "vi_113", "premise": "Cô ấy đã sống ở Thành phố Hồ Chí Minh được năm năm.", "hypothesis": "Cô ấy đã ở Thành phố Hồ Chí Minh nhiều năm.", "answer": "entailment", "language": "vi"},
    {"id": "vi_114", "premise": "Trong tủ lạnh không còn đồ ăn nữa.", "hypothesis": "Tủ lạnh vẫn còn rất nhiều thức ăn.", "answer": "contradiction", "language": "vi"},
    {"id": "vi_115", "premise": "Tôi đăng ký một khóa học tiếng Nhật online.", "hypothesis": "Khóa học kéo dài sáu tháng.", "answer": "neutral", "language": "vi"},

    # Thai (th) -------------------------------------------------------------
    {"id": "th_101", "premise": "เมื่อคืนฝนตกหนักตลอดทั้งคืน.", "hypothesis": "เมื่อคืนอากาศฝนตกทั้งคืน.", "answer": "entailment", "language": "th"},
    {"id": "th_102", "premise": "ไม่มีนักเรียนคนใดมาสายวันนี้.", "hypothesis": "นักเรียนทุกคนมาสายวันนี้.", "answer": "contradiction", "language": "th"},
    {"id": "th_103", "premise": "พิมพ์ทำงานอยู่ที่บริษัทเอกชนแห่งหนึ่ง.", "hypothesis": "พิมพ์เป็นเจ้าของบริษัทนั้น.", "answer": "neutral", "language": "th"},
    {"id": "th_104", "premise": "ห้องสมุดปิดตอนสองทุ่มทุกวัน.", "hypothesis": "หลังสองทุ่มไม่สามารถเข้าใช้ห้องสมุดได้.", "answer": "entailment", "language": "th"},
    {"id": "th_105", "premise": "เขาไม่กินเนื้อสัตว์เลย.", "hypothesis": "เขาชอบกินสเต็กเป็นประจำ.", "answer": "contradiction", "language": "th"},
    {"id": "th_106", "premise": "เมื่อวานฉันซื้อโทรศัพท์เครื่องใหม่.", "hypothesis": "โทรศัพท์เครื่องใหม่นี้เป็นสีดำ.", "answer": "neutral", "language": "th"},
    {"id": "th_107", "premise": "รถไฟออกจากสถานีตอนหกโมงเช้า.", "hypothesis": "รถไฟออกตอนเช้า.", "answer": "entailment", "language": "th"},
    {"id": "th_108", "premise": "ในห้องประชุมเงียบมาก.", "hypothesis": "ในห้องประชุมเสียงดังตลอดเวลา.", "answer": "contradiction", "language": "th"},
    {"id": "th_109", "premise": "หลังเลิกงานเขามักจะไปออกกำลังกาย.", "hypothesis": "เขาไปออกกำลังกายกับเพื่อนร่วมงาน.", "answer": "neutral", "language": "th"},
    {"id": "th_110", "premise": "โรงแรมอยู่ใกล้สนามบินมาก ขับรถแค่ห้านาที.", "hypothesis": "โรงแรมอยู่ไม่ไกลจากสนามบิน.", "answer": "entailment", "language": "th"},
    {"id": "th_111", "premise": "วันนี้เป็นวันหยุดราชการ ทุกคนหยุดงาน.", "hypothesis": "วันนี้ทุกคนต้องไปทำงานตามปกติ.", "answer": "contradiction", "language": "th"},
    {"id": "th_112", "premise": "พวกเขาย้ายบ้านไปอยู่ต่างจังหวัด.", "hypothesis": "บ้านใหม่ของพวกเขาอยู่ติดทะเล.", "answer": "neutral", "language": "th"},
    {"id": "th_113", "premise": "เธอเรียนภาษาจีนมาสามปีแล้ว.", "hypothesis": "เธอเรียนภาษาจีนนานหลายปี.", "answer": "entailment", "language": "th"},
    {"id": "th_114", "premise": "ในตู้เย็นไม่มีอาหารเหลือเลย.", "hypothesis": "ตู้เย็นเต็มไปด้วยอาหาร.", "answer": "contradiction", "language": "th"},
    {"id": "th_115", "premise": "เมื่อเช้าฉันดื่มกาแฟหนึ่งแก้ว.", "hypothesis": "กาแฟที่ฉันดื่มใส่นมเยอะมาก.", "answer": "neutral", "language": "th"},
]

XNLI_EDGE_CASES = [
    # Very short / minimal context, numerical & temporal, code-switching, etc.
    {"id": "en_edge_1", "premise": "Too late.", "hypothesis": "It is not early anymore.", "answer": "entailment", "language": "en"},
    {"id": "en_edge_2", "premise": "The match was canceled.", "hypothesis": "They did not play.", "answer": "entailment", "language": "en"},
    {"id": "en_edge_3", "premise": "There are exactly three apples on the table.", "hypothesis": "There are at least two apples on the table.", "answer": "entailment", "language": "en"},
    {"id": "en_edge_4", "premise": "The class has 20 students.", "hypothesis": "The class has 35 students.", "answer": "contradiction", "language": "en"},
    {"id": "en_edge_5", "premise": "The store will close in five minutes.", "hypothesis": "The store stays open for another hour.", "answer": "contradiction", "language": "en"},
    {"id": "en_edge_6", "premise": "John can lift 100 kilograms.", "hypothesis": "John is a professional weightlifter.", "answer": "neutral", "language": "en"},
    {"id": "en_edge_7", "premise": "She resigned from her job last week.", "hypothesis": "She quit her position at work a week ago.", "answer": "entailment", "language": "en"},

    {"id": "es_edge_1", "premise": "Ayer tuve una reunión con mi boss en la oficina.", "hypothesis": "Ayer me reuní con mi jefe en el trabajo.", "answer": "entailment", "language": "es"},
    {"id": "es_edge_2", "premise": "Mañana tengo un examen muy difícil de math.", "hypothesis": "Mañana tengo un examen fácil.", "answer": "contradiction", "language": "es"},

    {"id": "fr_edge_1", "premise": "Je vais au travail en métro tous les jours, sauf le week-end.", "hypothesis": "Je ne prends jamais le métro pour aller au travail.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_edge_2", "premise": "Trop tard.", "hypothesis": "Il n'est plus tôt.", "answer": "entailment", "language": "fr"},

    {"id": "de_edge_1", "premise": "Im Raum sitzen mindestens fünf Personen.", "hypothesis": "Im Raum sitzen genau zwei Personen.", "answer": "contradiction", "language": "de"},
    {"id": "de_edge_2", "premise": "Morgen früh um acht Uhr beginnt das Meeting.", "hypothesis": "Das Meeting beginnt morgen Nachmittag.", "answer": "contradiction", "language": "de"},

    {"id": "zh_edge_1", "premise": "已经开始了。", "hypothesis": "现在还没开始。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_edge_2", "premise": "我昨天跟manager开了一个很长的会。", "hypothesis": "我昨天和经理开了会。", "answer": "entailment", "language": "zh"},

    {"id": "ar_edge_1", "premise": "سيصل متأخرًا قليلًا.", "hypothesis": "لن يأتي اليوم أبدًا.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_edge_2", "premise": "لديه سيارة قديمة.", "hypothesis": "سيارته تحتاج إلى إصلاح كبير.", "answer": "neutral", "language": "ar"},

    {"id": "ru_edge_1", "premise": "Поезд прибудет через десять минут.", "hypothesis": "Поезд прибудет через час.", "answer": "contradiction", "language": "ru"},
    {"id": "ru_edge_2", "premise": "Она работает дома по удалёнке.", "hypothesis": "Она делает свою работу из дома.", "answer": "entailment", "language": "ru"},

    {"id": "hi_edge_1", "premise": "बहुत देर हो गई।", "hypothesis": "अब जल्दी नहीं है।", "answer": "entailment", "language": "hi"},
    {"id": "hi_edge_2", "premise": "कक्षा में पाँच छात्र बैठे हैं।", "hypothesis": "कक्षा में दस से कम छात्र हैं।", "answer": "entailment", "language": "hi"},

    {"id": "vi_edge_1", "premise": "Hôm nay mình phải làm presentation cho lớp.", "hypothesis": "Hôm nay mình thuyết trình trước lớp.", "answer": "entailment", "language": "vi"},
    {"id": "vi_edge_2", "premise": "Tối mai lúc 7 giờ chúng ta gặp nhau.", "hypothesis": "Chúng ta sẽ gặp nhau sáng mai.", "answer": "contradiction", "language": "vi"},

    {"id": "th_edge_1", "premise": "ยังไม่เริ่ม.", "hypothesis": "ตอนนี้กิจกรรมเริ่มแล้ว.", "answer": "contradiction", "language": "th"},
    {"id": "th_edge_2", "premise": "เมื่อวานเขาซื้อหนังสือเล่มหนึ่ง.", "hypothesis": "หนังสือเล่มนั้นเป็นนวนิยายรัก.", "answer": "neutral", "language": "th"},
]

XNLI_ADVERSARIAL_CASES = [
    # English adversarials --------------------------------------------------
    {"id": "en_adv_1", "premise": "Most students passed the exam, but John failed.", "hypothesis": "John passed the exam.", "answer": "contradiction", "language": "en"},
    {"id": "en_adv_2", "premise": "The restaurant is not unpopular; it gets busy every weekend.", "hypothesis": "The restaurant is unpopular.", "answer": "contradiction", "language": "en"},
    {"id": "en_adv_3", "premise": "Everyone except Maria signed the attendance sheet.", "hypothesis": "Maria signed the attendance sheet.", "answer": "contradiction", "language": "en"},
    {"id": "en_adv_4", "premise": "John is a doctor.", "hypothesis": "John is a pediatric surgeon.", "answer": "neutral", "language": "en"},
    {"id": "en_adv_5", "premise": "Emma called Olivia after the meeting to discuss the project.", "hypothesis": "Olivia called Emma after the meeting to discuss the project.", "answer": "neutral", "language": "en"},
    {"id": "en_adv_6", "premise": "Diwali is celebrated in many parts of India every year with lights and fireworks.", "hypothesis": "Diwali is an important festival in Indian culture.", "answer": "entailment", "language": "en"},

    # Spanish adversarials --------------------------------------------------
    {"id": "es_adv_1", "premise": "Durante el Ramadán, muchas personas musulmanas ayunan desde el amanecer hasta el anochecer.", "hypothesis": "Durante el Ramadán, las personas musulmanas no comen ni beben mientras hay sol.", "answer": "entailment", "language": "es"},
    {"id": "es_adv_2", "premise": "La película no fue nada mala; al público le encantó.", "hypothesis": "La película fue mala.", "answer": "contradiction", "language": "es"},

    # French adversarials ---------------------------------------------------
    {"id": "fr_adv_1", "premise": "Tous les étudiants, sauf Pierre, ont rendu leur devoir.", "hypothesis": "Pierre a rendu son devoir.", "answer": "contradiction", "language": "fr"},
    {"id": "fr_adv_2", "premise": "Marie habite à Paris.", "hypothesis": "Marie habite dans le 5ᵉ arrondissement de Paris.", "answer": "neutral", "language": "fr"},

    # German adversarials ---------------------------------------------------
    {"id": "de_adv_1", "premise": "Nach dem Unterricht bekam nur Lara das Buch von Anna.", "hypothesis": "Nach dem Unterricht bekam Anna das Buch von Lara.", "answer": "contradiction", "language": "de"},
    {"id": "de_adv_2", "premise": "Er ist keineswegs unerfahren, er arbeitet seit zehn Jahren als Ingenieur.", "hypothesis": "Er ist unerfahren.", "answer": "contradiction", "language": "de"},

    # Chinese adversarials --------------------------------------------------
    {"id": "zh_adv_1", "premise": "除了王明以外，所有同学都参加了比赛。", "hypothesis": "王明参加了比赛。", "answer": "contradiction", "language": "zh"},
    {"id": "zh_adv_2", "premise": "她在一家医院工作。", "hypothesis": "她在一家儿童医院当儿科医生。", "answer": "neutral", "language": "zh"},

    # Arabic adversarials ---------------------------------------------------
    {"id": "ar_adv_1", "premise": "هو ليس غير مهتم بالموضوع، بل يقرأ عنه كثيرًا.", "hypothesis": "هو غير مهتم بالموضوع.", "answer": "contradiction", "language": "ar"},
    {"id": "ar_adv_2", "premise": "بعد انتهاء الدرس، أعطت ليلى الكتاب لهدى.", "hypothesis": "بعد انتهاء الدرس، أعطت هدى الكتاب لليلى.", "answer": "contradiction", "language": "ar"},

    # Russian adversarial ---------------------------------------------------
    {"id": "ru_adv_1", "premise": "На Новый год в России люди обычно дарят друг другу подарки.", "hypothesis": "В России на Новый год принято обмениваться подарками.", "answer": "entailment", "language": "ru"},

    # Hindi adversarial -----------------------------------------------------
    {"id": "hi_adv_1", "premise": "यह विचार बिल्कुल बुरा नहीं है, कई लोग इसे पसंद करते हैं।", "hypothesis": "यह विचार बुरा है।", "answer": "contradiction", "language": "hi"},

    # Vietnamese adversarial ------------------------------------------------
    {"id": "vi_adv_1", "premise": "Minh làm việc ở một công ty công nghệ tại Sài Gòn.", "hypothesis": "Minh là trưởng phòng kỹ thuật ở một công ty công nghệ tại Sài Gòn.", "answer": "neutral", "language": "vi"},

    # Thai adversarial ------------------------------------------------------
    {"id": "th_adv_1", "premise": "ทุกคนยกเว้นนัทมาประชุมตรงเวลา.", "hypothesis": "นัทมาประชุมตรงเวลา.", "answer": "contradiction", "language": "th"},
]

XNLI_ALL_TEST_CASES = XNLI_STANDARD_CASES + XNLI_EDGE_CASES + XNLI_ADVERSARIAL_CASES