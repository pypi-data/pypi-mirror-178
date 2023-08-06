# Poetry Plugin: No Content Hash

This package is a plugin that removes the content hash mechanism of Poetry.

## Rationale

- The hash causes conflicts all the time (https://github.com/python-poetry/poetry/issues/496)
- Rust's Cargo had the same problem for a while (https://github.com/rust-lang/cargo/pull/7070)
