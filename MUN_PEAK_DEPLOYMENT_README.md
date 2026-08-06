# MUN Command Center Peak — Deployment

## What is included

- `00_UPLOAD_READY_MUN_MASTER/`: one self-contained master skill for always-on MUN behaviour and command routing.
- `skills/01...40/`: 40 specialist skills. Each specialist now contains an embedded core-enforcement block, so it remains safe and useful if activated without the master skill.

## Recommended setup

1. Upload and enable `00_UPLOAD_READY_MUN_MASTER.zip` as the permanent MUN base skill.
2. Upload the specialist ZIP files you use most often: country position, source research, verification, speeches, bloc-building, resolution drafting, and crisis.
3. Keep the master skill active. Enable only relevant specialist skills for the current job to avoid context clutter.
4. Add the committee background guide, Rules of Procedure, country assignment, and source materials before asking for substantive strategy.
5. Test the system with a real committee scenario before relying on it live.

## Initial prompt

```text
MUN COMMAND CENTER — INITIALIZE
Country: [COUNTRY]
Committee: [COMMITTEE]
Agenda: [EXACT AGENDA]
Committee type: [REGULAR / HISTORICAL / CRISIS]
Simulation date: [DATE]
Speech limit: [SECONDS]
Read all attached and connected MUN materials first.
Build my country doctrine, mandate brief, evidence ledger, bloc map, policy package, opening speech, attack-defense matrix, and clause bank.
```

## Mandatory test cases

- Ask it to verify five claims from your draft speech.
- Ask it to reject a proposal outside the committee mandate.
- Ask it to generate a position that conflicts with your country, then check that it catches the conflict.
- Ask it for a 45-second opening speech and time it aloud.
- Ask it to red-team your first draft resolution.

A skill suite becomes strong through testing against your real committee, not word count alone.
