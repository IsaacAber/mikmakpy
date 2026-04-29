# mikmakpy

A Python client library for the MikMak 1 game protocol.

Handles the complete authentication pipeline — handshake negotiation, server switching, and room initialization — alongside comprehensive in-game state management and action dispatching. (For a concrete breakdown, see [Implemented](#implemented).)

The abstraction layer is intentionally opinionated: protocol complexity is fully encapsulated so you can focus on building bots, automation tooling, analytics pipelines, or a fully-fledged cross-platform client on top of it. (The latter is the original motivating use case.)

The continuation of the protocol implementation is currently an open challenge — consider this an invitation. (For goals, see [Roadmap](#roadmap).)

There's a non-trivial probability I'll return to it within 2–3 weeks of the initial commit. We'll see about that. (¬‿¬)つ

## Roadmap

- [ ] Complete the Monit London protocol implementation — all edge cases, all state transitions, full deterministic coverage
- [ ] Implement the MikTok protocol end-to-end
- [ ] Implement user inventory interactions with persistent state tracking
- [ ] Implement turn-based multiplayer minigame protocols — cards and Snakes & Ladders at minimum, with hooks for extending to others
- [ ] **Bonus:** Implement the player home protocol in its entirety (almost entirely useless, but completeness is its own reward)
- [O] The trading protocol is explicitly out of scope — fork the repository and own it yourself

## Implemented

Not starting from zero — meaningful groundwork has already been laid:

1. Initial connection handshake and dynamic server list response parsing
2. Game server authentication and parsing of the post-login burst — achievements, user inventory, and the global room list with per-room active player counts
3. In-game room navigation, unsafe chat, and safe chat with hardcoded emoji, emote, and dance support
4. Room state change tracking (player enter / update / leave) with clean, renamed, and normalized objects — designed to minimize protocol archaeology and maximize build velocity
5. In-game map warping within a room, as well as switching between entirely separate game rooms

## How-To

See [HOWTO.md](HOWTO.md) for setup instructions, usage examples, protocol sniffing guidance, and how to contribute.

## License

GPLv3