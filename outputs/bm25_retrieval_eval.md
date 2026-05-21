# BM25 Retrieval Evaluation

Date: 2026-05-21T13:02:33

Top K: 5

BM25 parameters: k1=1.5, b=0.75

## Goal

Evaluate a BM25 lexical retrieval baseline against the manual RAG chunk map.

This is a retrieval test, not an answer-generation test.

BM25 is a stronger lexical baseline than raw keyword counting because it accounts for term rarity, term frequency saturation, and document length.

---

## Q01

### Question

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

### Query Terms

`relationship`, `between`, `muses`, `poetry`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`
- `BOETHIUS_CONSOLATION_001_CHUNK_003`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001` — BM25 score 8.290 — HIT
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_057` — BM25 score 2.495 — MISS
  - lines 4079-4126, 536 words
  - preview: 'As to the other side of the marvel, that the bad now meet with affliction, now get their hearts' desire, this, too, springs from the same causes. As to the afflictions, of course no one marvels, because all hold the wicked to be ill deserving. The truth is, their punishments both frighten others from crime, and amend those on whom they are inflicted; while their prosperity is a powerful sermon to the good, what judgments they ought to pass on good fortune of this kind, which often attends the w
- `BOETHIUS_CONSOLATION_001_CHUNK_055` — BM25 score 2.332 — MISS
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta
- `BOETHIUS_CONSOLATION_001_CHUNK_064` — BM25 score 2.320 — MISS
  - lines 4611-4667, 652 words
  - preview: 'Lastly, to think of a thing as being in any way other than what it is, is not only not knowledge, but it is false opinion widely different from the truth of knowledge. Consequently, if anything is about to be, and yet its occurrence is not certain and necessary, how can anyone foreknow that it will occur? For just as knowledge itself is free from all admixture of falsity, so any conception drawn from knowledge cannot be other than as it is conceived. For this, indeed, is the cause why knowledge
- `BOETHIUS_CONSOLATION_001_CHUNK_071` — BM25 score 2.156 — MISS
  - lines 5031-5093, 722 words
  - preview: 'Since, then, every mode of judgment comprehends its objects conformably to its own nature, and since God abides for ever in an eternal present, His knowledge, also transcending all movement of time, dwells in the simplicity of its own changeless present, and, embracing the whole infinite sweep of the past and of the future, contemplates all that falls within its simple cognition as if it were now taking place. And therefore, if thou wilt carefully consider that immediate presentment whereby it 

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_001

Recall@5: 0.50

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. BM25 retrieved a meaningful portion of the manually expected evidence, but did not fully reproduce the manual evidence map.

---

## Q02

### Question

How does Boethius describe his own misery in the opening complaint?

### Query Terms

`misery`, `opening`, `complaint`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001` — BM25 score 3.497 — HIT
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_051` — BM25 score 3.334 — MISS
  - lines 3673-3750, 641 words
  - preview: Then said I: 'A wonderful inference, and difficult to grant; but I see that it agrees entirely with our previous conclusions.'  'Thou art right,' said she; 'but if anyone finds it hard to admit the conclusion, he ought in fairness either to prove some falsity in the premises, or to show that the combination of propositions does not adequately enforce the necessity of the conclusion; otherwise, if the premises be granted, nothing whatever can be said against the inference of the conclusion. And h
- `BOETHIUS_CONSOLATION_001_CHUNK_016` — BM25 score 2.199 — MISS
  - lines 1247-1303, 465 words
  - preview: 'Why, then, ye children of mortality, seek ye from without that happiness whose seat is only within us? Error and ignorance bewilder you. I will show thee, in brief, the hinge on which perfect happiness turns. Is there anything more precious to thee than thyself? Nothing, thou wilt say. If, then, thou art master of thyself, thou wilt possess that which thou wilt never be willing to lose, and which Fortune cannot take from thee. And that thou mayst see that happiness cannot possibly consist in th
- `BOETHIUS_CONSOLATION_001_CHUNK_053` — BM25 score 2.103 — MISS
  - lines 3832-3904, 528 words
  - preview: SONG IV.  THE UNREASONABLENESS OF HATRED.  Why all this furious strife? Oh, why     With rash and wilful hand provoke death's destined day?       If death ye seek--lo! Death is nigh,     Not of their master's will those coursers swift delay!  The wild beasts vent on man their rage,     Yet 'gainst their brothers' lives men point the murderous steel;       Unjust and cruel wars they wage,     And haste with flying darts the death to meet or deal.  No right nor reason can they show;     'Tis but b
- `BOETHIUS_CONSOLATION_001_CHUNK_030` — BM25 score 2.091 — MISS
  - lines 2126-2181, 523 words
  - preview: 'Well, then, does sovereignty and the intimacy of kings prove able to confer power? Why, surely does not the happiness of kings endure for ever? And yet antiquity is full of examples, and these days also, of kings whose happiness has turned into calamity. How glorious a power, which is not even found effectual for its own preservation! But if happiness has its source in sovereign power, is not happiness diminished, and misery inflicted in its stead, in so far as that power falls short of complet

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_001

Recall@5: 1.00

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. BM25 retrieved all manually expected chunks in the top 5. This suggests lexical retrieval is sufficient for this question.

---

## Q03

### Question

How does Philosophy describe the nature of Fortune?

### Query Terms

`nature`, `fortune`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_011`
- `BOETHIUS_CONSOLATION_001_CHUNK_012`
- `BOETHIUS_CONSOLATION_001_CHUNK_014`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_010` — BM25 score 2.335 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_011` — BM25 score 2.191 — HIT
  - lines 943-1005, 717 words
  - preview: BOOK II.  I.  Thereafter for awhile she remained silent; and when she had restored my flagging attention by a moderate pause in her discourse, she thus began: 'If I have thoroughly ascertained the character and causes of thy sickness, thou art pining with regretful longing for thy former fortune. It is the change, as thou deemest, of this fortune that hath so wrought upon thy mind. Well do I understand that Siren's manifold wiles, the fatal charm of the friendship she pretends for her victims, s
- `BOETHIUS_CONSOLATION_001_CHUNK_022` — BM25 score 2.146 — MISS
  - lines 1606-1698, 625 words
  - preview: SONG VII.  GLORY MAY NOT LAST.  Oh, let him, who pants for glory's guerdon,       Deeming glory all in all,     Look and see how wide the heaven expandeth,       Earth's enclosing bounds how small!  Shame it is, if your proud-swelling glory       May not fill this narrow room!     Why, then, strive so vainly, oh, ye proud ones!       To escape your mortal doom?  Though your name, to distant regions bruited,       O'er the earth be widely spread,     Though full many a lofty-sounding title       
- `BOETHIUS_CONSOLATION_001_CHUNK_057` — BM25 score 2.054 — MISS
  - lines 4079-4126, 536 words
  - preview: 'As to the other side of the marvel, that the bad now meet with affliction, now get their hearts' desire, this, too, springs from the same causes. As to the afflictions, of course no one marvels, because all hold the wicked to be ill deserving. The truth is, their punishments both frighten others from crime, and amend those on whom they are inflicted; while their prosperity is a powerful sermon to the good, what judgments they ought to pass on good fortune of this kind, which often attends the w
- `BOETHIUS_CONSOLATION_001_CHUNK_014` — BM25 score 1.974 — HIT
  - lines 1148-1210, 531 words
  - preview: SONG III.  ALL PASSES.  When, in rosy chariot drawn,     Phoebus 'gins to light the dawn,     By his flaming beams assailed,     Every glimmering star is paled.     When the grove, by Zephyrs fed,     With rose-blossom blushes red;--     Doth rude Auster breathe thereon,     Bare it stands, its glory gone.     Smooth and tranquil lies the deep     While the winds are hushed in sleep.     Soon, when angry tempests lash,     Wild and high the billows dash.     Thus if Nature's changing face     Ho

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_011, BOETHIUS_CONSOLATION_001_CHUNK_014

Recall@5: 0.67

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. BM25 retrieved a meaningful portion of the manually expected evidence, but did not fully reproduce the manual evidence map.

---

## Q04

### Question

Why does Philosophy argue that wealth, rank, power, glory, and pleasure cannot provide true happiness?

### Query Terms

`that`, `wealth`, `rank`, `power`, `glory`, `pleasure`, `true`, `happiness`

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

- `BOETHIUS_CONSOLATION_001_CHUNK_034` — BM25 score 12.636 — HIT
  - lines 2399-2462, 542 words
  - preview: 'It does,' said I.  'That, then, which needs nothing outside itself, which can accomplish all things in its own strength, which enjoys fame and compels reverence, must not this evidently be also fully crowned with joy?'  'In sooth, I cannot conceive,' said I, 'how any sadness can find entrance into such a state; wherefore I must needs acknowledge it full of joy--at least, if our former conclusions are to hold.'  'Then, for the same reasons, this also is necessary--that independence, power, renow
- `BOETHIUS_CONSOLATION_001_CHUNK_026` — BM25 score 12.403 — HIT
  - lines 1877-1940, 507 words
  - preview: 'Thou hast, then, set before thine eyes something like a scheme of human happiness--wealth, rank, power, glory, pleasure. Now Epicurus, from a sole regard to these considerations, with some consistency concluded the highest good to be pleasure, because all the other objects seem to bring some delight to the soul. But to return to human pursuits and aims: man's mind seeks to recover its proper good, in spite of the mistiness of its recollection, but, like a drunken man, knows not by what path to 
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — BM25 score 11.291 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_020` — BM25 score 8.628 — MISS
  - lines 1474-1549, 674 words
  - preview: 'Besides, if there were any element of natural and proper good in rank and power, they would never come to the utterly bad, since opposites are not wont to be associated. Nature brooks not the union of contraries. So, seeing there is no doubt that wicked wretches are oftentimes set in high places, it is also clear that things which suffer association with the worst of men cannot be good in their own nature. Indeed, this judgment may with some reason be passed concerning all the gifts of fortune 
- `BOETHIUS_CONSOLATION_001_CHUNK_025` — BM25 score 8.333 — HIT
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_034, BOETHIUS_CONSOLATION_001_CHUNK_026, BOETHIUS_CONSOLATION_001_CHUNK_025

Recall@5: 0.38

Precision@5: 0.60

Max possible Recall@5 for this question: 0.62

### Notes

Weak-to-partial result. BM25 retrieved some expected evidence, but missed most of the manual evidence map.

---

## Q05

### Question

What does Philosophy identify as true happiness or the highest good?

### Query Terms

`true`, `happiness`, `highest`, `good`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_025`
- `BOETHIUS_CONSOLATION_001_CHUNK_034`
- `BOETHIUS_CONSOLATION_001_CHUNK_035`
- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_036` — BM25 score 7.377 — HIT
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt
- `BOETHIUS_CONSOLATION_001_CHUNK_037` — BM25 score 6.166 — HIT
  - lines 2618-2692, 551 words
  - preview: 'And most justly,' said I.  'But the highest good has been admitted to be happiness.'  'Yes.'  'Then,' said she, 'it is necessary to acknowledge that God is very happiness.'  'Yes,' said I; 'I cannot gainsay my former admissions, and I see clearly that this is a necessary inference therefrom.'  'Reflect, also,' said she, 'whether the same conclusion is not further confirmed by considering that there cannot be two supreme goods distinct one from the other. For the goods which are different clearl
- `BOETHIUS_CONSOLATION_001_CHUNK_026` — BM25 score 5.634 — MISS
  - lines 1877-1940, 507 words
  - preview: 'Thou hast, then, set before thine eyes something like a scheme of human happiness--wealth, rank, power, glory, pleasure. Now Epicurus, from a sole regard to these considerations, with some consistency concluded the highest good to be pleasure, because all the other objects seem to bring some delight to the soul. But to return to human pursuits and aims: man's mind seeks to recover its proper good, in spite of the mistiness of its recollection, but, like a drunken man, knows not by what path to 
- `BOETHIUS_CONSOLATION_001_CHUNK_016` — BM25 score 5.598 — MISS
  - lines 1247-1303, 465 words
  - preview: 'Why, then, ye children of mortality, seek ye from without that happiness whose seat is only within us? Error and ignorance bewilder you. I will show thee, in brief, the hinge on which perfect happiness turns. Is there anything more precious to thee than thyself? Nothing, thou wilt say. If, then, thou art master of thyself, thou wilt possess that which thou wilt never be willing to lose, and which Fortune cannot take from thee. And that thou mayst see that happiness cannot possibly consist in th
- `BOETHIUS_CONSOLATION_001_CHUNK_025` — BM25 score 5.434 — HIT
  - lines 1836-1875, 498 words
  - preview: 'All mortal creatures in those anxious aims which find employment in so many varied pursuits, though they take many paths, yet strive to reach one goal--the goal of happiness. Now, _the good_ is that which, when a man hath got, he can lack nothing further. This it is which is the supreme good of all, containing within itself all particular good; so that if anything is still wanting thereto, this cannot be the supreme good, since something would be left outside which might be desired. 'Tis clear,

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_036, BOETHIUS_CONSOLATION_001_CHUNK_037, BOETHIUS_CONSOLATION_001_CHUNK_025

Recall@5: 0.50

Precision@5: 0.60

Max possible Recall@5 for this question: 0.83

### Notes

Partial-to-good result. BM25 retrieved a meaningful portion of the manually expected evidence, but did not fully reproduce the manual evidence map.

---

## Q06

### Question

How does Philosophy distinguish providence from fate?

### Query Terms

`distinguish`, `providence`, `fate`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_054`
- `BOETHIUS_CONSOLATION_001_CHUNK_055`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_055` — BM25 score 7.480 — HIT
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta
- `BOETHIUS_CONSOLATION_001_CHUNK_054` — BM25 score 6.678 — HIT
  - lines 3906-3958, 475 words
  - preview: Weak-minded folly magnifies       All that is rare and strange,     And the dull herd's o'erwhelmed with awe       At unexpected change.     But wonder leaves enlightened minds,     When ignorance no longer blinds.  FOOTNOTES:  [M] To frighten away the monster swallowing the moon. The superstition was once common. See Tylor's 'Primitive Culture,' pp. 296-302.  VI.  'True,' said I; 'but, since it is thy office to unfold the hidden cause of things, and explain principles veiled in darkness, inform
- `BOETHIUS_CONSOLATION_001_CHUNK_056` — BM25 score 5.335 — MISS
  - lines 4017-4077, 639 words
  - preview: '"Yet what confusion," thou wilt say, "can be more unrighteous than that prosperity and adversity should indifferently befall the good, what they like and what they loathe come alternately to the bad!" Yes; but have men in real life such soundness of mind that their judgments of righteousness and wickedness must necessarily correspond with facts? Why, on this very point their verdicts conflict, and those whom some deem worthy of reward, others deem worthy of punishment. Yet granted there were on
- `BOETHIUS_CONSOLATION_001_CHUNK_071` — BM25 score 4.592 — MISS
  - lines 5031-5093, 722 words
  - preview: 'Since, then, every mode of judgment comprehends its objects conformably to its own nature, and since God abides for ever in an eternal present, His knowledge, also transcending all movement of time, dwells in the simplicity of its own changeless present, and, embracing the whole infinite sweep of the past and of the future, contemplates all that falls within its simple cognition as if it were now taking place. And therefore, if thou wilt carefully consider that immediate presentment whereby it 
- `BOETHIUS_CONSOLATION_001_CHUNK_060` — BM25 score 4.376 — MISS
  - lines 4314-4391, 579 words
  - preview: But blinded soon, and wild with pain--       In bitter tears and sore annoy--       For that foul feast's unholy joy     Grim Polyphemus paid again.  His labours for Alcides win       A name of glory far and wide;       He tamed the Centaur's haughty pride,     And from the lion reft his skin.  The foul birds with sure darts he slew;       The golden fruit he stole--in vain       The dragon's watch; with triple chain     From hell's depths Cerberus he drew.  With their fierce lord's own flesh he

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_055, BOETHIUS_CONSOLATION_001_CHUNK_054

Recall@5: 1.00

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Strong result. BM25 retrieved all manually expected chunks in the top 5. This suggests lexical retrieval is sufficient for this question.

---

## Q07

### Question

Why does Philosophy argue that wicked people are weak rather than powerful?

### Query Terms

`that`, `wicked`, `people`, `weak`, `powerful`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_045`
- `BOETHIUS_CONSOLATION_001_CHUNK_046`
- `BOETHIUS_CONSOLATION_001_CHUNK_047`
- `BOETHIUS_CONSOLATION_001_CHUNK_048`
- `BOETHIUS_CONSOLATION_001_CHUNK_049`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_053` — BM25 score 7.134 — MISS
  - lines 3832-3904, 528 words
  - preview: SONG IV.  THE UNREASONABLENESS OF HATRED.  Why all this furious strife? Oh, why     With rash and wilful hand provoke death's destined day?       If death ye seek--lo! Death is nigh,     Not of their master's will those coursers swift delay!  The wild beasts vent on man their rage,     Yet 'gainst their brothers' lives men point the murderous steel;       Unjust and cruel wars they wage,     And haste with flying darts the death to meet or deal.  No right nor reason can they show;     'Tis but b
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — BM25 score 5.699 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_057` — BM25 score 5.193 — MISS
  - lines 4079-4126, 536 words
  - preview: 'As to the other side of the marvel, that the bad now meet with affliction, now get their hearts' desire, this, too, springs from the same causes. As to the afflictions, of course no one marvels, because all hold the wicked to be ill deserving. The truth is, their punishments both frighten others from crime, and amend those on whom they are inflicted; while their prosperity is a powerful sermon to the good, what judgments they ought to pass on good fortune of this kind, which often attends the w
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — BM25 score 4.791 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_030` — BM25 score 4.712 — MISS
  - lines 2126-2181, 523 words
  - preview: 'Well, then, does sovereignty and the intimacy of kings prove able to confer power? Why, surely does not the happiness of kings endure for ever? And yet antiquity is full of examples, and these days also, of kings whose happiness has turned into calamity. How glorious a power, which is not even found effectual for its own preservation! But if happiness has its source in sovereign power, is not happiness diminished, and misery inflicted in its stead, in so far as that power falls short of complet

### Retrieval Result

Hits: None

Recall@5: 0.00

Precision@5: 0.00

Max possible Recall@5 for this question: 1.00

### Notes

Weak result. BM25 retrieved none of the manually expected chunks in the top 5. This suggests lexical retrieval is not enough for this question.

---

## Q08

### Question

In what sense does Philosophy claim that every fortune is good fortune?

### Query Terms

`that`, `every`, `fortune`, `good`, `fortune`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_056`
- `BOETHIUS_CONSOLATION_001_CHUNK_057`
- `BOETHIUS_CONSOLATION_001_CHUNK_058`
- `BOETHIUS_CONSOLATION_001_CHUNK_059`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_059` — BM25 score 6.848 — HIT
  - lines 4228-4312, 507 words
  - preview: 'And why so?' said she.  'Because ordinary speech is apt to assert, and that frequently, that some men's fortune is bad.'  'Shall we, then, for awhile approach more nearly to the language of the vulgar, that we may not seem to have departed too far from the usages of men?'  'At thy good pleasure,' said I.  'That which advantageth thou callest good, dost thou not?'  'Certainly.'  'And that which either tries or amends advantageth?'  'Granted.'  'Is good, then?'  'Of course.'  'Well, this is _thei
- `BOETHIUS_CONSOLATION_001_CHUNK_058` — BM25 score 6.400 — HIT
  - lines 4128-4226, 518 words
  - preview: 'But I see thou hast long been burdened with the weight of the subject, and fatigued with the prolixity of the argument, and now lookest for some refreshment of sweet poesy. Listen, then, and may the draught so restore thee that thou wilt bend thy mind more resolutely to what remains.'  FOOTNOTES:  [N] Parmenides. Boethius seems to forget for the moment that Philosophy is speaking.  SONG VI.  THE UNIVERSAL AIM.  Wouldst thou with unclouded mind     View the laws by God designed,     Lift thy ste
- `BOETHIUS_CONSOLATION_001_CHUNK_022` — BM25 score 5.780 — MISS
  - lines 1606-1698, 625 words
  - preview: SONG VII.  GLORY MAY NOT LAST.  Oh, let him, who pants for glory's guerdon,       Deeming glory all in all,     Look and see how wide the heaven expandeth,       Earth's enclosing bounds how small!  Shame it is, if your proud-swelling glory       May not fill this narrow room!     Why, then, strive so vainly, oh, ye proud ones!       To escape your mortal doom?  Though your name, to distant regions bruited,       O'er the earth be widely spread,     Though full many a lofty-sounding title       
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — BM25 score 5.080 — MISS
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_014` — BM25 score 4.599 — MISS
  - lines 1148-1210, 531 words
  - preview: SONG III.  ALL PASSES.  When, in rosy chariot drawn,     Phoebus 'gins to light the dawn,     By his flaming beams assailed,     Every glimmering star is paled.     When the grove, by Zephyrs fed,     With rose-blossom blushes red;--     Doth rude Auster breathe thereon,     Bare it stands, its glory gone.     Smooth and tranquil lies the deep     While the winds are hushed in sleep.     Soon, when angry tempests lash,     Wild and high the billows dash.     Thus if Nature's changing face     Ho

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_059, BOETHIUS_CONSOLATION_001_CHUNK_058

Recall@5: 0.50

Precision@5: 0.40

Max possible Recall@5 for this question: 1.00

### Notes

Partial-to-good result. BM25 retrieved a meaningful portion of the manually expected evidence, but did not fully reproduce the manual evidence map.

---

## Q09

### Question

Based only on the selected Boethius chunks, can we say whether the work is explicitly Christian?

### Query Terms

`only`, `explicitly`, `christian`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`
- `BOETHIUS_CONSOLATION_001_CHUNK_043`
- `BOETHIUS_CONSOLATION_001_CHUNK_071`
- `BOETHIUS_CONSOLATION_001_CHUNK_072`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_047` — BM25 score 1.035 — MISS
  - lines 3393-3447, 646 words
  - preview: 'Go on,' said I; 'no one can question but that he who has the natural capacity has more strength than he who has it not.'  'Now, the supreme good is set up as the end alike for the bad and for the good; but the good seek it through the natural action of the virtues, whereas the bad try to attain this same good through all manner of concupiscence, which is not the natural way of attaining good. Or dost thou think otherwise?'  'Nay; rather, one further consequence is clear to me: for from my admis
- `BOETHIUS_CONSOLATION_001_CHUNK_007` — BM25 score 0.995 — MISS
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_044` — BM25 score 0.958 — MISS
  - lines 3154-3232, 578 words
  - preview: At length the shadowy king,     His sorrows pitying,     'He hath prevailèd!' cried;     'We give him back his bride!     To him she shall belong,     As guerdon of his song.     One sole condition yet     Upon the boon is set:     Let him not turn his eyes     To view his hard-won prize,     Till they securely pass     The gates of Hell.' Alas!     What law can lovers move?     A higher law is love!     For Orpheus--woe is me!--     On his Eurydice--     Day's threshold all but won--     Looked
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — BM25 score 0.949 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_064` — BM25 score 0.939 — MISS
  - lines 4611-4667, 652 words
  - preview: 'Lastly, to think of a thing as being in any way other than what it is, is not only not knowledge, but it is false opinion widely different from the truth of knowledge. Consequently, if anything is about to be, and yet its occurrence is not certain and necessary, how can anyone foreknow that it will occur? For just as knowledge itself is free from all admixture of falsity, so any conception drawn from knowledge cannot be other than as it is conceived. For this, indeed, is the cause why knowledge

### Retrieval Result

Hits: None

Recall@5: 0.00

Precision@5: 0.00

Max possible Recall@5 for this question: 0.83

### Notes

Weak result. BM25 retrieved none of the manually expected chunks in the top 5. This suggests lexical retrieval is not enough for this question.

---

## Q10

### Question

Based only on the selected Boethius chunks, what can we safely say about the historical circumstances of Boethius’ imprisonment and death?

### Query Terms

`only`, `historical`, `circumstances`, `imprisonment`, `death`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_004`
- `BOETHIUS_CONSOLATION_001_CHUNK_005`
- `BOETHIUS_CONSOLATION_001_CHUNK_006`
- `BOETHIUS_CONSOLATION_001_CHUNK_007`
- `BOETHIUS_CONSOLATION_001_CHUNK_008`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_040` — BM25 score 5.088 — MISS
  - lines 2832-2876, 511 words
  - preview: 'And yet there is no possibility of question about this either, since thou seest how herbs and trees grow in places suitable for them, where, as far as their nature admits, they cannot quickly wither and die. Some spring up in the plains, others in the mountains; some grow in marshes, others cling to rocks; and others, again, find a fertile soil in the barren sands; and if you try to transplant these elsewhere, they wither away. Nature gives to each the soil that suits it, and uses her diligence
- `BOETHIUS_CONSOLATION_001_CHUNK_007` — BM25 score 4.588 — HIT
  - lines 620-674, 502 words
  - preview: 'Yet even my very accusers saw how honourable was the charge they brought against me, and, in order to overlay it with some shadow of guilt, they falsely asserted that in the pursuit of my ambition I had stained my conscience with sacrilegious acts. And yet thy spirit, indwelling in me, had driven from the chamber of my soul all lust of earthly success, and with thine eye ever upon me, there could be no place left for sacrilege. For thou didst daily repeat in my ear and instil into my mind the P
- `BOETHIUS_CONSOLATION_001_CHUNK_015` — BM25 score 4.434 — MISS
  - lines 1212-1245, 398 words
  - preview: 'We are gaining a little ground,' said she, 'if there is something in thy lot wherewith thou art not yet altogether discontented. But I cannot stomach thy daintiness when thou complainest with such violence of grief and anxiety because thy happiness falls short of completeness. Why, who enjoys such settled felicity as not to have some quarrel with the circumstances of his lot? A troublous matter are the conditions of human bliss; either they are never realized in full, or never stay permanently.
- `BOETHIUS_CONSOLATION_001_CHUNK_026` — BM25 score 4.063 — MISS
  - lines 1877-1940, 507 words
  - preview: 'Thou hast, then, set before thine eyes something like a scheme of human happiness--wealth, rank, power, glory, pleasure. Now Epicurus, from a sole regard to these considerations, with some consistency concluded the highest good to be pleasure, because all the other objects seem to bring some delight to the soul. But to return to human pursuits and aims: man's mind seeks to recover its proper good, in spite of the mistiness of its recollection, but, like a drunken man, knows not by what path to 
- `BOETHIUS_CONSOLATION_001_CHUNK_014` — BM25 score 3.568 — MISS
  - lines 1148-1210, 531 words
  - preview: SONG III.  ALL PASSES.  When, in rosy chariot drawn,     Phoebus 'gins to light the dawn,     By his flaming beams assailed,     Every glimmering star is paled.     When the grove, by Zephyrs fed,     With rose-blossom blushes red;--     Doth rude Auster breathe thereon,     Bare it stands, its glory gone.     Smooth and tranquil lies the deep     While the winds are hushed in sleep.     Soon, when angry tempests lash,     Wild and high the billows dash.     Thus if Nature's changing face     Ho

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_007

Recall@5: 0.20

Precision@5: 0.20

Max possible Recall@5 for this question: 1.00

### Notes

Weak-to-partial result. BM25 retrieved some expected evidence, but missed most of the manual evidence map.

---

# Overall Findings

Average Recall@5: 0.47

Average Precision@5: 0.30

## Interpretation

BM25 provides a stronger lexical retrieval baseline than raw keyword counting.

A high Recall@5 would mean the retriever usually gets the manually expected evidence into the model context. A low Recall@5 means the retriever is missing expected evidence and should not be trusted as the final retrieval method.

Precision@5 helps identify how much extra noise appears in the retrieved context. Recall asks whether the right chunks were found; precision asks how much of the retrieved set was actually expected evidence.

## Decision

Use BM25 as the serious lexical baseline for the MVP. Compare it against the earlier simple keyword-count baseline. If BM25 still performs poorly on interpretive questions, the next retrieval improvement should be semantic or hybrid retrieval.
