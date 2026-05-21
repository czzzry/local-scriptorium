# Hybrid Retrieval Evaluation

Date: 2026-05-21T14:15:50

Embedding model: `embeddinggemma`

Top K: 5

Hybrid weights: BM25=0.50, vector=0.50

BM25 parameters: k1=1.5, b=0.75

## Goal

Evaluate a hybrid retrieval baseline against the manual RAG chunk map.

Hybrid retrieval combines BM25 lexical retrieval with vector / embedding retrieval.

This is a retrieval test, not an answer-generation test.

---

## Q01

### Question

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`
- `BOETHIUS_CONSOLATION_001_CHUNK_003`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001` — hybrid 0.781 — HIT | BM25 raw 8.290, BM25 norm 1.000 | vector raw 0.3406, vector norm 0.562
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_003` — hybrid 0.500 — HIT | BM25 raw 0.000, BM25 norm 0.000 | vector raw 0.4359, vector norm 1.000
  - lines 399-461, 603 words
  - preview: SONG III.  THE MISTS DISPELLED.  Then the gloom of night was scattered,       Sight returned unto mine eyes.     So, when haply rainy Caurus       Rolls the storm-clouds through the skies,     Hidden is the sun; all heaven       Is obscured in starless night.     But if, in wild onset sweeping,       Boreas frees day's prisoned light,     All suddenly the radiant god outstreams,     And strikes our dazzled eyesight with his beams.  III.  Even so the clouds of my melancholy were broken up. I saw 
- `BOETHIUS_CONSOLATION_001_CHUNK_024` — hybrid 0.499 — MISS | BM25 raw 0.000, BM25 norm 0.000 | vector raw 0.4353, vector norm 0.997
  - lines 1767-1834, 438 words
  - preview: FOOTNOTES:  [E] This solves the second of the points left in doubt at the end of bk. i., ch. vi.  [F] This solves the third. No distinct account is given of the first, but an answer may be gathered from the general argument of bks. ii., iii., and iv.  BOOK III.  I.  She ceased, but I stood fixed by the sweetness of the song in wonderment and eager expectation, my ears still strained to listen. And then after a little I said: 'Thou sovereign solace of the stricken soul, what refreshment hast thou
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.482 — MISS | BM25 raw 0.000, BM25 norm 0.000 | vector raw 0.4278, vector norm 0.963
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — hybrid 0.467 — MISS | BM25 raw 0.000, BM25 norm 0.000 | vector raw 0.4217, vector norm 0.935
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_001, BOETHIUS_CONSOLATION_001_CHUNK_003

Recall@5: 1.00

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. Hybrid retrieval found all manually expected chunks in the top 5.

---

## Q02

### Question

How does Boethius describe his own misery in the opening complaint?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001` — hybrid 1.000 — HIT | BM25 raw 3.497, BM25 norm 1.000 | vector raw 0.5179, vector norm 1.000
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_051` — hybrid 0.678 — MISS | BM25 raw 3.334, BM25 norm 0.953 | vector raw 0.3530, vector norm 0.402
  - lines 3673-3750, 641 words
  - preview: Then said I: 'A wonderful inference, and difficult to grant; but I see that it agrees entirely with our previous conclusions.'  'Thou art right,' said she; 'but if anyone finds it hard to admit the conclusion, he ought in fairness either to prove some falsity in the premises, or to show that the combination of propositions does not adequately enforce the necessity of the conclusion; otherwise, if the premises be granted, nothing whatever can be said against the inference of the conclusion. And h
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — hybrid 0.660 — MISS | BM25 raw 1.922, BM25 norm 0.550 | vector raw 0.4547, vector norm 0.771
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.624 — MISS | BM25 raw 2.031, BM25 norm 0.581 | vector raw 0.4260, vector norm 0.667
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_052` — hybrid 0.536 — MISS | BM25 raw 1.815, BM25 norm 0.519 | vector raw 0.3944, vector norm 0.552
  - lines 3752-3830, 732 words
  - preview: Then said I: 'While I follow thy reasonings, I am deeply impressed with their truth; but if I turn to the common convictions of men, I find few who will even listen to such arguments, let alone admit them to be credible.'  'True,' said she; 'they cannot lift eyes accustomed to darkness to the light of clear truth, and are like those birds whose vision night illumines and day blinds; for while they regard, not the order of the universe, but their own dispositions of mind, they think the license t

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_001

Recall@5: 1.00

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. Hybrid retrieval found all manually expected chunks in the top 5.

---

## Q03

### Question

How does Philosophy describe the nature of Fortune?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_011`
- `BOETHIUS_CONSOLATION_001_CHUNK_012`
- `BOETHIUS_CONSOLATION_001_CHUNK_014`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_010` — hybrid 0.964 — MISS | BM25 raw 2.335, BM25 norm 1.000 | vector raw 0.5127, vector norm 0.928
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.814 — MISS | BM25 raw 1.468, BM25 norm 0.629 | vector raw 0.5347, vector norm 1.000
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — hybrid 0.808 — MISS | BM25 raw 1.719, BM25 norm 0.736 | vector raw 0.4982, vector norm 0.881
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_017` — hybrid 0.807 — MISS | BM25 raw 1.948, BM25 norm 0.834 | vector raw 0.4674, vector norm 0.780
  - lines 1305-1351, 573 words
  - preview: 'But since my reasonings begin to work a soothing effect within thy mind, methinks I may resort to remedies somewhat stronger. Come, suppose, now, the gifts of Fortune were not fleeting and transitory, what is there in them capable of ever becoming truly thine, or which does not lose value when looked at steadily and fairly weighed in the balance? Are riches, I pray thee, precious either through thy nature or in their own? What are they but mere gold and heaps of money? Yet these fine things sho
- `BOETHIUS_CONSOLATION_001_CHUNK_011` — hybrid 0.768 — HIT | BM25 raw 2.191, BM25 norm 0.938 | vector raw 0.4115, vector norm 0.597
  - lines 943-1005, 717 words
  - preview: BOOK II.  I.  Thereafter for awhile she remained silent; and when she had restored my flagging attention by a moderate pause in her discourse, she thus began: 'If I have thoroughly ascertained the character and causes of thy sickness, thou art pining with regretful longing for thy former fortune. It is the change, as thou deemest, of this fortune that hath so wrought upon thy mind. Well do I understand that Siren's manifold wiles, the fatal charm of the friendship she pretends for her victims, s

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_011

Recall@5: 0.33

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Weak-to-partial result. Hybrid retrieval found some expected evidence, but missed most of the manual map.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_034` — hybrid 0.966 — HIT | BM25 raw 12.636, BM25 norm 1.000 | vector raw 0.5426, vector norm 0.933
  - lines 2399-2462, 542 words
  - preview: 'It does,' said I.  'That, then, which needs nothing outside itself, which can accomplish all things in its own strength, which enjoys fame and compels reverence, must not this evidently be also fully crowned with joy?'  'In sooth, I cannot conceive,' said I, 'how any sadness can find entrance into such a state; wherefore I must needs acknowledge it full of joy--at least, if our former conclusions are to hold.'  'Then, for the same reasons, this also is necessary--that independence, power, renow
- `BOETHIUS_CONSOLATION_001_CHUNK_025` — hybrid 0.830 — HIT | BM25 raw 8.333, BM25 norm 0.659 | vector raw 0.5718, vector norm 1.000
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — hybrid 0.821 — MISS | BM25 raw 11.291, BM25 norm 0.894 | vector raw 0.4630, vector norm 0.749
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_026` — hybrid 0.732 — HIT | BM25 raw 12.403, BM25 norm 0.982 | vector raw 0.3472, vector norm 0.482
  - lines 1877-1940, 507 words
  - preview: 'Thou hast, then, set before thine eyes something like a scheme of human happiness--wealth, rank, power, glory, pleasure. Now Epicurus, from a sole regard to these considerations, with some consistency concluded the highest good to be pleasure, because all the other objects seem to bring some delight to the soul. But to return to human pursuits and aims: man's mind seeks to recover its proper good, in spite of the mistiness of its recollection, but, like a drunken man, knows not by what path to 
- `BOETHIUS_CONSOLATION_001_CHUNK_033` — hybrid 0.662 — MISS | BM25 raw 8.006, BM25 norm 0.634 | vector raw 0.4371, vector norm 0.689
  - lines 2309-2397, 514 words
  - preview: Alas! how wide astray     Doth Ignorance these wretched mortals lead       From Truth's own way!       For not on leafy stems     Do ye within the green wood look for gold,       Nor strip the vine for gems;  Your nets ye do not spread     Upon the hill-tops, that the groaning board       With fish be furnishèd;       If ye are fain to chase     The bounding goat, ye sweep not in vain search       The ocean's ruffled face.  The sea's far depths they know,     Each hidden nook, wherein the waves 

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_034, BOETHIUS_CONSOLATION_001_CHUNK_025, BOETHIUS_CONSOLATION_001_CHUNK_026

Recall@5: 0.38

Precision@5: 0.60

Max possible Recall@5 for this question: 0.62

### Notes

Weak-to-partial result. Hybrid retrieval found some expected evidence, but missed most of the manual map.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_036` — hybrid 0.891 — HIT | BM25 raw 7.377, BM25 norm 1.000 | vector raw 0.5008, vector norm 0.782
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt
- `BOETHIUS_CONSOLATION_001_CHUNK_025` — hybrid 0.868 — HIT | BM25 raw 5.434, BM25 norm 0.737 | vector raw 0.6000, vector norm 1.000
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,
- `BOETHIUS_CONSOLATION_001_CHUNK_037` — hybrid 0.856 — HIT | BM25 raw 6.166, BM25 norm 0.836 | vector raw 0.5432, vector norm 0.875
  - lines 2618-2692, 551 words
  - preview: 'And most justly,' said I.  'But the highest good has been admitted to be happiness.'  'Yes.'  'Then,' said she, 'it is necessary to acknowledge that God is very happiness.'  'Yes,' said I; 'I cannot gainsay my former admissions, and I see clearly that this is a necessary inference therefrom.'  'Reflect, also,' said she, 'whether the same conclusion is not further confirmed by considering that there cannot be two supreme goods distinct one from the other. For the goods which are different clearl
- `BOETHIUS_CONSOLATION_001_CHUNK_016` — hybrid 0.681 — MISS | BM25 raw 5.598, BM25 norm 0.759 | vector raw 0.4196, vector norm 0.604
  - lines 1247-1303, 465 words
  - preview: 'Why, then, ye children of mortality, seek ye from without that happiness whose seat is only within us? Error and ignorance bewilder you. I will show thee, in brief, the hinge on which perfect happiness turns. Is there anything more precious to thee than thyself? Nothing, thou wilt say. If, then, thou art master of thyself, thou wilt possess that which thou wilt never be willing to lose, and which Fortune cannot take from thee. And that thou mayst see that happiness cannot possibly consist in th
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — hybrid 0.628 — MISS | BM25 raw 3.903, BM25 norm 0.529 | vector raw 0.4753, vector norm 0.726
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_036, BOETHIUS_CONSOLATION_001_CHUNK_025, BOETHIUS_CONSOLATION_001_CHUNK_037

Recall@5: 0.50

Precision@5: 0.60

Max possible Recall@5 for this question: 0.83

### Notes

Partial-to-good result. Hybrid retrieval found a meaningful portion of the expected evidence, but did not fully reproduce the manual evidence map.

---

## Q06

### Question

How does Philosophy distinguish providence from fate?

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_054`
- `BOETHIUS_CONSOLATION_001_CHUNK_055`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_055` — hybrid 1.000 — HIT | BM25 raw 7.480, BM25 norm 1.000 | vector raw 0.5186, vector norm 1.000
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta
- `BOETHIUS_CONSOLATION_001_CHUNK_054` — hybrid 0.890 — HIT | BM25 raw 6.678, BM25 norm 0.893 | vector raw 0.4823, vector norm 0.887
  - lines 3906-3958, 475 words
  - preview: Weak-minded folly magnifies       All that is rare and strange,     And the dull herd's o'erwhelmed with awe       At unexpected change.     But wonder leaves enlightened minds,     When ignorance no longer blinds.  FOOTNOTES:  [M] To frighten away the monster swallowing the moon. The superstition was once common. See Tylor's 'Primitive Culture,' pp. 296-302.  VI.  'True,' said I; 'but, since it is thy office to unfold the hidden cause of things, and explain principles veiled in darkness, inform
- `BOETHIUS_CONSOLATION_001_CHUNK_071` — hybrid 0.754 — MISS | BM25 raw 4.592, BM25 norm 0.614 | vector raw 0.4848, vector norm 0.895
  - lines 5031-5093, 722 words
  - preview: 'Since, then, every mode of judgment comprehends its objects conformably to its own nature, and since God abides for ever in an eternal present, His knowledge, also transcending all movement of time, dwells in the simplicity of its own changeless present, and, embracing the whole infinite sweep of the past and of the future, contemplates all that falls within its simple cognition as if it were now taking place. And therefore, if thou wilt carefully consider that immediate presentment whereby it 
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.720 — MISS | BM25 raw 4.075, BM25 norm 0.545 | vector raw 0.4846, vector norm 0.894
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_056` — hybrid 0.717 — MISS | BM25 raw 5.335, BM25 norm 0.713 | vector raw 0.4284, vector norm 0.720
  - lines 4017-4077, 639 words
  - preview: '"Yet what confusion," thou wilt say, "can be more unrighteous than that prosperity and adversity should indifferently befall the good, what they like and what they loathe come alternately to the bad!" Yes; but have men in real life such soundness of mind that their judgments of righteousness and wickedness must necessarily correspond with facts? Why, on this very point their verdicts conflict, and those whom some deem worthy of reward, others deem worthy of punishment. Yet granted there were on

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_055, BOETHIUS_CONSOLATION_001_CHUNK_054

Recall@5: 1.00

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. Hybrid retrieval found all manually expected chunks in the top 5.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_047` — hybrid 0.815 — HIT | BM25 raw 4.491, BM25 norm 0.630 | vector raw 0.5243, vector norm 1.000
  - lines 3393-3447, 646 words
  - preview: 'Go on,' said I; 'no one can question but that he who has the natural capacity has more strength than he who has it not.'  'Now, the supreme good is set up as the end alike for the bad and for the good; but the good seek it through the natural action of the virtues, whereas the bad try to attain this same good through all manner of concupiscence, which is not the natural way of attaining good. Or dost thou think otherwise?'  'Nay; rather, one further consequence is clear to me: for from my admis
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.705 — MISS | BM25 raw 4.791, BM25 norm 0.672 | vector raw 0.4375, vector norm 0.739
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_053` — hybrid 0.663 — MISS | BM25 raw 7.134, BM25 norm 1.000 | vector raw 0.3002, vector norm 0.326
  - lines 3832-3904, 528 words
  - preview: SONG IV.  THE UNREASONABLENESS OF HATRED.  Why all this furious strife? Oh, why     With rash and wilful hand provoke death's destined day?       If death ye seek--lo! Death is nigh,     Not of their master's will those coursers swift delay!  The wild beasts vent on man their rage,     Yet 'gainst their brothers' lives men point the murderous steel;       Unjust and cruel wars they wage,     And haste with flying darts the death to meet or deal.  No right nor reason can they show;     'Tis but b
- `BOETHIUS_CONSOLATION_001_CHUNK_057` — hybrid 0.651 — MISS | BM25 raw 5.193, BM25 norm 0.728 | vector raw 0.3824, vector norm 0.574
  - lines 4079-4126, 536 words
  - preview: 'As to the other side of the marvel, that the bad now meet with affliction, now get their hearts' desire, this, too, springs from the same causes. As to the afflictions, of course no one marvels, because all hold the wicked to be ill deserving. The truth is, their punishments both frighten others from crime, and amend those on whom they are inflicted; while their prosperity is a powerful sermon to the good, what judgments they ought to pass on good fortune of this kind, which often attends the w
- `BOETHIUS_CONSOLATION_001_CHUNK_046` — hybrid 0.621 — HIT | BM25 raw 3.284, BM25 norm 0.460 | vector raw 0.4517, vector norm 0.782
  - lines 3313-3391, 506 words
  - preview: 'The carrying out of any human action depends upon two things--to wit, will and power; if either be wanting, nothing can be accomplished. For if the will be lacking, no attempt at all is made to do what is not willed; whereas if there be no power, the will is all in vain. And so, if thou seest any man wishing to attain some end, yet utterly failing to attain it, thou canst not doubt that he lacked the power of getting what he wished for.'  'Why, certainly not; there is no denying it.'  'Canst th

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_047, BOETHIUS_CONSOLATION_001_CHUNK_046

Recall@5: 0.40

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Weak-to-partial result. Hybrid retrieval found some expected evidence, but missed most of the manual map.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_058` — hybrid 0.903 — HIT | BM25 raw 6.400, BM25 norm 0.935 | vector raw 0.4641, vector norm 0.871
  - lines 4128-4226, 518 words
  - preview: 'But I see thou hast long been burdened with the weight of the subject, and fatigued with the prolixity of the argument, and now lookest for some refreshment of sweet poesy. Listen, then, and may the draught so restore thee that thou wilt bend thy mind more resolutely to what remains.'  FOOTNOTES:  [N] Parmenides. Boethius seems to forget for the moment that Philosophy is speaking.  SONG VI.  THE UNIVERSAL AIM.  Wouldst thou with unclouded mind     View the laws by God designed,     Lift thy ste
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.785 — MISS | BM25 raw 3.905, BM25 norm 0.570 | vector raw 0.5038, vector norm 1.000
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — hybrid 0.751 — MISS | BM25 raw 5.080, BM25 norm 0.742 | vector raw 0.4300, vector norm 0.760
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_059` — hybrid 0.732 — HIT | BM25 raw 6.848, BM25 norm 1.000 | vector raw 0.3387, vector norm 0.463
  - lines 4228-4312, 507 words
  - preview: 'And why so?' said she.  'Because ordinary speech is apt to assert, and that frequently, that some men's fortune is bad.'  'Shall we, then, for awhile approach more nearly to the language of the vulgar, that we may not seem to have departed too far from the usages of men?'  'At thy good pleasure,' said I.  'That which advantageth thou callest good, dost thou not?'  'Certainly.'  'And that which either tries or amends advantageth?'  'Granted.'  'Is good, then?'  'Of course.'  'Well, this is _thei
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — hybrid 0.666 — MISS | BM25 raw 4.001, BM25 norm 0.584 | vector raw 0.4265, vector norm 0.749
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_058, BOETHIUS_CONSOLATION_001_CHUNK_059

Recall@5: 0.50

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. Hybrid retrieval found a meaningful portion of the expected evidence, but did not fully reproduce the manual evidence map.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_007` — hybrid 0.979 — MISS | BM25 raw 0.995, BM25 norm 0.962 | vector raw 0.4391, vector norm 0.995
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — hybrid 0.959 — MISS | BM25 raw 0.949, BM25 norm 0.917 | vector raw 0.4401, vector norm 1.000
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_064` — hybrid 0.876 — MISS | BM25 raw 0.939, BM25 norm 0.907 | vector raw 0.4082, vector norm 0.844
  - lines 4611-4667, 652 words
  - preview: 'Lastly, to think of a thing as being in any way other than what it is, is not only not knowledge, but it is false opinion widely different from the truth of knowledge. Consequently, if anything is about to be, and yet its occurrence is not certain and necessary, how can anyone foreknow that it will occur? For just as knowledge itself is free from all admixture of falsity, so any conception drawn from knowledge cannot be other than as it is conceived. For this, indeed, is the cause why knowledge
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — hybrid 0.838 — MISS | BM25 raw 0.958, BM25 norm 0.926 | vector raw 0.3889, vector norm 0.749
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — hybrid 0.832 — MISS | BM25 raw 0.788, BM25 norm 0.762 | vector raw 0.4204, vector norm 0.903
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen

### Retrieval Result

Hits: None

Recall@5: 0.00

Precision@5: 0.00

Max possible Recall@5 for this question: 0.83

### Notes

Weak result. Hybrid retrieval found none of the manually expected chunks in the top 5.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_007` — hybrid 0.951 — HIT | BM25 raw 4.588, BM25 norm 0.902 | vector raw 0.5137, vector norm 1.000
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_040` — hybrid 0.630 — MISS | BM25 raw 5.088, BM25 norm 1.000 | vector raw 0.2736, vector norm 0.259
  - lines 2832-2876, 511 words
  - preview: 'And yet there is no possibility of question about this either, since thou seest how herbs and trees grow in places suitable for them, where, as far as their nature admits, they cannot quickly wither and die. Some spring up in the plains, others in the mountains; some grow in marshes, others cling to rocks; and others, again, find a fertile soil in the barren sands; and if you try to transplant these elsewhere, they wither away. Nature gives to each the soil that suits it, and uses her diligence
- `BOETHIUS_CONSOLATION_001_CHUNK_001` — hybrid 0.582 — MISS | BM25 raw 2.500, BM25 norm 0.491 | vector raw 0.4077, vector norm 0.673
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — hybrid 0.562 — MISS | BM25 raw 4.434, BM25 norm 0.871 | vector raw 0.2717, vector norm 0.253
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_006` — hybrid 0.554 — HIT | BM25 raw 2.189, BM25 norm 0.430 | vector raw 0.4091, vector norm 0.677
  - lines 577-618, 518 words
  - preview: 'What need to speak of the forged letters by which an attempt is made to prove that I hoped for the freedom of Rome? Their falsity would have been manifest, if I had been allowed to use the confession of the informers themselves, evidence which has in all matters the most convincing force. Why, what hope of freedom is left to us? Would there were any! I should have answered with the epigram of Canius when Caligula declared him to have been cognisant of a conspiracy against him. "If I had known,"

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_007, BOETHIUS_CONSOLATION_001_CHUNK_006

Recall@5: 0.40

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Weak-to-partial result. Hybrid retrieval found some expected evidence, but missed most of the manual map.

---

# Overall Findings

Average Recall@5: 0.55

Average Precision@5: 0.36

## Interpretation

Hybrid retrieval combines exact-word lexical matching with semantic vector similarity.

A strong hybrid result would suggest that BM25 and vector retrieval complement each other. A weak hybrid result would suggest that weighting, query design, chunk quality, or the manual evidence map need further review.

The default weights are intentionally simple: 50 percent BM25 and 50 percent vector. This avoids tuning the result to a tiny eval set.

## Decision

Compare this result against the keyword, BM25, and vector baselines. Use the comparison to decide which retrieval method is strongest for the MVP.
