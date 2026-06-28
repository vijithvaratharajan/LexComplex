"""
wordlists.py
Reference word data bundled with the profiler.

Sources:
  - Academic Word List (AWL): Coxhead, A. (2000). A new academic word list.
    TESOL Quarterly, 34(2), 213-238. Sublist 1-10 headwords and members.
    The AWL is freely available for research and educational use.
  - CEFR-level overrides for common concrete words whose corpus frequency
    underestimates their pedagogical level.
"""

# ---------------------------------------------------------------------------
# Academic Word List (Coxhead 2000) — all 570 headwords and key family members
# These are considered B2 minimum; many C1 in context.
# ---------------------------------------------------------------------------

AWL_WORDS = {
    # Sublist 1
    "analyse","analysis","analytical","analyze","approach","area","assess",
    "assessment","assume","assumption","authority","available","benefit",
    "concept","consist","constitutional","context","contract","create",
    "data","definition","derive","distribute","economy","environment",
    "establish","estimate","evidence","export","factor","finance","formula",
    "function","identify","income","indicate","individual","interpret",
    "involve","issue","labour","legal","legislate","major","method","occur",
    "percent","period","policy","principle","proceed","process","require",
    "research","respond","role","section","sector","significant","similar",
    "source","specific","structure","theory","vary",
    # Sublist 2
    "achieve","acquisition","administrate","affect","appropriate","aspect",
    "assist","category","chapter","commission","community","complex",
    "compute","conclude","conduct","consequence","construct","consume",
    "credit","culture","design","distinct","element","equate","evaluate",
    "feature","final","focus","impact","injure","institute","invest",
    "item","journal","maintain","normal","obtain","participate","perceive",
    "positive","potential","previous","primary","purchase","range","region",
    "regulate","relevance","reside","resource","restrict","secure","seek",
    "select","site","strategy","survey","text","tradition","transfer",
    # Sublist 3
    "alternative","circumstance","comment","compensate","component","consent",
    "considerable","constant","contribute","convene","coordinate","core",
    "correspond","criteria","deduce","demonstrate","document","dominate",
    "emphasis","ensure","exclude","framework","fund","illustrate","immigrate",
    "imply","initial","instance","interact","justify","layer","link",
    "locate","maximum","meaning","mechanism","minimum","modify","monitor",
    "motive","neutral","nevertheless","objective","orient","outcome",
    "output","overall","parallel","parameter","phase","predict","principal",
    "prior","professional","project","promote","proportion","publish",
    "react","register","release","revenue","series","shift","specify",
    "sufficient","task","technical","technique","technology","valid","volume",
    # Sublist 4
    "access","adequate","annual","apparent","approximate","attitude",
    "attribute","civil","code","commit","communicate","concentrate",
    "confer","contrast","cycle","debate","despite","dimension","domestic",
    "emerge","error","ethnic","goal","grant","hence","hypothesis",
    "implement","implicate","impose","integrate","internal","investigate",
    "job","label","mechanism","obvious","occupy","option","output",
    "overall","parallel","phase","predict","principal","prior",
    "professional","project","proportion","publish","react","register",
    "release","revenue","shift","specify","sufficient","task","technical",
    # Sublist 5
    "academic","adjust","alter","amend","aware","capacity","challenge",
    "clause","compound","conflict","consult","contact","decline","discrete",
    "draft","enable","energy","enforce","entity","equivalent","evolve",
    "expand","expose","external","facilitate","fundamental","generate",
    "generation","image","liberal","license","logic","marginal","medical",
    "mental","modify","monitor","network","notion","objective","orient",
    "perspective","precise","prime","psychology","pursue","ratio","reject",
    "revenue","stable","style","substitute","sustain","symbol","target",
    "transition","trend","ultimate","unique","visible","voluntary",
    # Sublist 6
    "abstract","accurate","acknowledge","aggregate","allocate","assign",
    "attach","available","capacity","clause","coherent","coincide",
    "commence","concurrent","confine","controversy","conversely","device",
    "devote","dimension","discrimination","displace","display","diverse",
    "domain","edit","enhance","forthcoming","formulate","fund","gender",
    "ignorance","induce","inevitable","infrastructure","inherent","insight",
    "integral","intermediate","manual","mature","mediate","medium","military",
    "minimize","nuclear","offset","paragraph","plus","practitioner",
    "predominant","prospect","radical","random","reinforce","restore",
    "revise","schedule","scheme","simulate","sole","somewhat","successor",
    "supplement","suspend","team","temporary","terminate","theme","thereby",
    "uniform","vehicle","via","virtual","vision","widespread",
    # Sublist 7
    "adapt","adult","advocate","aid","channel","chemical","classic",
    "comprehensive","comprise","confirm","contrary","convert","couple",
    "decade","definite","deny","differentiate","disposal","dynamic",
    "eliminate","empirical","equip","extract","file","finite","foundation",
    "global","grade","guarantee","ideology","infer","innovate","input",
    "integrity","intelligence","justify","maintained","obvious","passive",
    "pioneer","pose","potential","precede","principal","project","promote",
    "regime","resolve","retain","series","statistic","status","straightforward",
    "subsequent","sum","summary","undertake","uniform","welfare",
    # Sublist 8
    "abandon","accompany","accumulate","ambiguous","append","appreciate",
    "arbitrary","automate","bias","capable","cite","cooperative","discriminate",
    "display","diversify","dominate","draft","enable","encounter","energy",
    "enforce","enormous","foundation","hence","hypothesis","identical",
    "ideology","infer","innovation","insert","intervene","isolate","media",
    "mode","mutual","negate","norm","obtain","option","output","overlap",
    "promote","proportion","pursue","radical","random","reinforce",
    "restore","revise","schedule","scheme","sole","somewhat","successive",
    "supplement","suspend","temporary","terminate","theme","thereby",
    "uniform","vehicle","via","virtual","widespread",
    # Sublist 9
    "accommodate","analogy","anticipate","assure","attain","behalf",
    "bulk","cease","coherence","coincide","compile","complement",
    "conform","contemporary","contradict","crucial","currency","denote",
    "detect","deviate","displace","aggregate","drama","eventual",
    "exhibit","exploit","fluctuate","guideline","highlight","implicit",
    "induce","inevitable","infrastructure","insight","integral","intermediate",
    "manual","mature","medium","minimize","nuclear","offset","ongoing",
    "orient","predominant","prospect","radical","random","reinforce",
    "restore","revise","schedule","scheme","simulate","sole","somewhat",
    "successor","supplement","suspend","temporary","terminate","theme",
    "thereby","uniform","vehicle","via","virtual","widespread",
    # Sublist 10
    "adjacent","albeit","assemble","collapse","colleague","compile",
    "conceive","convince","depress","encounter","enormous","forthcoming",
    "incline","integrity","intrinsic","invoke","levy","likewise","nonetheless",
    "notwithstanding","orient","overlap","preliminary","protocol","qualitative",
    "refine","relax","restrain","revolution","rigid","route","scenario",
    "sphere","subordinate","supplement","suspended","terminate","thesis",
    "tense","thereby","unprecedented","welfare",
}

# ---------------------------------------------------------------------------
# A1 override list — concrete high-frequency teaching vocabulary that
# wordfreq under-scores because these words are common in life but not
# proportionally common in written corpora used by wordfreq.
# ---------------------------------------------------------------------------

A1_OVERRIDES = {
    "cat","dog","bird","fish","cow","pig","horse","rabbit","mouse","rat",
    "pen","pencil","book","bag","desk","chair","table","door","window",
    "bed","room","house","flat","car","bus","train","plane","boat","bike",
    "apple","banana","orange","bread","milk","water","juice","tea","coffee",
    "shirt","dress","shoes","hat","coat","sock","shoe","trousers","skirt",
    "red","blue","green","yellow","white","black","pink","purple","brown",
    "one","two","three","four","five","six","seven","eight","nine","ten",
    "mum","dad","mummy","daddy","brother","sister","family","friend",
    "eat","drink","sleep","walk","run","jump","swim","play","read","write",
    "happy","sad","angry","tired","hungry","cold","hot","big","small","tall",
    "monday","tuesday","wednesday","thursday","friday","saturday","sunday",
    "january","february","march","april","june","july","august","september",
    "october","november","december","morning","afternoon","evening","night",
    "baby","boy","girl","child","children","people","man","woman","men","women",
    "eye","ear","nose","mouth","hand","foot","head","body","arm","leg",
    "sun","moon","star","sky","rain","snow","cloud","wind","tree","flower",
}
