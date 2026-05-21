# Keyword Retrieval Evaluation

Date: 2026-05-21T12:39:31

Top K: 5

## Goal

Evaluate a simple keyword retrieval baseline against the manual RAG chunk map.

This tests whether a basic keyword search can retrieve the same chunks that were manually selected as relevant evidence.

This is a retrieval test, not an answer-generation test.

---

## Q01

### Question

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

### Query Terms

`relationship`, `between`, `muses`, `poetry`, `beginning`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`
- `BOETHIUS_CONSOLATION_001_CHUNK_003`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001` — score 4 — HIT
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the
- `BOETHIUS_CONSOLATION_001_CHUNK_035` — score 2 — MISS
  - lines 2464-2545, 518 words
  - preview: 'Happy art thou, my scholar, in this thy conviction; only one thing shouldst thou add.'  'What is that?' said I.  'Is there aught, thinkest thou, amid these mortal and perishable things which can produce a state such as this?'  'Nay, surely not; and this thou hast so amply demonstrated that no word more is needed.'  'Well, then, these things seem to give to mortals shadows of the true good, or some kind of imperfect good; but the true and perfect good they cannot bestow.'  'Even so,' said I.  'S
- `BOETHIUS_CONSOLATION_001_CHUNK_055` — score 2 — MISS
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta
- `BOETHIUS_CONSOLATION_001_CHUNK_070` — score 2 — MISS
  - lines 4985-5029, 557 words
  - preview: 'God is eternal; in this judgment all rational beings agree. Let us, then, consider what eternity is. For this word carries with it a revelation alike of the Divine nature and of the Divine knowledge. Now, eternity is the possession of endless life whole and perfect at a single moment. What this is becomes more clear and manifest from a comparison with things temporal. For whatever lives in time is a present proceeding from the past to the future, and there is nothing set in time which can embra
- `BOETHIUS_CONSOLATION_001_CHUNK_013` — score 1 — MISS
  - lines 1069-1146, 682 words
  - preview: SONG II.  MAN'S COVETOUSNESS.  What though Plenty pour her gifts       With a lavish hand,     Numberless as are the stars,       Countless as the sand,     Will the race of man, content,     Cease to murmur and lament?  Nay, though God, all-bounteous, give       Gold at man's desire--     Honours, rank, and fame--content       Not a whit is nigher;     But an all-devouring greed     Yawns with ever-widening need.  Then what bounds can e'er restrain       This wild lust of having,     When with 

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_001

Recall@5: 0.50

### Notes

Partial success.

Keyword retrieval found `BOETHIUS_CONSOLATION_001_CHUNK_001`, which is one of the two manually expected chunks. It missed `BOETHIUS_CONSOLATION_001_CHUNK_003`, which is important because that chunk helps explicitly identify the female figure as Philosophy.

The misses are mostly lexical false positives. They contain some overlapping words such as "between" or other common terms, but they are not strong evidence for the Philosophy/Muses relationship.

Takeaway: keyword retrieval can find the obvious opening chunk, but it missed a context-supporting chunk that matters for interpretation.

---

## Q02

### Question

How does Boethius describe his own misery in the opening complaint?

### Query Terms

`describe`, `his`, `own`, `misery`, `opening`, `complaint`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_001`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_030` — score 20 — MISS
  - lines 2126-2181, 523 words
  - preview: 'Well, then, does sovereignty and the intimacy of kings prove able to confer power? Why, surely does not the happiness of kings endure for ever? And yet antiquity is full of examples, and these days also, of kings whose happiness has turned into calamity. How glorious a power, which is not even found effectual for its own preservation! But if happiness has its source in sovereign power, is not happiness diminished, and misery inflicted in its stead, in so far as that power falls short of complet
- `BOETHIUS_CONSOLATION_001_CHUNK_060` — score 18 — MISS
  - lines 4314-4391, 579 words
  - preview: But blinded soon, and wild with pain--       In bitter tears and sore annoy--       For that foul feast's unholy joy     Grim Polyphemus paid again.  His labours for Alcides win       A name of glory far and wide;       He tamed the Centaur's haughty pride,     And from the lion reft his skin.  The foul birds with sure darts he slew;       The golden fruit he stole--in vain       The dragon's watch; with triple chain     From hell's depths Cerberus he drew.  With their fierce lord's own flesh he
- `BOETHIUS_CONSOLATION_001_CHUNK_071` — score 18 — MISS
  - lines 5031-5093, 722 words
  - preview: 'Since, then, every mode of judgment comprehends its objects conformably to its own nature, and since God abides for ever in an eternal present, His knowledge, also transcending all movement of time, dwells in the simplicity of its own changeless present, and, embracing the whole infinite sweep of the past and of the future, contemplates all that falls within its simple cognition as if it were now taking place. And therefore, if thou wilt carefully consider that immediate presentment whereby it 
- `BOETHIUS_CONSOLATION_001_CHUNK_004` — score 17 — MISS
  - lines 463-541, 686 words
  - preview: SONG IV.  NOTHING CAN SUBDUE VIRTUE.  Whoso calm, serene, sedate,     Sets his foot on haughty fate;     Firm and steadfast, come what will,     Keeps his mien unconquered still;     Him the rage of furious seas,     Tossing high wild menaces,     Nor the flames from smoky forges     That Vesuvius disgorges,     Nor the bolt that from the sky     Smites the tower, can terrify.     Why, then, shouldst thou feel affright     At the tyrant's weakling might?     Dread him not, nor fear no harm,     
- `BOETHIUS_CONSOLATION_001_CHUNK_008` — score 17 — MISS
  - lines 676-770, 747 words
  - preview: 'Who at fall of eventide,       Hesper, his cold radiance showeth,     Lucifer his beams doth hide,       Paling as the sun's light groweth,         Brief, while winter's frost holds sway,         By thy will the space of day;       Swift, when summer's fervour gloweth,         Speed the hours of night away.  'Thou dost rule the changing year:       When rude Boreas oppresses,     Fall the leaves; they reappear,       Wooed by Zephyr's soft caresses.         Fields that Sirius burns deep grown  

### Retrieval Result

Hits: None

Recall@5: 0.00

### Notes

Weak result.

Keyword retrieval found none of the manually expected chunks. This is a useful failure. The correct expected chunk is `BOETHIUS_CONSOLATION_001_CHUNK_001`, but the keyword scoring was pulled toward other chunks containing terms like "misery", "death", "happiness", or related emotional language.

This shows that exact keyword frequency does not reliably identify the right evidence when a question asks about a specific scene or passage.

Takeaway: high lexical overlap can produce false positives. The manually expected chunk was selected by context, not by raw keyword count.

---

## Q03

### Question

How does Philosophy describe the nature of Fortune?

### Query Terms

`describe`, `nature`, `fortune`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_011`
- `BOETHIUS_CONSOLATION_001_CHUNK_012`
- `BOETHIUS_CONSOLATION_001_CHUNK_014`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_010` — score 13 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_014` — score 11 — HIT
  - lines 1148-1210, 531 words
  - preview: SONG III.  ALL PASSES.  When, in rosy chariot drawn,     Phoebus 'gins to light the dawn,     By his flaming beams assailed,     Every glimmering star is paled.     When the grove, by Zephyrs fed,     With rose-blossom blushes red;--     Doth rude Auster breathe thereon,     Bare it stands, its glory gone.     Smooth and tranquil lies the deep     While the winds are hushed in sleep.     Soon, when angry tempests lash,     Wild and high the billows dash.     Thus if Nature's changing face     Ho
- `BOETHIUS_CONSOLATION_001_CHUNK_011` — score 10 — HIT
  - lines 943-1005, 717 words
  - preview: BOOK II.  I.  Thereafter for awhile she remained silent; and when she had restored my flagging attention by a moderate pause in her discourse, she thus began: 'If I have thoroughly ascertained the character and causes of thy sickness, thou art pining with regretful longing for thy former fortune. It is the change, as thou deemest, of this fortune that hath so wrought upon thy mind. Well do I understand that Siren's manifold wiles, the fatal charm of the friendship she pretends for her victims, s
- `BOETHIUS_CONSOLATION_001_CHUNK_022` — score 10 — MISS
  - lines 1606-1698, 625 words
  - preview: SONG VII.  GLORY MAY NOT LAST.  Oh, let him, who pants for glory's guerdon,       Deeming glory all in all,     Look and see how wide the heaven expandeth,       Earth's enclosing bounds how small!  Shame it is, if your proud-swelling glory       May not fill this narrow room!     Why, then, strive so vainly, oh, ye proud ones!       To escape your mortal doom?  Though your name, to distant regions bruited,       O'er the earth be widely spread,     Though full many a lofty-sounding title       
- `BOETHIUS_CONSOLATION_001_CHUNK_059` — score 10 — MISS
  - lines 4228-4312, 507 words
  - preview: 'And why so?' said she.  'Because ordinary speech is apt to assert, and that frequently, that some men's fortune is bad.'  'Shall we, then, for awhile approach more nearly to the language of the vulgar, that we may not seem to have departed too far from the usages of men?'  'At thy good pleasure,' said I.  'That which advantageth thou callest good, dost thou not?'  'Certainly.'  'And that which either tries or amends advantageth?'  'Granted.'  'Is good, then?'  'Of course.'  'Well, this is _thei

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_014, BOETHIUS_CONSOLATION_001_CHUNK_011

Recall@5: 0.67

### Notes

Partial success.

Keyword retrieval found two of the three manually expected chunks: `BOETHIUS_CONSOLATION_001_CHUNK_014` and `BOETHIUS_CONSOLATION_001_CHUNK_011`. It missed `BOETHIUS_CONSOLATION_001_CHUNK_012`, which is also relevant because it contains Fortune's imagined defense.

This is a decent baseline result. The question uses the term "Fortune", and the source passages also use that term heavily, so keyword retrieval performs better here than on more interpretive questions.

Takeaway: keyword retrieval works better when the question shares distinctive vocabulary with the source.

---

## Q04

### Question

Why does Philosophy argue that wealth, rank, power, glory, and pleasure cannot provide true happiness?

### Query Terms

`argue`, `that`, `wealth`, `rank`, `power`, `glory`, `pleasure`, `cannot`, `provide`, `true`, `happiness`

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

- `BOETHIUS_CONSOLATION_001_CHUNK_034` — score 34 — HIT
  - lines 2399-2462, 542 words
  - preview: 'It does,' said I.  'That, then, which needs nothing outside itself, which can accomplish all things in its own strength, which enjoys fame and compels reverence, must not this evidently be also fully crowned with joy?'  'In sooth, I cannot conceive,' said I, 'how any sadness can find entrance into such a state; wherefore I must needs acknowledge it full of joy--at least, if our former conclusions are to hold.'  'Then, for the same reasons, this also is necessary--that independence, power, renow
- `BOETHIUS_CONSOLATION_001_CHUNK_037` — score 33 — MISS
  - lines 2618-2692, 551 words
  - preview: 'And most justly,' said I.  'But the highest good has been admitted to be happiness.'  'Yes.'  'Then,' said she, 'it is necessary to acknowledge that God is very happiness.'  'Yes,' said I; 'I cannot gainsay my former admissions, and I see clearly that this is a necessary inference therefrom.'  'Reflect, also,' said she, 'whether the same conclusion is not further confirmed by considering that there cannot be two supreme goods distinct one from the other. For the goods which are different clearl
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — score 31 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_036` — score 31 — MISS
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt
- `BOETHIUS_CONSOLATION_001_CHUNK_063` — score 31 — MISS
  - lines 4545-4609, 665 words
  - preview: All that is, hath been, shall be,     In one glance's compass, He       Limitless descries;       And, save His, no eyes     All the world survey--no, none!     _Him_, then, truly name the Sun.  III.  Then said I: 'But now I am once more perplexed by a problem yet more difficult.'  'And what is that?' said she; 'yet, in truth, I can guess what it is that troubles you.'  'It seems,' said I, 'too much of a paradox and a contradiction that God should know all things, and yet there should be free wi

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_034

Recall@5: 0.12

### Notes

Weak result.

Keyword retrieval found only one of the eight manually expected chunks. The question asks for a broad synthesis across several false goods: wealth, rank, power, glory, pleasure, and true happiness. A simple top-5 keyword search is too narrow for that kind of multi-part conceptual question.

Several high-scoring misses contain terms like "good", "happiness", "power", or related vocabulary, but they do not cover the full expected evidence map.

Takeaway: keyword retrieval struggles with broad synthesis questions that require evidence spread across many chunks.

---

## Q05

### Question

What does Philosophy identify as true happiness or the highest good?

### Query Terms

`identify`, `true`, `happiness`, `highest`, `good`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_025`
- `BOETHIUS_CONSOLATION_001_CHUNK_034`
- `BOETHIUS_CONSOLATION_001_CHUNK_035`
- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_036` — score 30 — HIT
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt
- `BOETHIUS_CONSOLATION_001_CHUNK_037` — score 28 — HIT
  - lines 2618-2692, 551 words
  - preview: 'And most justly,' said I.  'But the highest good has been admitted to be happiness.'  'Yes.'  'Then,' said she, 'it is necessary to acknowledge that God is very happiness.'  'Yes,' said I; 'I cannot gainsay my former admissions, and I see clearly that this is a necessary inference therefrom.'  'Reflect, also,' said she, 'whether the same conclusion is not further confirmed by considering that there cannot be two supreme goods distinct one from the other. For the goods which are different clearl
- `BOETHIUS_CONSOLATION_001_CHUNK_023` — score 23 — MISS
  - lines 1700-1765, 598 words
  - preview: Tribes and nations Love unites     By just treaty's sacred rites;     Wedlock's bonds he sanctifies     By affection's softest ties.     Love appointeth, as is due,     Faithful laws to comrades true--     Love, all-sovereign Love!--oh, then,     Ye are blest, ye sons of men,     If the love that rules the sky     In your hearts is throned on high!  BOOK III.  TRUE HAPPINESS AND FALSE.  SUMMARY  CH. I. Boethius beseeches Philosophy to continue. She promises to      lead him to true happiness.--C
- `BOETHIUS_CONSOLATION_001_CHUNK_049` — score 21 — MISS
  - lines 3517-3578, 746 words
  - preview: 'Thou seest, then, in what foulness unrighteous deeds are sunk, with what splendour righteousness shines. Whereby it is manifest that goodness never lacks its reward, nor crime its punishment. For, verily, in all manner of transactions that for the sake of which the particular action is done may justly be accounted the reward of that action, even as the wreath for the sake of which the race is run is the reward offered for running. Now, we have shown happiness to be that very good for the sake o
- `BOETHIUS_CONSOLATION_001_CHUNK_038` — score 20 — HIT
  - lines 2694-2768, 517 words
  - preview: 'There can be no doubt as to that,' said I; 'but I am impatient to hear what remains.'  'Why, it is manifest that all the others are relative to the good. For the very reason why independence is sought is that it is judged good, and so power also, because it is believed to be good. The same, too, may be supposed of reverence, of renown, and of pleasant delight. Good, then, is the sum and source of all desirable things. That which has not in itself any good, either in reality or in semblance, can

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_036, BOETHIUS_CONSOLATION_001_CHUNK_037, BOETHIUS_CONSOLATION_001_CHUNK_038

Recall@5: 0.50

### Notes

Partial success.

Keyword retrieval found three expected chunks: `BOETHIUS_CONSOLATION_001_CHUNK_036`, `BOETHIUS_CONSOLATION_001_CHUNK_037`, and `BOETHIUS_CONSOLATION_001_CHUNK_038`. This is a useful result because the question's key terms — "true", "happiness", "highest", and "good" — overlap strongly with the relevant source passages.

However, it still missed several expected chunks that help build the full argument.

Takeaway: keyword retrieval is useful when the source and question share core terms, but it still gives an incomplete evidence set.

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

- `BOETHIUS_CONSOLATION_001_CHUNK_055` — score 21 — HIT
  - lines 3960-4015, 659 words
  - preview: 'So the unfolding of this temporal order unified into the foreview of the Divine mind is providence, while the same unity broken up and unfolded in time is fate. And although these are different, yet is there a dependence between them; for the order of destiny issues from the essential simplicity of providence. For as the artificer, forming in his mind beforehand the idea of the thing to be made, carries out his design, and develops from moment to moment what he had before seen in a single insta
- `BOETHIUS_CONSOLATION_001_CHUNK_054` — score 9 — HIT
  - lines 3906-3958, 475 words
  - preview: Weak-minded folly magnifies       All that is rare and strange,     And the dull herd's o'erwhelmed with awe       At unexpected change.     But wonder leaves enlightened minds,     When ignorance no longer blinds.  FOOTNOTES:  [M] To frighten away the monster swallowing the moon. The superstition was once common. See Tylor's 'Primitive Culture,' pp. 296-302.  VI.  'True,' said I; 'but, since it is thy office to unfold the hidden cause of things, and explain principles veiled in darkness, inform
- `BOETHIUS_CONSOLATION_001_CHUNK_056` — score 6 — MISS
  - lines 4017-4077, 639 words
  - preview: '"Yet what confusion," thou wilt say, "can be more unrighteous than that prosperity and adversity should indifferently befall the good, what they like and what they loathe come alternately to the bad!" Yes; but have men in real life such soundness of mind that their judgments of righteousness and wickedness must necessarily correspond with facts? Why, on this very point their verdicts conflict, and those whom some deem worthy of reward, others deem worthy of punishment. Yet granted there were on
- `BOETHIUS_CONSOLATION_001_CHUNK_063` — score 6 — MISS
  - lines 4545-4609, 665 words
  - preview: All that is, hath been, shall be,     In one glance's compass, He       Limitless descries;       And, save His, no eyes     All the world survey--no, none!     _Him_, then, truly name the Sun.  III.  Then said I: 'But now I am once more perplexed by a problem yet more difficult.'  'And what is that?' said she; 'yet, in truth, I can guess what it is that troubles you.'  'It seems,' said I, 'too much of a paradox and a contradiction that God should know all things, and yet there should be free wi
- `BOETHIUS_CONSOLATION_001_CHUNK_057` — score 4 — MISS
  - lines 4079-4126, 536 words
  - preview: 'As to the other side of the marvel, that the bad now meet with affliction, now get their hearts' desire, this, too, springs from the same causes. As to the afflictions, of course no one marvels, because all hold the wicked to be ill deserving. The truth is, their punishments both frighten others from crime, and amend those on whom they are inflicted; while their prosperity is a powerful sermon to the good, what judgments they ought to pass on good fortune of this kind, which often attends the w

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_055, BOETHIUS_CONSOLATION_001_CHUNK_054

Recall@5: 1.00

### Notes

Strong result.

Keyword retrieval found both manually expected chunks: `BOETHIUS_CONSOLATION_001_CHUNK_055` and `BOETHIUS_CONSOLATION_001_CHUNK_054`.

This is the cleanest retrieval case because the question uses distinctive technical terms — "providence" and "fate" — that appear directly in the relevant source passages.

Takeaway: keyword retrieval performs well for technical-definition questions with distinctive vocabulary.

---

## Q07

### Question

Why does Philosophy argue that wicked people are weak rather than powerful?

### Query Terms

`argue`, `that`, `wicked`, `people`, `weak`, `rather`, `than`, `powerful`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_045`
- `BOETHIUS_CONSOLATION_001_CHUNK_046`
- `BOETHIUS_CONSOLATION_001_CHUNK_047`
- `BOETHIUS_CONSOLATION_001_CHUNK_048`
- `BOETHIUS_CONSOLATION_001_CHUNK_049`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_051` — score 27 — MISS
  - lines 3673-3750, 641 words
  - preview: Then said I: 'A wonderful inference, and difficult to grant; but I see that it agrees entirely with our previous conclusions.'  'Thou art right,' said she; 'but if anyone finds it hard to admit the conclusion, he ought in fairness either to prove some falsity in the premises, or to show that the combination of propositions does not adequately enforce the necessity of the conclusion; otherwise, if the premises be granted, nothing whatever can be said against the inference of the conclusion. And h
- `BOETHIUS_CONSOLATION_001_CHUNK_047` — score 24 — HIT
  - lines 3393-3447, 646 words
  - preview: 'Go on,' said I; 'no one can question but that he who has the natural capacity has more strength than he who has it not.'  'Now, the supreme good is set up as the end alike for the bad and for the good; but the good seek it through the natural action of the virtues, whereas the bad try to attain this same good through all manner of concupiscence, which is not the natural way of attaining good. Or dost thou think otherwise?'  'Nay; rather, one further consequence is clear to me: for from my admis
- `BOETHIUS_CONSOLATION_001_CHUNK_063` — score 22 — MISS
  - lines 4545-4609, 665 words
  - preview: All that is, hath been, shall be,     In one glance's compass, He       Limitless descries;       And, save His, no eyes     All the world survey--no, none!     _Him_, then, truly name the Sun.  III.  Then said I: 'But now I am once more perplexed by a problem yet more difficult.'  'And what is that?' said she; 'yet, in truth, I can guess what it is that troubles you.'  'It seems,' said I, 'too much of a paradox and a contradiction that God should know all things, and yet there should be free wi
- `BOETHIUS_CONSOLATION_001_CHUNK_036` — score 21 — MISS
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt
- `BOETHIUS_CONSOLATION_001_CHUNK_049` — score 21 — HIT
  - lines 3517-3578, 746 words
  - preview: 'Thou seest, then, in what foulness unrighteous deeds are sunk, with what splendour righteousness shines. Whereby it is manifest that goodness never lacks its reward, nor crime its punishment. For, verily, in all manner of transactions that for the sake of which the particular action is done may justly be accounted the reward of that action, even as the wreath for the sake of which the race is run is the reward offered for running. Now, we have shown happiness to be that very good for the sake o

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_047, BOETHIUS_CONSOLATION_001_CHUNK_049

Recall@5: 0.40

### Notes

Partial result.

Keyword retrieval found two of the five manually expected chunks: `BOETHIUS_CONSOLATION_001_CHUNK_047` and `BOETHIUS_CONSOLATION_001_CHUNK_049`.

The high-scoring misses show the weakness of raw keyword matching. Chunks can contain terms like "wicked", "powerful", "good", or related vocabulary without being the best evidence for the specific argument that wicked people are weak rather than powerful.

Takeaway: keyword retrieval can locate parts of an argument, but it is unreliable for multi-step philosophical reasoning.

---

## Q08

### Question

In what sense does Philosophy claim that every fortune is good fortune?

### Query Terms

`sense`, `claim`, `that`, `every`, `fortune`, `good`, `fortune`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_056`
- `BOETHIUS_CONSOLATION_001_CHUNK_057`
- `BOETHIUS_CONSOLATION_001_CHUNK_058`
- `BOETHIUS_CONSOLATION_001_CHUNK_059`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_059` — score 38 — HIT
  - lines 4228-4312, 507 words
  - preview: 'And why so?' said she.  'Because ordinary speech is apt to assert, and that frequently, that some men's fortune is bad.'  'Shall we, then, for awhile approach more nearly to the language of the vulgar, that we may not seem to have departed too far from the usages of men?'  'At thy good pleasure,' said I.  'That which advantageth thou callest good, dost thou not?'  'Certainly.'  'And that which either tries or amends advantageth?'  'Granted.'  'Is good, then?'  'Of course.'  'Well, this is _thei
- `BOETHIUS_CONSOLATION_001_CHUNK_010` — score 36 — MISS
  - lines 850-941, 617 words
  - preview: Then she: 'Dost know nothing else that thou art?'  'Nothing.'  'Now,' said she, 'I know another cause of thy disease, one, too, of grave moment. Thou hast ceased to know thy own nature. So, then, I have made full discovery both of the causes of thy sickness and the means of restoring thy health. It is because forgetfulness of thyself hath bewildered thy mind that thou hast bewailed thee as an exile, as one stripped of the blessings that were his; it is because thou knowest not the end of existen
- `BOETHIUS_CONSOLATION_001_CHUNK_049` — score 36 — MISS
  - lines 3517-3578, 746 words
  - preview: 'Thou seest, then, in what foulness unrighteous deeds are sunk, with what splendour righteousness shines. Whereby it is manifest that goodness never lacks its reward, nor crime its punishment. For, verily, in all manner of transactions that for the sake of which the particular action is done may justly be accounted the reward of that action, even as the wreath for the sake of which the race is run is the reward offered for running. Now, we have shown happiness to be that very good for the sake o
- `BOETHIUS_CONSOLATION_001_CHUNK_022` — score 34 — MISS
  - lines 1606-1698, 625 words
  - preview: SONG VII.  GLORY MAY NOT LAST.  Oh, let him, who pants for glory's guerdon,       Deeming glory all in all,     Look and see how wide the heaven expandeth,       Earth's enclosing bounds how small!  Shame it is, if your proud-swelling glory       May not fill this narrow room!     Why, then, strive so vainly, oh, ye proud ones!       To escape your mortal doom?  Though your name, to distant regions bruited,       O'er the earth be widely spread,     Though full many a lofty-sounding title       
- `BOETHIUS_CONSOLATION_001_CHUNK_036` — score 31 — MISS
  - lines 2547-2616, 679 words
  - preview: FOOTNOTES:  [I] The substance of this poem is taken from Plato's 'Timæus,' 29-42. See Jowett, vol. iii., pp. 448-462 (third edition).  X.  'Since now thou hast seen what is the form of the imperfect good, and what the form of the perfect also, methinks I should next show in what manner this perfection of felicity is built up. And here I conceive it proper to inquire, first, whether any excellence, such as thou hast lately defined, can exist in the nature of things, lest we be deceived by an empt

### Retrieval Result

Hits: BOETHIUS_CONSOLATION_001_CHUNK_059

Recall@5: 0.25

### Notes

Weak-to-partial result.

Keyword retrieval found `BOETHIUS_CONSOLATION_001_CHUNK_059`, which is highly relevant, but missed the earlier expected chunks that build up the broader argument.

This is a good example of keyword retrieval finding the most obvious answer-bearing chunk while missing surrounding argumentative context.

Takeaway: keyword retrieval can find the punchline, but may miss the supporting chain of reasoning.

---

## Q09

### Question

Based only on the selected Boethius chunks, can we say whether the work is explicitly Christian?

### Query Terms

`explicitly`, `christian`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`
- `BOETHIUS_CONSOLATION_001_CHUNK_043`
- `BOETHIUS_CONSOLATION_001_CHUNK_071`
- `BOETHIUS_CONSOLATION_001_CHUNK_072`

### Retrieved Top 5 Chunks

- No chunks retrieved

### Retrieval Result

Hits: None

Recall@5: 0.00

### Notes

Expected weak result.

Keyword retrieval found no chunks because the query terms were only `explicitly` and `christian`, and those words do not appear in the retrieved corpus.

This is not necessarily a bad system result. It reveals that the question is asking for a judgment about absence/insufficient evidence, not for a passage containing the words "explicitly Christian."

Takeaway: keyword retrieval is poor for negative-evidence or insufficient-evidence questions. These require source-aware reasoning, not just term matching.

---

## Q10

### Question

Based only on the selected Boethius chunks, what can we safely say about the historical circumstances of Boethius’ imprisonment and death?

### Query Terms

`safely`, `about`, `historical`, `circumstances`, `imprisonment`, `death`

### Expected Manual Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_004`
- `BOETHIUS_CONSOLATION_001_CHUNK_005`
- `BOETHIUS_CONSOLATION_001_CHUNK_006`
- `BOETHIUS_CONSOLATION_001_CHUNK_007`
- `BOETHIUS_CONSOLATION_001_CHUNK_008`

### Retrieved Top 5 Chunks

- `BOETHIUS_CONSOLATION_001_CHUNK_063` — score 6 — MISS
  - lines 4545-4609, 665 words
  - preview: All that is, hath been, shall be,     In one glance's compass, He       Limitless descries;       And, save His, no eyes     All the world survey--no, none!     _Him_, then, truly name the Sun.  III.  Then said I: 'But now I am once more perplexed by a problem yet more difficult.'  'And what is that?' said she; 'yet, in truth, I can guess what it is that troubles you.'  'It seems,' said I, 'too much of a paradox and a contradiction that God should know all things, and yet there should be free wi
- `BOETHIUS_CONSOLATION_001_CHUNK_040` — score 4 — MISS
  - lines 2832-2876, 511 words
  - preview: 'And yet there is no possibility of question about this either, since thou seest how herbs and trees grow in places suitable for them, where, as far as their nature admits, they cannot quickly wither and die. Some spring up in the plains, others in the mountains; some grow in marshes, others cling to rocks; and others, again, find a fertile soil in the barren sands; and if you try to transplant these elsewhere, they wither away. Nature gives to each the soil that suits it, and uses her diligence
- `BOETHIUS_CONSOLATION_001_CHUNK_053` — score 4 — MISS
  - lines 3832-3904, 528 words
  - preview: SONG IV.  THE UNREASONABLENESS OF HATRED.  Why all this furious strife? Oh, why     With rash and wilful hand provoke death's destined day?       If death ye seek--lo! Death is nigh,     Not of their master's will those coursers swift delay!  The wild beasts vent on man their rage,     Yet 'gainst their brothers' lives men point the murderous steel;       Unjust and cruel wars they wage,     And haste with flying darts the death to meet or deal.  No right nor reason can they show;     'Tis but b
- `BOETHIUS_CONSOLATION_001_CHUNK_066` — score 4 — MISS
  - lines 4747-4794, 515 words
  - preview: 'Certainly not.'  'Let us assume foreknowledge again, but without its involving any actual necessity; the freedom of the will, I imagine, will remain in complete integrity. But thou wilt say that, even although the foreknowledge is not the necessity of the future event's occurrence, yet it is a sign that it will necessarily happen. Granted; but in this case it is plain that, even if there had been no foreknowledge, the issues would have been inevitably certain. For a sign only indicates somethin
- `BOETHIUS_CONSOLATION_001_CHUNK_001` — score 3 — MISS
  - lines 238-323, 691 words
  - preview: SONG I.  BOETHIUS' COMPLAINT.  Who wrought my studious numbers       Smoothly once in happier days,     Now perforce in tears and sadness       Learn a mournful strain to raise.     Lo, the Muses, grief-dishevelled,       Guide my pen and voice my woe;     Down their cheeks unfeigned the tear drops       To my sad complainings flow!     These alone in danger's hour       Faithful found, have dared attend     On the footsteps of the exile       To his lonely journey's end.     These that were the

### Retrieval Result

Hits: None

Recall@5: 0.00

### Notes

Weak result.

Keyword retrieval found none of the manually expected chunks. The expected chunks were selected because they relate to Boethius' accusation, imprisonment context, and ruin. The keyword query used terms like "historical", "circumstances", "imprisonment", and "death", but the source may describe those circumstances using different vocabulary.

This is another example where contextual relevance does not equal keyword overlap.

Takeaway: keyword retrieval fails when the question uses modern framing terms that do not appear directly in the source.

---

# Overall Findings

Average Recall@5: 0.34

## Interpretation

Keyword retrieval is useful as a baseline, but it is not good enough as the final retrieval method for this corpus.

Average Recall@5 was 0.34, which means the keyword retriever found about one third of the manually expected evidence chunks in its top five results.

The pattern is clear:

- keyword retrieval works best when the question contains distinctive terms that also appear in the source, such as `providence` and `fate`
- keyword retrieval performs moderately when the question and source share conceptual vocabulary, such as `fortune`, `happiness`, or `good`
- keyword retrieval performs poorly on interpretive, contextual, broad synthesis, or insufficient-evidence questions
- high keyword scores can be false positives because score measures word overlap, not relevance

This baseline is valuable because it gives us a measurable retrieval result before adding semantic search.

## Next Step

Keep this as the baseline retrieval evaluation.

The next improvement should be one of:

1. add manual query terms for each question and compare results
2. improve the keyword retriever with better stopwords and phrase matching
3. add semantic / embedding-based retrieval
4. test hybrid retrieval that combines keyword matches with semantic similarity

For now, this result is good enough to close the keyword baseline ticket. It proves that simple keyword retrieval is measurable but brittle.

## Scoring Explanation

The keyword score is not a correctness score.

The score is a simple count of how often the question's remaining search terms appear in a chunk after basic stopword removal.

For example, if the query terms are:

```text
describe, own, misery, opening, complaint
```

then a chunk receives points whenever those words appear in its text.

This means a chunk can score highly because it repeats common or question-adjacent words, even if it is not the right evidence for the question.

`HIT` and `MISS` are different from the score:

- `HIT` means the retrieved chunk appears in the manual evidence map for that question
- `MISS` means the retrieved chunk does not appear in the manual evidence map

Therefore:

- high-score HIT = strong lexical match and expected evidence
- low-score HIT = expected evidence, but weak exact word overlap
- high-score MISS = lexical false positive
- low-score MISS = weak lexical match and not expected evidence

This is why a result like `MISS — score 20` and `HIT — score 4` can happen. The miss had more word overlap, but the hit was judged more relevant by the manual evidence map.

## Manual Evidence vs Keyword Evidence

The manually selected chunks were chosen based on context and relevance, not by checking whether they contained the exact query words.

That is intentional.

The goal of this evaluation is to ask:

```text
Can simple keyword search rediscover the same evidence chunks that a human selected by context?
```

Sometimes it can. Sometimes it cannot.

When it cannot, that tells us keyword search is too brittle for that type of question.

