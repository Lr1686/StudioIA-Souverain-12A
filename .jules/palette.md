## 2026-03-30 - CLI Input Cancellation Handling

**Learning:** Interactive CLI tools in Python throw unhandled `KeyboardInterrupt` (`Ctrl+C`) or `EOFError` (`Ctrl+D`) tracebacks when users cancel input. Wrapping `input()` prompts in a `try...except (KeyboardInterrupt, EOFError)` block provides clean, user-friendly feedback upon cancellation.
**Action:** Always wrap interactive Python CLI input prompts in cancellation-handling try blocks with friendly exit messages.
