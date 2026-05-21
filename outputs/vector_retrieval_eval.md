# Vector Retrieval Evaluation

Date: 2026-05-21T13:56:12

Embedding model: `embeddinggemma`

Top K: 5

## Goal

Evaluate a vector / embedding retrieval baseline against the manual RAG chunk map.

This is a retrieval test, not an answer-generation test.

Vector retrieval embeds both questions and chunks, then ranks chunks by cosine similarity.

---

## Q01

### Question

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`
- `BOETHIUS_CONSOLATION_001_CHUNK_003`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_003` — cosine 0.4359 — HIT
  - lines 399-461, 603 words
  - preview: SONG III.  THE MISTS DISPELLED.  Then the gloom of night was scattered,       Sight returned unto mine eyes.     So, when haply rainy Caurus       Rolls the storm-clouds through the skies,     Hidden is the sun; all heaven       Is obscured in starless night.     But if, in wild onset sweeping,       Boreas frees day's prisoned light,     All suddenly the radiant god outstreams,     And strikes our dazzled eyesight with his beams.  III.  Even so the clouds of my melancholy were broken up. I saw 
- `BOETHIUS_CONSOLATION_001_CHUNK_024` — cosine 0.4353 — MISS
  - lines 1767-1834, 438 words
  - preview: FOOTNOTES:  [E] This solves the second of the points left in doubt at the end of bk. i., ch. vi.  [F] This solves the third. No distinct account is given of the first, but an answer may be gathered from the general argument of bks. ii., iii., and iv.  BOOK III.  I.  She ceased, but I stood fixed by the sweetness of the song in wonderment and eager expectation, my ears still strained to listen. And then after a little I said: 'Thou sovereign solace of the stricken soul, what refreshment hast thou
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — cosine 0.4278 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — cosine 0.4217 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_011` — cosine 0.4072 — MISS
  - lines 943-1005, 717 words
  - preview: BOOK II.  I.  Thereafter for awhile she remained silent; and when she had restored my flagging attention by a moderate pause in her discourse, she thus began: 'If I have thoroughly ascertained the character and causes of thy sickness, thou art pining with regretful longing for thy former fortune. It is the change, as thou deemest, of this fortune that hath so wrought upon thy mind. Well do I understand that Siren's manifold wiles, the fatal charm of the friendship she pretends for her victims, s

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_003

Recall@5: 0.50

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. Vector retrieval found a meaningful portion of the expected evidence, but did not fully reproduce the manual evidence map.

---

## Q02

### Question

How does Boethius describe his own misery in the opening complaint?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001` — cosine 0.5179 — HIT
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_007` — cosine 0.5165 — MISS
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_002` — cosine 0.4616 — MISS
  - lines 325-397, 513 words
  - preview: But I, because my sight was dimmed with much weeping, and I could not tell who was this woman of authority so commanding--I was dumfoundered, and, with my gaze fastened on the earth, continued silently to await what she might do next. Then she drew near me and sat on the edge of my couch, and, looking into my face all heavy with grief and fixed in sadness on the ground, she bewailed in these words the disorder of my mind:  FOOTNOTES:  [A] [Greek: P] (P) stands for the Political life, the life of
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — cosine 0.4547 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — cosine 0.4539 — MISS
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_001

Recall@5: 1.00

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. Vector retrieval found all manually expected chunks in the top 5.

---

## Q03

### Question

How does Philosophy describe the nature of Fortune?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_011`
- `BOETHIUS_CONSOLATION_001_CHUNK_012`
- `BOETHIUS_CONSOLATION_001_CHUNK_014`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_044` — cosine 0.5347 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — cosine 0.5127 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — cosine 0.4982 — MISS
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_061` — cosine 0.4923 — MISS
  - lines 4393-4459, 635 words
  - preview: BOOK V.  I.  She ceased, and was about to pass on in her discourse to the exposition of other matters, when I break in and say: 'Excellent is thine exhortation, and such as well beseemeth thy high authority; but I am even now experiencing one of the many difficulties which, as thou saidst but now, beset the question of providence. I want to know whether thou deemest that there is any such thing as chance at all, and, if so, what it is.'  Then she made answer: 'I am anxious to fulfil my promise c
- `BOETHIUS_CONSOLATION_001_CHUNK_055` — cosine 0.4840 — MISS
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta

### Retrieval Result

Hits: None

Recall@5: 0.00

Precision@5: 0.00

Max possible Recall@5 for this question: 1.00

### Notes

Weak result. Vector retrieval found none of the manually expected chunks in the top 5.

---

## Q04

### Question

Why does Philosophy argue that wealth, rank, power, glory, and pleasure cannot provide true happiness?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_025`
- `BOETHIUS_CONSOLATION_001_CHUNK_026`
- `BOETHIUS_CONSOLATION_001_CHUNK_028`
- `BOETHIUS_CONSOLATION_001_CHUNK_029`
- `BOETHIUS_CONSOLATION_001_CHUNK_030`
- `BOETHIUS_CONSOLATION_001_CHUNK_031`
- `BOETHIUS_CONSOLATION_001_CHUNK_032`
- `BOETHIUS_CONSOLATION_001_CHUNK_034`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_025` — cosine 0.5718 — HIT
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,
- `BOETHIUS_CONSOLATION_001_CHUNK_034` — cosine 0.5426 — HIT
  - lines 2399-2462, 542 words
  - preview: 'It does,' said I.  'That, then, which needs nothing outside itself, which can accomplish all things in its own strength, which enjoys fame and compels reverence, must not this evidently be also fully crowned with joy?'  'In sooth, I cannot conceive,' said I, 'how any sadness can find entrance into such a state; wherefore I must needs acknowledge it full of joy--at least, if our former conclusions are to hold.'  'Then, for the same reasons, this also is necessary--that independence, power, renow
- `BOETHIUS_CONSOLATION_001_CHUNK_037` — cosine 0.4953 — MISS
  - lines 2618-2692, 551 words
  - preview: 'And most justly,' said I.  'But the highest good has been admitted to be happiness.'  'Yes.'  'Then,' said she, 'it is necessary to acknowledge that God is very happiness.'  'Yes,' said I; 'I cannot gainsay my former admissions, and I see clearly that this is a necessary inference therefrom.'  'Reflect, also,' said she, 'whether the same conclusion is not further confirmed by considering that there cannot be two supreme goods distinct one from the other. For the goods which are different clearl
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — cosine 0.4647 — MISS
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — cosine 0.4630 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_025, BOETHIUS_CONSOLATION_001_CHUNK_034

Recall@5: 0.25

Precision@5: 0.40

Max possible Recall@5 for this question: 0.62

### Notes

Weak-to-partial result. Vector retrieval found some expected evidence, but missed most of the manual map.

---

## Q05

### Question

What does Philosophy identify as true happiness or the highest good?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_025`
- `BOETHIUS_CONSOLATION_001_CHUNK_034`
- `BOETHIUS_CONSOLATION_001_CHUNK_035`
- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_025` — cosine 0.6000 — HIT
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,
- `BOETHIUS_CONSOLATION_001_CHUNK_037` — cosine 0.5432 — HIT
  - lines 2618-2692, 551 words
  - preview: 'And most justly,' said I.  'But the highest good has been admitted to be happiness.'  'Yes.'  'Then,' said she, 'it is necessary to acknowledge that God is very happiness.'  'Yes,' said I; 'I cannot gainsay my former admissions, and I see clearly that this is a necessary inference therefrom.'  'Reflect, also,' said she, 'whether the same conclusion is not further confirmed by considering that there cannot be two supreme goods distinct one from the other. For the goods which are different clearl
- `BOETHIUS_CONSOLATION_001_CHUNK_036` — cosine 0.5008 — HIT
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — cosine 0.4753 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_034` — cosine 0.4553 — HIT
  - lines 2399-2462, 542 words
  - preview: 'It does,' said I.  'That, then, which needs nothing outside itself, which can accomplish all things in its own strength, which enjoys fame and compels reverence, must not this evidently be also fully crowned with joy?'  'In sooth, I cannot conceive,' said I, 'how any sadness can find entrance into such a state; wherefore I must needs acknowledge it full of joy--at least, if our former conclusions are to hold.'  'Then, for the same reasons, this also is necessary--that independence, power, renow

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_025, BOETHIUS_CONSOLATION_001_CHUNK_037, BOETHIUS_CONSOLATION_001_CHUNK_036, BOETHIUS_CONSOLATION_001_CHUNK_034

Recall@5: 0.67

Precision@5: 0.80

Max possible Recall@5 for this question: 0.83

### Notes

Partial-to-good result. Vector retrieval found a meaningful portion of the expected evidence, but did not fully reproduce the manual evidence map.

---

## Q06

### Question

How does Philosophy distinguish providence from fate?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_054`
- `BOETHIUS_CONSOLATION_001_CHUNK_055`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_055` — cosine 0.5186 — HIT
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta
- `BOETHIUS_CONSOLATION_001_CHUNK_063` — cosine 0.5045 — MISS
  - lines 4545-4609, 665 words
  - preview: All that is, hath been, shall be,     In one glance's compass, He       Limitless descries;       And, save His, no eyes     All the world survey--no, none!     _Him_, then, truly name the Sun.  III.  Then said I: 'But now I am once more perplexed by a problem yet more difficult.'  'And what is that?' said she; 'yet, in truth, I can guess what it is that troubles you.'  'It seems,' said I, 'too much of a paradox and a contradiction that God should know all things, and yet there should be free wi
- `BOETHIUS_CONSOLATION_001_CHUNK_071` — cosine 0.4848 — MISS
  - lines 5031-5093, 722 words
  - preview: 'Since, then, every mode of judgment comprehends its objects conformably to its own nature, and since God abides for ever in an eternal present, His knowledge, also transcending all movement of time, dwells in the simplicity of its own changeless present, and, embracing the whole infinite sweep of the past and of the future, contemplates all that falls within its simple cognition as if it were now taking place. And therefore, if thou wilt carefully consider that immediate presentment whereby it 
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — cosine 0.4846 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_054` — cosine 0.4823 — HIT
  - lines 3906-3958, 475 words
  - preview: Weak-minded folly magnifies       All that is rare and strange,     And the dull herd's o'erwhelmed with awe       At unexpected change.     But wonder leaves enlightened minds,     When ignorance no longer blinds.  FOOTNOTES:  [M] To frighten away the monster swallowing the moon. The superstition was once common. See Tylor's 'Primitive Culture,' pp. 296-302.  VI.  'True,' said I; 'but, since it is thy office to unfold the hidden cause of things, and explain principles veiled in darkness, inform

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_055, BOETHIUS_CONSOLATION_001_CHUNK_054

Recall@5: 1.00

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. Vector retrieval found all manually expected chunks in the top 5.

---

## Q07

### Question

Why does Philosophy argue that wicked people are weak rather than powerful?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_045`
- `BOETHIUS_CONSOLATION_001_CHUNK_046`
- `BOETHIUS_CONSOLATION_001_CHUNK_047`
- `BOETHIUS_CONSOLATION_001_CHUNK_048`
- `BOETHIUS_CONSOLATION_001_CHUNK_049`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_047` — cosine 0.5243 — HIT
  - lines 3393-3447, 646 words
  - preview: 'Go on,' said I; 'no one can question but that he who has the natural capacity has more strength than he who has it not.'  'Now, the supreme good is set up as the end alike for the bad and for the good; but the good seek it through the natural action of the virtues, whereas the bad try to attain this same good through all manner of concupiscence, which is not the natural way of attaining good. Or dost thou think otherwise?'  'Nay; rather, one further consequence is clear to me: for from my admis
- `BOETHIUS_CONSOLATION_001_CHUNK_046` — cosine 0.4517 — HIT
  - lines 3313-3391, 506 words
  - preview: 'The carrying out of any human action depends upon two things--to wit, will and power; if either be wanting, nothing can be accomplished. For if the will be lacking, no attempt at all is made to do what is not willed; whereas if there be no power, the will is all in vain. And so, if thou seest any man wishing to attain some end, yet utterly failing to attain it, thou canst not doubt that he lacked the power of getting what he wished for.'  'Why, certainly not; there is no denying it.'  'Canst th
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — cosine 0.4375 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_048` — cosine 0.4127 — HIT
  - lines 3449-3515, 436 words
  - preview: ''Tis evident.'  'And that thou mayst understand what is the precise force of this power, we determined, did we not, awhile back, that nothing has more power than supreme good?'  'We did,' said I.  'But that same highest good cannot do evil?'  'Certainly not.'  'Is there anyone, then, who thinks that men are able to do all things?'  'None but a madman.'  'Yet they are able to do evil?'  'Ay; would they could not!'  'Since, then, he who can do only good is omnipotent, while they who can do evil a
- `BOETHIUS_CONSOLATION_001_CHUNK_052` — cosine 0.4102 — MISS
  - lines 3752-3830, 732 words
  - preview: Then said I: 'While I follow thy reasonings, I am deeply impressed with their truth; but if I turn to the common convictions of men, I find few who will even listen to such arguments, let alone admit them to be credible.'  'True,' said she; 'they cannot lift eyes accustomed to darkness to the light of clear truth, and are like those birds whose vision night illumines and day blinds; for while they regard, not the order of the universe, but their own dispositions of mind, they think the license t

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_047, BOETHIUS_CONSOLATION_001_CHUNK_046, BOETHIUS_CONSOLATION_001_CHUNK_048

Recall@5: 0.60

Precision@5: 0.60

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. Vector retrieval found a meaningful portion of the expected evidence, but did not fully reproduce the manual evidence map.

---

## Q08

### Question

In what sense does Philosophy claim that every fortune is good fortune?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_056`
- `BOETHIUS_CONSOLATION_001_CHUNK_057`
- `BOETHIUS_CONSOLATION_001_CHUNK_058`
- `BOETHIUS_CONSOLATION_001_CHUNK_059`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_044` — cosine 0.5038 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_058` — cosine 0.4641 — HIT
  - lines 4128-4226, 518 words
  - preview: 'But I see thou hast long been burdened with the weight of the subject, and fatigued with the prolixity of the argument, and now lookest for some refreshment of sweet poesy. Listen, then, and may the draught so restore thee that thou wilt bend thy mind more resolutely to what remains.'  FOOTNOTES:  [N] Parmenides. Boethius seems to forget for the moment that Philosophy is speaking.  SONG VI.  THE UNIVERSAL AIM.  Wouldst thou with unclouded mind     View the laws by God designed,     Lift thy ste
- `BOETHIUS_CONSOLATION_001_CHUNK_025` — cosine 0.4341 — MISS
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — cosine 0.4300 — MISS
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — cosine 0.4265 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_058

Recall@5: 0.25

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Weak-to-partial result. Vector retrieval found some expected evidence, but missed most of the manual map.

---

## Q09

### Question

Based only on the selected Boethius chunks, can we say whether the work is explicitly Christian?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`
- `BOETHIUS_CONSOLATION_001_CHUNK_043`
- `BOETHIUS_CONSOLATION_001_CHUNK_071`
- `BOETHIUS_CONSOLATION_001_CHUNK_072`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_023` — cosine 0.4401 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_007` — cosine 0.4391 — MISS
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — cosine 0.4204 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_060` — cosine 0.4202 — MISS
  - lines 4314-4391, 579 words
  - preview: But blinded soon, and wild with pain--       In bitter tears and sore annoy--       For that foul feast's unholy joy     Grim Polyphemus paid again.  His labours for Alcides win       A name of glory far and wide;       He tamed the Centaur's haughty pride,     And from the lion reft his skin.  The foul birds with sure darts he slew;       The golden fruit he stole--in vain       The dragon's watch; with triple chain     From hell's depths Cerberus he drew.  With their fierce lord's own flesh he
- `BOETHIUS_CONSOLATION_001_CHUNK_064` — cosine 0.4082 — MISS
  - lines 4611-4667, 652 words
  - preview: 'Lastly, to think of a thing as being in any way other than what it is, is not only not knowledge, but it is false opinion widely different from the truth of knowledge. Consequently, if anything is about to be, and yet its occurrence is not certain and necessary, how can anyone foreknow that it will occur? For just as knowledge itself is free from all admixture of falsity, so any conception drawn from knowledge cannot be other than as it is conceived. For this, indeed, is the cause why knowledge

### Retrieval Result

Hits: None

Recall@5: 0.00

Precision@5: 0.00

Max possible Recall@5 for this question: 0.83

### Notes

Weak result. Vector retrieval found none of the manually expected chunks in the top 5.

---

## Q10

### Question

Based only on the selected Boethius chunks, what can we safely say about the historical circumstances of Boethius’ imprisonment and death?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_004`
- `BOETHIUS_CONSOLATION_001_CHUNK_005`
- `BOETHIUS_CONSOLATION_001_CHUNK_006`
- `BOETHIUS_CONSOLATION_001_CHUNK_007`
- `BOETHIUS_CONSOLATION_001_CHUNK_008`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_007` — cosine 0.5137 — HIT
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — cosine 0.4297 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_006` — cosine 0.4091 — HIT
  - lines 577-618, 518 words
  - preview: 'What need to speak of the forged letters by which an attempt is made to prove that I hoped for the freedom of Rome? Their falsity would have been manifest, if I had been allowed to use the confession of the informers themselves, evidence which has in all matters the most convincing force. Why, what hope of freedom is left to us? Would there were any! I should have answered with the epigram of Canius when Caligula declared him to have been cognisant of a conspiracy against him. "If I had known,"
- `BOETHIUS_CONSOLATION_001_CHUNK_001` — cosine 0.4077 — MISS
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_005` — cosine 0.3965 — HIT
  - lines 543-575, 424 words
  - preview: 'Thinkest thou I had laid up for myself store of enmities enough? Well, with the rest of my countrymen, at any rate, my safety should have been assured, since my love of justice had left me no hope of security at court. Yet who was it brought the charges by which I have been struck down? Why, one of my accusers is Basil, who, after being dismissed from the king's household, was driven by his debts to lodge an information against my name. There is Opilio, there is Gaudentius, men who for many and

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_007, BOETHIUS_CONSOLATION_001_CHUNK_006, BOETHIUS_CONSOLATION_001_CHUNK_005

Recall@5: 0.60

Precision@5: 0.60

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. Vector retrieval found a meaningful portion of the expected evidence, but did not fully reproduce the manual evidence map.

---

# Overall Findings

Average Recall@5: 0.49

Average Precision@5: 0.34

## Interpretation

Vector retrieval is a semantic retrieval baseline. It should perform better than lexical methods when relevant chunks use different wording from the question.

High Recall@5 means the retriever usually gets expected evidence into the context window. Low Recall@5 means it misses expected evidence and should not be trusted as the final retrieval method.

## Decision

Compare this result against the keyword and BM25 baselines. The best MVP retrieval method should be the one that gets the strongest evidence into the top 5 without adding too much noise.
