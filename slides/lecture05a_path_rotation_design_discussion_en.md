# Lecture 5.5: Design Discussion on Path Rotation

As part of `MTD (Moving Target Defense)`, this document discusses **what information the server and the Pico each need** when rotating the destination path of an `HTTP POST`.

The target is the minimal setup of the local Python receiver and the `Raspberry Pi Pico 2 W` defined in the previous document, [lecture05_mtd_local_post_spec_en.md](lecture05_mtd_local_post_spec_en.md).

## 1. Problem Statement

With a fixed path `/ingest`, the destination is easy to spot for an attacker or observer.

So we would like to rotate the path, for example:

- `10:00-10:10`: `/ingest/a`
- `10:10-10:20`: `/ingest/b`
- `10:20-10:30`: `/ingest/c`

The hard part is that **the server and the Pico cannot communicate unless they share the same rotation rule**.

## 2. Information Both Sides Must Share

At minimum, the following is needed.

- List of candidate paths
  - e.g. `/ingest/a`, `/ingest/b`, `/ingest/c`
- When to rotate
  - time based
  - send-count based
  - random / pseudo-random based
- Which rule selects the next path
  - fixed order
  - table lookup
  - formula
- When rotation starts
  - active from boot
  - active after a signal
- How to treat old paths
  - disable immediately
  - accept in parallel for a short time

## 3. Candidate Designs

## 3.1 Option A: Hard-code in Source

### Overview

- Embed the same path list and rotation rule in both the server and the Pico
- e.g.:
  - path array `["/ingest/a", "/ingest/b", "/ingest/c"]`
  - select with `(seq - 1) % 3` (`seq` is 1-based)

### Information for the Pico

- candidate path list
- selection rule

### Information for the Server

- the same candidate path list
- the same selection rule

### Pros

- simplest to implement
- easy to understand in class
- no dependency beyond the network

### Cons

- once the rule leaks, it is trivially reproduced
- every rule change requires reflashing the Pico
- low operational flexibility

### Educational assessment

- good for a first look at the `MTD idea`
- weak as a `real operation`

## 3.2 Option B: Distribute a Config File in Advance

### Overview

- The instructor distributes the rotation rule as a config file
- The server reads that config
- The Pico copies an equivalent config into its source

### Information for the Pico

- candidate path list
- rotation method
- interval or timing

### Information for the Server

- the same config file

### Pros

- rule changes are easy
- the spec and the config can be separated
- gives a real-world feel of `changing behavior via config`

### Cons

- the Pico still needs to be edited
- config transcription mistakes are easy to make
- somewhat cumbersome to operate in class

### Educational assessment

- good for intermediate learners
- a bit heavy for a first class

## 3.3 Option C: The Server Tells the Pico the Next Valid Path

### Overview

- The Pico first accesses a fixed lookup endpoint
- The server returns the path to use now
- The Pico follows that instruction for the real send

### Example

1. The Pico calls `GET /config`
2. The server returns `{"post_path":"/ingest/b","valid_for_ms":30000}`
3. The Pico POSTs to `/ingest/b`

### Information for the Pico

- the fixed config endpoint
- how to read the returned JSON

### Information for the Server

- the currently valid path
- its expiry

### Pros

- no reflashing of the Pico when the path changes
- rotation is server-driven
- fairly natural in practice

### Cons

- the fixed target `GET /config` remains
- a little complex for learners
- becomes a two-step flow: fetch config, then send

### Educational assessment

- teaches the difference between a `control channel` and a `data channel`
- interesting as an advanced task

## 3.4 Option D: Decide by Time

### Overview

- The server and the Pico share the same clock and the same rule
- e.g.:
  - pick the path by the last digit of the minute
  - `minute % 3`

### Information for the Pico

- candidate path list
- clock reference
- rule to derive the path from time

### Information for the Server

- the same candidate path list
- the same time rule

### Pros

- synchronizes without extra communication
- looks elegant

### Cons

- the Pico needs clock synchronization
- clock drift in class easily causes failures
- tends to be overkill for a local experiment

### Educational assessment

- interesting, but not suited to a first exercise

## 3.5 Option E: Share a Pseudo-random Sequence

### Overview

- The server and the Pico share the same seed
- They pick the next path from the same pseudo-random sequence

### Information for the Pico

- candidate path list
- seed
- random algorithm
- state of how many sends have happened

### Information for the Server

- the same seed
- the same random algorithm
- the same state management

### Pros

- the rule is hard to see
- easy to produce `apparent irregularity`

### Cons

- once the state slips by one, everything after it slips
- hard to debug
- difficult as a first classroom topic

### Educational assessment

- good as an advanced theme
- heavy for the main class

## 4. Comparison Table

| Option | Impl. difficulty | Classroom clarity | No reflash needed | MTD-likeness | Recommended stage |
|---|---|---|---|---|---|
| A source-embedded | low | high | low | medium | first time |
| B config distribution | medium | medium | low | medium | second time on |
| C server-directed | medium | medium | high | high | advanced |
| D time-based | medium | low | high | high | advanced |
| E shared PRNG | high | low | high | high | expert |

## 5. What to Adopt for Class

In conclusion, a **two-stage structure** is easiest to handle in class.

### Stage 1

- Start with `Option A: source-embedded`
- Depending on the send count `seq`:
  - 1st send: `/ingest/a`
  - 2nd send: `/ingest/b`
  - 3rd send: `/ingest/c`
  - 4th send onward repeats

At this stage, learners grasp the idea of `rotating several candidates instead of a fixed target`.

### Stage 2

- Then move to `Option C: the server tells the next path`
- `GET /config` or `POST /config`
- The server returns the valid path and its expiry

At this stage, learners see that `the control information itself is a design target`.

## 6. What to Give the Server Concretely

For a minimal classroom design, the server only needs to hold:

- `allowed_paths`
  - e.g. `["/ingest/a", "/ingest/b", "/ingest/c"]`
- `path_mode`
  - e.g. `round_robin`, `fixed`, `server_selected`
- `grace_window_seconds`
  - how many seconds to keep accepting the old path
- `current_index`
  - the currently valid path number
- `token_map` (optional)
  - manage per-path tokens here if used

## 7. What to Give the Pico Concretely

For a minimal classroom design, the Pico only needs to hold:

- `PATH_LIST`
  - e.g. `"/ingest/a", "/ingest/b", "/ingest/c"`
- `PATH_MODE`
  - `round_robin` or `fixed`
- `PATH_ROTATE_EVERY`
  - how many sends between rotations
- `CONFIG_URL` (for the advanced stage)
  - e.g. `/config`
- `DEVICE_TOKEN` (optional)

## 8. How to Treat Old Paths

For teaching, it is safer to keep **a short grace window** than to cut the old path immediately.

Reasons:

- Wi-Fi has latency and retransmissions
- send timing differs per learner
- immediate invalidation makes `trouble` more prominent than the `concept`

So at first we recommend:

- keep accepting the old path for `10 seconds` after activating the new path

## 9. Recommended Adoption for Class

As the first teaching material, the following spec is the most realistic.

### Adopted design

- Both the server and the Pico hold the same `PATH_LIST`
- The Pico selects the path with `(seq - 1) % N` (`seq` is 1-based)
- The server accepts all of those paths
- The send JSON includes `mode` and a newly added `path_index` (the selected path number)

### Advantages of this design

- simple to implement
- easy to debug
- learners can follow the rule by eye
- easy to migrate to the `server_selected` method in the next stage

### Limits of this design

- strictly speaking it is not a `server tells the path` design
- if the rule leaks to an attacker, it is easy to follow

## 10. The Next Stage as an Extension

If moving forward, this order is natural.

1. distribute the valid path via `/config`
2. vary the token per path
3. combine path rotation with randomized send intervals
4. tune the timing of old-path rejection

## 11. Points to Ask in the Exercise

- When changing from a fixed path to a variable path, what becomes harder to observe?
- With which information should the Pico and the server stay synchronized?
- In class, why is the `round_robin` design easier to handle than the time-sync design?
- Does the `fixed URL used to fetch control information` itself become a new fixed target?

## 12. Conclusion

For a first classroom implementation, the best fit is **giving both the Pico and the server the same candidate path list and letting the Pico rotate with a simple rule**.

On top of that, adding **a design where the server distributes the valid path** as an advanced task is clean both educationally and in implementation.

## 13. Related Materials

- [lecture05_mtd_local_post_spec_en.md](lecture05_mtd_local_post_spec_en.md)
- [lecture01_iot_security_pico2w_en.md](lecture01_iot_security_pico2w_en.md)
