# Intent (accepted)

Status: accepted by Ty 30/09 ("approve for all four", in chat), follow-up 3 of the routine heartbeat-notes spec.

This repo is public, and `data/.last-check` is a public file. On a fill night `tools/sync.js` writes the CSV file names and the fill count into it (e.g. `... newest-source=<csv name> (<n> new fills, last ...)`), and the wiring page used to copy that note. The heartbeat should say only that the run happened and how new the data is.
