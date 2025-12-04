"""
Comprehensive test cases for SST-2 - Sentiment Analysis

Dataset: SST-2 (Stanford Sentiment Treebank)
Task: text_classification
Classes: positive, negative (binary)
Total Cases: Will be 150+ after you generate with ChatGPT

---

INSTRUCTIONS:
1. Use the ChatGPT prompt below
2. Paste the generated cases in the appropriate sections
3. Verify label balance (roughly 50-50 positive/negative)
4. Update ALL_TEST_CASES at the bottom

---

CHATGPT PROMPT:

I need comprehensive test cases for SST-2 (binary sentiment classification: positive, negative).

Current examples from the dataset:
{"id": "1", "question": "a masterpiece four years in the making", "answer": "positive"}
{"id": "2", "question": "everything is off about this film", "answer": "negative"}
{"id": "3", "question": "a gorgeous , witty , seductive movie", "answer": "positive"}

Generate:
1. **150 standard examples** (75 positive, 75 negative):
   - Movie review snippets (phrases and short sentences)
   - Mix of vocabulary: simple and sophisticated
   - Varied intensity: mildly positive to extremely positive, slightly negative to harshly negative
   - Different aspects: acting, plot, direction, cinematography, soundtrack
   - Sequential IDs: "101", "102", ..., "250"

2. **20 edge cases**:
   - Empty review (ID: "edge_1")
   - Single word: "brilliant" (ID: "edge_2")
   - Single word: "awful" (ID: "edge_3")
   - Very long review 200+ words (ID: "edge_4")
   - All punctuation: "!!!" (ID: "edge_5")
   - Numbers only: "10/10" vs "1/10" (ID: "edge_6", "edge_7")
   - Mixed case: "GrEaT MoViE" (ID: "edge_8")
   - Sarcasm markers: "oh great, another sequel" (ID: "edge_9" - "edge_20")

3. **15 adversarial cases**:
   - Negations: "not bad", "wasn't terrible", "hardly disappointing" (ID: "adv_1" - "adv_5")
   - Backhanded compliments: "it's good... for a low-budget film" (ID: "adv_6")
   - Mixed sentiment: "great acting but terrible plot" (ID: "adv_7" - "adv_10")
   - Subtle sarcasm: "oh wonderful, another CGI fest" (ID: "adv_11" - "adv_15")

Output as three Python lists with format:
{"id": "...", "question": "review text", "answer": "positive" or "negative"}
"""

# ============================================================================
# STANDARD CASES (150 examples, 75 positive + 75 negative)
# Paste ChatGPT output here
# ============================================================================
SST2_STANDARD_CASES = [
    {"id": "101", "question": "A moving, confident film that balances humor and heart with ease. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "102", "question": "This movie is funny and surprisingly sincere, that reminds you why you love going to the movies. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "103", "question": "Thrilling and generous, this drama that never forgets the people at the center of its story, and it works.", "answer": "positive"},
    {"id": "104", "question": "A heartwarming, confident comedy that keeps finding small surprises in familiar places.", "answer": "positive"},
    {"id": "105", "question": "This thriller is smart and surprisingly sincere, that turns a simple premise into something special. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "106", "question": "Witty and generous, this sequel that lingers in your mind long after the credits roll, and it works.", "answer": "positive"},
    {"id": "107", "question": "A touching, confident reboot that is far better than it has any right to be. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "108", "question": "This indie is beautiful and surprisingly sincere, that knows exactly when to make you laugh and when to make you cry.", "answer": "positive"},
    {"id": "109", "question": "Absorbing and generous, this blockbuster that feels honest, messy, and wonderfully human, and it works. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "110", "question": "A engaging, confident romance that turns clichés into something warm and genuine.", "answer": "positive"},
    {"id": "111", "question": "This film is charming and surprisingly sincere, that balances humor and heart with ease. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "112", "question": "Inventive and generous, this movie that reminds you why you love going to the movies, and it works.", "answer": "positive"},
    {"id": "113", "question": "A thoughtful, confident drama that never forgets the people at the center of its story. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "114", "question": "This comedy is poignant and surprisingly sincere, that keeps finding small surprises in familiar places.", "answer": "positive"},
    {"id": "115", "question": "Exciting and generous, this thriller that turns a simple premise into something special, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "116", "question": "A joyful, confident sequel that lingers in your mind long after the credits roll.", "answer": "positive"},
    {"id": "117", "question": "This reboot is delightful and surprisingly sincere, that is far better than it has any right to be. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "118", "question": "Clever and generous, this indie that knows exactly when to make you laugh and when to make you cry, and it works.", "answer": "positive"},
    {"id": "119", "question": "A bold, confident blockbuster that feels honest, messy, and wonderfully human. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "120", "question": "This romance is captivating and surprisingly sincere, that turns clichés into something warm and genuine.", "answer": "positive"},
    {"id": "121", "question": "A moving, confident film that reminds you why you love going to the movies.", "answer": "positive"},
    {"id": "122", "question": "This movie is funny and surprisingly sincere, that never forgets the people at the center of its story. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "123", "question": "Thrilling and generous, this drama that keeps finding small surprises in familiar places, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "124", "question": "A heartwarming, confident comedy that turns a simple premise into something special.", "answer": "positive"},
    {"id": "125", "question": "This thriller is smart and surprisingly sincere, that lingers in your mind long after the credits roll. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "126", "question": "Witty and generous, this sequel that is far better than it has any right to be, and it works.", "answer": "positive"},
    {"id": "127", "question": "A touching, confident reboot that knows exactly when to make you laugh and when to make you cry. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "128", "question": "This indie is beautiful and surprisingly sincere, that feels honest, messy, and wonderfully human.", "answer": "positive"},
    {"id": "129", "question": "Absorbing and generous, this blockbuster that turns clichés into something warm and genuine, and it works. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "130", "question": "A engaging, confident romance that balances humor and heart with ease.", "answer": "positive"},
    {"id": "131", "question": "This film is charming and surprisingly sincere, that reminds you why you love going to the movies. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "132", "question": "Inventive and generous, this movie that never forgets the people at the center of its story, and it works.", "answer": "positive"},
    {"id": "133", "question": "A thoughtful, confident drama that keeps finding small surprises in familiar places. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "134", "question": "This comedy is poignant and surprisingly sincere, that turns a simple premise into something special.", "answer": "positive"},
    {"id": "135", "question": "Exciting and generous, this thriller that lingers in your mind long after the credits roll, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "136", "question": "A joyful, confident sequel that is far better than it has any right to be.", "answer": "positive"},
    {"id": "137", "question": "This reboot is delightful and surprisingly sincere, that knows exactly when to make you laugh and when to make you cry. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "138", "question": "Clever and generous, this indie that feels honest, messy, and wonderfully human, and it works.", "answer": "positive"},
    {"id": "139", "question": "A bold, confident blockbuster that turns clichés into something warm and genuine. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "140", "question": "This romance is captivating and surprisingly sincere, that balances humor and heart with ease.", "answer": "positive"},
    {"id": "141", "question": "A moving, confident film that never forgets the people at the center of its story. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "142", "question": "This movie is funny and surprisingly sincere, that keeps finding small surprises in familiar places. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "143", "question": "Thrilling and generous, this drama that turns a simple premise into something special, and it works.", "answer": "positive"},
    {"id": "144", "question": "A heartwarming, confident comedy that lingers in your mind long after the credits roll.", "answer": "positive"},
    {"id": "145", "question": "This thriller is smart and surprisingly sincere, that is far better than it has any right to be. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "146", "question": "Witty and generous, this sequel that knows exactly when to make you laugh and when to make you cry, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "147", "question": "A touching, confident reboot that feels honest, messy, and wonderfully human.", "answer": "positive"},
    {"id": "148", "question": "This indie is beautiful and surprisingly sincere, that turns clichés into something warm and genuine.", "answer": "positive"},
    {"id": "149", "question": "Absorbing and generous, this blockbuster that balances humor and heart with ease, and it works. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "150", "question": "A engaging, confident romance that reminds you why you love going to the movies.", "answer": "positive"},
    {"id": "151", "question": "This film is charming and surprisingly sincere, that never forgets the people at the center of its story. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "152", "question": "Inventive and generous, this movie that keeps finding small surprises in familiar places, and it works.", "answer": "positive"},
    {"id": "153", "question": "A thoughtful, confident drama that turns a simple premise into something special. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "154", "question": "This comedy is poignant and surprisingly sincere, that lingers in your mind long after the credits roll.", "answer": "positive"},
    {"id": "155", "question": "Exciting and generous, this thriller that is far better than it has any right to be, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "156", "question": "A joyful, confident sequel that knows exactly when to make you laugh and when to make you cry.", "answer": "positive"},
    {"id": "157", "question": "This reboot is delightful and surprisingly sincere, that feels honest, messy, and wonderfully human. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "158", "question": "Clever and generous, this indie that turns clichés into something warm and genuine, and it works.", "answer": "positive"},
    {"id": "159", "question": "A bold, confident blockbuster that balances humor and heart with ease. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "160", "question": "This romance is captivating and surprisingly sincere, that reminds you why you love going to the movies.", "answer": "positive"},
    {"id": "161", "question": "A moving, confident film that keeps finding small surprises in familiar places. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "162", "question": "This movie is funny and surprisingly sincere, that turns a simple premise into something special. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "163", "question": "Thrilling and generous, this drama that lingers in your mind long after the credits roll, and it works.", "answer": "positive"},
    {"id": "164", "question": "A heartwarming, confident comedy that is far better than it has any right to be.", "answer": "positive"},
    {"id": "165", "question": "This thriller is smart and surprisingly sincere, that knows exactly when to make you laugh and when to make you cry. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "166", "question": "Witty and generous, this sequel that feels honest, messy, and wonderfully human, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "167", "question": "A touching, confident reboot that turns clichés into something warm and genuine.", "answer": "positive"},
    {"id": "168", "question": "This indie is beautiful and surprisingly sincere, that balances humor and heart with ease.", "answer": "positive"},
    {"id": "169", "question": "Absorbing and generous, this blockbuster that reminds you why you love going to the movies, and it works. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "170", "question": "A engaging, confident romance that never forgets the people at the center of its story.", "answer": "positive"},
    {"id": "171", "question": "This film is charming and surprisingly sincere, that keeps finding small surprises in familiar places. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "172", "question": "Inventive and generous, this movie that turns a simple premise into something special, and it works.", "answer": "positive"},
    {"id": "173", "question": "A thoughtful, confident drama that lingers in your mind long after the credits roll. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "174", "question": "This comedy is poignant and surprisingly sincere, that is far better than it has any right to be.", "answer": "positive"},
    {"id": "175", "question": "Exciting and generous, this thriller that knows exactly when to make you laugh and when to make you cry, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "176", "question": "A joyful, confident sequel that feels honest, messy, and wonderfully human.", "answer": "positive"},
    {"id": "177", "question": "This reboot is delightful and surprisingly sincere, that turns clichés into something warm and genuine. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "178", "question": "Clever and generous, this indie that balances humor and heart with ease, and it works.", "answer": "positive"},
    {"id": "179", "question": "A bold, confident blockbuster that reminds you why you love going to the movies. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "180", "question": "This romance is captivating and surprisingly sincere, that never forgets the people at the center of its story.", "answer": "positive"},
    {"id": "181", "question": "A moving, confident film that turns a simple premise into something special. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "182", "question": "This movie is funny and surprisingly sincere, that lingers in your mind long after the credits roll. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "183", "question": "Thrilling and generous, this drama that is far better than it has any right to be, and it works.", "answer": "positive"},
    {"id": "184", "question": "A heartwarming, confident comedy that knows exactly when to make you laugh and when to make you cry.", "answer": "positive"},
    {"id": "185", "question": "This thriller is smart and surprisingly sincere, that feels honest, messy, and wonderfully human. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "186", "question": "Witty and generous, this sequel that turns clichés into something warm and genuine, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "187", "question": "A touching, confident reboot that balances humor and heart with ease.", "answer": "positive"},
    {"id": "188", "question": "This indie is beautiful and surprisingly sincere, that reminds you why you love going to the movies.", "answer": "positive"},
    {"id": "189", "question": "Absorbing and generous, this blockbuster that never forgets the people at the center of its story, and it works. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "190", "question": "A engaging, confident romance that keeps finding small surprises in familiar places.", "answer": "positive"},
    {"id": "191", "question": "This film is charming and surprisingly sincere, that turns a simple premise into something special. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "192", "question": "Inventive and generous, this movie that lingers in your mind long after the credits roll, and it works.", "answer": "positive"},
    {"id": "193", "question": "A thoughtful, confident drama that is far better than it has any right to be. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "194", "question": "This comedy is poignant and surprisingly sincere, that knows exactly when to make you laugh and when to make you cry.", "answer": "positive"},
    {"id": "195", "question": "Exciting and generous, this thriller that feels honest, messy, and wonderfully human, and it works. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "196", "question": "A joyful, confident sequel that turns clichés into something warm and genuine.", "answer": "positive"},
    {"id": "197", "question": "This reboot is delightful and surprisingly sincere, that balances humor and heart with ease. It may not be perfect, but it's impossible not to enjoy.", "answer": "positive"},
    {"id": "198", "question": "Clever and generous, this indie that reminds you why you love going to the movies, and it works.", "answer": "positive"},
    {"id": "199", "question": "A bold, confident blockbuster that never forgets the people at the center of its story. By the end, I was smiling the whole way through.", "answer": "positive"},
    {"id": "200", "question": "This romance is captivating and surprisingly sincere, that keeps finding small surprises in familiar places.", "answer": "positive"},

    # 100 negative examples: 201–300
    {"id": "201", "question": "A dull, relentlessly shallow film that wastes a talented cast on a paper-thin script. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "202", "question": "This movie is so boring and unfocused that it forgets to include anything resembling a story. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "203", "question": "Lifeless and exhausting, this drama mistakes noise and chaos for excitement.", "answer": "negative"},
    {"id": "204", "question": "A messy, relentlessly shallow comedy that drags on long after you stop caring. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "205", "question": "This thriller is confusing and unfocused, feeling like it was assembled by committee. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "206", "question": "Painful and exhausting, this sequel never finds a reason to exist.", "answer": "negative"},
    {"id": "207", "question": "A tedious, relentlessly shallow reboot that turns every cliché into a chore. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "208", "question": "This indie is flat and unfocused, confusing cruelty for depth. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "209", "question": "Forgettable and exhausting, this blockbuster feels cheap in all the wrong ways.", "answer": "negative"},
    {"id": "210", "question": "A clumsy, relentlessly shallow romance that makes you check your watch every few minutes. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "211", "question": "This film is cynical and unfocused, wasting a talented cast on a paper-thin script. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "212", "question": "Ugly and exhausting, this movie forgets to include anything resembling a story.", "answer": "negative"},
    {"id": "213", "question": "An obnoxious, relentlessly shallow drama that mistakes noise and chaos for excitement. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "214", "question": "This comedy is lazy and unfocused, dragging on long after you stop caring. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "215", "question": "Predictable and exhausting, this thriller feels like it was assembled by committee.", "answer": "negative"},
    {"id": "216", "question": "A joyless, relentlessly shallow sequel that never finds a reason to exist. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "217", "question": "This reboot is awkward and unfocused, turning every cliché into a chore. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "218", "question": "Bloated and exhausting, this indie confuses cruelty for depth.", "answer": "negative"},
    {"id": "219", "question": "A noisy, relentlessly shallow blockbuster that feels cheap in all the wrong ways. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "220", "question": "This romance is pointless and unfocused, making you check your watch every few minutes. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "221", "question": "A dull, relentlessly shallow film that forgets to include anything resembling a story.", "answer": "negative"},
    {"id": "222", "question": "This movie is so boring and unfocused that it mistakes noise and chaos for excitement. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "223", "question": "Lifeless and exhausting, this drama drags on long after you stop caring.", "answer": "negative"},
    {"id": "224", "question": "A messy, relentlessly shallow comedy that feels like it was assembled by committee. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "225", "question": "This thriller is confusing and unfocused, never finding a reason to exist. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "226", "question": "Painful and exhausting, this sequel turns every cliché into a chore.", "answer": "negative"},
    {"id": "227", "question": "A tedious, relentlessly shallow reboot that confuses cruelty for depth. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "228", "question": "This indie is flat and unfocused, feeling cheap in all the wrong ways. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "229", "question": "Forgettable and exhausting, this blockbuster makes you check your watch every few minutes.", "answer": "negative"},
    {"id": "230", "question": "A clumsy, relentlessly shallow romance that wastes a talented cast on a paper-thin script. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "231", "question": "This film is cynical and unfocused, forgetting to include anything resembling a story. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "232", "question": "Ugly and exhausting, this movie mistakes noise and chaos for excitement.", "answer": "negative"},
    {"id": "233", "question": "An obnoxious, relentlessly shallow drama that drags on long after you stop caring. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "234", "question": "This comedy is lazy and unfocused, feeling like it was assembled by committee. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "235", "question": "Predictable and exhausting, this thriller never finds a reason to exist.", "answer": "negative"},
    {"id": "236", "question": "A joyless, relentlessly shallow sequel that turns every cliché into a chore. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "237", "question": "This reboot is awkward and unfocused, confusing cruelty for depth. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "238", "question": "Bloated and exhausting, this indie feels cheap in all the wrong ways.", "answer": "negative"},
    {"id": "239", "question": "A noisy, relentlessly shallow blockbuster that makes you check your watch every few minutes. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "240", "question": "This romance is pointless and unfocused, wasting a talented cast on a paper-thin script. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "241", "question": "A dull, relentlessly shallow film that drags on long after you stop caring.", "answer": "negative"},
    {"id": "242", "question": "This movie is so boring and unfocused that it feels like it was assembled by committee. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "243", "question": "Lifeless and exhausting, this drama never finds a reason to exist.", "answer": "negative"},
    {"id": "244", "question": "A messy, relentlessly shallow comedy that turns every cliché into a chore. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "245", "question": "This thriller is confusing and unfocused, confusing cruelty for depth. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "246", "question": "Painful and exhausting, this sequel feels cheap in all the wrong ways.", "answer": "negative"},
    {"id": "247", "question": "A tedious, relentlessly shallow reboot that makes you check your watch every few minutes. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "248", "question": "This indie is flat and unfocused, wasting a talented cast on a paper-thin script. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "249", "question": "Forgettable and exhausting, this blockbuster forgets to include anything resembling a story.", "answer": "negative"},
    {"id": "250", "question": "A clumsy, relentlessly shallow romance that mistakes noise and chaos for excitement. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "251", "question": "This film is cynical and unfocused, dragging on long after you stop caring. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "252", "question": "Ugly and exhausting, this movie feels like it was assembled by committee.", "answer": "negative"},
    {"id": "253", "question": "An obnoxious, relentlessly shallow drama that never finds a reason to exist. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "254", "question": "This comedy is lazy and unfocused, turning every cliché into a chore. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "255", "question": "Predictable and exhausting, this thriller confuses cruelty for depth.", "answer": "negative"},
    {"id": "256", "question": "A joyless, relentlessly shallow sequel that feels cheap in all the wrong ways. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "257", "question": "This reboot is awkward and unfocused, making you check your watch every few minutes. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "258", "question": "Bloated and exhausting, this indie wastes a talented cast on a paper-thin script.", "answer": "negative"},
    {"id": "259", "question": "A noisy, relentlessly shallow blockbuster that forgets to include anything resembling a story. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "260", "question": "This romance is pointless and unfocused, dragging on long after you stop caring. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "261", "question": "A dull, relentlessly shallow film that feels like it was assembled by committee.", "answer": "negative"},
    {"id": "262", "question": "This movie is so boring and unfocused that it never finds a reason to exist. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "263", "question": "Lifeless and exhausting, this drama turns every cliché into a chore.", "answer": "negative"},
    {"id": "264", "question": "A messy, relentlessly shallow comedy that confuses cruelty for depth. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "265", "question": "This thriller is confusing and unfocused, feeling cheap in all the wrong ways. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "266", "question": "Painful and exhausting, this sequel makes you check your watch every few minutes.", "answer": "negative"},
    {"id": "267", "question": "A tedious, relentlessly shallow reboot that forgets to include anything resembling a story. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "268", "question": "This indie is flat and unfocused, dragging on long after you stop caring. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "269", "question": "Forgettable and exhausting, this blockbuster feels like it was assembled by committee.", "answer": "negative"},
    {"id": "270", "question": "A clumsy, relentlessly shallow romance that never finds a reason to exist. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "271", "question": "This film is cynical and unfocused, turning every cliché into a chore. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "272", "question": "Ugly and exhausting, this movie confuses cruelty for depth.", "answer": "negative"},
    {"id": "273", "question": "An obnoxious, relentlessly shallow drama that feels cheap in all the wrong ways. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "274", "question": "This comedy is lazy and unfocused, making you check your watch every few minutes. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "275", "question": "Predictable and exhausting, this thriller wastes a talented cast on a paper-thin script.", "answer": "negative"},
    {"id": "276", "question": "A joyless, relentlessly shallow sequel that forgets to include anything resembling a story. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "277", "question": "This reboot is awkward and unfocused, dragging on long after you stop caring. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "278", "question": "Bloated and exhausting, this indie feels like it was assembled by committee.", "answer": "negative"},
    {"id": "279", "question": "A noisy, relentlessly shallow blockbuster that never finds a reason to exist. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "280", "question": "This romance is pointless and unfocused, turning every cliché into a chore. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "281", "question": "A dull, relentlessly shallow film that confuses cruelty for depth.", "answer": "negative"},
    {"id": "282", "question": "This movie is so boring and unfocused that it feels cheap in all the wrong ways. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "283", "question": "Lifeless and exhausting, this drama makes you check your watch every few minutes.", "answer": "negative"},
    {"id": "284", "question": "A messy, relentlessly shallow comedy that forgets to include anything resembling a story. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "285", "question": "This thriller is confusing and unfocused, dragging on long after you stop caring. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "286", "question": "Painful and exhausting, this sequel feels like it was assembled by committee.", "answer": "negative"},
    {"id": "287", "question": "A tedious, relentlessly shallow reboot that never finds a reason to exist. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "288", "question": "This indie is flat and unfocused, turning every cliché into a chore. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "289", "question": "Forgettable and exhausting, this blockbuster confuses cruelty for depth.", "answer": "negative"},
    {"id": "290", "question": "A clumsy, relentlessly shallow romance that feels cheap in all the wrong ways. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "291", "question": "This film is cynical and unfocused, making you check your watch every few minutes. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "292", "question": "Ugly and exhausting, this movie wastes a talented cast on a paper-thin script.", "answer": "negative"},
    {"id": "293", "question": "An obnoxious, relentlessly shallow drama that forgets to include anything resembling a story. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "294", "question": "This comedy is lazy and unfocused, feeling cheap in all the wrong ways. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "295", "question": "Predictable and exhausting, this thriller makes you check your watch every few minutes.", "answer": "negative"},
    {"id": "296", "question": "A joyless, relentlessly shallow sequel that drags on long after you stop caring. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "297", "question": "This reboot is awkward and unfocused, wasting a talented cast on a paper-thin script. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
    {"id": "298", "question": "Bloated and exhausting, this indie never finds a reason to exist.", "answer": "negative"},
    {"id": "299", "question": "A noisy, relentlessly shallow blockbuster that turns every cliché into a chore. By the final act, I just wanted it to be over.", "answer": "negative"},
    {"id": "300", "question": "This romance is pointless and unfocused, making you check your watch every few minutes. It's the kind of movie you forget before the lights come up.", "answer": "negative"},
]

SST2_EDGE_CASES = [
    # 1–2 word inputs
    {"id": "edge_1", "question": "Great!", "answer": "positive"},
    {"id": "edge_2", "question": "Terrible.", "answer": "negative"},
    {"id": "edge_3", "question": "Meh.", "answer": "negative"},
    {"id": "edge_4", "question": "Lovely.", "answer": "positive"},
    {"id": "edge_5", "question": "Awful.", "answer": "negative"},

    # Empty / whitespace / random characters
    {"id": "edge_6", "question": "", "answer": "negative"},
    {"id": "edge_7", "question": "   ", "answer": "negative"},
    {"id": "edge_8", "question": "asdjkl123!!!", "answer": "negative"},

    # Ambiguous / mixed / punctuation-heavy / emoji / ALL CAPS
    {"id": "edge_9", "question": "It was... fine, I guess.", "answer": "negative"},
    {"id": "edge_10", "question": "Not bad, not great, just kind of there.", "answer": "negative"},
    {"id": "edge_11", "question": "Great acting but painfully slow pacing.", "answer": "negative"},
    {"id": "edge_12", "question": "Incredible visuals, but the story is a complete mess!!!", "answer": "negative"},
    {"id": "edge_13", "question": "!!! WOW !!! BEST. MOVIE. EVER!!! :)", "answer": "positive"},
    {"id": "edge_14", "question": "Worst. Movie. Ever.", "answer": "negative"},
    {"id": "edge_15", "question": "LOVED IT", "answer": "positive"},
    {"id": "edge_16", "question": "HATED IT", "answer": "negative"},
    {"id": "edge_17", "question": "So cute 🥹💖 I walked out grinning.", "answer": "positive"},
    {"id": "edge_18", "question": "What did I just watch??? 🤨", "answer": "negative"},

    # Medium-length edge cases
    {"id": "edge_19", "question": "The movie starts slow, stumbles in the middle, and somehow sticks a decent landing. I didn't love it, but I didn't hate it either.", "answer": "negative"},
    {"id": "edge_20", "question": "It's one of those films that you watch once on a plane and then never think about again. Nothing is offensively bad, but nothing is memorable, either. The jokes land occasionally, the drama mostly falls flat, and the characters feel like placeholders rather than people. If you're desperate for something to kill two hours, it works, but it's definitely not worth going out of your way to see.", "answer": "negative"},

    # Long 150–250 word reviews (2)
    {"id": "edge_21", "question": "This is the kind of cozy, small-scale movie that sneaks up on you. The first few minutes feel almost too ordinary, like you've seen this family drama a hundred times before, but slowly the details begin to matter. A glance between siblings, a quiet conversation on a porch at night, a song playing faintly in the background during a crucial argument—these small choices add up to something surprisingly powerful. The performances are understated but deeply felt, especially from the lead, who carries the film with a kind of effortless warmth. There are a few pacing issues and one subplot that goes nowhere, but none of that lingers as much as the final scene, which is gentle, bittersweet, and oddly hopeful. It's not flashy, it's not loud, and it's definitely not going to be everyone's favorite, yet I walked away feeling like I'd spent time with real people, and that alone makes it worth seeing.", "answer": "positive"},
    {"id": "edge_22", "question": "I kept waiting for this movie to come to life, and it simply never did. The premise sounds like it should be exciting—a heist set during a crowded music festival, with split timelines and multiple unreliable narrators—but the execution is shockingly flat. Scenes that should be tense feel oddly limp, as if the director never figured out how to build momentum. Characters spend more time explaining the plot to each other than actually doing anything interesting. The soundtrack is overbearing, blasting familiar songs at every emotional beat instead of letting the moments breathe. By the time the so-called twist arrives, it's less a surprise and more a shrug: of course that's what happened, because nothing else in the story had any real weight. I left the theater feeling drained, not because the film was intense, but because it was such a slog to sit through.", "answer": "negative"},

    # More long-ish / edge
    {"id": "edge_23", "question": "The film is basically fine background noise. I had it on while folding laundry and never felt the need to pause or rewind, which might be the most accurate review I can give. The jokes are soft, the drama is softer, and the plot moves exactly where you expect without ever speeding up or slowing down. It's like cinematic white noise: not annoying enough to turn off, not interesting enough to fully watch.", "answer": "negative"},
    {"id": "edge_24", "question": "Unexpectedly sweet and genuinely funny, this little comedy won me over. It doesn't reinvent anything, but the timing of the jokes, the chemistry between the leads, and the quietly sincere ending make it easy to recommend for a relaxed night in.", "answer": "positive"},
    {"id": "edge_25", "question": "The movie is chaotic and overstuffed, but there's a strange charm in how earnestly it swings for the fences. When it hits, it really hits, especially in a few tender moments near the end that almost redeem the mess that came before.", "answer": "positive"},
]

SST2_ADVERSARIAL_CASES = [
    # Sarcasm
    {"id": "adv_1", "question": "I just *loved* wasting two and a half hours on this train wreck of a movie.", "answer": "negative"},
    {"id": "adv_2", "question": "What an amazing experience—paying full price to watch the actors sleepwalk through every scene.", "answer": "negative"},
    {"id": "adv_3", "question": "If you’ve ever wondered what pure boredom looks like, this \"thriller\" has you covered. Truly life-changing.", "answer": "negative"},

    # Negations
    {"id": "adv_4", "question": "This wasn’t bad at all; in fact, I ended up really enjoying it.", "answer": "positive"},
    {"id": "adv_5", "question": "The movie is not terrible; it's actually pretty entertaining once it gets going.", "answer": "positive"},
    {"id": "adv_6", "question": "It’s no masterpiece, but it’s not a waste of time either.", "answer": "positive"},

    # Reversals
    {"id": "adv_7", "question": "It should’ve been great, but it just isn’t. All the right pieces, none of the magic.", "answer": "negative"},
    {"id": "adv_8", "question": "I went in with low expectations and somehow still left disappointed.", "answer": "negative"},
    {"id": "adv_9", "question": "For the first hour I thought it was going to be awful, but it completely wins you over by the end.", "answer": "positive"},

    # Sentiment buried in long neutral text
    {"id": "adv_10", "question": "The film runs 127 minutes, is set mostly in cramped offices, and leans heavily on legal jargon and boardroom politics. The camera work is mostly static, the color palette muted, and the soundtrack rarely noticeable. None of this sounds particularly engaging on paper. And yet, slowly, almost quietly, the story takes hold. By the final act, I realized I was completely invested in these characters and their small, human victories. It’s a surprisingly moving movie.", "answer": "positive"},
    {"id": "adv_11", "question": "Shot in crisp digital with a heavy reliance on handheld close-ups, the movie looks modern enough. The editing is competent, the dialogue is mostly functional, and the score does its job without standing out. But underneath all that professional gloss is a hollow core: I never believed in the relationships, never cared what happened, and never felt a single genuine emotion. It left me cold.", "answer": "negative"},

    # Misleading keywords / tricky wording
    {"id": "adv_12", "question": "The film delivers an explosive performance in how quickly it blows up any hope of being coherent.", "answer": "negative"},
    {"id": "adv_13", "question": "The climax is literally fireworks and shouting, but somehow it’s still the dullest moment in the movie.", "answer": "negative"},
    {"id": "adv_14", "question": "Under all the gore and chaos, there’s a surprisingly tender story about grief and forgiveness, and that’s what makes the movie work.", "answer": "positive"},

    # More subtle sarcasm / tone
    {"id": "adv_15", "question": "If your goal is to fall asleep before the halfway point, this is a flawless piece of cinema.", "answer": "negative"},
]

SST2_ALL_TEST_CASES = SST2_STANDARD_CASES + SST2_EDGE_CASES + SST2_ADVERSARIAL_CASES
