# Manual RAG Chunk Map

## Goal

Map each manual RAG question to candidate Boethius chunks.

This file creates a human-reviewed evidence map before automated retrieval is built.

## Source

Source ID: `BOETHIUS_CONSOLATION_001`

Question file:

`evals/manual_rag_questions.md`

Chunk file:

`chunks/boethius_consolation_chunks.json`

## Method

This map was created by using simple keyword searches over the generated chunks, then manually selecting the chunks that appear most likely to support a grounded answer.

This is not final automated retrieval. This is a manual evidence map used to establish a baseline for later retrieval testing.

## Important Note

The purpose of this file is not to produce perfect Boethius scholarship. The purpose is to define a small “golden evidence set” so later retrieval tests can ask:

- Did the retrieval system find the expected chunks?
- Did it miss important chunks?
- Did it retrieve noisy chunks?
- Did the answer use the supplied chunks correctly?
- Did the answer refuse or caveat when evidence was insufficient?

---

## Q01: Philosophy and Poetry

Question:

What is the relationship between Philosophy and the Muses of Poetry at the beginning of the work?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_001`
- `BOETHIUS_CONSOLATION_001_CHUNK_003`

Rationale:

Chunk 001 is the strongest evidence. It contains the opening complaint and the scene where the authoritative female figure rebukes the Muses of Poetry for feeding Boethius's sickness with "sweet poison" rather than healing him.

Chunk 003 is useful supporting evidence because it explicitly identifies the female figure as Philosophy after Boethius regains his sight and recognizes her. This helps resolve the ambiguity in Chunk 001, where the figure is symbolically described before being explicitly named.

Evidence sufficiency:

Sufficient with caveat.

Uncertainty caveat needed?

Yes. Chunk 001 alone is partially ambiguous because the female figure is not yet explicitly named as Philosophy. Chunk 003 strengthens the answer by identifying her.

---

## Q02: Boethius’ Complaint

Question:

How does Boethius describe his own misery in the opening complaint?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_001`

Rationale:

Chunk 001 is the strongest and probably sufficient evidence. It contains "Boethius' Complaint," where he presents himself as sorrowful, aged before his time, abandoned to grief, wishing for death but not receiving it, and fallen from former happiness.

Evidence sufficiency:

Sufficient.

Uncertainty caveat needed?

No.

---

## Q03: Fortune’s Nature

Question:

How does Philosophy describe the nature of Fortune?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_011`
- `BOETHIUS_CONSOLATION_001_CHUNK_012`
- `BOETHIUS_CONSOLATION_001_CHUNK_014`

Rationale:

Chunk 011 is the strongest conceptual evidence. It introduces Book II and Philosophy's argument that Boethius is suffering because Fortune has changed, but that change is Fortune's true nature.

Chunk 012 supports this by presenting Fortune's own imagined defense, including the idea that Fortune gives and takes what is under her control.

Chunk 014 adds the broader theme that created things and human fortunes are transient, unstable, and cannot be relied on as lasting happiness.

Evidence sufficiency:

Sufficient.

Uncertainty caveat needed?

No.

---

## Q04: False Happiness

Question:

Why does Philosophy argue that wealth, rank, power, glory, and pleasure cannot provide true happiness?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_025`
- `BOETHIUS_CONSOLATION_001_CHUNK_026`
- `BOETHIUS_CONSOLATION_001_CHUNK_028`
- `BOETHIUS_CONSOLATION_001_CHUNK_029`
- `BOETHIUS_CONSOLATION_001_CHUNK_030`
- `BOETHIUS_CONSOLATION_001_CHUNK_031`
- `BOETHIUS_CONSOLATION_001_CHUNK_032`
- `BOETHIUS_CONSOLATION_001_CHUNK_034`

Rationale:

Chunk 025 establishes the general frame: all people seek happiness/the good, but they pursue it through different apparent goods.

Chunk 026 names the false candidates directly: wealth, rank, power, glory, and pleasure.

Chunk 028 addresses wealth specifically and argues that riches do not remove want and may create new dependencies.

Chunk 029 addresses rank/dignity and argues that public honors cannot produce true reverence or virtue.

Chunk 030 addresses power/sovereignty and argues that political power cannot secure happiness or freedom from fear.

Chunk 031 addresses glory and reputation, arguing that fame is unstable, limited, and not the true measure of the wise.

Chunk 032 addresses pleasure and the failure of these paths to lead to happiness.

Chunk 034 synthesizes the problem: human error separates what is actually one and simple, seeking parts of happiness rather than the whole.

Evidence sufficiency:

Sufficient, but broad.

Uncertainty caveat needed?

No, but an answer should avoid overcompressing the argument. This question may require several chunks because it asks for a synthesis across multiple false goods.

---

## Q05: True Happiness

Question:

What does Philosophy identify as true happiness or the highest good?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_025`
- `BOETHIUS_CONSOLATION_001_CHUNK_034`
- `BOETHIUS_CONSOLATION_001_CHUNK_035`
- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`

Rationale:

Chunk 025 defines happiness as the state perfected by the assembling together of all good things and identifies the good as that which leaves nothing further lacking.

Chunk 034 explains that independence, power, renown, reverence, and joy are not separate goods but aspects of one simple good.

Chunk 035 distinguishes imperfect earthly goods from true and perfect good and prepares the move toward the source of happiness.

Chunk 036 argues that perfect happiness must exist and that its dwelling place is in God.

Chunk 037 gives the strongest direct answer: the highest good is happiness, and God is very happiness.

Chunk 038 further explains that goodness is the sum, hinge, and cause of all desirable things.

Evidence sufficiency:

Sufficient.

Uncertainty caveat needed?

No.

---

## Q06: Providence and Fate

Question:

How does Philosophy distinguish providence from fate?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_054`
- `BOETHIUS_CONSOLATION_001_CHUNK_055`

Rationale:

Chunk 054 introduces the problem and begins the explanation of providence and fate.

Chunk 055 is the core evidence. It distinguishes providence as the fixed, simple form in the Divine mind from fate as the shifting temporal series by which providence disposes individual things. This is the strongest chunk for the question.

Evidence sufficiency:

Sufficient.

Uncertainty caveat needed?

No.

---

## Q07: Evil and Power

Question:

Why does Philosophy argue that wicked people are weak rather than powerful?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_045`
- `BOETHIUS_CONSOLATION_001_CHUNK_046`
- `BOETHIUS_CONSOLATION_001_CHUNK_047`
- `BOETHIUS_CONSOLATION_001_CHUNK_048`
- `BOETHIUS_CONSOLATION_001_CHUNK_049`

Rationale:

Chunk 045 frames the paradox: the good are strong and the bad are weak or impotent.

Chunk 046 begins the argument from will and power, explaining that action requires both.

Chunk 047 gives the strongest evidence: both good and bad seek the good, but the good seek it through virtue while the bad pursue it through disordered desire and therefore fail to attain their true end.

Chunk 048 sharpens the paradox by arguing that the ability to do evil is not true power, because power is desirable and ordered to the good.

Chunk 049 provides related support by arguing that goodness carries its own reward and wickedness its own punishment.

Evidence sufficiency:

Sufficient.

Uncertainty caveat needed?

No, but the answer should label this as Philosophy's paradoxical argument rather than as an ordinary claim that wicked people lack worldly force.

---

## Q08: Good and Bad Fortune

Question:

In what sense does Philosophy claim that every fortune is good fortune?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_056`
- `BOETHIUS_CONSOLATION_001_CHUNK_057`
- `BOETHIUS_CONSOLATION_001_CHUNK_058`
- `BOETHIUS_CONSOLATION_001_CHUNK_059`

Rationale:

Chunk 056 explains that apparent disorder in fortune comes from human ignorance of divine providence and the condition of souls.

Chunk 057 explains how even prosperity and adversity among the wicked can be used providentially for punishment, correction, testing, or reform.

Chunk 058 contains the direct claim that every fortune is good fortune because every fortune has as its object the reward or trial of the good and the punishing or amending of the bad.

Chunk 059 translates the paradox into more ordinary language, distinguishing how fortune may be good for those advancing in virtue and bad for those remaining in wickedness.

Evidence sufficiency:

Sufficient.

Uncertainty caveat needed?

No, but the answer should make clear that this is a philosophical/theological claim about providential use, not a simple claim that all experiences feel good.

---

## Q09: Insufficient Evidence — Christianity

Question:

Based only on the selected Boethius chunks, can we say whether the work is explicitly Christian?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_036`
- `BOETHIUS_CONSOLATION_001_CHUNK_037`
- `BOETHIUS_CONSOLATION_001_CHUNK_038`
- `BOETHIUS_CONSOLATION_001_CHUNK_043`
- `BOETHIUS_CONSOLATION_001_CHUNK_071`
- `BOETHIUS_CONSOLATION_001_CHUNK_072`

Rationale:

These chunks contain strong theistic and providential language: God, the supreme good, divine knowledge, providence, judgment, rewards, punishments, and prayer. They are relevant because they show that the text is deeply concerned with God and divine governance.

However, these chunks do not by themselves establish that the work is explicitly Christian. They do not clearly rely on specifically Christian claims such as Christ, the Incarnation, the Trinity, the Church, Scripture, sacraments, or Christian revelation.

Evidence sufficiency:

Insufficient for the claim "explicitly Christian."

Sufficient only for the narrower claim that the selected chunks contain theistic/philosophical language about God, providence, goodness, and judgment.

Uncertainty caveat needed?

Yes. A grounded answer should say that, based only on these chunks, we can identify theological/theistic language, but we should not claim explicit Christianity unless additional chunks or external context are supplied.

---

## Q10: Insufficient Evidence — Author Biography

Question:

Based only on the selected Boethius chunks, what can we safely say about the historical circumstances of Boethius’ imprisonment and death?

Candidate chunks:

- `BOETHIUS_CONSOLATION_001_CHUNK_004`
- `BOETHIUS_CONSOLATION_001_CHUNK_005`
- `BOETHIUS_CONSOLATION_001_CHUNK_006`
- `BOETHIUS_CONSOLATION_001_CHUNK_007`
- `BOETHIUS_CONSOLATION_001_CHUNK_008`

Rationale:

Chunk 004 begins Boethius's self-vindication and describes his public service, conflicts with powerful people, and efforts to protect others from injustice.

Chunk 005 gives key accusations: named accusers, the allegation that he wished to save the senate, and the charge involving treason evidence.

Chunk 006 discusses forged letters, the freedom of Rome, the charge related to the senate, and says he was condemned to outlawry and death unheard and undefended at a distance of nearly five hundred miles.

Chunk 007 adds further details about accusations of sacrilege, reputation, banishment from life's blessings, and includes the footnote identifying Pavia as the place of imprisonment.

Chunk 008 is relevant mainly because Philosophy responds to Boethius's lament and reframes his exile spiritually rather than simply geographically.

Evidence sufficiency:

Partial.

These chunks support a limited answer about what the text itself says: Boethius presents himself as unjustly accused, politically targeted, connected to charges about the senate and Rome, condemned unheard, and suffering exile/imprisonment.

They are insufficient for a full historical biography or a confident account of the exact circumstances of his death without external historical sources or the excluded proem/front matter.

Uncertainty caveat needed?

Yes. A grounded answer should distinguish between what Boethius says in the main text and broader historical claims about his imprisonment and death.

---

# Findings

## Questions with strong evidence

- Q01: Philosophy and Poetry
- Q02: Boethius’ Complaint
- Q03: Fortune’s Nature
- Q04: False Happiness
- Q05: True Happiness
- Q06: Providence and Fate
- Q07: Evil and Power
- Q08: Good and Bad Fortune

## Questions with partial evidence

- Q10: Author Biography

## Questions where the system should refuse or caveat

- Q09: Explicit Christianity
- Q10: Author Biography

## Notes for Retrieval Testing

The manual evidence map shows that some questions can be answered from one or two chunks, while broader synthesis questions require several chunks.

Expected retrieval behavior:

- Q01 should retrieve Chunk 001 and ideally Chunk 003.
- Q02 should retrieve Chunk 001.
- Q03 should retrieve Chunk 011 or 012, with Chunk 014 as support.
- Q04 should retrieve several Book III chunks dealing with wealth, rank, power, glory, pleasure, and the unity of the good.
- Q05 should retrieve Chunks 036–038, especially Chunk 037.
- Q06 should retrieve Chunk 055.
- Q07 should retrieve Chunks 046–048.
- Q08 should retrieve Chunks 058–059, with 056–057 as context.
- Q09 should retrieve God/providence chunks but still caveat that explicit Christianity is not established.
- Q10 should retrieve the accusation/imprisonment chunks but caveat that full biography/death details require more context.

The main future retrieval challenge is that simple keyword search may over-rank noisy chunks with repeated terms while under-ranking the best conceptual evidence. Human review remains necessary until semantic retrieval or better scoring is added.
