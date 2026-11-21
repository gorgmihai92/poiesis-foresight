# Scan: which signals to keep

Poiesis Research records what was observed about a subject. This playbook decides which of those signals to keep,
what each might mean and what to watch. It collects nothing itself: triage reads what was gathered.

## Read first
Notes in `research/notes` of the plugin's repository. Each says how much of its source was read.
- `go-science-2024-futures-toolkit`: the UK Government Office for Science's Futures Toolkit, read in part: the
  Horizon Scanning section in full (p. 34–41) and the glossary. It is practitioner guidance, not evidence that
  scanning works. "Triage" below adapts its steps 4 and 5 (Open Government Licence v3.0).
- `cuhls-2020-horizon-scanning-foresight`: abstract only. Scanning and making sense of a scan are two activities.
- `amanatidou-2012-horizon-scanning-methods`: abstract only. No single scanning method is best everywhere.
- `hiltunen-2008-future-sign`: title only. poiesis-insight credits it with the three fields of the signal
  template (signal, issue, interpretation). Here they are a format; no rule rests on the paper.

## Input
1. **Signals from poiesis-research,** when the project has them: `research/signals/<date>-<name>.md`, each with an
   **Id** (SG-001), **What**, **Where**, **When**, **How visible**, **How widespread**, **Kind of source** and
   **Read**. Read `research/README.md` first to see what is there.
2. **Signals the user gives:** a link, a note, a list. Each needs what, where and when. Ask for what is missing; a
   signal with no source is kept as "given by the user, not checked".
3. **No signals at all:** say so, and offer the choices: the user gives some, or poiesis-research scans for them
   (`signal-scout`). Never write signals from memory.

## Triage
1. **Coverage first.** Count the signals by kind of source. If one kind holds most of them, say the scan is
   narrow before reading anything into it, and name the kinds that are absent: patents, regulators, sources not
   in English (toolkit, p. 38–39).
2. **Keep the observation apart from the reading.** Copy the observation as it was recorded, numbers included.
   Write what it might mean on its own line, marked as interpretation.
3. **Sort each signal** (toolkit, p. 39–40):
   - what it points to: an established trend, an expected development, a newly emerging issue, a risk or an
     opportunity, a possible event;
   - how new it is to the project: known and already planned for, known and not planned for, or new.
4. **Rate it twice,** each with one line of reason: how much it would matter to the scoping question, and how
   likely it is to matter within the horizon. Both are judgments: label them as interpretation.
   - Matters much, likely: carry it into `playbooks/drivers.md`.
   - Matters much, unlikely: keep it and write a signpost for it (`playbooks/signposts.md`).
   - Matters little: park it, with the line that says why.
5. **Keep four to eight,** the unlikely ones that would matter much among them (toolkit, p. 40). List what was
   parked: what was set aside teaches as much.
6. **Do not drop a signal for seeming irrelevant at first.** Park it with its reason (toolkit, p. 39).
7. **Write each kept signal** from `templates/signal.md`: **From** (its SG id), the observation, visibility,
   spread, interpretation, **Horizon** (`playbooks/horizons.md`) and what to watch for.

## What a triage cannot say
- One signal is not a trend. A count of signals is a count of what the sources hold on the day they were read.
- A weak signal is kept as a lead. The toolkit's own definition calls weak signals "intuitively thought to be
  significant" (p. 115): the significance is a guess until a forecast or a signpost tests it.
- A source that refused, or was never asked, is not a source with nothing. Keep the Coverage line of the scan.

## Then
Every reading goes through `playbooks/challenge.md` before it is reported.

## Report
- **Kept,** one entry each, and **parked,** one line each.
- **By kind of source:** how many signals came from each, and which kinds are missing.
- **Not checked:** the originals that were not opened, the kinds of source not scanned.

## Save (see SKILL.md, "Saving")
In `foresight/<YYYY-MM-DD>-<topic>.md`, under "Signals".
